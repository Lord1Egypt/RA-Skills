#!/usr/bin/env python3
"""Tweet scheduler — checks Notion Tweet Pipeline for approved tweets and schedules
one-shot OpenClaw crons to post each at its exact scheduled time.

Tweets already past their scheduled time get posted immediately.
Future tweets get a cron scheduled for the right moment.

Run from heartbeat. Actual posting is done by tweet_post_one.py via cron.

Usage:
  python3 scripts/tweet_poster.py [--dry-run]
"""

import sys, os, json, subprocess, urllib.request
from datetime import datetime
from zoneinfo import ZoneInfo

AEST = ZoneInfo("Australia/Sydney")
TWEET_DB = "314c9a82-0734-81be-ac58-ddd878576cf0"
PYTHON = "/Users/loki/.pyenv/versions/3.14.3/bin/python3"
POST_SCRIPT = "/Users/loki/.openclaw/workspace/scripts/tweet_post_one.py"
STATE_FILE = os.path.expanduser("~/.openclaw/workspace/memory/scheduled-tweets.json")


def notion_headers():
    sa = open(os.path.expanduser("~/.config/openclaw/.op-service-token")).read().strip()
    env = {**os.environ, "OP_SERVICE_ACCOUNT_TOKEN": sa}
    key = subprocess.check_output(
        ["op", "read", "op://OpenClaw/Notion API Key/credential"], env=env
    ).decode().strip()
    return {
        "Authorization": f"Bearer {key}",
        "Notion-Version": "2022-06-28",
        "Content-Type": "application/json",
    }


def get_approved_tweets(headers: dict) -> list[dict]:
    """Query Notion for all Approved tweets."""
    payload = {
        "filter": {
            "property": "Status",
            "select": {"equals": "Approved"}
        },
        "sorts": [{"property": "Scheduled Time", "direction": "ascending"}]
    }
    data = json.dumps(payload).encode()
    req = urllib.request.Request(
        f"https://api.notion.com/v1/databases/{TWEET_DB}/query",
        data=data, headers=headers
    )
    resp = urllib.request.urlopen(req)
    results = json.loads(resp.read()).get("results", [])

    tweets = []
    for page in results:
        props = page["properties"]
        sched = props.get("Scheduled Time", {}).get("date", {})
        if not sched or not sched.get("start"):
            continue
        sched_dt = datetime.fromisoformat(sched["start"])
        page_id = page["id"]

        # Get preview text for logging
        blocks_req = urllib.request.Request(
            f"https://api.notion.com/v1/blocks/{page_id}/children",
            headers=headers
        )
        blocks = json.loads(urllib.request.urlopen(blocks_req).read()).get("results", [])
        text_parts = []
        for block in blocks:
            if block["type"] == "paragraph":
                for rt in block["paragraph"].get("rich_text", []):
                    text_parts.append(rt.get("plain_text", ""))
        text = "\n".join(text_parts).strip()

        tweets.append({
            "page_id": page_id,
            "text": text,
            "scheduled_dt": sched_dt,
            "scheduled": sched["start"],
            "chars": len(text),
        })
    return tweets


def load_scheduled():
    """Load set of page IDs already scheduled."""
    if os.path.exists(STATE_FILE):
        with open(STATE_FILE) as f:
            return set(json.load(f).get("scheduled", []))
    return set()


def save_scheduled(scheduled: set):
    os.makedirs(os.path.dirname(STATE_FILE), exist_ok=True)
    with open(STATE_FILE, "w") as f:
        json.dump({"scheduled": list(scheduled)}, f)


def schedule_cron(page_id: str, sched_dt: datetime, preview: str):
    """Schedule a one-shot OpenClaw cron to post the tweet."""
    cron_time = sched_dt.strftime("%Y-%m-%dT%H:%M")
    name = f"Tweet {page_id[:8]}"
    message = (
        f"Post this scheduled tweet now. Run:\n"
        f"{PYTHON} {POST_SCRIPT} {page_id}\n"
        f"Report success or failure."
    )

    node = "/opt/homebrew/Cellar/node@24/24.14.0/bin/node"
    openclaw = os.path.expanduser("~/.npm-global/bin/openclaw")
    cmd = [
        node, openclaw, "cron", "add",
        "--name", name,
        "--at", cron_time,
        "--tz", "Australia/Sydney",
        "--message", message,
        "--delete-after-run",
        "--announce",
        "--model", "sonnet",
        "--timeout-seconds", "60",
    ]
    result = subprocess.run(cmd, capture_output=True, text=True)
    if result.returncode == 0:
        print(f"  ⏰ Cron scheduled for {cron_time} AEST")
    else:
        print(f"  ❌ Cron scheduling failed: {result.stderr.strip()}")
        if result.stdout:
            print(f"     stdout: {result.stdout.strip()}")
    return result.returncode == 0


def post_immediately(page_id: str):
    """Post a past-due tweet immediately."""
    result = subprocess.run(
        [PYTHON, POST_SCRIPT, page_id],
        capture_output=True, text=True
    )
    print(result.stdout.strip())
    if result.returncode != 0 and result.stderr:
        print(f"  stderr: {result.stderr.strip()}")


def main():
    dry_run = "--dry-run" in sys.argv
    headers = notion_headers()
    tweets = get_approved_tweets(headers)

    if not tweets:
        print("No approved tweets in pipeline.")
        return

    now = datetime.now(AEST)
    already_scheduled = load_scheduled()
    newly_scheduled = set()

    print(f"Found {len(tweets)} approved tweet(s):")

    for tweet in tweets:
        page_id = tweet["page_id"]
        print(f"\n  Page: {page_id}")
        print(f"  Scheduled: {tweet['scheduled']}")
        print(f"  Text ({tweet['chars']} chars): {tweet['text'][:80]}...")

        if tweet["chars"] > 280:
            print("  ⚠️ Over 280 chars — skipping (fix in Notion)")
            continue

        if page_id in already_scheduled:
            print("  ⏭️ Already scheduled — skipping")
            newly_scheduled.add(page_id)
            continue

        if dry_run:
            if tweet["scheduled_dt"] <= now:
                print("  [DRY RUN] Would post immediately (past due)")
            else:
                print(f"  [DRY RUN] Would schedule cron for {tweet['scheduled_dt'].strftime('%Y-%m-%d %H:%M')}")
            continue

        if tweet["scheduled_dt"] <= now:
            print("  📤 Past due — posting now...")
            post_immediately(page_id)
        else:
            if schedule_cron(page_id, tweet["scheduled_dt"], tweet["text"][:60]):
                newly_scheduled.add(page_id)

    # Save state (keep only tweets we just saw as still approved)
    save_scheduled(newly_scheduled)
    print("\nDone.")


if __name__ == "__main__":
    main()
