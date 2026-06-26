#!/usr/bin/env python3
from __future__ import annotations
import argparse, json, os, sys, urllib.request
from datetime import datetime, timezone
from common import CONFIG_PATH, STATE_PATH, load_json, save_json

API_URL = 'https://ai.6551.io/open/twitter_user_tweets'
SEARCH_URL = 'https://ai.6551.io/open/twitter_search'


def now_iso() -> str:
    return datetime.now(timezone.utc).isoformat()


def _post_json(url: str, payload: dict, token: str):
    req = urllib.request.Request(url, data=json.dumps(payload).encode('utf-8'), method='POST')
    req.add_header('Authorization', f'Bearer {token}')
    req.add_header('Content-Type', 'application/json')
    with urllib.request.urlopen(req, timeout=30) as resp:
        raw = resp.read().decode('utf-8')
    try:
        return json.loads(raw)
    except Exception:
        return {'raw': raw}


def call_6551_user_tweets(username: str, token: str, max_results: int, include_replies: bool, include_retweets: bool):
    return _post_json(API_URL, {
        'username': username,
        'maxResults': max_results,
        'product': 'Latest',
        'includeReplies': include_replies,
        'includeRetweets': include_retweets,
    }, token)


def call_6551_search_from_user(username: str, token: str, max_results: int, exclude_replies: bool, exclude_retweets: bool):
    return _post_json(SEARCH_URL, {
        'fromUser': username,
        'maxResults': max_results,
        'product': 'Latest',
        'excludeReplies': exclude_replies,
        'excludeRetweets': exclude_retweets,
    }, token)


def normalize_tweets(data):
    if isinstance(data, list):
        return data
    if isinstance(data, dict):
        for key in ['tweets', 'data', 'items', 'list']:
            v = data.get(key)
            if isinstance(v, list):
                return v
            if isinstance(v, dict):
                for kk in ['tweets', 'items', 'list', 'data']:
                    vv = v.get(kk) if isinstance(v, dict) else None
                    if isinstance(vv, list):
                        return vv
    return []


def tweet_id(tweet):
    return str(tweet.get('id') or tweet.get('tweetId') or tweet.get('rest_id') or '')


def tweet_text(tweet):
    return tweet.get('text') or tweet.get('fullText') or tweet.get('content') or ''


def is_reply(tweet):
    return bool(tweet.get('inReplyToStatusId') or tweet.get('inReplyToTweetId') or tweet.get('in_reply_to_status_id') or tweet.get('isReply'))


def is_retweet(tweet):
    text = tweet_text(tweet)
    return bool(tweet.get('retweetedTweetId') or tweet.get('retweeted_status_result') or text.startswith('RT @'))


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--author')
    args = ap.parse_args()

    token = os.environ.get('TWITTER_TOKEN')
    if not token:
        print(json.dumps({'ok': False, 'error': 'TWITTER_TOKEN missing'}), file=sys.stderr)
        raise SystemExit(2)

    cfg = load_json(CONFIG_PATH, {})
    state = load_json(STATE_PATH, {'seenTweetIds': [], 'replyLog': [], 'pendingTweets': [], 'lastCheckedAt': None, 'lastCheckedByAuthor': {}})
    authors = [args.author] if args.author else cfg.get('authors', [])
    max_results = int(cfg.get('maxResultsPerAuthor', 5))
    skip_replies = bool(cfg.get('skipReplies', True))
    skip_retweets = bool(cfg.get('skipRetweets', True))
    seen = set(state.get('seenTweetIds', []))

    results = []
    pending_acc = []
    for author in authors:
        source = 'twitter_user_tweets'
        try:
            data = call_6551_user_tweets(author, token, max_results, include_replies=not skip_replies, include_retweets=not skip_retweets)
            tweets = normalize_tweets(data)
            if not tweets:
                raise ValueError('empty tweets from twitter_user_tweets')
        except Exception:
            source = 'twitter_search_fromUser'
            data = call_6551_search_from_user(author, token, max_results, exclude_replies=skip_replies, exclude_retweets=skip_retweets)
            tweets = normalize_tweets(data)

        fresh = []
        for t in tweets:
            tid = tweet_id(t)
            if not tid or tid in seen:
                continue
            if skip_replies and is_reply(t):
                continue
            if skip_retweets and is_retweet(t):
                continue
            fresh.append({
                'id': tid,
                'author': author,
                'text': tweet_text(t),
                'createdAt': t.get('createdAt') or t.get('created_at'),
                'url': f'https://x.com/{author}/status/{tid}'
            })
        state.setdefault('lastCheckedByAuthor', {})[author] = now_iso()
        results.append({'author': author, 'source': source, 'newTweets': fresh, 'fetchedCount': len(tweets)})
        pending_acc.extend(fresh)

    state['pendingTweets'] = pending_acc
    state['lastCheckedAt'] = now_iso()
    save_json(STATE_PATH, state)
    print(json.dumps({'ok': True, 'results': results}, ensure_ascii=False, indent=2))


if __name__ == '__main__':
    main()
