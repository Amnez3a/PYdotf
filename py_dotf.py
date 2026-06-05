from py_dotf_parseArgs import parse_args
from py_dotf_logic import load_config, sync, status, add


def main():
    args = parse_args()
    config = load_config(args.config)

    if args.command == "sync":
        sync(config)
    elif args.command == "status":
        status(config)
    elif args.command == "add":
        add(args.path, args.dest)
    else:
        print("Unknown command")


if __name__ == "__main__":
    main()
