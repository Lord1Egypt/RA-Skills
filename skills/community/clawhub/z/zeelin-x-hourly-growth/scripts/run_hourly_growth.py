#!/usr/bin/env python3
import argparse
import json
import os
import random
import re
import subprocess
import sys
import time
import urllib.parse
import urllib.request
from datetime import datetime, timedelta
from pathlib import Path

try:
    import websocket
except ImportError as exc:
    raise SystemExit("Missing websocket-client. Install with: python3 -m pip install websocket-client") from exc


PORT_DEFAULT = 9222
HOME_DIR = Path(os.path.expanduser("~"))
PROFILE_DIR = Path(os.environ.get("OPENCLAW_CHROME_PROFILE", str(HOME_DIR / ".openclaw/browser/user/user-data")))
STATE_DIR_DEFAULT = Path(os.environ.get("X_GROWTH_STATE_DIR", str(HOME_DIR / ".openclaw/workspace/state/x-hourly-growth")))
TEMPLATE_FILE = Path(__file__).resolve().parents[1] / "references" / "comment-templates.txt"
ACCOUNT_HINTS = ("@Gsdata5566", "AI Professor")

DEFAULT_QUERIES = [
    "follow back AI builders",
    "AI builders follow back",
    "mutuals AI builders",
    "looking to connect AI builders",
    "agent builders mutuals",
    "SaaS builders follow back",
    "LLM builders follow back",
    "automation builders mutuals",
]

GOOD_TERMS = (
    "ai", "automation", "agent", "agents", "llm", "rag", "builder", "builders",
    "startup", "saas", "open source", "workflow", "workflows", "shipping",
)
FOLLOW_TERMS = (
    "follow back", "follow = follow", "follow=follow", "mutual", "mutuals",
    "connect", "grow together", "looking to connect", "let's connect", "lets connect",
)
BAD_TERMS = (
    "airdrop", "casino", "forex", "nft", "crypto", "pump", "onlyfans",
    "giveaway", "whitelist", "presale", "telegram", "betting", "loan",
    "bnb", "blockchain", "on-chain", "web3", "mainnet", "token", "wallet",
)


class CDP:
    def __init__(self, port: int):
        self.port = port
        self.ws = None
        self.seq = 0

    def connect(self):
        ws_url = get_page_ws_url(self.port)
        origins = [f"http://127.0.0.1:{self.port}", "http://localhost", None]
        last_error = None
        for origin in origins:
            try:
                opts = {}
                if origin:
                    opts["origin"] = origin
                self.ws = websocket.create_connection(ws_url, timeout=60, **opts)
                self.send("Page.enable")
                self.send("Runtime.enable")
                return
            except Exception as exc:
                last_error = exc
                try:
                    if self.ws:
                        self.ws.close()
                except Exception:
                    pass
        raise RuntimeError(f"CDP websocket failed: {last_error}")

    def close(self):
        try:
            if self.ws:
                self.ws.close()
        except Exception:
            pass

    def send(self, method, params=None):
        self.seq += 1
        payload = {"id": self.seq, "method": method}
        if params is not None:
            payload["params"] = params
        self.ws.send(json.dumps(payload))
        while True:
            msg = json.loads(self.ws.recv())
            if msg.get("id") == self.seq:
                if "error" in msg:
                    raise RuntimeError(f"{method} failed: {msg['error']}")
                return msg.get("result", {})

    def eval(self, expression, await_promise=False):
        return self.send("Runtime.evaluate", {
            "expression": expression,
            "awaitPromise": await_promise,
            "returnByValue": True,
        }).get("result", {}).get("value")

    def navigate(self, url):
        self.send("Page.navigate", {"url": url})
        time.sleep(5)

    def insert_text(self, text):
        self.send("Input.insertText", {"text": text})


def get_json(url, timeout=5):
    with urllib.request.urlopen(url, timeout=timeout) as res:
        return json.loads(res.read().decode("utf-8"))


def get_page_ws_url(port):
    targets = get_json(f"http://127.0.0.1:{port}/json/list")
    for target in targets:
        if target.get("type") == "page" and target.get("webSocketDebuggerUrl"):
            return target["webSocketDebuggerUrl"]
    # Some Chrome builds require PUT for /json/new, so try both.
    new_url = f"http://127.0.0.1:{port}/json/new?{urllib.parse.quote('https://x.com/home')}"
    for method in ("PUT", "GET"):
        try:
            req = urllib.request.Request(new_url, method=method)
            with urllib.request.urlopen(req, timeout=5) as res:
                target = json.loads(res.read().decode("utf-8"))
            if target.get("webSocketDebuggerUrl"):
                return target["webSocketDebuggerUrl"]
        except Exception:
            pass
    targets = get_json(f"http://127.0.0.1:{port}/json/list")
    for target in targets:
        if target.get("type") == "page" and target.get("webSocketDebuggerUrl"):
            return target["webSocketDebuggerUrl"]
    raise RuntimeError("No Chrome page target found for CDP")


def ensure_chrome(port):
    try:
        cdp = CDP(port)
        cdp.connect()
        cdp.close()
        return
    except Exception:
        pass

    # Restart only the OpenClaw profile Chrome so normal personal Chrome windows are left alone.
    subprocess.run(["pkill", "-f", str(PROFILE_DIR)], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    time.sleep(2)
    for name in ("SingletonLock", "SingletonSocket", "SingletonCookie"):
        try:
            (PROFILE_DIR / name).unlink()
        except FileNotFoundError:
            pass

    args = [
        "open", "-na", "Google Chrome", "--args",
        f"--remote-debugging-port={port}",
        f"--user-data-dir={PROFILE_DIR}",
        "--remote-allow-origins=*",
        "--no-first-run",
        "--no-default-browser-check",
        "https://x.com/home",
    ]
    subprocess.Popen(args, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    deadline = time.time() + 30
    last = None
    while time.time() < deadline:
        try:
            cdp = CDP(port)
            cdp.connect()
            cdp.close()
            return
        except Exception as exc:
            last = exc
            time.sleep(1)
    raise RuntimeError(f"Chrome CDP did not become ready: {last}")


def today_key():
    return datetime.now().strftime("%Y-%m-%d")


def load_ledger(state_dir):
    path = state_dir / "ledger.json"
    if not path.exists():
        return {"posts": {}, "authors": {}, "daily": {}}
    with path.open("r", encoding="utf-8") as fh:
        data = json.load(fh)
    data.setdefault("posts", {})
    data.setdefault("authors", {})
    data.setdefault("daily", {})
    return data


def save_ledger(state_dir, ledger):
    state_dir.mkdir(parents=True, exist_ok=True)
    tmp = state_dir / "ledger.json.tmp"
    with tmp.open("w", encoding="utf-8") as fh:
        json.dump(ledger, fh, ensure_ascii=False, indent=2)
    tmp.replace(state_dir / "ledger.json")


def in_active_hours(spec):
    if not spec:
        return True
    hour = datetime.now().hour
    match = re.fullmatch(r"\s*(\d{1,2})\s*-\s*(\d{1,2})\s*", spec)
    if not match:
        raise ValueError(f"Invalid active hours: {spec}")
    start, end = int(match.group(1)), int(match.group(2))
    if start <= end:
        return start <= hour <= end
    return hour >= start or hour <= end


def load_templates():
    if TEMPLATE_FILE.exists():
        templates = [line.strip() for line in TEMPLATE_FILE.read_text(encoding="utf-8").splitlines() if line.strip()]
        if templates:
            return templates
    return [
        "Great to connect. I am building AI automation and agent workflows too. Happy to meet more real builders in this space.",
        "Nice to meet another AI builder. I am focused on agents, automation workflows, and growth systems. Happy to stay connected.",
    ]


def normalize_status(url):
    match = re.search(r"https://x\.com/([^/\s]+)/status/(\d+)", url)
    if not match:
        return None
    return f"https://x.com/{match.group(1)}/status/{match.group(2)}"


def author_from_url(url):
    match = re.search(r"https://x\.com/([^/\s]+)/status/\d+", url)
    return match.group(1).lower() if match else ""


def score_text(text):
    lower = text.lower()
    if any(term in lower for term in BAD_TERMS):
        return -20
    if not any(term in lower for term in FOLLOW_TERMS):
        return -10
    if not any(term in lower for term in GOOD_TERMS):
        return -10
    score = 0
    score += 6 if any(term in lower for term in FOLLOW_TERMS) else 0
    score += sum(2 for term in GOOD_TERMS if term in lower)
    if "follow back" in lower or "follow = follow" in lower or "follow=follow" in lower:
        score += 4
    if len(text) < 30:
        score -= 4
    if len(text) > 1200:
        score -= 2
    return score


def search_candidates(cdp, queries, limit_per_query=14):
    candidates = {}
    since = (datetime.now() - timedelta(days=14)).strftime("%Y-%m-%d")
    for query in queries:
        scoped_query = query if "since:" in query else f"{query} since:{since}"
        url = "https://x.com/search?q=" + urllib.parse.quote(scoped_query) + "&src=typed_query&f=live"
        cdp.navigate(url)
        for _ in range(3):
            cdp.eval("window.scrollBy(0, 900); true")
            time.sleep(1.2)
        rows = cdp.eval("""
(() => {
  const out = [];
  const articles = Array.from(document.querySelectorAll('article')).slice(0, 30);
  for (const article of articles) {
    const text = article.innerText || '';
    const links = Array.from(article.querySelectorAll('a[href*="/status/"]')).map(a => a.href);
    for (const href of links) {
      out.push({href, text});
    }
  }
  return out;
})()
""") or []
        for row in rows[:limit_per_query]:
            url = normalize_status(row.get("href", ""))
            text = (row.get("text") or "").strip()
            if not url or not text:
                continue
            score = score_text(text)
            if score < 7:
                continue
            if url not in candidates or score > candidates[url]["score"]:
                candidates[url] = {"url": url, "text": text, "query": scoped_query, "score": score}
        time.sleep(random.uniform(1.5, 3.5))
    return sorted(candidates.values(), key=lambda item: item["score"], reverse=True)


def choose_comment(templates, url, text):
    seed = f"{today_key()}:{url}:{len(text)}"
    rng = random.Random(seed)
    return rng.choice(templates)


def post_reply(cdp, url, text):
    cdp.navigate(url)
    time.sleep(random.uniform(2, 4))
    focused = cdp.eval("""
(() => {
  const candidates = Array.from(document.querySelectorAll(
    '[data-testid="tweetTextarea_0"], [contenteditable="true"][role="textbox"], [role="textbox"]'
  )).filter(el => el.offsetParent !== null);
  const box = candidates[0];
  if (!box) return false;
  box.scrollIntoView({block: 'center'});
  box.focus();
  return true;
})()
""")
    if not focused:
        raise RuntimeError("reply composer not found")
    time.sleep(0.7)
    cdp.insert_text(text)
    time.sleep(random.uniform(0.8, 1.6))
    clicked = cdp.eval("""
(() => {
  const buttons = Array.from(document.querySelectorAll('[data-testid="tweetButtonInline"], [data-testid="tweetButton"]'))
    .filter(btn => btn.offsetParent !== null && !btn.disabled && btn.getAttribute('aria-disabled') !== 'true');
  const btn = buttons[0];
  if (!btn) return false;
  btn.click();
  return true;
})()
""")
    if not clicked:
        raise RuntimeError("reply send button not available")
    time.sleep(5)
    verify = cdp.eval("""
(() => {
  const body = document.body.innerText || '';
  return {
    sent: /Your post was sent|Your reply was sent|你的帖子已发送|已发送/.test(body),
    error: /Something went wrong|出错了|请稍后再试|Try again/.test(body)
  };
})()
""")
    if isinstance(verify, dict) and verify.get("error") and not verify.get("sent"):
        raise RuntimeError("X displayed a send error")
    return True


def safe_post_reply(cdp, url, comment):
    try:
        return post_reply(cdp, url, comment), comment
    except Exception:
        fallback = "Great to connect. I am building AI automation and agent workflows too. Happy to meet more builders here."
        return post_reply(cdp, url, fallback), fallback


def main():
    parser = argparse.ArgumentParser(description="Hourly X growth comments via Chrome CDP")
    parser.add_argument("--max-comments", type=int, default=int(os.environ.get("X_GROWTH_MAX_COMMENTS", "8")))
    parser.add_argument("--daily-cap", type=int, default=int(os.environ.get("X_GROWTH_DAILY_CAP", "56")))
    parser.add_argument("--active-hours", default=os.environ.get("X_GROWTH_ACTIVE_HOURS", "9-15"))
    parser.add_argument("--state-dir", default=str(STATE_DIR_DEFAULT))
    parser.add_argument("--port", type=int, default=PORT_DEFAULT)
    parser.add_argument("--dry-run", action="store_true")
    parser.add_argument("--query", action="append", dest="queries")
    args = parser.parse_args()

    state_dir = Path(args.state_dir).expanduser()
    state_dir.mkdir(parents=True, exist_ok=True)
    ledger = load_ledger(state_dir)
    day = today_key()
    daily = ledger["daily"].setdefault(day, {"success": 0, "fail": 0})

    if not args.dry_run and not in_active_hours(args.active_hours):
        print(f"Outside active hours ({args.active_hours}); exiting.")
        return 0
    if not args.dry_run and daily.get("success", 0) >= args.daily_cap:
        print(f"Daily cap reached: {daily.get('success', 0)}/{args.daily_cap}")
        return 0

    ensure_chrome(args.port)
    cdp = CDP(args.port)
    cdp.connect()
    templates = load_templates()
    queries = args.queries or DEFAULT_QUERIES

    try:
        candidates = search_candidates(cdp, queries)
        filtered = []
        today_authors = set(ledger.get("authors", {}).get(day, []))
        for item in candidates:
            author = author_from_url(item["url"])
            if item["url"] in ledger["posts"]:
                continue
            if author in today_authors:
                continue
            filtered.append(item)

        if args.dry_run:
            print(json.dumps(filtered[: args.max_comments], ensure_ascii=False, indent=2))
            return 0

        sent = 0
        for item in filtered:
            author = author_from_url(item["url"])
            if author and author in ledger.setdefault("authors", {}).setdefault(day, []):
                continue
            if sent >= args.max_comments:
                break
            if daily.get("success", 0) >= args.daily_cap:
                break
            comment = choose_comment(templates, item["url"], item["text"])
            now = datetime.now().isoformat(timespec="seconds")
            try:
                _, used_comment = safe_post_reply(cdp, item["url"], comment)
                ledger["posts"][item["url"]] = {
                    "status": "success",
                    "time": now,
                    "query": item["query"],
                    "score": item["score"],
                    "comment": used_comment,
                }
                if author and author not in ledger["authors"][day]:
                    ledger["authors"][day].append(author)
                daily["success"] = daily.get("success", 0) + 1
                sent += 1
                print(f"OK {item['url']}")
                save_ledger(state_dir, ledger)
                time.sleep(random.uniform(45, 120))
            except Exception as exc:
                ledger["posts"][item["url"]] = {
                    "status": "failed",
                    "time": now,
                    "query": item["query"],
                    "score": item["score"],
                    "error": str(exc),
                }
                daily["fail"] = daily.get("fail", 0) + 1
                save_ledger(state_dir, ledger)
                print(f"FAIL {item['url']} {exc}", file=sys.stderr)
                time.sleep(random.uniform(10, 25))
        print(f"Sent {sent} replies. Daily success: {daily.get('success', 0)}/{args.daily_cap}")
        return 0
    finally:
        cdp.close()
        save_ledger(state_dir, ledger)


if __name__ == "__main__":
    raise SystemExit(main())
