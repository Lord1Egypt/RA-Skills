#!/usr/bin/env python3
"""
X.com 全量推文抓取 - 浏览器滚动模式
- 打开用户主页，模拟真人滚动加载推文
- 从 DOM 提取推文内容（不依赖 GraphQL API）
- X.com 对浏览器滚动限制极松，可拿到远超 900 条的推文
- 支持断点续滚（保存已展开的推文 ID）
"""
import json, time, os, sys, argparse, re
from datetime import datetime
from playwright.sync_api import sync_playwright

OUTPUT_DIR      = None
TWEETS_FILE     = None
COOKIE_FILE     = None
SCROLL_STATE_FILE = None

SCROLL_DELAY    = 3      # 收集模式：每次滚动后等待秒数
SKIP_DELAY      = 1      # 跳过模式：快速滚动间隔（秒）
SAVE_INTERVAL   = 100    # 每收集多少条保存一次
MAX_EMPTY       = 50     # 收集模式：连续多少页无新推文视为到达底部
MAX_TWEETS      = 5000   # 安全上限


def init_paths(username):
    global OUTPUT_DIR, TWEETS_FILE, COOKIE_FILE, SCROLL_STATE_FILE
    OUTPUT_DIR = f"{username}_data"
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    TWEETS_FILE       = f"{OUTPUT_DIR}/scroll_tweets.json"
    COOKIE_FILE       = f"{OUTPUT_DIR}/x_cookies.json"
    SCROLL_STATE_FILE = f"{OUTPUT_DIR}/scroll_state.json"


def log(msg):
    ts = datetime.now().strftime("%m-%d %H:%M:%S")
    print(f"[{ts}] {msg}", flush=True)


def load_cookies():
    with open(COOKIE_FILE, encoding="utf-8") as f:
        raw = json.load(f)
    ssm = {"no_restriction": "None", "lax": "Lax", "strict": "Strict", None: "Lax"}
    out = []
    for c in raw:
        c2 = {k: v for k, v in c.items()
               if k in ("name", "value", "domain", "path", "httpOnly", "secure")}
        c2["sameSite"] = ssm.get(c.get("sameSite"), "Lax")
        out.append(c2)
    return out


def load_state():
    if os.path.exists(SCROLL_STATE_FILE):
        try:
            with open(SCROLL_STATE_FILE, encoding="utf-8") as f:
                return json.load(f)
        except: pass
    return {"existing_ids": [], "tweets": [], "scroll_y": 0}


def save_state(existing_ids, tweets, scroll_y=0):
    with open(SCROLL_STATE_FILE, "w", encoding="utf-8") as f:
        json.dump({"existing_ids": list(existing_ids), "tweets": tweets, "scroll_y": scroll_y}, f, ensure_ascii=False, indent=2)
    with open(TWEETS_FILE, "w", encoding="utf-8") as f:
        json.dump(tweets, f, ensure_ascii=False, indent=2)


def extract_tweets_from_dom(page):
    """从 DOM 提取当前可见的推文"""
    return page.evaluate("""
        () => {
            const articles = document.querySelectorAll('article[data-testid="tweet"]');
            const results = [];
            for (const art of articles) {
                try {
                    const link = art.querySelector('a[href*="/status/"]');
                    const id = link ? link.href.match(/\\/status\\/(\\d+)/)?.[1] || '' : '';
                    if (!id) continue;

                    const textEl = art.querySelector('[data-testid="tweetText"]');
                    const text = textEl ? textEl.innerText : '';

                    const timeEl = art.querySelector('time');
                    const timestamp = timeEl ? timeEl.getAttribute('datetime') : '';

                    const userLink = art.querySelector('a[href*="/"][role="link"]');
                    const username = userLink ? userLink.href.split('/').pop() : '';

                    const stats = {};
                    const metricEls = art.querySelectorAll('[data-testid$="count"]');
                    for (const el of metricEls) {
                        const key = el.getAttribute('data-testid') || '';
                        stats[key] = el.innerText || '0';
                    }

                    results.push({
                        id, text, timestamp, username, stats,
                        url: link ? link.href : ''
                    });
                } catch(e) {}
            }
            return results;
        }
    """)


def scrape(username, existing_seed_file=None, start_delay=0):
    init_paths(username)

    # 加载已有数据
    state = load_state()
    if state.get("tweets"):
        all_tweets = state["tweets"]
        existing_ids = set(state["existing_ids"])
        saved_scroll_y = state.get("scroll_y", 0)
        log(f"从滚动 checkpoint 恢复: {len(all_tweets)} 条，滚动位置 y={saved_scroll_y}")
    else:
        all_tweets = []
        existing_ids = set()
        saved_scroll_y = 0
        log("无滚动 checkpoint，全新开始")

    # 加载种子文件
    seed_tweets = []
    if existing_seed_file and os.path.exists(existing_seed_file):
        try:
            with open(existing_seed_file, encoding='utf-8') as f:
                raw = json.load(f)
            seed_tweets = raw.get('tweets', raw) if isinstance(raw, dict) else raw
            for t in seed_tweets:
                if 'id' in t:
                    existing_ids.add(t['id'])
            log(f"从种子文件加载 {len(seed_tweets)} 个已知 ID")
        except Exception as e:
            log(f"种子文件加载失败: {e}")

    # 自动推算缺口范围
    oldest_date = None
    for t in seed_tweets:
        c = t.get('created_at', '')
        if c and len(c) >= 10:
            try:
                from datetime import datetime as dt
                d = dt.strptime(c[:10], '%Y-%m-%d') if 'T' in c else dt.strptime(c[:10], '%a %b %d') if c[0].isalpha() else None
            except: pass
    # 用 ID 排序找最早
    valid_dates = []
    for t in seed_tweets:
        c = t.get('created_at', '')
        if c:
            valid_dates.append((t.get('id', '0'), c))
    valid_dates.sort(key=lambda x: int(x[0]) if x[0].isdigit() else 0)
    if valid_dates:
        raw = valid_dates[0][1]
        try:
            if raw[0].isalpha():
                from datetime import datetime as dt
                oldest_date = dt.strptime(raw, '%a %b %d %H:%M:%S %z %Y').strftime('%Y-%m-%d')
            else:
                oldest_date = raw[:10]
        except:
            oldest_date = '2025-12-26'
    else:
        oldest_date = '2025-12-26'

    log(f"种子最早日期: {oldest_date}")

    # 生成月份块：从 2025-07 到 oldest_date 所在月
    months = []
    for y in range(2025, 2027):
        for m in range(1, 13):
            ym = f"{y}-{m:02d}"
            if ym >= '2025-07' and ym <= oldest_date[:7]:
                months.append(ym)
    log(f"自动生成 {len(months)} 个搜索块: {months[0]} ~ {months[-1]}")

    cookies = load_cookies()
    pre_count = len(existing_ids)

    for idx, month in enumerate(months):
        # 计算本月起止
        ym_end = int(month[5:7]) + 1
        y_end = int(month[:4])
        if ym_end > 12:
            ym_end = 1
            y_end += 1
        since = f"{month}-01"
        until = f"{y_end}-{ym_end:02d}-01"

        # 如果本月在 oldest_date 之后（已有数据），跳过
        if month > oldest_date[:7]:
            log(f"跳过 {month}（已在已知范围内）")
            continue

        search_url = f"https://x.com/search?q=from%3A{username}%20until%3A{until}%20since%3A{since}&src=typed_query"
        log(f"\n{'='*50}")
        log(f"搜索块 {idx+1}/{len(months)}: {since} ~ {until}")
        log(f"URL: {search_url}")

        with sync_playwright() as pw:
            br = pw.chromium.launch(headless=True)
            ctx = br.new_context(viewport={"width": 1280, "height": 900},
                user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36")
            ctx.add_cookies(cookies)
            page = ctx.new_page()

            log("打开搜索页...")
            try:
                page.goto(search_url, wait_until="domcontentloaded", timeout=60000)
            except: pass
            time.sleep(5)

            if "Sign in" in page.content():
                log("Cookie 过期")
                br.close()
                sys.exit(1)

            # 检查是否有返回
            articles = page.query_selector_all('article[data-testid="tweet"]')
            if len(articles) == 0:
                log("本月无结果，跳过")
                br.close()
                continue

            log(f"首屏 {len(articles)} 条推文")

            # 开始滚动收集
            same_pos = 0
            last_y = 0
            got_any = False

            for scroll_round in range(150):
                page.evaluate("window.scrollTo(0, document.body.scrollHeight)")
                time.sleep(3)

                dom = extract_tweets_from_dom(page)
                if not dom:
                    # 回拉再试
                    page.evaluate("window.scrollTo(0, document.body.scrollHeight - 2000)")
                    time.sleep(2)
                    page.evaluate("window.scrollTo(0, document.body.scrollHeight)")
                    time.sleep(3)
                    dom = extract_tweets_from_dom(page)

                new_count = 0
                seen = set()
                for t in dom if dom else []:
                    tid = t.get("id", "")
                    if not tid or tid in seen:
                        continue
                    seen.add(tid)
                    if tid not in existing_ids:
                        existing_ids.add(tid)
                        all_tweets.append(t)
                        new_count += 1
                        got_any = True

                y = page.evaluate("window.scrollY || document.documentElement.scrollTop")
                if y == last_y:
                    same_pos += 1
                else:
                    same_pos = 0
                last_y = y

                if new_count > 0:
                    log(f"  滚 {scroll_round+1}: +{new_count} 条 (y={y})")

                # 到底退出
                if same_pos >= 30 or (not dom and same_pos >= 5):
                    log(f"  到达本月底部 (y={y})")
                    break

            br.close()

        if got_any:
            log(f"  {month}: 已收集")

    # 最终保存
    log(f"\n合计: 新增 {len(existing_ids) - pre_count} 条，总计 {len(existing_ids)} 条")

    with sync_playwright() as pw:
        br = pw.chromium.launch(headless=True)
        ctx = br.new_context(
            viewport={"width": 1280, "height": 900},
            user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36"
        )
        ctx.add_cookies(cookies)
        page = ctx.new_page()

        log(f"打开 {profile_url} ...")
        try:
            page.goto(profile_url, wait_until="domcontentloaded", timeout=60000)
        except Exception as e:
            log(f"页面加载超时（正常）: {e}")
        time.sleep(5)

        # 检查登录
        content = page.content()
        if "Sign in" in content:
            log("Cookie 已过期")
            br.close()
            sys.exit(1)
        log("登录验证通过")

        # 如果有保存的滚动位置，直接跳过去
        if saved_scroll_y > 0:
            log(f"跳过已收集区域: 滚动到 y={saved_scroll_y} ...")
            page.evaluate(f"window.scrollTo(0, {saved_scroll_y})")
            time.sleep(3)
            # 再往下多滚一点确保过了边界
            page.evaluate(f"window.scrollTo(0, {saved_scroll_y + 500})")
            time.sleep(3)
            log("跳转完成，开始继续向下滚动")

        if start_delay > 0:
            log(f"等待 {start_delay//60} 分钟冷却...")
            time.sleep(start_delay)

        # 计算已有推文数
        pre_count = len(existing_ids)
        seek_mode = len(existing_ids) > 0  # 有已知数据则进入快速跳过模式
        BIG_JUMP = 50000  # 大跳滚动步长（像素）

        log(f"\n开始滚动抓取...")
        log(f"已有: {pre_count} 条 | 新文件: {len(all_tweets)} 条")
        if seek_mode:
            log(f"模式: ⚡大跳跳过（{BIG_JUMP}px/步）→ 发现未知推文后切换 3秒/滚")
        log(f"每 {SAVE_INTERVAL} 条保存一次 | 最多抓 {MAX_TWEETS} 条\n")

        empty_rounds = 0
        last_count = 0
        consecutive_empty = 0
        big_jump_count = 0

        while len(all_tweets) < MAX_TWEETS:
            if seek_mode:
                # ⭐ 跳过模式：大跳滚动
                big_jump_count += 1
                scroll_target = big_jump_count * BIG_JUMP
                page.evaluate(f"window.scrollTo(0, {scroll_target})")
                time.sleep(3)  # 等推文加载

                dom_tweets = extract_tweets_from_dom(page)
                if not dom_tweets:
                    # 大跳后空白？往上翻一点触发加载，再跳回去
                    log(f"大跳 {big_jump_count} 无内容，回拉触发加载...")
                    page.evaluate(f"window.scrollTo(0, {scroll_target - 2000})")
                    time.sleep(2)
                    page.evaluate(f"window.scrollTo(0, {scroll_target})")
                    time.sleep(3)
                    dom_tweets = extract_tweets_from_dom(page)
                    if not dom_tweets:
                        # 还没内容，可能是到底了，切收集模式试试
                        log("回拉仍然无内容，切换到收集模式")
                        seek_mode = False
                        continue

                consecutive_empty = 0
                # 检查本页推文：有不在 known 里的吗？
                found_unknown = False
                for t in dom_tweets:
                    tid = t.get("id", "")
                    if tid and tid not in existing_ids:
                        found_unknown = True
                        break

                if found_unknown:
                    log(f"大跳 {big_jump_count} 发现未知推文! 切换到收集模式")
                    seek_mode = False
                else:
                    log(f"⚡大跳 {big_jump_count} / scrollY={scroll_target} | {len(dom_tweets)}条均已知")
                    if big_jump_count >= 20:
                        log("大跳达到 20 次上限，切换到收集模式")
                        seek_mode = False
                    continue

            # ⭐ 收集模式：正常滚动
            page.evaluate("window.scrollTo(0, document.body.scrollHeight)")
            time.sleep(SCROLL_DELAY)

            dom_tweets = extract_tweets_from_dom(page)
            if not dom_tweets:
                time.sleep(SCROLL_DELAY * 2)
                dom_tweets = extract_tweets_from_dom(page)
                if not dom_tweets:
                    consecutive_empty += 1
                    log(f"无推文（连续 {consecutive_empty}/{MAX_EMPTY} 轮）")
                    if consecutive_empty >= MAX_EMPTY:
                        log("到达底部，停止")
                        break
                    continue
            consecutive_empty = 0

            # 去重合并
            new_on_page = 0
            seen_on_page = set()
            for t in dom_tweets:
                tid = t.get("id", "")
                if not tid or tid in seen_on_page:
                    continue
                seen_on_page.add(tid)
                if tid not in existing_ids:
                    existing_ids.add(tid)
                    all_tweets.append(t)
                    new_on_page += 1

            if new_on_page > 0:
                log(f"本轮 +{new_on_page} 条 | 累计 {len(all_tweets)} 条 | 全局 {len(existing_ids)}")
                empty_rounds = 0
            elif empty_rounds == 0:
                # 第一次无新增：回拉再试（触发空白内容加载）
                log("无新增，回拉触发加载...")
                page.evaluate("window.scrollTo(0, document.body.scrollHeight - 3000)")
                time.sleep(2)
                page.evaluate("window.scrollTo(0, document.body.scrollHeight)")
                time.sleep(SCROLL_DELAY)
                # 重新提取
                dom_tweets2 = extract_tweets_from_dom(page)
                for t in dom_tweets2 if dom_tweets2 else []:
                    tid = t.get("id", "")
                    if tid and tid not in existing_ids:
                        existing_ids.add(tid)
                        all_tweets.append(t)
                        new_on_page += 1
                if new_on_page > 0:
                    log(f"回拉后恢复: +{new_on_page} 条")
                    continue
                empty_rounds += 1
            else:
                empty_rounds += 1
                log(f"无新增（连续 {empty_rounds}/{MAX_EMPTY} 轮）")
                if empty_rounds >= MAX_EMPTY:
                    log("到达底部，停止")
                    break

            # 定期保存
            if len(all_tweets) % SAVE_INTERVAL < 50 and len(all_tweets) > 0:
                sy = page.evaluate("window.scrollY || window.pageYOffset || document.documentElement.scrollTop")
                save_state(existing_ids, all_tweets, sy)
                log(f"自动保存: {len(all_tweets)} 条 (y={sy})")

        # 最终保存
        # 先获取当前滚动位置再保存
        scroll_y = page.evaluate("window.scrollY || window.pageYOffset || document.documentElement.scrollTop")
        save_state(existing_ids, all_tweets, scroll_y)
        br.close()

    # 报告
    new_total = len(existing_ids) - pre_count
    log(f"\n滚动抓取完成!")
    log(f"新抓取: {len(all_tweets)} 条")
    log(f"全局去重后新增: {new_total} 条")

    # 可选：合并到种子文件
    if existing_seed_file and os.path.exists(existing_seed_file):
        try:
            with open(existing_seed_file, encoding='utf-8') as f:
                raw = json.load(f)
            target = raw.get('tweets', raw) if isinstance(raw, dict) else raw
            target_dict = {t['id']: t for t in target if 'id' in t}
            for t in all_tweets:
                target_dict[t['id']] = t
            merged = list(target_dict.values())
            if isinstance(raw, dict) and 'tweets' in raw:
                raw['tweets'] = merged
                raw['total_tweets'] = len(merged)
                raw['fetch_time'] = datetime.now().isoformat()
                with open(existing_seed_file, 'w', encoding='utf-8') as f:
                    json.dump(raw, f, ensure_ascii=False, indent=2)
            log(f"已合并到 {existing_seed_file}: {len(merged)} 条")
            # 合并成功后清理 checkpoint，避免下次重复扫描
            for f in [SCROLL_STATE_FILE, TWEETS_FILE]:
                if os.path.exists(f):
                    os.remove(f)
                    log(f"已清理 checkpoint: {f}")
        except Exception as e:
            log(f"合并失败: {e}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="X.com 推文滚动抓取（浏览器滚动模式）")
    parser.add_argument("--username",  "-u", required=True)
    parser.add_argument("--seed",      type=str, default=None,
                        help="种子文件（已有 data.json，用于去重）")
    parser.add_argument("--start-delay", type=int, default=0, help="开始前等待秒数")
    args = parser.parse_args()
    scrape(args.username, args.seed, args.start_delay)
