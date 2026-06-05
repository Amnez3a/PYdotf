import argparse
import pathlib


def parse_args():
    parser = argparse.ArgumentParser(
        description="PYdotf - A Python implementation of the DOTF file format."
    )
    subparsers = parser.add_subparsers(dest="command", required=True)

    parser.add_argument(
        "-c",
        "--config",
        type=pathlib.Path,
        default=pathlib.Path("~/.config/dotf/dotf.toml").expanduser(),
        help="Path to the config file.",
    )
    subparsers.add_parser("sync")
    subparsers.add_parser("status")
    add_parser = subparsers.add_parser("add")
    add_parser.add_argument(
        "path", type=pathlib.Path, help="Path to the file or directory to add."
    )
    add_parser.add_argument("dest", type=pathlib.Path)

    return parser.parse_args()
