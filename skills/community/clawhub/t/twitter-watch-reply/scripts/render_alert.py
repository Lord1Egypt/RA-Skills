#!/usr/bin/env python3
from __future__ import annotations
import json
from common import CONFIG_PATH, STATE_PATH, load_json


def build_candidates(text: str):
    text = (text or '').strip()
    short = text[:120].replace('\n', ' ')
    return [
        f'收到，这条新推已经抓到了：{short} 👀',
        f'可以，这条内容已经进监控队列了，后面就能按这个链路继续半自动回复。',
        f'已检测到新推，当前监控链路正常，这条可以继续生成更细的互动回复。'
    ]


def main():
    cfg = load_json(CONFIG_PATH, {})
    state = load_json(STATE_PATH, {})
    pending = state.get('pendingTweets', [])
    notified = set(state.get('notifiedTweetIds', []))
    target = None
    for item in pending:
        tid = str(item.get('id') or '')
        if tid and tid not in notified:
            target = item
            break
    if not target:
        print(json.dumps({'ok': True, 'alert': None}, ensure_ascii=False))
        return

    candidates = build_candidates(target.get('text', ''))[: int(cfg.get('candidateCount', 3) or 3)]
    alert = {
        'tweetId': target.get('id'),
        'author': target.get('author'),
        'url': target.get('url'),
        'text': target.get('text'),
        'candidates': candidates,
        'notify': cfg.get('notify', {}),
    }
    print(json.dumps({'ok': True, 'alert': alert}, ensure_ascii=False, indent=2))


if __name__ == '__main__':
    main()
