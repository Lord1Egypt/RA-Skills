#!/usr/bin/env python3
"""CLI entry point for image generation skill."""

import argparse
import json
import sys
import os

# Allow running as script without package install
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from config_manager import load_config
from providers import get_provider


def main():
    parser = argparse.ArgumentParser(description="Generate images from text prompts")
    parser.add_argument(
        "-p", "--prompt", type=str, help="Text prompt for image generation"
    )
    parser.add_argument(
        "--provider",
        type=str,
        default=None,
        help="Provider: openrouter (default) or kie",
    )
    parser.add_argument("-m", "--model", type=str, default=None, help="Model name")
    parser.add_argument("-o", "--output", type=str, default=None, help="Output file path")
    parser.add_argument(
        "-i", "--input", type=str, default=None,
        help="Input image path for editing (optional)"
    )
    parser.add_argument(
        "-c", "--config", type=str, default=None, help="Path to config.json"
    )
    parser.add_argument(
        "--list-models", action="store_true", help="List available models and exit"
    )
    parser.add_argument(
        "-v", "--verbose", action="store_true", help="Enable verbose output"
    )

    args = parser.parse_args()

    try:
        config = load_config(args.config)
    except Exception as e:
        print(json.dumps({"status": "error", "error": f"Config error: {e}"}))
        sys.exit(1)

    provider_name = args.provider or config.get("default_provider", "openrouter")

    try:
        provider_cls = get_provider(provider_name)
    except ValueError as e:
        print(json.dumps({"status": "error", "error": str(e)}))
        sys.exit(1)

    provider = provider_cls(config)

    # List models mode
    if args.list_models:
        models = provider.list_models()
        print(json.dumps({"provider": provider_name, "models": models}))
        return

    # Generate mode — prompt is required
    if not args.prompt:
        print(json.dumps({"status": "error", "error": "Prompt is required. Use -p/--prompt."}))
        sys.exit(1)

    # Validate config
    if not provider.validate_config(config):
        print(
            json.dumps(
                {
                    "status": "error",
                    "error": f"Missing API key for provider '{provider_name}'. Check environment variables.",
                }
            )
        )
        sys.exit(1)

    if args.verbose:
        print(
            json.dumps(
                {
                    "status": "info",
                    "message": f"Generating with {provider_name}, model={args.model or provider.default_model}",
                }
            ),
            file=sys.stderr,
        )

    try:
        result = provider.generate(
            prompt=args.prompt, model=args.model, output_path=args.output,
            input_image=args.input
        )
    except Exception as e:
        result = {
            "status": "error",
            "error": str(e),
            "provider": provider_name,
        }

    print(json.dumps(result, ensure_ascii=False))

    if result.get("status") != "ok":
        sys.exit(1)


if __name__ == "__main__":
    main()
