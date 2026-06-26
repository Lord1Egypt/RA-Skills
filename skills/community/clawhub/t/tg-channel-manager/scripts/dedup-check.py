#!/usr/bin/env python3
"""
Check topic/link for duplicates against existing channel posts.

Usage:
  python3 dedup-check.py --base-dir /path/to/workspace --topic "topic" --links "url1" "url2"
  python3 dedup-check.py --base-dir /path/to/workspace --add 123 --topic "topic" --links "url"
  python3 dedup-check.py --base-dir /path/to/workspace --rebuild --channel-id "-100xxx"

--base-dir points to the agent's workspace where content-index.json is located.
If not specified, the current directory is used.
"""

import argparse
import json
import os
import re
import sys
import time


def get_paths(base_dir):
    """Return paths to index and log files."""
    base = os.path.abspath(base_dir)
    return {
        'index': os.path.join(base, 'content-index.json'),
        'perf_log': os.path.join(base, 'content-perf.log'),
    }


def log_perf(perf_log, action, duration_ms, details=""):
    with open(perf_log, "a") as f:
        ts = time.strftime("%Y-%m-%d %H:%M:%S", time.gmtime())
        f.write(f"{ts} | {action} | {duration_ms:.0f}ms | {details}\n")


def load_index(index_file):
    if not os.path.exists(index_file):
        return []
    try:
        with open(index_file, "r") as f:
            data = json.load(f)
    except (json.JSONDecodeError, OSError) as e:
        print(f"Warning: corrupt index {index_file}: {e}", file=sys.stderr)
        return []
    if isinstance(data, dict) and "posts" in data:
        return data["posts"]
    return data


def save_index(index_file, index):
    # Preserve versioned wrapper if the file already has one
    wrapper = None
    if os.path.exists(index_file):
        try:
            with open(index_file, "r") as f:
                existing = json.load(f)
        except (json.JSONDecodeError, OSError):
            existing = None
        if isinstance(existing, dict) and "version" in existing:
            wrapper = {"version": existing["version"], "posts": index}
    with open(index_file, 'w') as f:
        json.dump(wrapper if wrapper else index, f, ensure_ascii=False, indent=2)


def check_topic(topic, index):
    """Check topic by keywords. Returns a list of matches."""
    topic_words = set(re.findall(r'[^\W\d_]{4,}', topic.lower(), re.UNICODE))
    stop = {'this', 'that', 'with', 'from', 'have', 'been', 'will', 'what', 'when',
            'which', 'their', 'about', 'would', 'could', 'should', 'more', 'some',
            'into', 'than', 'other', 'these', 'those', 'just', 'also', 'only',
            'agent', 'agents'}
    topic_words -= stop

    matches = []
    for post in index:
        post_words = set(w.lower() for w in post.get('keywords', []))
        post_words -= stop
        if not topic_words or not post_words:
            continue
        # Exact match
        overlap = topic_words & post_words
        # Fuzzy: common stem (first 5 chars)
        topic_stems = {w[:5] for w in topic_words if len(w) >= 5}
        post_stems = {w[:5] for w in post_words if len(w) >= 5}
        stem_overlap = topic_stems & post_stems
        # Take the best of both methods
        best_overlap = max(len(overlap), len(stem_overlap))
        score = best_overlap / min(len(topic_words), len(post_words)) if topic_words and post_words else 0
        # Collect all matched words for the report
        all_overlap = overlap | {f"{s}*" for s in stem_overlap - {w[:5] for w in overlap}}
        if score >= 0.4 and best_overlap >= 2:
            matches.append({
                'msgId': post['msgId'],
                'topic': post['topic'][:100],
                'score': round(score, 2),
                'overlap': list(all_overlap)
            })

    matches.sort(key=lambda x: x['score'], reverse=True)
    return matches


def check_links(links, index):
    """Check links for exact matches."""
    norm = lambda u: re.sub(r'https?://(www\.)?', '', u.rstrip('/'))
    matches = []
    for post in index:
        for link in links:
            for plink in post.get('links', []):
                if norm(link) == norm(plink):
                    matches.append({
                        'msgId': post['msgId'],
                        'topic': post['topic'][:100],
                        'link': plink
                    })
    return matches


def rebuild_index_instructions(channel_id):
    """Print instructions for rebuilding the index via Telegram search API."""
    print("📋 Index rebuild via Telegram search API:")
    print()
    print("The agent should perform the following steps:")
    print()
    print(f"1. Fetch recent channel messages:")
    print(f'   message tool (action=search, channel=telegram, target={channel_id}, query="")')
    print()
    print("2. For each found message:")
    print("   - Extract msgId, text, links")
    print("   - Add to the index via --add:")
    print(f'   python3 dedup-check.py --base-dir <workspace> --add <msgId> --topic "first line" --links "url"')
    print()
    print("3. Repeat search with different keywords for completeness")
    print()
    print("Note: Bot API cannot read the full channel history.")
    print("A complete rebuild may require multiple queries with different keywords.")


def add_post(index_file, msg_id, topic, links=None, keywords=None):
    """Add a post to the index after publishing."""
    index = load_index(index_file)

    if not index and os.path.isfile(index_file) and os.path.getsize(index_file) > 0:
        try:
            with open(index_file, "r") as f:
                json.load(f)
            # Valid JSON with empty posts — not corrupt, proceed normally
        except (json.JSONDecodeError, OSError):
            print(f"Error: {index_file} exists but failed to load (corrupt?). "
                  "Refusing --add to avoid data loss.", file=sys.stderr)
            return None

    if any(p['msgId'] == msg_id for p in index):
        return False

    if not keywords:
        keywords = list(set(re.findall(r'[^\W\d_]{4,}', topic.lower(), re.UNICODE)))

    index.append({
        'msgId': msg_id,
        'topic': topic,
        'links': links or [],
        'keywords': keywords
    })
    index.sort(key=lambda x: x['msgId'])
    save_index(index_file, index)
    return True


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Content deduplication for Telegram channels')
    parser.add_argument('--base-dir', type=str, default='.', help='Path to workspace (where content-index.json is located)')
    parser.add_argument('--topic', type=str, help='Topic to check')
    parser.add_argument('--links', type=str, nargs='*', help='Links to check')
    parser.add_argument('--rebuild', action='store_true', help='Print index rebuild instructions')
    parser.add_argument('--channel-id', type=str, help='Channel ID (for --rebuild)')
    parser.add_argument('--add', type=int, help='Add a post (msgId)')
    args = parser.parse_args()

    paths = get_paths(args.base_dir)

    if args.rebuild:
        channel_id = args.channel_id or "<channelId>"
        rebuild_index_instructions(channel_id)
        sys.exit(0)

    if args.add is not None and args.topic:
        result = add_post(paths['index'], args.add, args.topic, args.links)
        if result is None:
            sys.exit(1)
        elif result:
            print(f"✅ Post {args.add} added to index")
        else:
            print(f"⚠️ Post {args.add} already in index")
        sys.exit(0)

    if not args.topic and not args.links:
        print("Provide --topic and/or --links")
        sys.exit(1)

    t0 = time.time()
    index = load_index(paths['index'])
    results = {'topic_matches': [], 'link_matches': []}

    if args.topic:
        results['topic_matches'] = check_topic(args.topic, index)

    if args.links:
        results['link_matches'] = check_links(args.links, index)

    dur = (time.time() - t0) * 1000
    total = len(results['topic_matches']) + len(results['link_matches'])
    log_perf(paths['perf_log'], "check", dur,
             f"topic={'yes' if args.topic else 'no'} links={len(args.links or [])} matches={total} index_size={len(index)}")

    if total == 0:
        print(f"✅ No duplicates found ({dur:.0f}ms, {len(index)} posts in index)")
    else:
        print(f"⚠️ Possible duplicates found ({dur:.0f}ms):")
        for m in results['topic_matches']:
            print(f"  📝 msg {m['msgId']} (score {m['score']}): {m['topic']}")
            print(f"     matches: {', '.join(m['overlap'])}")
        for m in results['link_matches']:
            print(f"  🔗 msg {m['msgId']}: {m['topic']}")
            print(f"     link: {m['link']}")
