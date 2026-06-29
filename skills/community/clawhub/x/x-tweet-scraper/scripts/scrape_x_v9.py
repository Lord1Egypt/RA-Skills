#!/usr/bin/env python3
"""
X.com 全量推文爬虫 v9
- v8-fastskip 的全面修复版
- 修复项见下方注释（C=Critical, I=Important, E=Edge, P=Improve）
- 详细介绍见：https://x.com（TODO: 外部文档链接）
"""
import json, time, os, sys, argparse
from datetime import datetime
from playwright.sync_api import sync_playwright

# ═── 配置 ─────────────────────────────────────
# C1: 改为变量，由 --username 参数传入
TARGET_USER     = None
OUTPUT_DIR      = None  # 由 TARGET_USER 动态生成
TWEET_IDS_FILE  = None
TWEETS_FILE     = None
COOKIE_FILE     = None
CURSOR_FILE     = None

USER_BY_QID   = "IGgvgiOx4QZndDHuD3x9TQ"
USER_TWEETS_QID = "JwvZ6uT2F7xU2uMozVeOQA"
BEARER          = "AAAAAAAAAAAAAAAAAAAAANRILgAAAAAAnNwIzUejRCOuH5E6I8xnZz4puTs=1Zv7ttfk8LF81IUq16cHjhLTvJu4FA33AGWWjCpTnA"

TWEETS_PER_PAGE = 20
SKIP_DELAY      = 1     # 快速跳过：1秒/页
PAGE_DELAY      = 900   # 收集模式：15分钟/页
START_DELAY     = 900   # 初始等待（可配 --start-delay 改为0）
RATE_WAIT       = 1800  # 限流等待：30分
MAX_STALLED     = 300
BATCH_PAGES     = 100
MAX_RATE_LIMITS = 60    # C4: 限流次数上限，防死循环
# ═───────────────────────────────────────────────


def init_paths(username):
    """根据用户名动态初始化文件路径"""
    global OUTPUT_DIR, TWEET_IDS_FILE, TWEETS_FILE, COOKIE_FILE, CURSOR_FILE
    dir_name = f"{username}_data"
    OUTPUT_DIR = dir_name
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    TWEET_IDS_FILE = f"{OUTPUT_DIR}/all_tweet_ids.json"
    TWEETS_FILE    = f"{OUTPUT_DIR}/all_tweets.json"
    COOKIE_FILE    = f"{OUTPUT_DIR}/x_cookies.json"
    CURSOR_FILE    = f"{OUTPUT_DIR}/last_cursor.json"


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
    return out, raw


def parse_dt(s):
    try:
        return datetime.strptime(s, "%a %b %d %H:%M:%S +0000 %Y")
    except Exception:
        return None


def load_seed_ids(seed_file):
    if not seed_file or not os.path.exists(seed_file):
        return set()
    try:
        with open(seed_file, 'r', encoding='utf-8') as f:
            raw = json.load(f)
        tweets = raw.get('tweets', raw) if isinstance(raw, dict) else raw
        ids = set(t['id'] for t in tweets if 'id' in t)
        log(f"从种子文件加载 {len(ids)} 个已知推文 ID")
        return ids
    except Exception as e:
        log(f"加载种子文件失败: {e}")
        return set()


def load_checkpoint_cursor():
    """I1: 从 CURSOR_FILE 加载保存的游标"""
    if os.path.exists(CURSOR_FILE):
        try:
            with open(CURSOR_FILE, encoding="utf-8") as f:
                cp = json.load(f)
            c = cp.get("cursor")
            p = cp.get("page", 0)
            if c:
                log(f"从 checkpoint 恢复游标 (page {p}): {c[:35]}...")
                return c, p
        except Exception as e:
            log(f"读取 checkpoint 游标失败: {e}")
    return None, 0


# ═── GraphQL 请求 ─────────────────
def graphql(page, ct0, qid, op_name, vars_dict):
    import json as json_mod
    vs = json_mod.dumps(vars_dict, ensure_ascii=False)
    raw = page.evaluate("""
        async (a) => {
            const h = {
                'authorization': 'Bearer ' + a.b,
                'x-csrf-token': a.c,
                'x-twitter-active-user': 'yes',
                'x-twitter-client-language': 'en',
            };
            const v = encodeURIComponent(a.v);
            const url = 'https://x.com/i/api/graphql/' + a.q + '/' + a.op + '?variables=' + v;
            try {
                const r = await fetch(url, {headers: h, credentials: 'include', mode: 'cors'});
                if (r.status === 429) return '__RL__';
                return await r.text();
            } catch(e) {
                return '__ERR__:' + (e.message || '');
            }
        }
    """, {"b": BEARER, "c": ct0, "q": qid, "op": op_name, "v": vs})

    if raw == "__RL__":
        return None, "RATE_LIMIT"
    if raw.startswith("__ERR__"):
        return None, raw
    try:
        data = json_mod.loads(raw)
        return data, None
    except Exception as e:
        if "rate" in raw.lower() or "limit" in raw.lower():
            return None, "RATE_LIMIT"
        return None, f"NOT_JSON:{raw[:300]}"


# ═── 提取推文 ─────────────────────────────
def extract(page, ct0, uid, cursor, known_set):
    import json as json_mod
    vars_dict = {
        "userId": uid, "count": TWEETS_PER_PAGE,
        "includePromotedContent": False,
        "withQuickPromoteEligibilityTweetFields": False,
        "withVoice": False, "withV2Timeline": True,
    }
    if cursor:
        vars_dict["cursor"] = cursor

    data, err = graphql(page, ct0, USER_TWEETS_QID, "UserTweets", vars_dict)
    if err:
        return [], None, err

    try:
        instrs = data["data"]["user"]["result"]["timeline"]["timeline"]["instructions"]
    except (KeyError, TypeError) as e:
        return [], None, f"NO_INSTRUCTIONS:{e}"

    entries = []
    next_cursor = None
    for instr in instrs:
        t = instr.get("type", "")
        if t == "TimelineAddEntries":
            entries.extend(instr.get("entries", []))
        elif t == "TimelinePinEntry":
            pe = instr.get("entry")
            if pe:
                entries.append(pe)

    new_tweets = []
    for e in entries:
        eid = e.get("entryId", "")
        if "cursor-bottom" in eid:
            next_cursor = e.get("content", {}).get("value", "")
        elif "tweet" in eid and "promotion" not in eid:
            social_ctx = e.get("content", {}).get("socialContext", {})
            if social_ctx.get("contextType", "") == "Pin":
                continue
            try:
                item = e.get("content", {}).get("itemContent", {})
                res = item.get("tweet_results", {}).get("result", {})
                if not res:
                    continue
                leg = res.get("legacy", {})
                tid = res.get("rest_id", "")
                if not tid:
                    continue
                new_tweets.append({
                    "id": tid,
                    "text": leg.get("full_text", ""),
                    "created_at": leg.get("created_at", ""),
                    "favorite_count": leg.get("favorite_count", 0),
                    "retweet_count": leg.get("retweet_count", 0),
                    "reply_count": leg.get("reply_count", 0),
                    "quote_count": leg.get("quote_count", 0),
                    "bookmark_count": leg.get("bookmark_count", 0),
                    "view_count": res.get("views", {}).get("count", 0),
                    "lang": leg.get("lang", ""),
                    "is_quote_status": leg.get("is_quote_status", False),
                })
            except Exception:
                pass

    return new_tweets, next_cursor, None


# ═── 保存进度 ─────────────────────
def save(all_ids, all_tweets, cursor, page_num):
    with open(TWEET_IDS_FILE, "w", encoding="utf-8") as f:
        json.dump(all_ids, f, ensure_ascii=False, indent=2)
    with open(TWEETS_FILE, "w", encoding="utf-8") as f:
        json.dump(all_tweets, f, ensure_ascii=False, indent=2)
    with open(CURSOR_FILE, "w", encoding="utf-8") as f:
        json.dump({"cursor": cursor, "page": page_num}, f, ensure_ascii=False, indent=2)


def merge_into_output(tweets_list, output_file):
    """P2: 将本次收集的推文合并到种子输出文件"""
    if not output_file or not os.path.exists(output_file):
        return
    try:
        with open(output_file, 'r', encoding='utf-8') as f:
            raw = json.load(f)
        target = raw.get('tweets', raw) if isinstance(raw, dict) else raw
        target_dict = {t['id']: t for t in target if 'id' in t}
        for t in tweets_list:
            target_dict[t['id']] = t
        merged = list(target_dict.values())
        if isinstance(raw, dict) and 'tweets' in raw:
            raw['tweets'] = merged
            raw['total_tweets'] = len(merged)
            raw['fetch_time'] = datetime.utcnow().isoformat() + 'Z'
            with open(output_file, 'w', encoding='utf-8') as f:
                json.dump(raw, f, ensure_ascii=False, indent=2)
        else:
            with open(output_file, 'w', encoding='utf-8') as f:
                json.dump(merged, f, ensure_ascii=False, indent=2)
        log(f"合并完成: {len(target_dict)} -> {len(merged)} 条 (写入 {output_file})")
    except Exception as e:
        log(f"合并失败: {e}")


# ═── 登录验证 ─────────────────────
def login(page):
    log("连接 X.com ...")
    try:
        page.goto("https://x.com/home", wait_until="domcontentloaded", timeout=120000)
    except Exception as e:
        log(f"页面加载超时（正常），继续... 错误: {e}")
    time.sleep(5)

    try:
        content = page.content()
    except Exception as e:
        log(f"无法读取页面内容: {e}")
        log("可能 Cookie 已过期或网络问题，请检查！")
        return False

    if "Sign in" in content:
        log("Cookie 已过期，请重新从浏览器导出！")
        return False
    log("登录验证通过")
    return True


def get_user_info(page, ct0):
    log("获取用户信息 ...")
    for retry in range(5):
        try:
            if retry > 0:
                log(f"第{retry}次重试，重新加载页面...")
                try:
                    page.goto("https://x.com/home", wait_until="networkidle", timeout=60000)
                    time.sleep(10)
                except Exception:
                    pass
            time.sleep(5)
            info = page.evaluate("""
                async (a) => {
                    const h = {'authorization':'Bearer '+a.b,'x-csrf-token':a.c};
                    const v = encodeURIComponent(JSON.stringify({screen_name:a.u}));
                    const r = await fetch('/i/api/graphql/'+a.q+'/UserByScreenName?variables='+v, {headers:h});
                    const d = await r.json();
                    const u = d?.data?.user?.result?.legacy;
                    return {id: d?.data?.user?.result?.rest_id || '',
                            name: u?.name || '',
                            followers: u?.followers_count || 0,
                            statuses: u?.statuses_count || 0};
                }
            """, {"b": BEARER, "c": ct0, "q": USER_BY_QID, "u": TARGET_USER})
            return info.get("id", ""), info.get("statuses", 0)
        except Exception as e:
            log(f"第{retry+1}次获取用户信息失败: {e}")
            if retry < 4:
                log("等待 30 秒后重试...")
                time.sleep(30)
    return "", 0


# ═── 主函数 ─────────────────────────────
def scrape(username, batch_mode=False, max_pages=None, max_new=None,
           start_delay=START_DELAY, seed_file=None, auto_merge=None):
    global TARGET_USER
    TARGET_USER = username
    init_paths(username)

    cookies, raw_cookies = load_cookies()
    ct0 = next((c["value"] for c in raw_cookies if c["name"] == "ct0"), "")

    # 加载 v8 checkpoint
    all_ids, all_tweets = [], []
    if os.path.exists(TWEET_IDS_FILE):
        with open(TWEET_IDS_FILE, encoding="utf-8") as f:
            all_ids = json.load(f)
        all_ids = list(dict.fromkeys(all_ids))
    if os.path.exists(TWEETS_FILE):
        with open(TWEETS_FILE, encoding="utf-8") as f:
            all_tweets = json.load(f)

    # 种子 ID
    seed_ids = load_seed_ids(seed_file)

    # 全量已知 ID
    known_set = seed_ids | set(all_ids)
    total_known = len(all_tweets) + len(seed_ids)

    local_dates = [parse_dt(t.get("created_at", "")) for t in all_tweets]
    local_dates = [d for d in local_dates if d is not None]
    local_oldest = min(local_dates) if local_dates else None
    if local_oldest:
        log(f"本地最早推文: {local_oldest.strftime('%Y-%m-%d')}")
    else:
        log("本地无推文记录，将从最新开始收集")

    with sync_playwright() as pw:
        br = pw.chromium.launch(headless=True)
        ctx = br.new_context(viewport={"width": 1280, "height": 900})
        ctx.add_cookies(cookies)
        page = ctx.new_page()

        if not login(page):
            br.close()
            sys.exit(1)

        # 可配置的初始等待
        if start_delay > 0:
            log(f"开始爬取前等待 {start_delay//60} 分钟，让速率限制重置...")
            time.sleep(start_delay)
            log("等待结束，开始爬取")

        uid, remote_total = get_user_info(page, ct0)
        if not uid:
            log("无法获取 user_id，退出")
            br.close()
            sys.exit(1)

        log(f"user_id: {uid} | 昵称/粉丝略")
        log(f"远程总数: {remote_total} | v8 checkpoint: {len(all_tweets)} | 种子跳过: {len(seed_ids)}")

        # ═══ 分页爬取 ═══
        # I1: 尝试从 checkpoint 游标恢复；如果无游标则从第1页开始
        checkpoint_cursor, start_page = load_checkpoint_cursor()
        cursor     = None if not seed_file else checkpoint_cursor
        # I1逻辑：有种子文件时，用快速跳过模式从 checkpoint cursor 开始
        #        无种子文件时，从第1页开始（cursor = None）
        #        如果 checkpoint 存在且有种子，从上次位置继续
        use_checkpoint = seed_file and checkpoint_cursor
        cursor = checkpoint_cursor if use_checkpoint else None

        page_num   = start_page if use_checkpoint else 0
        total_new  = 0
        stalled    = 0
        batch_cnt  = 0
        seek_mode  = True if seed_file else False
        rate_limit_cnt = 0
        actual_max = max_pages if max_pages else 99999

        log(f"\n开始爬取（每页 {TWEETS_PER_PAGE} 条）")
        log(f"策略: {'已知跳过+15分收集' if seek_mode else '持续15分/页'}")
        log(f"起始: page {page_num+1}{' (checkpoint)' if use_checkpoint else ''}")
        log(f"本地已有: {len(all_tweets)}/{remote_total or '?'}\n")

        while page_num < actual_max:
            page_num += 1
            batch_cnt += 1

            if batch_mode and batch_cnt > BATCH_PAGES:
                log(f"批次模式: 已达 {BATCH_PAGES} 页上限，保存进度后退出")
                break

            # 发请求
            tweets, next_cursor, err = None, None, None
            for extract_retry in range(3):
                try:
                    tweets, next_cursor, err = extract(page, ct0, uid, cursor, known_set)
                    break
                except Exception as e:
                    if "Execution context was destroyed" in str(e) and extract_retry < 2:
                        log(f"浏览器上下文销毁，第{extract_retry+1}次重试...")
                        try:
                            page.goto("https://x.com/home", wait_until="networkidle", timeout=60000)
                            time.sleep(10)
                        except Exception:
                            pass
                        continue
                    else:
                        raise

            # C4: 限流次数上限
            if err == "RATE_LIMIT":
                rate_limit_cnt += 1
                log(f"第{page_num}页 限流！(第{rate_limit_cnt}/{MAX_RATE_LIMITS}次) 等待 {RATE_WAIT//60} 分钟 ...")
                save(all_ids, all_tweets, cursor, page_num)
                if rate_limit_cnt >= MAX_RATE_LIMITS:
                    log("达到限流上限，退出")
                    break
                time.sleep(RATE_WAIT)
                continue

            if err:
                log(f"第{page_num}页 错误: {err[:150]}")
                time.sleep(10)
                continue

            if not next_cursor:
                log("\n已到达推文末尾（无 cursor）")
                break

            # ⭐ 快速跳过模式
            if seek_mode:
                all_known = all(t["id"] in known_set for t in tweets) if tweets else True
                if all_known:
                    cursor = next_cursor
                    log(f"[⚡跳过] 第{page_num}页: {len(tweets)}条均已知")
                    # P1: 跳过模式每20页存一次 checkpoint
                    if page_num % 20 == 0:
                        save(all_ids, all_tweets, cursor, page_num)
                        log(f"跳过模式 checkpoint 已保存 (page {page_num})")
                    time.sleep(SKIP_DELAY)
                    # E1: 跳过模式也重置 stalled
                    stalled = 0
                    continue
                else:
                    new_count = sum(1 for t in tweets if t["id"] not in known_set)
                    log(f"发现 {new_count} 条新推文！退出跳过模式，进入正常收集")
                    seek_mode = False

            # ⭐ 收集模式：合并新推文
            for t in tweets:
                if t["id"] not in known_set:
                    known_set.add(t["id"])
                    all_ids.append(t["id"])
                    all_tweets.append(t)
                    total_new += 1

            # 日期诊断
            date_info = ""
            if tweets:
                dts = [(parse_dt(t["created_at"]), t["created_at"]) for t in tweets]
                dts = [(d, s) for d, s in dts if d is not None]
                if dts:
                    dts.sort()
                    date_info = f" | 本页: {dts[0][1][:10]} ~ {dts[-1][1][:10]}"
                stalled = 0
            else:
                stalled += 1
                date_info = f" | 无新推文（连续 {stalled} 页）"

            log(f"[●收集] 第{page_num}页: +{sum(1 for t in tweets if t['id'] in known_set and [None])}条 | 累计 {len(all_tweets)}/{remote_total or '?'}{date_info}")
            log(f"  cursor={next_cursor[:35]}...")

            if page_num % 5 == 0:
                save(all_ids, all_tweets, next_cursor, page_num)

            # 终止条件
            # C2: 远程总数比较包含种子条数
            if remote_total and (len(all_tweets) + len(seed_ids)) >= remote_total:
                log(f"\n本地 {len(all_tweets) + len(seed_ids)} >= 远程 {remote_total}，全部收集完成！")
                break
            if stalled >= MAX_STALLED:
                log(f"\n连续 {MAX_STALLED} 页无新推文，停止")
                break
            if max_new and total_new >= max_new:
                log(f"\n本次新增已达 {max_new} 条，停止")
                break
            if rate_limit_cnt >= MAX_RATE_LIMITS:
                log("\n限流超限，退出")
                break

            cursor = next_cursor
            time.sleep(PAGE_DELAY)

        # 结束保存
        save(all_ids, all_tweets, cursor, page_num)
        br.close()

    # 最终报告
    log(f"\n爬取完成！")
    log(f"v8 checkpoint 推文: {len(all_tweets)} 条")
    log(f"本次新增: {total_new} 条")
    dts = [(parse_dt(t["created_at"]), t["created_at"]) for t in all_tweets]
    dts = [(d, s) for d, s in dts if d is not None]
    if dts:
        dts.sort()
        log(f"v8 时间范围: {dts[0][1][:16]} ~ {dts[-1][1][:16]}")

    # P2: 自动合并到种子输出文件
    if auto_merge:
        merge_into_output(all_tweets, auto_merge)


# ═── 入口 ──────────────────────────
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="X.com 全量推文爬虫 v9（修复版）")
    parser.add_argument("--username",  "-u", type=str, required=True, help="X.com 用户名")
    parser.add_argument("--batch",     action="store_true", help="批次模式（跑 BATCH_PAGES 页后退出）")
    parser.add_argument("--pages",     type=int, default=None,  help="本次最大页数")
    parser.add_argument("--max-new",   type=int, default=None,  help="本次最多新增多少条")
    parser.add_argument("--start-delay", type=int, default=None,
                        help="开始前等待秒数（0=不等，默认900=15分钟）")
    parser.add_argument("--seed",      type=str, default=None,
                        help="种子 JSON 文件路径（已知推文，用于快速跳过）")
    parser.add_argument("--auto-merge", type=str, default=None,
                        help="跑完后自动合并到指定 JSON 文件")
    parser.add_argument("--debug",     action="store_true", help="调试模式（暂无效果）")
    args = parser.parse_args()

    sd = args.start_delay if args.start_delay is not None else START_DELAY
    scrape(username=args.username, batch_mode=args.batch, max_pages=args.pages,
           max_new=args.max_new, start_delay=sd,
           seed_file=args.seed, auto_merge=args.auto_merge)
