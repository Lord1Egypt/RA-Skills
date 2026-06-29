"""
搜索驱动校准器 v1.0 (取代 data_provider.py 的 API 依赖)

数据流:
  agent 网页搜索最新比赛结果/伤病情报 → 结构化为 JSON → 本脚本校准数据文件

  1. Elo 更新: FIFA 风格 K 因子 + 净胜球放大 + 东道主主场加成
  2. 攻防数据更新: 指数衰减加权 (EWMA, 新结果权重 alpha=0.30),
     近期状态权重高于历史均值 → 预测更贴近临场
  3. 自动备份原数据 (.bak), 校准记录追加到 logs/calibration_log.md

输入 JSON 格式 (由 agent 搜索后填写, 绝不编造):
{
  "source": "搜索来源描述, 如 'FIFA官网 2026-06-12'",
  "results": [
    {"home": "墨西哥", "away": "南非", "home_goals": 2, "away_goals": 0,
     "neutral": false}
  ]
}
neutral=false 且 home 为东道主(美/加/墨) 时享受主场 Elo 加成。

用法:
  python3 calibrate.py results.json              # 用搜索到的结果校准 (主路径)
  python3 calibrate.py --from-api [起日] [止日]   # API backup: football-data.org 拉赛果
  python3 calibrate.py --groups groups.json      # 写入官方分组 {"A": ["队1",...], ...}
  python3 calibrate.py --demo                    # 演示 (不写盘)

API backup (网页搜索不可用时的兜底):
  - 数据源: football-data.org v4 (免费档 10次/分钟, 含世界杯)
  - 凭证: 环境变量 FOOTBALL_DATA_API_KEY (https://www.football-data.org/client/register)
  - 英文队名经 data/team_names.json 映射为中文; 无法映射的队名如实报告并跳过, 不猜

依赖: 纯标准库
"""

import json
import os
import shutil
import sys
import urllib.parse
import urllib.request
from datetime import date, timedelta
from typing import Dict, List

HERE = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(HERE, '..', 'data')
LOG_PATH = os.path.join(HERE, '..', 'logs', 'calibration_log.md')

# Elo 更新参数
ELO_K = 30           # K 因子 (大赛单场)
ELO_HOME_ADV = 65    # 东道主主场 Elo 加成 (仅用于期望计算)
HOST_TEAMS = ["美国", "加拿大", "墨西哥"]

# 攻防数据 EWMA 参数
STATS_ALPHA = 0.30   # 新结果权重 (0.30 ≈ 近 3 场主导)


# ----------------------------------------------------
# Elo 更新 (从 data_provider 移植)
# ----------------------------------------------------
def update_elo(elo: Dict[str, float], results: List[Dict]) -> Dict[str, float]:
    """FIFA 风格增量 Elo: K=30, 净胜球放大, 东道主真主场加成。返回新 dict。"""
    elo = dict(elo)
    for m in results:
        h, a = m["home"], m["away"]
        hg, ag = m["home_goals"], m["away_goals"]
        is_home = (not m.get("neutral", True)) and h in HOST_TEAMS
        ra = elo.get(h, 1500) + (ELO_HOME_ADV if is_home else 0)
        rb = elo.get(a, 1500)
        exp_h = 1 / (1 + 10 ** ((rb - ra) / 400))
        score_h = 1.0 if hg > ag else (0.5 if hg == ag else 0.0)
        gd = abs(hg - ag)
        mult = 1.0 if gd <= 1 else (1.5 if gd == 2 else (1.75 + (gd - 3) / 8))
        delta = ELO_K * mult * (score_h - exp_h)
        elo[h] = round(elo.get(h, 1500) + delta, 1)
        elo[a] = round(elo.get(a, 1500) - delta, 1)
    return elo


# ----------------------------------------------------
# 攻防数据 EWMA 更新 (v2.1 新增: 近期状态权重更高)
# ----------------------------------------------------
def update_stats(stats: Dict[str, Dict], results: List[Dict],
                 alpha: float = STATS_ALPHA) -> Dict[str, Dict]:
    """指数衰减更新 avg_goals / avg_conceded。返回新 dict。"""
    stats = {k: dict(v) for k, v in stats.items()}
    for m in results:
        for team, scored, conceded in (
                (m["home"], m["home_goals"], m["away_goals"]),
                (m["away"], m["away_goals"], m["home_goals"])):
            s = stats.setdefault(team, {"avg_goals": 1.35, "avg_conceded": 1.35})
            s["avg_goals"] = round((1 - alpha) * s["avg_goals"] + alpha * scored, 2)
            s["avg_conceded"] = round((1 - alpha) * s["avg_conceded"] + alpha * conceded, 2)
    return stats


# ----------------------------------------------------
# 文件操作
# ----------------------------------------------------
def _load(name):
    with open(os.path.join(DATA_DIR, name), encoding="utf-8") as f:
        return json.load(f)


def _save_with_backup(name, data):
    path = os.path.join(DATA_DIR, name)
    if os.path.exists(path):
        shutil.copy2(path, path + ".bak")
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)


def _append_log(source: str, results: List[Dict], elo_old: Dict, elo_new: Dict):
    os.makedirs(os.path.dirname(LOG_PATH), exist_ok=True)
    if not os.path.exists(LOG_PATH):
        with open(LOG_PATH, "w", encoding="utf-8") as f:
            f.write("# 校准日志\n\n搜索驱动的 Elo/攻防数据校准记录。\n\n")
    movers = sorted(
        ((t, elo_new[t] - elo_old.get(t, 1500)) for t in
         {x for m in results for x in (m["home"], m["away"])}),
        key=lambda x: abs(x[1]), reverse=True)
    with open(LOG_PATH, "a", encoding="utf-8") as f:
        f.write(f"## {date.today().isoformat()} | 来源: {source}\n\n")
        for m in results:
            f.write(f"- {m['home']} {m['home_goals']}-{m['away_goals']} {m['away']}\n")
        f.write("\nElo 变动: " + ", ".join(
            f"{t} {'+' if d >= 0 else ''}{round(d,1)}" for t, d in movers) + "\n\n")


# ----------------------------------------------------
# 主流程
# ----------------------------------------------------
def calibrate(results_path: str, dry_run: bool = False) -> Dict:
    with open(results_path, encoding="utf-8") as f:
        payload = json.load(f)
    results = payload["results"]
    source = payload.get("source", "未注明来源")
    if not results:
        raise ValueError("results 为空 — 没有可校准的比赛结果")
    for m in results:
        for k in ("home", "away", "home_goals", "away_goals"):
            if k not in m:
                raise ValueError(f"结果缺少字段 {k}: {m}")

    elo_old = _load("elo_ratings.json")
    stats_old = _load("team_stats.json")
    elo_new = update_elo(elo_old, results)
    stats_new = update_stats(stats_old, results)

    if not dry_run:
        _save_with_backup("elo_ratings.json", elo_new)
        _save_with_backup("team_stats.json", stats_new)
        _append_log(source, results, elo_old, elo_new)

    changed = {x for m in results for x in (m["home"], m["away"])}
    return {
        "matches": len(results), "source": source, "dry_run": dry_run,
        "elo_changes": {t: (elo_old.get(t, 1500), elo_new[t]) for t in changed},
        "stats_changes": {t: stats_new[t] for t in changed},
    }


# ----------------------------------------------------
# API backup: football-data.org (搜索不可用时的兜底)
# ----------------------------------------------------
FOOTBALL_DATA_URL = "https://api.football-data.org/v4/competitions/WC/matches"
HOST_VENUES_HOME = True  # API 的 homeTeam 即东道主主场判断依据


def _map_name(name: str, name_map: Dict[str, str]) -> str:
    """英文队名 → 中文; 映射失败返回 None (不猜)"""
    key = name.lower().replace(" national team", "").strip()
    return name_map.get(key)


def fetch_results_from_api(date_from: str = None, date_to: str = None) -> Dict:
    """
    从 football-data.org 拉取已结束的世界杯赛果, 返回与搜索路径相同的 payload 格式。
    仅作 backup: 需要 FOOTBALL_DATA_API_KEY。
    """
    api_key = os.getenv("FOOTBALL_DATA_API_KEY")
    if not api_key:
        raise ValueError(
            "缺少 FOOTBALL_DATA_API_KEY (API backup 凭证)。"
            "免费注册: https://www.football-data.org/client/register 。"
            "或改用主路径: 网页搜索赛果 → calibrate.py results.json")
    if not date_to:
        date_to = date.today().isoformat()
    if not date_from:
        date_from = (date.today() - timedelta(days=3)).isoformat()
    params = urllib.parse.urlencode({"dateFrom": date_from, "dateTo": date_to})
    req = urllib.request.Request(
        f"{FOOTBALL_DATA_URL}?{params}",
        headers={"X-Auth-Token": api_key, "User-Agent": "wc2026-skill/2.1"})
    try:
        with urllib.request.urlopen(req, timeout=30) as resp:
            data = json.loads(resp.read().decode("utf-8"))
    except urllib.error.HTTPError as e:
        raise Exception(f"football-data.org 请求失败 {e.code}: {e.read()[:200]}")

    with open(os.path.join(DATA_DIR, "team_names.json"), encoding="utf-8") as f:
        name_map = {k: v for k, v in json.load(f).items() if not k.startswith("_")}

    results, skipped = [], []
    for m in data.get("matches", []):
        if m.get("status") != "FINISHED":
            continue
        ft = m.get("score", {}).get("fullTime", {})
        if ft.get("home") is None or ft.get("away") is None:
            continue
        h_en = m.get("homeTeam", {}).get("name", "")
        a_en = m.get("awayTeam", {}).get("name", "")
        h, a = _map_name(h_en, name_map), _map_name(a_en, name_map)
        if not h or not a:
            skipped.append(f"{h_en} vs {a_en}")
            continue
        results.append({
            "home": h, "away": a,
            "home_goals": ft["home"], "away_goals": ft["away"],
            # API 的 homeTeam 为名义主队; 仅东道主算真主场 (update_elo 内部判断)
            "neutral": h not in HOST_TEAMS,
        })
    if skipped:
        print(f"[警告] {len(skipped)} 场队名无法映射, 已跳过 (不猜): {skipped}")
        print("       如需收录, 在 data/team_names.json 中补充别名后重跑")
    return {
        "source": f"API backup: football-data.org WC matches {date_from}~{date_to}",
        "results": results,
    }


def set_groups(groups_path: str) -> Dict:
    """把搜索到的官方分组写入 world_cup_schedule.json (要求注明来源)"""
    with open(groups_path, encoding="utf-8") as f:
        payload = json.load(f)
    groups = payload.get("groups", payload)
    source = payload.get("source")
    if not source:
        raise ValueError("必须注明 source (分组是事实型数据, 需可溯源, 不可编造)")
    sched = _load("world_cup_schedule.json")
    for g, teams in groups.items():
        if g == "source":
            continue
        sched["groups"][g] = {"teams": teams}
    sched["_populated"] = True
    sched["_source"] = source
    _save_with_backup("world_cup_schedule.json", sched)
    return {"groups_set": [g for g in groups if g != "source"], "source": source}


if __name__ == "__main__":
    args = sys.argv[1:]
    if not args or args[0] == "--demo":
        # 演示模式: 假想数据, dry-run 不写盘
        demo = {"source": "演示数据(非真实结果)", "results": [
            {"home": "墨西哥", "away": "南非", "home_goals": 2, "away_goals": 0,
             "neutral": False}]}
        tmp = os.path.join(HERE, "_demo_results.json")
        with open(tmp, "w", encoding="utf-8") as f:
            json.dump(demo, f, ensure_ascii=False)
        try:
            r = calibrate(tmp, dry_run=True)
        finally:
            os.remove(tmp)
        print("=== 演示 (dry-run, 不写盘) ===")
        for t, (o, n) in r["elo_changes"].items():
            print(f"  {t}: Elo {o} → {n} | stats → {r['stats_changes'][t]}")
    elif args[0] == "--groups":
        r = set_groups(args[1])
        print(f"已写入分组 {r['groups_set']} (来源: {r['source']})")
    elif args[0] == "--from-api":
        date_from = args[1] if len(args) > 1 else None
        date_to = args[2] if len(args) > 2 else None
        try:
            payload = fetch_results_from_api(date_from, date_to)
        except Exception as e:
            print(f"[API backup 不可用, 降级] {e}")
            sys.exit(0)
        if not payload["results"]:
            print("API 未返回已结束的比赛, 无可校准内容")
            sys.exit(0)
        tmp = os.path.join(HERE, "_api_results.json")
        with open(tmp, "w", encoding="utf-8") as f:
            json.dump(payload, f, ensure_ascii=False)
        try:
            r = calibrate(tmp, dry_run="--dry-run" in args)
        finally:
            os.remove(tmp)
        print(f"API backup 校准完成: {r['matches']} 场 (来源: {r['source']})")
        for t, (o, n) in r["elo_changes"].items():
            print(f"  {t}: Elo {o} → {n}")
    else:
        dry = "--dry-run" in args
        r = calibrate(args[0], dry_run=dry)
        print(f"校准完成: {r['matches']} 场 (来源: {r['source']}"
              f"{', dry-run 未写盘' if dry else ''})")
        for t, (o, n) in r["elo_changes"].items():
            print(f"  {t}: Elo {o} → {n} | stats → {r['stats_changes'][t]}")
