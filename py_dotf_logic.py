import os
import shutil
import pathlib
import tomllib
import tomli_w


def load_config(path: str) -> dict:
    try:
        with open(path, "rb") as f:
            config = tomllib.load(f)
    except FileNotFoundError:
        raise ValueError("Config file not found.")
    return config


def _resolve_mapping_paths(source: str, target: str, repo_dir: pathlib.Path):
    source_path = pathlib.Path(source)
    target_path = pathlib.Path(target)

    source_is_abs = source_path.is_absolute() or str(source).startswith("~")
    target_is_abs = target_path.is_absolute() or str(target).startswith("~")

    if str(source).startswith("~"):
        source_path = source_path.expanduser()
    if str(target).startswith("~"):
        target_path = target_path.expanduser()

    if source_is_abs and not target_is_abs:
        source_path, target_path = target_path, source_path

    return repo_dir / source_path, target_path


# синхронизация файлов / synchronization of files
def sync(config):
    repo_dir = pathlib.Path(config["settings"]["dir"]).expanduser()
    for source, target in config["mappings"].items():
        source, target = _resolve_mapping_paths(source, target, repo_dir)

        if target.exists() or target.is_symlink():
            if target.is_symlink() and target.readlink() == source:
                continue

            backup = target.with_suffix(target.suffix + ".bak")
            target.rename(backup)

        target.parent.mkdir(parents=True, exist_ok=True)

        target.symlink_to(source)
        print(f"Synced {source} to {target}.")


"""
linked    ✓
conflict  !
broken    ✗
missing   ?
"""  # status symbols


def status(config):
    repo_dir = pathlib.Path(config["settings"]["dir"]).expanduser()
    for mapping in config["mappings"].items():
        source, target = mapping
        source, target = _resolve_mapping_paths(source, target, repo_dir)

        if target.is_symlink():
            if target.readlink() == source:
                print(f"{target} [✓] linked")
            else:
                print(f"{target} [✗] broken")
        elif target.exists():
            print(f"{target} [!] conflict")
        else:
            print(f"{target} [?] missing")


def add(path: str, dest: str):
    src = pathlib.Path(path).expanduser()

    if src.is_symlink():
        raise ValueError("Path is already a symlink.")

    if not src.exists():
        raise ValueError("File does not exist.")

    config_path = pathlib.Path.home() / ".config/dotf/dotf.toml"
    if not config_path.exists():
        config_path.parent.mkdir(parents=True, exist_ok=True)
        config_path.touch()

    with open(config_path, "rb") as f:
        config = tomllib.load(f)

    config.setdefault("mappings", {})
    repo_dir = pathlib.Path(config["settings"]["dir"]).expanduser()
    dest_path = repo_dir / dest

    dest_path.parent.mkdir(parents=True, exist_ok=True)
    shutil.move(str(src), str(dest_path))

    config["mappings"][str(dest)] = "~/" + str(src.relative_to(pathlib.Path.home()))
    with open(config_path, "wb") as f:
        tomli_w.dump(config, f)

    src.symlink_to(dest_path)
    print(f"Added {src} → {dest_path}")
