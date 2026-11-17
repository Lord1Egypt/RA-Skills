#!/usr/bin/env python3
"""Preview, add or restore one Hermes 0.21.3 provider without changing accounts or defaults."""

import json
import os
from pathlib import Path
import re
import subprocess
import sys

from setup_files import SafeParser, SetupError, read_file
from provider_config import apply, check_model, check_provider, inspect_client, prepare
from hermes_yaml import insert_provider


def provider(model: str) -> dict:
    check_model(model)
    return {"api": "https://api.tokenlab.sh/v1", "key_env": "TOKENLAB_API_KEY",
            "transport": "chat_completions", "default_model": model}


def resolve_home(explicit: Path | None) -> tuple[Path, dict]:
    guards = {}
    native = (Path(os.environ.get("LOCALAPPDATA") or Path.home() / "AppData" / "Local") / "hermes"
              if sys.platform == "win32" else Path.home() / ".hermes")
    root = (explicit or Path(os.environ.get("HERMES_HOME") or native)).expanduser().absolute()
    if explicit is None and root.parent.name != "profiles":
        active = root / "active_profile"
        content = read_file(active, allow_links=True)
        guards[active] = content
        try:
            name = (content or b"").decode("utf-8").strip()
        except UnicodeDecodeError:
            raise SetupError("Cannot read the active Hermes profile; select --hermes-home explicitly.") from None
        if name and name != "default":
            if not re.fullmatch(r"[a-z0-9][a-z0-9_-]{0,63}", name):
                raise SetupError("Cannot resolve the active Hermes profile; select --hermes-home explicitly.")
            root = root / "profiles" / name
            if not root.is_dir():
                raise SetupError("The active Hermes profile is missing; no configuration was created.")
    return root, guards


def inspect_settings(root: Path, name: str) -> dict:
    if os.environ.get("WSL_DISTRO_NAME"):
        raise SetupError("WSL policy inheritance has not been validated. Use the manual guide for now.")
    if any(os.environ.get(key) for key in ("HERMES_CONFIG", "HERMES_CONFIG_PATH", "HERMES_ENV",
                                          "HERMES_ENV_PATH", "HERMES_PROFILE", "HERMES_IGNORE_USER_CONFIG")):
        raise SetupError("Hermes configuration overrides need manual review; no settings were changed.")
    managed = os.environ.get("HERMES_MANAGED", "").strip().lower()
    marker = read_file(root / ".managed", allow_links=True)
    if not managed and marker is not None:
        managed = marker.decode("utf-8", errors="replace").strip().lower() or "true"
    if managed and managed not in {"false", "0", "no", "off", "brew", "homebrew"}:
        raise SetupError("Hermes is managed by another configuration owner; use its configuration process.")
    managed_dir = Path(os.environ.get("HERMES_MANAGED_DIR", "").strip() or "/etc/hermes")
    if managed_dir.is_dir():
        raise SetupError("A Hermes managed scope is present; automatic setup will not override it.")
    guards = {root / ".managed": marker}
    for filename in ("config.yaml", ".env"):
        guards[managed_dir / filename] = read_file(managed_dir / filename, allow_links=True)
    for filename in (".env", "auth.json"):
        guards[root / filename] = read_file(root / filename, allow_links=True)
    auth = guards[root / "auth.json"]
    if auth is not None:
        try:
            stored = json.loads(auth)
            if not isinstance(stored, dict):
                raise ValueError()
            names = {name, f"custom:{name}"}
            for section in ("providers", "credential_pool"):
                entries = stored.get(section, {})
                if not isinstance(entries, dict):
                    raise ValueError()
                if names.intersection(entries):
                    raise SetupError("A saved Hermes account already uses that provider; choose another name.")
            if stored.get("active_provider") in names:
                raise SetupError("The active Hermes account already uses that provider; choose another name.")
        except (ValueError, TypeError, UnicodeDecodeError):
            raise SetupError("Hermes account storage needs manual review; its contents were not printed.") from None
    return guards


def main(argv=None) -> int:
    arguments = list(sys.argv[1:] if argv is None else argv)
    parser = SafeParser(description=__doc__, allow_abbrev=False)
    parser.add_argument("--hermes-home", type=Path)
    parser.add_argument("--hermes-bin")
    parser.add_argument("--hermes-python", type=Path)
    parser.add_argument("--provider", default="tokenlab")
    parser.add_argument("--model")
    parser.add_argument("--apply", action="store_true")
    parser.add_argument("--restore", action="store_true")
    args = parser.parse_args(arguments)
    try:
        check_provider(args.provider)
        if not args.restore and args.hermes_python is not None:
            # Explicit runtime selection, never a global pip install or a guess at
            # another Python installation. Remove the flag before re-execution.
            runtime = args.hermes_python.expanduser().absolute()
            if not runtime.is_file():
                raise SetupError("The selected Hermes Python was not found; use its installed virtual environment.")
            if str(runtime) != str(Path(sys.executable).absolute()):
                forwarded = []
                index = 0
                while index < len(arguments):
                    if arguments[index] == "--hermes-python":
                        index += 2
                    elif arguments[index].startswith("--hermes-python="):
                        index += 1
                    else:
                        forwarded.append(arguments[index])
                        index += 1
                return subprocess.run([str(runtime), str(Path(__file__).absolute()), *forwarded], check=False).returncode
        root, guards = resolve_home(args.hermes_home)
        desired = None
        if not args.restore:
            if not args.model:
                raise SetupError("--model is required; choose a public Chat Completions model with tool support.")
            desired = provider(args.model)
            version = inspect_client("hermes", args.hermes_bin, (0, 21, 3))
            if version != "0.21.3":
                raise SetupError("This helper targets Hermes 0.21.3. Use the manual guide for other versions.")
            guards.update(inspect_settings(root, args.provider))
            print(f"Hermes {version}; Python {sys.version_info.major}.{sys.version_info.minor}; configuration: {root / 'config.yaml'}")
            print("Endpoint: https://api.tokenlab.sh/v1 (Chat Completions); credential: TOKENLAB_API_KEY environment reference only.")
        plan = prepare(root / "config.yaml", "Hermes", "providers", args.provider, desired,
                       restore=args.restore, guards=guards, insert=insert_provider, comment="#")
        if args.apply:
            # A managed scope can appear between preview and write. Inspect it
            # again rather than relying only on the initial file snapshot.
            if not args.restore:
                inspect_settings(root, args.provider)
            apply(plan)
        print(f"{'Applied' if args.apply else 'Preview'}: {plan.action}; configuration: {plan.target}")
        if not args.restore:
            profile_flag = "" if root.parent.name == "profiles" else " --profile default"
            print(f"Set HERMES_HOME to {root} for this invocation; keep TOKENLAB_API_KEY in its trusted local environment.")
            print(f"Check loading: hermes{profile_flag} config get providers.{args.provider}.api")
            print(f"Start explicitly: hermes{profile_flag} chat --provider custom:{args.provider} --model {args.model}")
            print("Normal launches keep their existing selection. This helper does not request inference.")
        return 0
    except (SetupError, OSError) as error:
        print(str(error) if isinstance(error, SetupError) else "File or runtime operation failed; no existing configuration or credentials were printed.", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
