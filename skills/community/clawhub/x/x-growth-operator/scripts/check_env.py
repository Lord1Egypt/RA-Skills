from __future__ import annotations

import argparse
import os
import shutil
import subprocess

from common import load_local_env


def check_binary(name: str) -> tuple[bool, str]:
    path = shutil.which(name)
    return (path is not None, path or "")


def main() -> int:
    parser = argparse.ArgumentParser(description="Validate local environment for x-growth-operator.")
    parser.add_argument("--mode", choices=["planning", "execution"], default="planning")
    args = parser.parse_args()
    load_local_env()

    checks: list[tuple[str, bool, str]] = []

    python_ok, python_path = check_binary("python3")
    checks.append(("python3", python_ok, python_path))

    node_ok, node_path = check_binary("node")
    checks.append(("node", node_ok, node_path))

    npm_ok, npm_path = check_binary("npm")
    checks.append(("npm", npm_ok, npm_path))

    if args.mode == "execution":
      for env_name in ("X_API_KEY", "X_API_SECRET", "X_ACCESS_TOKEN", "X_ACCESS_TOKEN_SECRET"):
        value = os.environ.get(env_name)
        checks.append((env_name, bool(value), "set" if value else "missing"))

      install_dir = os.path.dirname(os.path.abspath(__file__))
      commander_module = os.path.join(install_dir, "node_modules", "commander")
      checks.append(("npm deps (commander)", os.path.isdir(commander_module), commander_module if os.path.isdir(commander_module) else "not installed"))
      checks.append(("x_oauth_cli.js", os.path.isfile(os.path.join(install_dir, "x_oauth_cli.js")), "present" if os.path.isfile(os.path.join(install_dir, "x_oauth_cli.js")) else "missing"))
      checks.append(("DESEARCH_API_KEY", bool(os.environ.get("DESEARCH_API_KEY")), "set" if os.environ.get("DESEARCH_API_KEY") else "optional"))

    failed = False
    for name, ok, detail in checks:
        status = "OK" if ok else "MISSING"
        print(f"{status:7} {name:20} {detail}")
        failed = failed or not ok

    if not failed:
        try:
            version = subprocess.run(["node", "-v"], check=False, capture_output=True, text=True).stdout.strip()
            if version:
                print(f"Node version: {version}")
        except Exception:
            pass
        return 0
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
