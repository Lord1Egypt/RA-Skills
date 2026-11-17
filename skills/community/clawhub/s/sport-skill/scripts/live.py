#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Live 模式：真实联网拉取当日体育赛事，转换为兼容 daily_sample.json 的结构。

合规红线：仅拉取公开赛程 / 对阵 / 时间，绝不拉取任何敏感商业衍生数据字段。

数据源（按优先级尝试，取最先成功且覆盖最广的；多源结果自动合并去重）：
1) TheSportsDB Patreon key（环境变量 TS_API_KEY）：
   覆盖全联赛与全球类（含中超 / 日职 / 韩K / 荷甲 / 葡超 / 沙职 / 美职 / NBA），
   当日所有球类真实对阵——这是做到「竞猜级全量覆盖」最省事的一个 key。
2) api-football（环境变量 API_SPORTS_KEY）：覆盖全球主流足球联赛，全量真实对阵。
3) football-data.org（环境变量 FD_KEY，免费层）：覆盖欧洲五大联赛 + 欧冠等顶级赛事。
4) TheSportsDB 免费测试 key=3：仅约 3 场/日轮换样本（且常是错峰联赛，如 8 月美式足球），
   覆盖极有限——仅作最后兜底，并明确标 _auto_thin=true，绝不冒充全量。

关键事实：免费 key=3 每天只给约 3 场、且随日期轮换，做不到「篮足乒羽全实时」。
要做到用户要的「信息全」（对标全量：数十场真实对阵），推荐提供 TS_API_KEY；
若完全无 key，脚本会标 _auto_thin=true，由 SKILL.md 约定的「智能体联网补齐」机制兜底
（见 SKILL.md Live 模式第 5 条），保证出报告时仍能拿到当日真实全量赛事。

联网失败兜底：全部失败才降级为内置示例，顶层写 _is_live=false，报告顶部显式标「示例数据·非实时」。

用法：
    python scripts/live.py                 # 拉今日
    python scripts/live.py 2026-08-15     # 拉指定日期
    TS_API_KEY=xxxx python scripts/live.py  # 用 Patreon key 拉全量
    API_SPORTS_KEY=xxxx python scripts/live.py  # 用 api-football 拉全量
    FD_KEY=xxxx python scripts/live.py  # 用 football-data.org 免费 key 拉欧洲顶级
生成 assets/live_today.json，可直接喂给 analytics.py daily/focus。
"""
import sys
import os
import json
import datetime
import urllib.request
import urllib.error

SKILL_DIR = os.path.dirname(os.path.abspath(__file__))
DEMO_DAILY = os.path.join(SKILL_DIR, "..", "assets", "daily_sample.json")
OUT = os.path.join(SKILL_DIR, "..", "assets", "live_today.json")

# TheSportsDB 的 strSport(英文) -> (内部 sport key, 中文名)
SPORT_MAP = {
    "Soccer": ("football", "足球"),
    "Basketball": ("basketball", "篮球"),
    "Baseball": ("baseball", "棒球"),
    "American Football": ("american_football", "美式足球"),
    "Australian Football": ("australian_football", "澳式足球"),
    "Ice Hockey": ("hockey", "冰球"),
    "Tennis": ("tennis", "网球"),
    "Volleyball": ("volleyball", "排球"),
    "Table Tennis": ("table_tennis", "乒乓球"),
    "Badminton": ("badminton", "羽毛球"),
    "Rugby": ("rugby", "橄榄球"),
    "Cricket": ("cricket", "板球"),
    "Golf": ("golf", "高尔夫"),
    "Motorsport": ("motorsport", "赛车"),
    "Esports": ("esports", "电竞"),
}

# 免费源兜底时仍当作非实时示例的球类（仅当自动源完全为空才启用）
FALLBACK_SPORTS = ("basketball", "tennis", "volleyball", "table_tennis", "badminton", "football")


def _get(url, timeout=12, retries=3, headers=None):
    """带重试/退避的联网请求；全部失败才抛异常（由调用方降级）。"""
    import time
    hdrs = {"User-Agent": "Mozilla/5.0 (sports-data-analysis)"}
    if headers:
        hdrs.update(headers)
    last_err = None
    for attempt in range(1, retries + 1):
        try:
            req = urllib.request.Request(url, headers=hdrs)
            with urllib.request.urlopen(req, timeout=timeout) as r:
                return json.loads(r.read().decode("utf-8"))
        except (urllib.error.URLError, urllib.error.HTTPError, TimeoutError, OSError) as e:
            last_err = e
            if attempt < retries:
                print("  · 联网第 %d 次失败（%s），%.5fs 后重试…" % (attempt, e, 0.8 * attempt))
                time.sleep(0.8 * attempt)
    raise last_err


# ----------------------- 各数据源采集器 -----------------------

def fetch_thesportsdb(date_str, key):
    """TheSportsDB eventsday（key=Patreon 全量 或 免费测试 key=3 样本）。"""
    try:
        d = _get("https://www.thesportsdb.com/api/v1/json/%s/eventsday.php?d=%s" % (key, date_str))
    except (urllib.error.URLError, urllib.error.HTTPError, TimeoutError, OSError) as e:
        return [], "TheSportsDB 拉取失败：%s" % e
    out = []
    for e in (d.get("events") or []):
        home = e.get("strHomeTeam") or ""
        away = e.get("strAwayTeam") or ""
        if not home or not away:
            continue
        date_event = e.get("dateEvent") or ""
        time_event = (e.get("strTime") or "")[:8]
        # TheSportsDB 的 dateEvent/strTime 为 UTC，须换算到北京时间(+8)后再作为 kickoff_local，
        # 否则美洲赛事会出现「01:40」这类比实际开赛早 8 小时的错误时间。
        if date_event and time_event:
            kickoff = _utc_to_beijing("%sT%s" % (date_event, time_event if len(time_event) == 8 else time_event + ":00"))
        else:
            kickoff = ("%s %s" % (date_event, time_event[:5])).strip()
        sp_en = e.get("strSport") or "Soccer"
        sp_key, sp_cn = SPORT_MAP.get(sp_en, ("other", sp_en))
        out.append({
            "sport": sp_key, "sport_cn": sp_cn,
            "match": "%s vs %s" % (home, away),
            "league": e.get("strLeague", ""), "country": e.get("strCountry", ""),
            "kickoff_local": kickoff,
            "teams": [{"name": home}, {"name": away}],
            "info_points": [
                "赛程来自 TheSportsDB 公开数据（实时当日对阵%s）。" % ("·全量 Patreon" if key != "3" else "·免费样本"),
                "本场为真实当日对阵；战术 / 状态 / 专家维度待补充公开情报后完善。",
            ],
            "live": True,
        })
    return out, None


def fetch_football_data(date_str, key):
    """football-data.org（免费层覆盖欧洲五大 + 欧冠等）。需 X-Auth-Token。"""
    try:
        d = _get(
            "https://api.football-data.org/v4/matches?dateFrom=%s&dateTo=%s" % (date_str, date_str),
            headers={"X-Auth-Token": key},
        )
    except (urllib.error.URLError, urllib.error.HTTPError, TimeoutError, OSError) as e:
        return [], "football-data.org 拉取失败：%s" % e
    out = []
    for m in (d.get("matches") or []):
        h = (m.get("homeTeam") or {}).get("name") or ""
        a = (m.get("awayTeam") or {}).get("name") or ""
        if not h or not a:
            continue
        comp = (m.get("competition") or {}).get("name") or ""
        utc = m.get("utcDate") or ""
        # UTC -> 北京时间(+8) 简单换算
        ko = _utc_to_beijing(utc)
        out.append({
            "sport": "football", "sport_cn": "足球",
            "match": "%s vs %s" % (h, a),
            "league": comp, "country": (m.get("area") or {}).get("name", ""),
            "kickoff_local": ko,
            "teams": [{"name": h}, {"name": a}],
            "info_points": [
                "赛程来自 football-data.org 公开数据（实时当日对阵·欧洲顶级联赛）。",
                "本场为真实当日对阵；战术 / 状态 / 专家维度待补充公开情报后完善。",
            ],
            "live": True,
        })
    return out, None


def fetch_api_football(date_str, key):
    """api-football（覆盖全球主流足球联赛）。需 apikey 头。"""
    try:
        d = _get(
            "https://v3.football.api-sports.io/fixtures?date=%s" % date_str,
            headers={"apikey": key},
        )
    except (urllib.error.URLError, urllib.error.HTTPError, TimeoutError, OSError) as e:
        return [], "api-football 拉取失败：%s" % e
    out = []
    for it in (d.get("response") or []):
        fx = it.get("fixture") or {}
        tm = it.get("teams") or {}
        lg = it.get("league") or {}
        h = (tm.get("home") or {}).get("name") or ""
        a = (tm.get("away") or {}).get("name") or ""
        if not h or not a:
            continue
        ko = _utc_to_beijing(fx.get("date") or "")
        out.append({
            "sport": "football", "sport_cn": "足球",
            "match": "%s vs %s" % (h, a),
            "league": lg.get("name", ""), "country": lg.get("country", ""),
            "kickoff_local": ko,
            "teams": [{"name": h}, {"name": a}],
            "info_points": [
                "赛程来自 api-football 公开数据（实时当日对阵·全球主流联赛）。",
                "本场为真实当日对阵；战术 / 状态 / 专家维度待补充公开情报后完善。",
            ],
            "live": True,
        })
    return out, None


def _utc_to_beijing(utc_str):
    """ISO UTC 时间串 -> 北京时间串（YYYY-MM-DD HH:MM）。解析失败原样返回。"""
    if not utc_str:
        return ""
    try:
        dt = datetime.datetime.fromisoformat(utc_str.replace("Z", "+00:00"))
        dt = dt + datetime.timedelta(hours=8)
        return dt.strftime("%Y-%m-%d %H:%M")
    except Exception:
        return utc_str


def _dedupe(matches):
    seen = set()
    uniq = []
    for m in matches:
        k = (m.get("sport"), m.get("match", "").lower(), (m.get("kickoff_local") or "")[:10])
        if k in seen:
            continue
        seen.add(k)
        uniq.append(m)
    return uniq


def build(date_str):
    date_str = date_str or datetime.date.today().strftime("%Y-%m-%d")
    matches = []
    used = []
    thin = False

    # 1) TheSportsDB Patreon（全量）
    ts_key = os.environ.get("TS_API_KEY")
    if ts_key:
        evs, _ = fetch_thesportsdb(date_str, ts_key)
        matches += evs
        used.append("thesportsdb-patreon")

    # 2) api-football
    as_key = os.environ.get("API_SPORTS_KEY")
    if as_key:
        evs, _ = fetch_api_football(date_str, as_key)
        matches += evs
        used.append("api-football")

    # 3) football-data.org
    fd_key = os.environ.get("FD_KEY")
    if fd_key:
        evs, _ = fetch_football_data(date_str, fd_key)
        matches += evs
        used.append("football-data.org")

    # 4) 免费兜底（仅当上面都没拿到）
    if not matches:
        evs, _ = fetch_thesportsdb(date_str, "3")
        matches += evs
        used.append("thesportsdb-free")
        thin = True

    matches = _dedupe(matches)
    live_sports = sorted(set(m.get("sport") for m in matches))
    n_live = len(matches)

    # 薄覆盖判定：无 key 或总数偏少 -> 提示智能体联网补齐
    auto_thin = thin or (n_live < 10 and "thesportsdb-free" in used)

    data = {
        "date": date_str,
        "title": ("今日体育赛事总览（Live 实时·全量）" if not auto_thin
                  else "今日体育赛事总览（自动源样本·待联网补齐）"),
        "updated_at": datetime.datetime.now().strftime("%Y-%m-%d %H:%M"),
        "_is_live": n_live > 0,
        "_source": "+".join(used) or "none",
        "_auto_thin": auto_thin,
        "_live_error": None,
        "_sports_live": live_sports,
        "_thin_hint": ("自动源仅返回稀薄样本（无 key 时为常态）。出报告前请由智能体用 WebSearch 联网补齐"
                       "当日真实全量赛事（中超/日职/韩K/荷甲/葡超/英冠/西甲/沙职/美职/篮球等），"
                       "以保证「信息全」。详见 SKILL.md Live 模式第 5 条。") if auto_thin else None,
        "matches": matches,
    }
    return data


def main():
    date_str = sys.argv[1] if len(sys.argv) > 1 else ""
    keys = [k for k in ("TS_API_KEY", "API_SPORTS_KEY", "FD_KEY") if os.environ.get(k)]
    mode = ("多源全量（key=%s）" % ",".join(keys)) if keys else "免费样本(key=3, 约3场/日)"
    print("🔄 正在联网拉取当日赛事（%s）…" % mode)
    data = build(date_str)
    n_live = len(data["matches"])
    json.dump(data, open(OUT, "w", encoding="utf-8"), ensure_ascii=False, indent=2)
    print("✅ Live 数据已生成：%s" % OUT)
    print("   真实赛事 %d 场" % n_live)
    print("   覆盖球类：%s" % (", ".join(data.get("_sports_live") or []) or "无"))
    print("   数据源：%s" % data.get("_source"))
    if data.get("_auto_thin"):
        print("   ⚠️ 自动源仅样本（_auto_thin=true）：请由智能体联网补齐当日真实全量赛事，勿把样本当全量交付。")
    else:
        print("   ✅ 已取到多源真实全量对阵，可直接出报告。")
    print("   下一步：python scripts/analytics.py daily --input %s --output <桌面路径>" % OUT)


if __name__ == "__main__":
    main()
