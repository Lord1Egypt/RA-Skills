#!/usr/bin/env python3
"""Create an explicitly loaded OpenCode provider layer, preserving JSONC and defaults. Python 3.11+."""

import os
from pathlib import Path
import sys

from setup_files import SetupError, SafeParser, read_file
from provider_config import apply, check_model, check_provider, inspect_client, parse, prepare, reject_saved_credential


def provider(model: str) -> dict:
    check_model(model)
    return {"npm": "@ai-sdk/openai-compatible", "name": "TokenLab",
            "options": {"baseURL": "https://api.tokenlab.sh/v1", "apiKey": "{env:TOKENLAB_API_KEY}"},
            "models": {model: {"name": model}}}


def user_config_paths() -> list[Path]:
    root = Path(os.environ.get("XDG_CONFIG_HOME") or Path.home() / ".config") / "opencode"
    paths = [root / name for name in ("config.json", "opencode.json", "opencode.jsonc")]
    if os.environ.get("OPENCODE_CONFIG_DIR"):
        extra = Path(os.environ["OPENCODE_CONFIG_DIR"]).expanduser()
        paths += [extra / name for name in ("opencode.json", "opencode.jsonc")]
    if os.environ.get("OPENCODE_CONFIG"):
        paths.append(Path(os.environ["OPENCODE_CONFIG"]).expanduser())
    return paths


def config_path(explicit: Path | None, name: str = "tokenlab") -> Path:
    root = Path(os.environ.get("XDG_CONFIG_HOME") or Path.home() / ".config") / "opencode"
    target = (explicit or root / f"{name}.jsonc").expanduser().absolute()
    if target.name.lower() in ("config.json", "opencode.json", "opencode.jsonc"):
        raise SetupError("Choose a separate layer such as tokenlab.jsonc. Automatically loaded files can change the default provider.")
    return target


def inspect_selection(target: Path, name: str) -> dict[Path, bytes | None]:
    if os.environ.get("OPENCODE_CONFIG_CONTENT"):
        raise SetupError("Inline OpenCode configuration can override this provider; resolve that selection explicitly first.")
    active = os.environ.get("OPENCODE_CONFIG")
    if active and Path(active).expanduser().resolve() != target.resolve():
        raise SetupError("OPENCODE_CONFIG already selects another layer. Keep it; use a separate launch environment for TokenLab.")
    guards = {}
    for candidate in [target, *user_config_paths()]:
        path = candidate.expanduser().absolute()
        is_target = path.resolve() == target.resolve()
        if path in guards:
            continue
        content = read_file(path, allow_links=not is_target)
        if not is_target:
            guards[path] = content
        _, _, config = parse(content if content is not None else b"{}", trailing_commas=True)
        providers = config.get("provider", {})
        if not isinstance(providers, dict):
            raise SetupError("Existing provider configuration has an unsupported shape.")
        if not is_target and name in providers:
            raise SetupError("That provider already exists in another user configuration. Choose another provider name.")
        for key in ("enabled_providers", "disabled_providers"):
            if key in config and (not isinstance(config[key], list) or
                                  any(not isinstance(value, str) for value in config[key])):
                raise SetupError("Existing provider selection has an unsupported shape; no settings were changed.")
        if name in config.get("disabled_providers", []) or (
            "enabled_providers" in config and name not in config["enabled_providers"]
        ):
            raise SetupError("The selected provider is excluded by this configuration. No allowlist or permissions were changed.")
    return guards


def main(argv: list[str] | None = None) -> int:
    parser = SafeParser(description=__doc__)
    parser.add_argument("--config", type=Path)
    parser.add_argument("--opencode-bin")
    parser.add_argument("--provider", default="tokenlab")
    parser.add_argument("--model")
    parser.add_argument("--apply", action="store_true")
    parser.add_argument("--restore", action="store_true")
    args = parser.parse_args(argv)
    try:
        check_provider(args.provider)
        target = config_path(args.config, args.provider)
        desired, guards = None, {}
        if not args.restore:
            if not args.model:
                raise SetupError("--model is required; choose a model whose public contract accepts Chat Completions.")
            desired = provider(args.model)
            version = inspect_client("opencode", args.opencode_bin, (1, 18, 31))
            guards = inspect_selection(target, args.provider)
            auth = Path(os.environ.get("XDG_DATA_HOME") or Path.home() / ".local" / "share") / "opencode" / "auth.json"
            guards[auth] = reject_saved_credential(auth, args.provider)
            print(f"Detected OpenCode {version}.")
        plan = prepare(target, "OpenCode", "provider", args.provider, desired, restore=args.restore,
                       trailing_commas=True, guards=guards)
        if args.apply:
            apply(plan)
        print(f"{'Applied' if args.apply else 'Preview'}: {plan.action}; configuration: {plan.target}")
        if not args.restore:
            print("Provider endpoint: https://api.tokenlab.sh/v1 (Chat Completions); credential: TOKENLAB_API_KEY environment reference only.")
            print(f"For this invocation only, set OPENCODE_CONFIG to: {plan.target}")
            print(f"Set TOKENLAB_API_KEY in the launch environment, then select: opencode --model {args.provider}/{args.model}")
            print(f"With the same layer selected: opencode models {args.provider}. Project or managed settings may override this file.")
        return 0
    except (SetupError, OSError) as error:
        print(str(error) if isinstance(error, SetupError) else "File operation failed; inspect the retained backup before retrying.", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
