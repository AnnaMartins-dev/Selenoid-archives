import argparse


def should_use_selenoid() -> bool:
    parser = argparse.ArgumentParser(add_help=False)

    parser.add_argument(
        "--docker",
        default="Disabled"
    )

    args, unknow_args = parser.parse_known_args()

    print(f"Configuração: --docker={args.docker}")

    if args.docker.lower() == "enabled":
        return True
    else:
        return False