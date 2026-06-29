#!/usr/bin/env python3
"""
X.com 全量推文抓取 v2 - 智能搜索模式
- 从最早的推文开始，按时间顺序往前搜索
- 稀疏月份自动拆周搜索
- 回拉触发加载 + 断线恢复
"""
import json, time, os, sys
from datetime import datetime, timedelta
from playwright.sync_api import sync_playwright

OUTPUT_DIR = None
TWEETS_FILE = None
COOKIE_FILE = None
SCROLL_STATE_FILE = None
SCROLL_DELAY = 3
WEEK_CHUNK_THRESHOLD = 30
NEW_TWEET_IDLE_LIMIT = 8  # 连续 N 轮无新推文则退出（回填场景防止死循环）

def init_paths(username):
    global OUTPUT_DIR, TWEETS_FILE, COOKIE_FILE, SCROLL_STATE_FILE
    OUTPUT_DIR = f"{username}_data"
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    TWEETS_FILE = f"{OUTPUT_DIR}/scroll_tweets.json"
    COOKIE_FILE = f"{OUTPUT_DIR}/x_cookies.json"
    SCROLL_STATE_FILE = f"{OUTPUT_DIR}/scroll_state.json"

def log(msg): print(f"[{datetime.now().strftime('%m-%d %H:%M:%S')}] {msg}", flush=True)

def load_cookies():
    with open(COOKIE_FILE, encoding="utf-8") as f:
        raw = json.load(f)
    ssm = {"no_restriction": "None", "lax": "Lax", "strict": "Strict", None: "Lax"}
    out = []
    for c in raw:
        c2 = {k: v for k, v in c.items() if k in ("name","value","domain","path","httpOnly","secure")}
        c2["sameSite"] = ssm.get(c.get("sameSite"), "Lax")
        out.append(c2)
    return out

def extract(page):
    return page.evaluate("""
        () => {
            const r = [];
            document.querySelectorAll('article[data-testid="tweet"]').forEach(a => {
                try {
                    const l = a.querySelector('a[href*="/status/"]');
                    const id = l ? l.href.match(/\\/status\\/(\\d+)/)?.[1] : '';
                    if (!id) return;
                    r.push({
                        id, text: (a.querySelector('[data-testid="tweetText"]')?.innerText || ''),
                        timestamp: (a.querySelector('time')?.getAttribute('datetime') || ''),
                        username: (a.querySelector('a[href*="/"][role="link"]')?.href?.split('/').pop() || ''),
                        url: l?.href
                    });
                } catch(e) {}
            });
            return r;
        }
    """)

def find_oldest(seed_tweets):
    from datetime import timezone
    valid = []
    for t in seed_tweets:
        c = t.get('created_at','') or t.get('timestamp','')
        if c:
            try:
                s = str(c)
                if s[0].isalpha():
                    dt = datetime.strptime(s[:25], '%a %b %d %H:%M:%S %z %Y')
                    valid.append(dt)
                else:
                    dt = datetime.fromisoformat(s.replace('Z','+00:00'))
                    if dt.tzinfo is None: dt = dt.replace(tzinfo=timezone.utc)
                    valid.append(dt)
            except: pass
    if valid: valid.sort(); return valid[0].strftime('%Y-%m-%d')
    return '2025-07-01'

def search_and_scroll(page, existing_ids, all_tweets, since, until, username):
    """搜索指定日期范围并滚动收集，返回本块新增数"""
    url = f"https://x.com/search?q=from%3A{username}%20until%3A{until}%20since%3A{since}&src=typed_query"
    log(f"  搜索: {since} ~ {until}")
    try: page.goto(url, wait_until="domcontentloaded", timeout=30000)
    except: pass
    time.sleep(5)
    if "Sign in" in page.content():
        log("  Cookie 过期"); return -1
    if not page.query_selector_all('article[data-testid="tweet"]'):
        # 检查是否有错误信息
        body = page.inner_text("body")
        if "Something went wrong" in body or "try again" in body.lower():
            log("  搜索页错误，跳过"); return 0
        log("  无结果"); return 0

    block_new = 0; same_pos = 0; last_y = 0; retries = 0; no_new_streak = 0
    start_time = time.time()
    for rnd in range(200):
        # 总超时：一个块最多跑 3 分钟
        if time.time() - start_time > 180:
            log(f"  超时 ({since}~{until})，强制进入下一块"); break
        page.evaluate("window.scrollTo(0, document.body.scrollHeight)")
        time.sleep(SCROLL_DELAY)
        dom = extract(page)
        if not dom:
            page.evaluate("window.scrollTo(0, document.body.scrollHeight - 2000)")
            time.sleep(2)
            page.evaluate("window.scrollTo(0, document.body.scrollHeight)")
            time.sleep(3)
            dom = extract(page)
            if not dom:
                retries += 1; time.sleep(2)
                if retries >= 3: break
                continue
            retries = 0
        new_c = 0; seen = set()
        for t in dom:
            tid = t.get("id","")
            if not tid or tid in seen: continue
            seen.add(tid)
            if tid not in existing_ids:
                existing_ids.add(tid); all_tweets.append(t); new_c += 1; block_new += 1
        y_pos = page.evaluate("window.scrollY || document.documentElement.scrollTop")
        same_pos = 0 if y_pos != last_y else same_pos + 1
        last_y = y_pos
        if new_c:
            no_new_streak = 0
            log(f"    滚{rnd+1}: +{new_c} 条 (y={y_pos})")
        else:
            no_new_streak += 1
            if no_new_streak >= NEW_TWEET_IDLE_LIMIT:
                log(f"    滚{rnd+1}: 连续 {no_new_streak} 轮无新推文，提前退出")
                break
        if same_pos >= 25: break
    return block_new

def gen_chunks():
    """生成搜索块列表: [(since, until), ...]，从最早（账号创建）到今天"""
    CHUNK_DAYS = 14
    
    from datetime import timezone
    start = datetime(2025, 7, 1, tzinfo=timezone.utc)
    end = datetime.now(timezone.utc)
    
    chunks = []
    cur = start
    while cur < end:
        nxt = cur + timedelta(days=CHUNK_DAYS)
        if nxt > end: nxt = end
        chunks.append((cur.strftime('%Y-%m-%d'), nxt.strftime('%Y-%m-%d')))
        cur = nxt
    
    log(f"生成 {len(chunks)} 个搜索块, {chunks[0][0]} ~ {chunks[-1][1]}")
    return chunks

def scrape(username, existing_seed_file=None):
    init_paths(username)
    all_tweets = []; existing_ids = set()

    seed_tweets = []
    if existing_seed_file and os.path.exists(existing_seed_file):
        with open(existing_seed_file, encoding='utf-8') as f:
            raw = json.load(f)
        seed_tweets = raw.get('tweets', raw) if isinstance(raw, dict) else raw
        for t in seed_tweets:
            if 'id' in t: existing_ids.add(t['id'])

    oldest = find_oldest(seed_tweets)
    log(f"种子: {len(seed_tweets)} 条, 最早: {oldest}")

    chunks = gen_chunks()
    if not chunks:
        log("无需搜索: 已达最早日期"); return

    pre_count = len(existing_ids)
    cookies = load_cookies()

    with sync_playwright() as pw:
        br = pw.chromium.launch(headless=True)
        ctx = br.new_context(viewport={"width":1280,"height":900},
            user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36")
        ctx.add_cookies(cookies)
        page = ctx.new_page()

        total_new = 0
        for idx, (since, until) in enumerate(chunks):
            log(f"\n{'='*50}\n块 {idx+1}/{len(chunks)}: {since} ~ {until}")
            
            n = search_and_scroll(page, existing_ids, all_tweets, since, until, username)
            if n == -1: log("Cookie过期"); break
            if n > 0: total_new += n

            # 如果是月末边界，且本月新增很少，切到周模式重扫
            dt_since = datetime.fromisoformat(since)
            dt_until = datetime.fromisoformat(until)
            days_in_block = (dt_until - dt_since).days
            
            if n < WEEK_CHUNK_THRESHOLD and days_in_block >= 10:
                log(f"  本月新增仅 {n} 条 (<{WEEK_CHUNK_THRESHOLD}), 拆周重新搜索")
                # 拆成 7 天一块
                cur = dt_since
                while cur < dt_until:
                    wk_end = cur + timedelta(days=7)
                    if wk_end > dt_until: wk_end = dt_until
                    s = cur.strftime('%Y-%m-%d')
                    u = wk_end.strftime('%Y-%m-%d')
                    n2 = search_and_scroll(page, existing_ids, all_tweets, s, u, username)
                    if n2 == -1: break
                    if n2 > 0: total_new += n2
                    cur = wk_end

        br.close()

    new_total = len(existing_ids) - pre_count
    log(f"\n{'='*50}\n新增 {new_total} 条, 总计 {len(existing_ids)} 条")

    if existing_seed_file and os.path.exists(existing_seed_file):
        with open(existing_seed_file, encoding='utf-8') as f:
            raw = json.load(f)
        target = raw.get('tweets', raw) if isinstance(raw, dict) else raw
        d = {t['id']: t for t in target if 'id' in t}
        for t in all_tweets:
            d[t['id']] = t
        merged = list(d.values())
        if isinstance(raw, dict) and 'tweets' in raw:
            raw['tweets'] = merged
            raw['total_tweets'] = len(merged)
            raw['fetch_time'] = datetime.now().isoformat()
        with open(existing_seed_file, 'w', encoding='utf-8') as f:
            json.dump(raw, f, ensure_ascii=False, indent=2)
        log(f"已合并 -> {len(merged)} 条")

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("--username","-u", required=True)
    parser.add_argument("--seed", type=str, default=None)
    args = parser.parse_args()
    scrape(args.username, args.seed)
