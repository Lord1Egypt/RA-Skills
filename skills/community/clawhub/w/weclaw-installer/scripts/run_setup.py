import argparse
from pathlib import Path
import sys


def _repo_root() -> Path:
    return Path(__file__).resolve().parents[3]


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Run WeClaw installer setup_package.py wrapper"
    )
    parser.add_argument("--api-key", default=None, help="API key for setup")
    parser.add_argument(
        "--mac-permission-confirmed",
        action="store_true",
        help="Set when macOS Accessibility permission is enabled",
    )
    args = parser.parse_args()

    repo_root = _repo_root()
    sys.path.insert(0, str(repo_root))

    try:
        from setup_package import setup_openclaw_package  # type: ignore
    except Exception as e:
        print(f"STATUS: FAILED. Could not import setup_package.py: {e}")
        return 1

    result = setup_openclaw_package(
        api_key=args.api_key,
        mac_permission_confirmed=bool(args.mac_permission_confirmed),
    )
    print(result)
    return 0 if isinstance(result, str) and result.startswith("STATUS: SUCCESS") else 2


if __name__ == "__main__":
    raise SystemExit(main())

