#!/usr/bin/env python3
"""Build the JSON request body for POST /api/v1/items.

Standard library only. No network access, no credentials, no environment reads:
this script only turns a local archive plus its metadata into a JSON file that a
wallet CLI can send.

Why it exists: a wallet CLI passes the request body as a single command-line
argument, and Linux caps one argument at MAX_ARG_STRLEN = 131072 bytes. Base64
inflates the archive by a third, so the JSON path fails with E2BIG well below the
API's own 10 MB limit. This script refuses up front, with the reason, instead of
letting the shell fail cryptically after the archive has been prepared.
"""

import argparse
import base64
import hashlib
import json
from pathlib import Path

# Linux caps a single argv entry at 32 pages, including its NUL terminator: an
# argument of exactly this many bytes already fails with E2BIG. A body larger
# than this cannot reach a wallet CLI at all, whatever the API would accept.
MAX_ARG_STRLEN = 131072

# Leave room for the flags and quoting the CLI wraps around the body.
ARG_SAFETY_MARGIN = 1024
SAFE_BODY_BYTES = MAX_ARG_STRLEN - ARG_SAFETY_MARGIN

# Enforced by the API; checked here so a doomed upload fails locally and for free.
MAX_ARCHIVE_BYTES = 10 * 1024 * 1024
MIN_PRICE_USD = 0.1
MAX_PRICE_USD = 100.0
# Per-field limits the API enforces. It counts JavaScript string length, i.e.
# UTF-16 code units, so `text_length` below counts the same way.
MAX_FIELD_LENGTH = {
    "title": 200,
    "description": 4000,
    "tech_stack": 200,
    "prompt_summary": 1000,
}


def text_length(text):
    return len(text.encode("utf-16-le")) // 2

COMPRESSION_BY_SUFFIX = {
    ".zip": "zip",
    ".gz": "tar.gz",
    ".tgz": "tgz",
}


class ListingBodyError(Exception):
    """Raised for any input the API or the shell would reject."""


def detect_compression(archive_path):
    """Return the API's `compression` value for an archive path."""
    suffixes = Path(archive_path).suffixes
    if suffixes[-2:] == [".tar", ".gz"]:
        return "tar.gz"
    suffix = Path(archive_path).suffix.lower()
    compression = COMPRESSION_BY_SUFFIX.get(suffix)
    if compression is None:
        raise ListingBodyError(
            f"unsupported archive type {suffix!r}; use .zip, .tar.gz or .tgz"
        )
    return compression


def build_listing_body(
    archive_path,
    title,
    description,
    tech_stack,
    price_usdc,
    prompt_summary=None,
    arg_limit=SAFE_BODY_BYTES,
):
    """Build the listing request body.

    Returns a dict with the serialized `body` text plus the facts a caller needs
    to report: `sha256`, `archive_bytes`, `body_bytes`, `compression`.
    Raises ListingBodyError rather than exiting, so this function is reusable.
    """
    archive = Path(archive_path)
    if not archive.is_file():
        raise ListingBodyError(f"archive not found: {archive}")

    raw = archive.read_bytes()
    if not raw:
        raise ListingBodyError(f"archive is empty: {archive}")
    if len(raw) > MAX_ARCHIVE_BYTES:
        raise ListingBodyError(
            f"archive is {len(raw)} bytes; the API limit is {MAX_ARCHIVE_BYTES}"
        )

    if not title.strip():
        raise ListingBodyError("title must not be empty")
    if not description.strip():
        raise ListingBodyError("description must not be empty")
    if not tech_stack.strip():
        raise ListingBodyError("tech_stack must be a non-empty string")
    if not MIN_PRICE_USD <= price_usdc <= MAX_PRICE_USD:
        raise ListingBodyError(
            f"price {price_usdc} is outside the allowed band "
            f"{MIN_PRICE_USD}..{MAX_PRICE_USD} USD"
        )

    metadata = {
        "title": title.strip(),
        "description": description.strip(),
        "tech_stack": tech_stack.strip(),
        "prices": {"USDC": price_usdc},
    }
    if prompt_summary and prompt_summary.strip():
        metadata["prompt_summary"] = prompt_summary.strip()

    for field, limit in MAX_FIELD_LENGTH.items():
        if field in metadata and text_length(metadata[field]) > limit:
            raise ListingBodyError(
                f"{field} is {text_length(metadata[field])} characters; "
                f"the API limit is {limit}"
            )

    body = {
        "compression": detect_compression(archive),
        "file": base64.b64encode(raw).decode("ascii"),
        "metadata": metadata,
    }
    body_text = json.dumps(body, ensure_ascii=False)

    if len(body_text.encode("utf-8")) > arg_limit:
        raise ListingBodyError(
            f"the encoded body is {len(body_text.encode('utf-8'))} bytes, over the "
            f"{arg_limit}-byte practical limit a wallet CLI can carry in one "
            f"argument (Linux MAX_ARG_STRLEN is {MAX_ARG_STRLEN}). "
            "Shrink the archive to roughly 96 KB, or use spawnxchange-cdp-cli, which "
            "signs the payment separately and can send the body from a file."
        )

    return {
        "body": body_text,
        "sha256": hashlib.sha256(raw).hexdigest(),
        "archive_bytes": len(raw),
        "body_bytes": len(body_text.encode("utf-8")),
        "compression": body["compression"],
    }


def read_text_argument(inline, path):
    """Return inline text, or the contents of path, whichever was supplied."""
    if inline is not None:
        return inline
    return Path(path).read_text(encoding="utf-8")


def main():
    parser = argparse.ArgumentParser(
        description="Build the JSON body for POST /api/v1/items."
    )
    parser.add_argument("--archive", required=True, help=".zip or .tar.gz to list")
    parser.add_argument("--title", required=True)
    description = parser.add_mutually_exclusive_group(required=True)
    description.add_argument("--description")
    description.add_argument("--description-file")
    parser.add_argument("--tech-stack", required=True, help="comma-separated string")
    parser.add_argument("--price-usdc", type=float, required=True)
    summary = parser.add_mutually_exclusive_group()
    summary.add_argument("--prompt-summary")
    summary.add_argument("--prompt-summary-file")
    parser.add_argument("--out", required=True, help="path to write the JSON body to")
    args = parser.parse_args()

    try:
        result = build_listing_body(
            archive_path=args.archive,
            title=args.title,
            description=read_text_argument(args.description, args.description_file),
            tech_stack=args.tech_stack,
            price_usdc=args.price_usdc,
            prompt_summary=(
                read_text_argument(args.prompt_summary, args.prompt_summary_file)
                if (args.prompt_summary or args.prompt_summary_file)
                else None
            ),
        )
    except ListingBodyError as error:
        parser.exit(2, f"error: {error}\n")

    out = Path(args.out)
    out.write_text(result["body"], encoding="utf-8")
    out.chmod(0o600)

    print(f"wrote        {out}")
    print(f"compression  {result['compression']}")
    print(f"archive      {result['archive_bytes']} bytes")
    print(f"sha256       {result['sha256']}")
    print(f"body         {result['body_bytes']} bytes (argv budget {SAFE_BODY_BYTES})")
    print()
    print("This file is only the request body. Nothing has been uploaded and no fee")
    print("has been paid. Send it with your wallet CLI to POST /api/v1/items.")


if __name__ == "__main__":
    main()
