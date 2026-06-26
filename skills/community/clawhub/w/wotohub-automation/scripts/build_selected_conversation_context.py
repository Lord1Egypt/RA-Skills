#!/usr/bin/env python3
import argparse
import json
from pathlib import Path

import inbox
from common import get_token


def _extract_dialogue_items(resp: dict) -> list[dict]:
    data = resp.get('data') if isinstance(resp, dict) else None
    if isinstance(data, list):
        return [x for x in data if isinstance(x, dict)]
    if isinstance(data, dict):
        for key in ('records', 'list', 'rows', 'dataList'):
            if isinstance(data.get(key), list):
                return [x for x in data[key] if isinstance(x, dict)]
    return []


def load_candidates(path: str) -> dict:
    return json.loads(Path(path).read_text())


def normalize_item(item: dict) -> dict:
    return {
        'id': item.get('id'),
        'type': item.get('type'),
        'subject': item.get('subject'),
        'cleanContent': item.get('cleanContent') or item.get('content'),
        'createTime': item.get('createTime'),
        'addresser': item.get('addresser'),
        'addressee': item.get('addressee'),
        'cc': item.get('cc'),
        'userName': item.get('userName'),
        'bloggerName': item.get('bloggerName'),
        'bloggerUserName': item.get('bloggerUserName'),
    }


def build_selected_context(token: str, candidates: dict, limit: int = 3) -> dict:
    items = candidates.get('items') or []
    enriched = []
    for item in items[:limit]:
        chat_id = item.get('chatId')
        if not chat_id:
            continue
        dialogue_resp = inbox.get_dialogue(token, str(chat_id))
        dialogue_items = _extract_dialogue_items(dialogue_resp)
        enriched.append({
            **item,
            'thread': [normalize_item(x) for x in dialogue_items],
            'threadDeferred': False,
        })
    return {
        'instruction': 'Use prompts/conversation-analysis.md and references/conversation-analysis-schema.md to generate conversation_analysis JSON for selected threads.',
        'items': enriched,
        'count': len(enriched),
        'source': 'selected-thread-context',
    }


def main():
    ap = argparse.ArgumentParser(description='Load full dialogue only for selected reply candidates')
    ap.add_argument('--input', required=True, help='conversation candidate JSON from build_conversation_analysis_input.py')
    ap.add_argument('--token')
    ap.add_argument('--limit', type=int, default=3)
    ap.add_argument('--output')
    args = ap.parse_args()

    token = get_token(args.token, feature="conversation_context")
    candidates = load_candidates(args.input)
    result = build_selected_context(token, candidates, limit=args.limit)
    if args.output:
        Path(args.output).write_text(json.dumps(result, ensure_ascii=False, indent=2))
    print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == '__main__':
    main()
