#!/usr/bin/env python3
"""
Classify YouTube comments using Gemini Flash.
Categories: spam, question, praise, hate, neutral, constructive
"""

import argparse
import json
import os
import sys
import time
from datetime import datetime, timezone
from urllib.request import urlopen, Request
from urllib.error import HTTPError

GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY") or os.environ.get("GOOGLE_AI_API_KEY")
GEMINI_URL = "https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent"
OUTPUT_DIR = "data/youtube-comment-moderator"

SYSTEM_PROMPT = """You are a YouTube comment classifier. Classify each comment into exactly one category:

- spam: Promotional links, scam offers, bot-like repetitive text, crypto/forex schemes, "check out my channel", self-promotion, phishing
- question: Genuine question about the video content, creator, topic, or requesting information
- praise: Positive feedback, compliments, encouragement, expressing enjoyment
- hate: Hateful, abusive, harassing, or threatening content
- neutral: Generic reactions ("lol", "wow", "first"), timestamps, emojis only, simple agreement
- constructive: Thoughtful criticism, suggestions, detailed feedback, corrections

Also rate confidence 0-100 and suggest an action:
- spam → delete
- question → reply
- praise → thank (or ignore if generic)
- hate → delete
- neutral → ignore
- constructive → flag_review

Respond in JSON array format. Each item: {"id": "comment_id", "category": "...", "confidence": 0-100, "action": "...", "reason": "brief reason"}"""


def classify_batch(comments, batch_size=20):
    """Classify a batch of comments using Gemini Flash."""
    if not GEMINI_API_KEY:
        print("Error: GEMINI_API_KEY not set", file=sys.stderr)
        sys.exit(1)
    
    results = []
    
    for i in range(0, len(comments), batch_size):
        batch = comments[i:i + batch_size]
        
        # Build the prompt
        comment_text = "\n".join([
            f"[{c['comment_id']}] @{c['author']}: {c['text'][:500]}"
            for c in batch
        ])
        
        payload = {
            "contents": [{
                "parts": [{"text": f"{SYSTEM_PROMPT}\n\nClassify these comments:\n\n{comment_text}"}]
            }],
            "generationConfig": {
                "temperature": 0.1,
                "maxOutputTokens": 4096,
                "responseMimeType": "application/json"
            }
        }
        
        url = f"{GEMINI_URL}?key={GEMINI_API_KEY}"
        req = Request(url, data=json.dumps(payload).encode(), headers={
            "Content-Type": "application/json"
        })
        
        try:
            with urlopen(req, timeout=30) as resp:
                data = json.loads(resp.read())
            
            text = data["candidates"][0]["content"]["parts"][0]["text"]
            batch_results = json.loads(text)
            
            if isinstance(batch_results, list):
                results.extend(batch_results)
            else:
                results.append(batch_results)
            
            print(f"  Classified batch {i//batch_size + 1}: {len(batch)} comments")
            
        except (HTTPError, json.JSONDecodeError, KeyError) as e:
            print(f"  Error on batch {i//batch_size + 1}: {e}", file=sys.stderr)
            # Mark as unclassified
            for c in batch:
                results.append({
                    "id": c["comment_id"],
                    "category": "error",
                    "confidence": 0,
                    "action": "flag_review",
                    "reason": f"Classification error: {str(e)[:100]}"
                })
        
        # Rate limit
        if i + batch_size < len(comments):
            time.sleep(1)
    
    return results


def merge_results(comments, classifications):
    """Merge classification results back into comment data."""
    class_map = {c["id"]: c for c in classifications}
    
    merged = []
    for comment in comments:
        cid = comment["comment_id"]
        cls = class_map.get(cid, {
            "category": "unclassified",
            "confidence": 0,
            "action": "flag_review",
            "reason": "Not classified"
        })
        
        merged.append({
            **comment,
            "classification": cls.get("category", "unclassified"),
            "confidence": cls.get("confidence", 0),
            "action": cls.get("action", "flag_review"),
            "reason": cls.get("reason", "")
        })
    
    return merged


def print_summary(classified):
    """Print classification summary."""
    counts = {}
    actions = {}
    for c in classified:
        cat = c["classification"]
        act = c["action"]
        counts[cat] = counts.get(cat, 0) + 1
        actions[act] = actions.get(act, 0) + 1
    
    print("\n=== CLASSIFICATION SUMMARY ===")
    print(f"Total comments: {len(classified)}")
    print("\nBy category:")
    for cat, count in sorted(counts.items(), key=lambda x: -x[1]):
        pct = count / len(classified) * 100
        print(f"  {cat:15s}: {count:4d} ({pct:.1f}%)")
    
    print("\nBy action:")
    for act, count in sorted(actions.items(), key=lambda x: -x[1]):
        print(f"  {act:15s}: {count:4d}")
    
    # Show some examples per category
    print("\n=== EXAMPLES ===")
    shown = {}
    for c in classified:
        cat = c["classification"]
        if cat not in shown:
            shown[cat] = 0
        if shown[cat] < 2:
            print(f"\n[{cat.upper()}] @{c['author']}: {c['text'][:120]}")
            print(f"  → {c['action']} (confidence: {c['confidence']}%) — {c['reason']}")
            shown[cat] += 1


def get_channel_owner_id(video_id):
    """Get the channel owner's author channel ID for a video."""
    api_key = os.environ.get("YOUTUBE_API_KEY")
    if not api_key:
        return None
    from urllib.parse import urlencode as _urlencode
    url = f"https://www.googleapis.com/youtube/v3/videos?part=snippet&id={video_id}&key={api_key}"
    req = Request(url, headers={"User-Agent": "YT-Moderator/1.0"})
    try:
        with urlopen(req, timeout=15) as resp:
            data = json.loads(resp.read())
        if data.get("items"):
            return data["items"][0]["snippet"]["channelId"]
    except Exception:
        pass
    return None


def main():
    parser = argparse.ArgumentParser(description="Classify YouTube comments")
    parser.add_argument("--input", default=os.path.join(OUTPUT_DIR, "comments-raw.json"))
    parser.add_argument("--output", default=os.path.join(OUTPUT_DIR, "comments-classified.json"))
    parser.add_argument("--batch-size", type=int, default=20)
    parser.add_argument("--whitelist-owner", action="store_true", default=True,
                        help="Auto-whitelist channel owner comments (skip classification)")
    args = parser.parse_args()
    
    # Load comments
    with open(args.input) as f:
        data = json.load(f)
    
    comments = data["comments"]
    print(f"Loaded {len(comments)} comments from {args.input}")
    
    # Get channel owner IDs for whitelisting
    owner_ids = set()
    if args.whitelist_owner:
        video_ids = set(c["video_id"] for c in comments)
        for vid in video_ids:
            owner_id = get_channel_owner_id(vid)
            if owner_id:
                owner_ids.add(owner_id)
        if owner_ids:
            print(f"Whitelisted {len(owner_ids)} channel owner(s)")
    
    # Separate owner comments from others
    owner_comments = []
    classify_comments_list = []
    for c in comments:
        if c.get("author_channel_id") in owner_ids:
            owner_comments.append(c)
        else:
            classify_comments_list.append(c)
    
    if owner_comments:
        print(f"Skipping {len(owner_comments)} channel owner comments (whitelisted)")
    
    # Classify non-owner comments
    print(f"Classifying {len(classify_comments_list)} comments with Gemini Flash...")
    classifications = classify_batch(classify_comments_list, args.batch_size)
    
    # Merge — classify non-owner, mark owner as whitelisted
    classified = merge_results(classify_comments_list, classifications)
    
    # Add owner comments back as whitelisted
    for c in owner_comments:
        classified.append({
            **c,
            "classification": "owner",
            "confidence": 100,
            "action": "skip",
            "reason": "Channel owner (whitelisted)"
        })
    
    # Write output
    result = {
        "classified_at": datetime.now(timezone.utc).isoformat(),
        "source": args.input,
        "total": len(classified),
        "comments": classified
    }
    
    with open(args.output, "w") as f:
        json.dump(result, f, indent=2)
    
    print(f"\nClassified → {args.output}")
    print_summary(classified)


if __name__ == "__main__":
    main()
