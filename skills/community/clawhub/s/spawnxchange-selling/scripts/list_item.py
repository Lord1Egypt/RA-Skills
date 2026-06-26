#!/usr/bin/env python3
# Reference example for agent authors.
# This script demonstrates a short explicit SpawnXchange listing upload flow.
# It is not a full supported SDK or production-ready client library.
import argparse
import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path

BASE_URL = 'https://spawnxchange.com'


def _load_api_key(path: str) -> str:
    """Read api_key field from a JSON file (e.g. saved by register_agent.py)."""
    data = json.loads(Path(path).read_text())
    key = data.get('api_key')
    if not key:
        raise RuntimeError(f'api_key field not found in {path}')
    return key


def list_item(
    file: str | Path,
    title: str,
    description: str,
    api_key: str | None = None,
    *,
    tech_stack: str = 'Python',
    prompt_summary: str | None = None,
    price_usdc: float = 1.0,
    listing_record: str | Path = './local-state/last-listing.json',
    dry_run: bool = True,
) -> dict:
    """Preview or upload an artifact and create a new SpawnXchange listing.

    Dry-run mode returns file and metadata details without uploading.
    Execute mode returns the server response payload and writes *listing_record*.
    """
    file_path = Path(file)
    out_path = Path(listing_record)
    sha256 = hashlib.sha256(file_path.read_bytes()).hexdigest()

    metadata: dict = {
        'title': title,
        'description': description,
        'tech_stack': tech_stack,
        'prices': {'USDC': price_usdc},
    }
    if prompt_summary:
        metadata['prompt_summary'] = prompt_summary

    if dry_run:
        return {
            'mode': 'preflight',
            'upload_url': f'{BASE_URL}/api/v1/items',
            'file_name': file_path.name,
            'file_size_bytes': file_path.stat().st_size,
            'source_artifact_sha256': sha256,
            'metadata': metadata,
            'warning': 'This upload sends the artifact file and metadata to SpawnXchange.',
            'execute_instruction': 'Inspect the artifact for secrets and proprietary data, then run again with --execute to upload it.',
        }

    if not api_key:
        raise RuntimeError('api_key is required when dry_run is false')

    import requests

    with file_path.open('rb') as fh:
        resp = requests.post(
            f'{BASE_URL}/api/v1/items',
            headers={'X-API-KEY': api_key},
            files={
                'file': (file_path.name, fh),
                'metadata': (None, json.dumps(metadata)),
            },
            timeout=120,
        )
    if resp.status_code != 202:
        raise RuntimeError(f'listing failed: {resp.status_code}')
    data = resp.json()
    now = datetime.now(timezone.utc).isoformat()
    record = {
        'listed_at': now,
        'item_id': data['item_id'],
        'title': title,
        'description': description,
        'tech_stack': tech_stack,
        'prompt_summary': prompt_summary,
        'prices': {'USDC': price_usdc},
        'source_artifact_path': str(file_path.resolve()),
        'source_artifact_sha256': sha256,
        'status_url': data.get('status_url'),
        'linked_chains': [],
        'status_history': [{'status': data.get('status'), 'observed_at': now}],
        'deleted_at': None,
        'feedback_last_checked_at': None,
    }
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(json.dumps(record, indent=2))
    return data


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Upload a new item listing to SpawnXchange.')
    parser.add_argument('--file', required=True, metavar='FILE',
                        help='Path to the artifact file to upload')
    parser.add_argument('--title', required=True, help='Listing title')

    desc_group = parser.add_mutually_exclusive_group(required=True)
    desc_group.add_argument('--description', help='Listing description (inline)')
    desc_group.add_argument('--description-file', metavar='FILE',
                            help='Path to a plain-text file containing the listing description')

    parser.add_argument('--tech-stack', default='Python',
                        help='Tech stack label (default: Python)')

    ps_group = parser.add_mutually_exclusive_group()
    ps_group.add_argument('--prompt-summary', default=None,
                          help='Optional prompt summary (inline)')
    ps_group.add_argument('--prompt-summary-file', metavar='FILE',
                          help='Path to a plain-text file containing the prompt summary')

    parser.add_argument('--price', type=float, default=1.0,
                        help='Item price in USDC (default: 1.0)')
    parser.add_argument('--listing-record', default='./local-state/last-listing.json',
                        metavar='FILE',
                        help='Path to write the listing record (default: ./local-state/last-listing.json)')
    parser.add_argument('--api-key-file', metavar='FILE',
                        help='Path to api-key.json written by register_agent.py; required with --execute')
    parser.add_argument('--execute', action='store_true',
                        help='Upload the artifact and metadata to SpawnXchange')
    args = parser.parse_args()

    description = (
        Path(args.description_file).read_text()
        if args.description_file
        else args.description
    )
    prompt_summary = (
        Path(args.prompt_summary_file).read_text()
        if args.prompt_summary_file
        else args.prompt_summary
    )

    try:
        if args.execute and not args.api_key_file:
            raise RuntimeError('--api-key-file is required with --execute')
        api_key = _load_api_key(args.api_key_file) if args.execute else None
        data = list_item(
            args.file,
            args.title,
            description,
            api_key,
            tech_stack=args.tech_stack,
            prompt_summary=prompt_summary,
            price_usdc=args.price,
            listing_record=args.listing_record,
            dry_run=not args.execute,
        )
    except RuntimeError as exc:
        raise SystemExit(str(exc)) from exc
    print(json.dumps(data, indent=2))
