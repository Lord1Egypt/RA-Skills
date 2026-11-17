#!/usr/bin/env python3
"""Add a reversible Pi provider without changing its default model or saved accounts. Python 3.11+."""

import os
from pathlib import Path
import sys

from setup_files import SetupError, SafeParser
from provider_config import apply, check_model, check_provider, inspect_client, prepare, reject_saved_credential


def provider(model: str) -> dict:
    check_model(model)
    return {"baseUrl": "https://api.tokenlab.sh/v1", "api": "openai-completions",
            "apiKey": "$TOKENLAB_API_KEY", "models": [{"id": model}]}


def main(argv: list[str] | None = None) -> int:
    parser = SafeParser(description=__doc__)
    parser.add_argument("--agent-dir", type=Path)
    parser.add_argument("--pi-bin")
    parser.add_argument("--provider", default="tokenlab")
    parser.add_argument("--model")
    parser.add_argument("--apply", action="store_true")
    parser.add_argument("--restore", action="store_true")
    args = parser.parse_args(argv)
    try:
        check_provider(args.provider)
        root = (args.agent_dir or Path(os.environ.get("PI_CODING_AGENT_DIR") or Path.home() / ".pi" / "agent")).expanduser().absolute()
        guards = {}
        desired = None
        if not args.restore:
            print("Provider endpoint: https://api.tokenlab.sh/v1 (Chat Completions); credential: TOKENLAB_API_KEY environment reference only.")
            if not args.model:
                raise SetupError("--model is required; choose a model whose public contract accepts Chat Completions.")
            desired = provider(args.model)
            version = inspect_client("pi", args.pi_bin, (0, 85, 1))
            auth = root / "auth.json"
            guards[auth] = reject_saved_credential(auth, args.provider)
            print(f"Detected Pi {version}.")
        plan = prepare(root / "models.json", "Pi", "providers", args.provider, desired,
                       restore=args.restore, trailing_commas=True, block_comments=False, guards=guards)
        if args.apply:
            apply(plan)
        print(f"{'Applied' if args.apply else 'Preview'}: {plan.action}; configuration: {plan.target}")
        if not args.restore:
            print(f"Set TOKENLAB_API_KEY in the launch environment, then select: pi --provider {args.provider} --model {args.model}")
            print(f"Model discovery: pi --list-models {args.provider}. This helper does not make API requests.")
        return 0
    except (SetupError, OSError) as error:
        print(str(error) if isinstance(error, SetupError) else "File operation failed; inspect the retained backup before retrying.", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
