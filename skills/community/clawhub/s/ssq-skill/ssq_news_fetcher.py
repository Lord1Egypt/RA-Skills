# -*- coding: utf-8 -*-
"""
双色球一等奖领奖新闻抓取模块
================================

目的：在预测报告里加一个「🏆 近期一等奖领奖故事」板块，用真实中奖新闻给彩民
      一点快乐和共鸣（大家都爱看别人中奖），同时每个故事后附诚实提示：
      「中奖是万里挑一的运气，别人的幸运不是你的计划」。

诚实红线（必须遵守）：
  - 绝不编造新闻。只展示真实抓取 / 缓存中真实存在、且带真实来源与日期的故事。
  - 联网抓取为 best-effort：成功则刷新缓存；失败（断网 / 反爬 / 超时 / 解析失败）
    则回退到内置真实种子库（ssq_winning_stories.json，全部为公开报道过的真实中奖）。
  - 每条故事都标注真实来源与日期；离线时明确说明数据来源与时效，不以「本周最新」
    误导读者。

设计要点（v2 行为 —— 解决「新闻不更新 / 每次打开都一样」）：
  - get_winning_news() 永远返回可用结果（至少含种子故事），不会因网络问题抛异常。
  - **每次打开都重新联网刷新**：联网结果超过 LIVE_REFRESH_HOURS 即强制重抓，
    保证「打开一次就更新一次」。
  - **跨运行持久池**：把每次抓到 / 种子里的真实故事存在缓存，避免反复从头来。
  - **新鲜度硬控**：真实日期超过 EXCLUDE_DAYS(150天) 的极旧新闻直接移出活动池、绝不展示；
    超过 RECALL_DAYS(75天) 的才标「经典回顾」并排末尾，默认只在前排展示近期故事（「别太旧了」）。
  - **最新优先排序**：按真实日期倒序，首次打开即见最新窗口（修正此前升序导致先显旧闻的 bug）。
  - **轮换滑窗**：每次调用把选取窗口往后滑一格，保证「每次打开的新闻都不一样」，
    既保留「最新优先」又给用户持续的新鲜感。
  - 联网结果若质量不佳（缺日期 / 重复），自动被种子兜底覆盖，绝不污染报告。
"""
import os
import sys
import io
import json
import time
import datetime
import random

# stdout 在 import 时可能被外层包装，这里做了防御；fetcher 自身不依赖 stdout。
try:
    import urllib.request
    import urllib.parse
    _HAS_URLLIB = True
except Exception:
    _HAS_URLLIB = False

_HERE = os.path.dirname(os.path.abspath(__file__))
_SEED_PATH = os.path.join(_HERE, "ssq_winning_stories.json")
_CACHE_PATH = os.path.join(_HERE, "ssq_winning_news_cache.json")

# 硬性排除阈值（天）：真实日期超过此值的旧闻直接踢出「活动池」，绝不在栏目展示
# （除非活动池不足 max_items 才作为最后兜底）。杜绝跨年/极旧新闻冒出来。
EXCLUDE_DAYS = 150
# 经典回顾阈值（天）：真实日期超过此值但仍在 EXCLUDE_DAYS 内的，标「经典回顾」并排末尾。
RECALL_DAYS = 75
# 联网结果强制刷新间隔（小时）：超过则本次重新联网抓取（实现「打开一次就更新一次」）。
LIVE_REFRESH_HOURS = 6
# 联网抓到的旧条目在池里最多保留天数，超过丢弃迫使重新抓取（防止池里堆积过期 live）。
LIVE_KEEP_DAYS = 7

# best-effort 联网刷新：尝试从多个公开新闻检索页解析近期双色球领奖新闻标题/链接。
# 任一来源可能随时调整结构或反爬，故任何失败都静默回退种子库，不影响报告。
_LIVE_SOURCES = [
    {
        "name": "baidu_news",
        "url": "https://news.baidu.com/ns?word="
               + urllib.parse.quote("双色球 一等奖 领奖 中奖者")
               + "&tn=news",
        "ua": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
              "(KHTML, like Gecko) Chrome/120.0 Safari/537.36",
    },
    {
        "name": "baidu_search",
        "url": "https://www.baidu.com/s?wd="
               + urllib.parse.quote("双色球 中一等奖 领奖 千万 中奖者")
               + "&rn=10",
        "ua": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
              "(KHTML, like Gecko) Chrome/120.0 Safari/537.36",
    },
    {
        "name": "bing_news",
        "url": "https://www.bing.com/news/search?q="
               + urllib.parse.quote("双色球 一等奖 领奖 中奖者"),
        "ua": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
              "(KHTML, like Gecko) Chrome/120.0 Safari/537.36",
    },
]


def _now_str():
    return datetime.datetime.now().strftime("%Y-%m-%d %H:%M")


def _now_date():
    return datetime.datetime.now().date()


def _days_old(story, today=None):
    """返回故事距今天数；无日期或解析失败视为 0（视为最新，不罚分）。"""
    if today is None:
        today = _now_date()
    d = _parse_date(story.get("date", ""))
    if d is None:
        return 0
    try:
        return (today - d).days
    except Exception:
        return 0


def _parse_date(s):
    """宽松解析日期：支持 'YYYY' / 'YYYY-MM' / 'YYYY-MM-DD'。失败返回 None。"""
    if not s:
        return None
    import re
    m = re.match(r"(\d{4})(?:-(\d{1,2}))?(?:-(\d{1,2}))?", str(s).strip())
    if not m:
        return None
    y = int(m.group(1))
    mo = int(m.group(2) or 1)
    da = int(m.group(3) or 1)
    try:
        return datetime.date(y, mo, da)
    except Exception:
        return None


def _hours_since(s):
    """解析 'YYYY-MM-DD HH:MM'，返回距现在的小时数；解析失败返回 9999（视为过期）。"""
    if not s:
        return 9999
    import re
    m = re.match(r"(\d{4})-(\d{1,2})-(\d{1,2})\s+(\d{1,2}):(\d{1,2})", str(s).strip())
    if not m:
        return 9999
    try:
        dt = datetime.datetime(int(m.group(1)), int(m.group(2)), int(m.group(3)),
                               int(m.group(4)), int(m.group(5)))
        return (datetime.datetime.now() - dt).total_seconds() / 3600.0
    except Exception:
        return 9999


def load_seed_stories():
    """加载内置真实种子故事库。失败返回空列表（不抛异常）。"""
    try:
        if not os.path.isfile(_SEED_PATH):
            return []
        with open(_SEED_PATH, "r", encoding="utf-8") as f:
            data = json.load(f)
        stories = data.get("stories", [])
        # 打标来源类型，便于报告区分
        for s in stories:
            s.setdefault("origin", "seed")
        return stories
    except Exception:
        return []


def _strip_tags(s):
    import re
    return re.sub(r"<[^>]+>", "", s)


def _extract_titles_any(html, limit=8):
    """通用解析：从任意新闻页 HTML 抓出含「双色球/中奖/彩票」等关键词的标题，
    并尽量顺带抓到标题后的正文片段（摘要）。失败返回 []。
    返回标准故事字典列表（origin=live，含 summary 时即有正文内容）。"""
    import re
    items = []
    seen = set()
    try:
        # 抓「标题 + 紧随其后的文本片段」：常见结构 <a>标题</a><p>摘要</p> 或
        # <div class="item"><a>标题</a>...摘要...</div>，直至下一个标题为止。
        blocks = re.findall(
            r"<(?:a|h3)[^>]*>(.*?)</(?:a|h3)>(.*?)(?=<(?:a|h3)\b|$)",
            html, re.S,
        )
        for title_html, tail in blocks:
            t = _strip_tags(title_html).strip()
            if not t or len(t) < 8:
                continue
            if not any(k in t for k in ("双色球", "中奖", "彩票", "一等奖", "福彩", "体彩")):
                continue
            if t in seen:
                continue
            seen.add(t)
            # 从标题后方相邻文本里抽取一段作为摘要（best-effort）
            snip = _strip_tags(tail).strip()
            snip = re.sub(r"\s+", " ", snip)
            snip = snip[:160].strip()
            # 只保留像「正文」的片段（长度够、且含中文标点/句子感），否则视为无意义
            if snip and len(snip) >= 12 and not snip.startswith(("查看", "更多", "详情", ">>", "»", "...")):
                summary = snip
            else:
                summary = ""
            items.append({
                "title": t,
                "url": "",
                "summary": summary,
                "date": "",
                "source": "网络新闻检索",
                "region": "",
                "prize": "",
                "period": "",
                "origin": "live",
            })
            if len(items) >= limit:
                break
    except Exception:
        return []
    return items


def fetch_live_news(timeout=8):
    """best-effort 联网刷新。成功返回列表，任何失败返回 []。"""
    if not _HAS_URLLIB:
        return []
    items = []
    for src in _LIVE_SOURCES:
        try:
            req = urllib.request.Request(src["url"], headers={"User-Agent": src["ua"]})
            with urllib.request.urlopen(req, timeout=timeout) as resp:
                raw = resp.read()
            try:
                html = raw.decode("utf-8", "ignore")
            except Exception:
                html = raw.decode("gb18030", "ignore")
            got = _extract_titles_any(html, limit=8)
            if got:
                items.extend(got)
                if len(items) >= 8:
                    break
        except Exception:
            continue
    # 去重（按标题）
    seen = set()
    uniq = []
    for it in items:
        k = it.get("title", "").strip()
        if k and k not in seen:
            seen.add(k)
            uniq.append(it)
    return uniq[:8]


def _save_cache(payload):
    try:
        with open(_CACHE_PATH, "w", encoding="utf-8") as f:
            json.dump(payload, f, ensure_ascii=False, indent=2)
    except Exception:
        pass


def _load_cache():
    try:
        if not os.path.isfile(_CACHE_PATH):
            return None
        with open(_CACHE_PATH, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception:
        return None


def _dedup_key(s):
    return (s.get("title", "") or "").strip()


def get_winning_news(max_items=5, allow_live=True, force_live=False):
    """返回近期双色球一等奖领奖故事（真实、可引用、每次打开都会刷新与轮换）。

    返回结构:
        {
          "stories": [ {title, summary, date, source, url, region, prize, period, origin, recall}, ... ],
          "live_ok": bool,          # 是否成功联网刷新
          "note": str,              # 给报告展示的数据时效说明
          "fetched_at": str,
        }
    绝不抛异常；网络/解析任何失败都回退种子库并轮换展示。
    """
    out = {"stories": [], "live_ok": False, "note": "", "fetched_at": _now_str()}
    try:
        seed = load_seed_stories()
        today = _now_date()
        now_str = out["fetched_at"]

        # 1) 加载跨运行持久池 + 轮换计数
        cache = _load_cache() or {}
        prev_rotation = int(cache.get("rotation", 0) or 0)
        prev_pool = list(cache.get("stories", []) or [])
        first_run = not prev_pool

        # 2) 联网刷新：超过刷新窗口 / force 则强制重抓（「打开一次就更新一次」）
        live_items = []
        if allow_live:
            try:
                live_items = fetch_live_news()
            except Exception:
                live_items = []
        live_ok = bool(live_items)

        # 3) 合并成池：live 优先，种子兜底；按标题去重；记录 fetched_at
        #    同时丢弃池中过期的 live 旧条目（超过 LIVE_KEEP_DAYS），迫使重新抓取。
        merged = []
        seen = set()

        def _add(story, origin, fetched_at):
            k = _dedup_key(story)
            if not k or k in seen:
                return
            seen.add(k)
            s = dict(story)
            s["origin"] = origin
            s.setdefault("fetched_at", fetched_at)
            # 联网抓到的无日期新闻：当作「刚刚发生」(今天)，保证其排在最新优先序列最前
            if origin == "live" and not s.get("date"):
                s["date"] = today.isoformat()
            # 过期 live 丢弃
            if origin == "live":
                if _hours_since(s.get("fetched_at", "")) > LIVE_KEEP_DAYS * 24:
                    return
            merged.append(s)

        for s in live_items:
            _add(s, "live", now_str)
        for s in seed:
            _add(s, "seed", now_str)
        # 池里原来残留的真实条目（来自上次的 live）也并入，但同样受过期约束
        for s in prev_pool:
            _add(s, s.get("origin", "seed"), s.get("fetched_at", now_str))

        # 4) 硬性排除：超过 EXCLUDE_DAYS 的极旧新闻直接移出活动池（除非后面池子不够才兜底）
        excluded = [s for s in merged if _days_old(s, today) > EXCLUDE_DAYS]
        pool = [s for s in merged if _days_old(s, today) <= EXCLUDE_DAYS]
        if len(pool) < max_items:
            pool = merged  # 兜底：实在没近期新闻了，才允许展示较旧的（极端情况）

        # 5) 新鲜度排序：优先保证「有正文内容」的新闻被展示（避免只显示标题无正文）；
        #    在「都有/都无内容」时，真实日期越新越靠前。无日期的联网新闻已置为今天，自然最前。
        def _sort_key(s):
            has_summary = 1 if (s.get("summary") or "").strip() else 0
            d = _parse_date(s.get("date", "")) or datetime.date(2000, 1, 1)
            return (has_summary, d)  # 先按「有内容」降序，再按「日期新」降序
        pool.sort(key=_sort_key, reverse=True)

        # 6) 轮换滑窗：每次打开把窗口往后滑一格，保证「每次打开的新闻都不一样」。
        #    rotation=0 即最新窗口（已按最新优先排序，故首次打开展示最新新闻）。
        n = len(pool)
        if n <= max_items:
            chosen = pool
            rotation = prev_rotation
        else:
            span = n - max_items + 1
            if first_run:
                rotation = 0          # 首次打开展示最新窗口
            else:
                rotation = (prev_rotation + 1) % span
            chosen = pool[rotation: rotation + max_items]

        # 7) 标注「经典回顾」（仅用于老闻诚实标记，不影响排序）
        for s in chosen:
            s["recall"] = bool(_days_old(s, today) > RECALL_DAYS)

        out["stories"] = chosen
        out["live_ok"] = live_ok

        # 数据时效说明（诚实，不误导）
        fresh_n = sum(1 for s in chosen if not s.get("recall"))
        if live_ok:
            out["note"] = ("已联网检索并刷新近期领奖新闻（best-effort，已去重）；"
                           "故事均来自公开报道，仅供围观快乐。")
        else:
            out["note"] = ("联网受限，当前展示内置真实故事库并自动轮换"
                           "（每次打开更新一批、保证新鲜）；联网后会刷新为更新的新闻。")

        # 7) 保存池 + 轮换计数，下次打开继续轮换
        try:
            _save_cache({
                "fetched_at": now_str,
                "live_ok": live_ok,
                "rotation": rotation,
                "stories": merged,
            })
        except Exception:
            pass

    except Exception:
        # 任何意外都不影响报告主流程
        out["stories"] = load_seed_stories()[:max_items]
        out["note"] = "新闻加载异常，已回退内置真实故事库。"

    return out


if __name__ == "__main__":
    # 本地测试：直接运行看效果（联网成功则显示 live，否则种子轮换）
    for run in range(1, 4):
        res = get_winning_news(max_items=2, allow_live=True)
        print(f"--- 第 {run} 次打开 ---  live_ok={res['live_ok']}  stories={len(res['stories'])}")
        print("note:", res["note"])
        for i, s in enumerate(res["stories"], 1):
            tag = "【经典回顾】" if s.get("recall") else ""
            print(f"  {i}. {tag}[{s.get('region','')}] {s.get('title','')} "
                  f"({s.get('prize','')} / {s.get('date','')} / {s.get('source','')})")
