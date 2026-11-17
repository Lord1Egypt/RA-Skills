"""CLI wrapper for the Unlimited-OCR Agent Skill."""

# /// script
# requires-python = ">=3.9"
# dependencies = [
#   "httpx>=0.27,<1",
#   "pymupdf>=1.24,<2",
# ]
# ///

from __future__ import annotations

import argparse
import json
import os
import sys
import tempfile
import uuid
from datetime import datetime
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from client import parse_document


def default_output_path() -> Path:
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S_%f")
    return Path(tempfile.gettempdir()) / "unlimited-ocr" / "results" / f"result-{timestamp}-{uuid.uuid4().hex[:8]}.json"


def main() -> None:
    parser = argparse.ArgumentParser(description="Parse a document with Unlimited-OCR")
    parser.add_argument("--provider", choices=["baidu", "local"], default=os.getenv("UNLIMITED_OCR_PROVIDER", "baidu"))
    source = parser.add_mutually_exclusive_group(required=True)
    source.add_argument("--file-path")
    source.add_argument("--file-url")
    parser.add_argument("--timeout", type=float, default=float(os.getenv("UNLIMITED_OCR_TIMEOUT", "1200")))
    parser.add_argument("--poll-interval", type=float, default=float(os.getenv("UNLIMITED_OCR_POLL_INTERVAL", "5")))
    parser.add_argument("--backend", choices=["sglang", "openai"])
    parser.add_argument("--model")
    parser.add_argument("--prompt")
    parser.add_argument("--image-mode", choices=["auto", "base", "gundam"], default="auto")
    parser.add_argument("--pretty", action="store_true")
    output = parser.add_mutually_exclusive_group()
    output.add_argument("--output", "-o")
    output.add_argument("--stdout", action="store_true")
    parser.add_argument("--markdown-output")
    args = parser.parse_args()

    result = parse_document(
        provider=args.provider,
        file_path=args.file_path,
        file_url=args.file_url,
        timeout_seconds=args.timeout,
        poll_interval_seconds=args.poll_interval,
        backend=args.backend,
        model=args.model,
        prompt=args.prompt,
        image_mode=args.image_mode,
    )
    rendered = json.dumps(result, ensure_ascii=False, indent=2 if args.pretty else None)
    if args.markdown_output and result.get("ok"):
        markdown_path = Path(args.markdown_output).expanduser().resolve()
        markdown_path.parent.mkdir(parents=True, exist_ok=True)
        markdown_path.write_text(str(result.get("text", "")), encoding="utf-8")
    if args.stdout:
        print(rendered)
    else:
        output_path = Path(args.output).expanduser().resolve() if args.output else default_output_path().resolve()
        output_path.parent.mkdir(parents=True, exist_ok=True)
        output_path.write_text(rendered, encoding="utf-8")
        print(f"Result saved to: {output_path}", file=sys.stderr)
    raise SystemExit(0 if result.get("ok") else 1)


if __name__ == "__main__":
    main()

