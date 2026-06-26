"""
单场预测 — 5 数据源融合 + 64 卦推演 + 经验库写入

用法：
    python scripts/predict.py "Napoli vs Lazio"
    python scripts/predict.py "Chelsea vs Manchester United" --league premier-league
"""
import sys
import json
import time
import hashlib
import argparse
from pathlib import Path
from datetime import datetime, timezone

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

from core import hexagram, yao, kongming
from core.welcome import (NEON_CYAN, NEON_PINK, NEON_GREEN, NEON_YELLOW,
                          GOLD, WHITE, HOT_RED as RED, DIM, BOLD, RESET,
                          GRAY, NEON_PURPLE)
from adapters import api_football, the_odds, understat


DB = ROOT / "data" / "experience.jsonl"


def _load_dotenv():
    env = ROOT / ".env"
    if not env.exists():
        return
    for line in env.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        k, v = line.split("=", 1)
        import os
        os.environ.setdefault(k.strip(), v.strip())


_load_dotenv()


def parse_match(s: str):
    """'Napoli vs Lazio' → ('Napoli', 'Lazio')"""
    for sep in [" vs ", " VS ", " v ", " - "]:
        if sep in s:
            h, a = s.split(sep, 1)
            return h.strip(), a.strip()
    raise ValueError(f"无法解析比赛名: {s} (用 'Home vs Away' 格式)")


def predict_match(match_str: str, league: str = "serie-a", save: bool = True,
                  use_xg: bool = True, use_cross_validate: bool = True):
    """单场预测主流程"""
    home, away = parse_match(match_str)

    print(f"\n  {NEON_CYAN}┌{'─' * 56}┐{RESET}")
    print(f"  {NEON_CYAN}│{RESET} {BOLD}{NEON_PINK}诸葛亮推演 · {match_str}{RESET}")
    print(f"  {NEON_CYAN}└{'─' * 56}┘{RESET}\n")

    # === Step 1: API-Football ===
    print(f"  {DIM}>{RESET} {NEON_GREEN}[1/5]{RESET} 拉取 API-Football...")
    fid = api_football.find_fixture(home, away, league=league)
    if not fid:
        print(f"  {DIM}    未找到 fixture，启用 demo 模式 (配 API_FOOTBALL_KEY 才跑真数据){RESET}")
        return run_demo(match_str=match_str)
    print(f"  {DIM}    fixture id: {fid}{RESET}")

    odds = api_football.get_odds(fid)
    home_id, away_id = api_football.get_fixture_teams(fid)
    if not (home_id and away_id):
        print(f"  {DIM}    无球队 ID{RESET}")
        return

    home_form = api_football.get_recent_form(home_id, n=5) or {"form": [], "goals_for": 0, "goals_against": 0}
    away_form = api_football.get_recent_form(away_id, n=5) or {"form": [], "goals_for": 0, "goals_against": 0}
    h2h = api_football.get_h2h(home_id, away_id, n=5) or {"home_wins": 0, "draws": 0, "away_wins": 0}

    if odds:
        print(f"  {DIM}    赔率: 主{odds.get('home')} 平{odds.get('draw')} 客{odds.get('away')}{RESET}")
    print(f"  {DIM}    主队近5: {''.join(home_form['form'])} 进{home_form['goals_for']}/失{home_form['goals_against']}{RESET}")
    print(f"  {DIM}    客队近5: {''.join(away_form['form'])} 进{away_form['goals_for']}/失{away_form['goals_against']}{RESET}")

    # === Step 2: The Odds API（可选）===
    cross = None
    if use_cross_validate:
        print(f"  {DIM}>{RESET} {NEON_GREEN}[2/5]{RESET} 跨多家博彩验证...")
        cross = the_odds.cross_validate(home, away, league=league)
        if cross:
            print(f"  {DIM}    {cross['bookmaker_count']} 家博彩平均: 主{cross['home_avg']:.2f} 平{cross['draw_avg']:.2f} 客{cross['away_avg']:.2f}{RESET}")
            print(f"  {DIM}    去抽水真实概率: 主{cross['home_implied']*100:.0f}% 平{cross['draw_implied']*100:.0f}% 客{cross['away_implied']*100:.0f}%{RESET}")
        else:
            print(f"  {DIM}    跳过（key 未配或 API 不可达）{RESET}")
    else:
        print(f"  {DIM}>{RESET} {NEON_GREEN}[2/5]{RESET} 跳过跨验证")

    # === Step 3: Understat xG（可选）===
    home_xg_data = away_xg_data = None
    if use_xg:
        print(f"  {DIM}>{RESET} {NEON_GREEN}[3/5]{RESET} 拉取 xG 数据...")
        home_xg_data = understat.get_team_xg(home, league=league)
        away_xg_data = understat.get_team_xg(away, league=league)
        if home_xg_data and away_xg_data:
            print(f"  {DIM}    {home}: xG={home_xg_data['avg_xg']} xGA={home_xg_data['avg_xga']}{RESET}")
            print(f"  {DIM}    {away}: xG={away_xg_data['avg_xg']} xGA={away_xg_data['avg_xga']}{RESET}")
        else:
            print(f"  {DIM}    xG 数据不可用，将用进球数代替{RESET}")

    # === Step 4: 6 维爻位计算 ===
    print(f"  {DIM}>{RESET} {NEON_GREEN}[4/5]{RESET} 计算 6 维爻位...")
    yao_summary = yao.build_yao_summary(
        home_goals=[home_form["goals_for"]] * 5,  # 简化为均值
        away_goals=[away_form["goals_for"]] * 5,
        home_conceded=[home_form["goals_against"]] * 5,
        away_conceded=[away_form["goals_against"]] * 5,
        home_form=home_form["form"],
        away_form=away_form["form"],
        h2h=(h2h["home_wins"], h2h["draws"], h2h["away_wins"]),
        odds=(odds["home"] if odds else 99,
              odds["draw"] if odds else 99,
              odds["away"] if odds else 99),
        league=league,
        home_xg=home_xg_data["avg_xg"] if home_xg_data else None,
        away_xg=away_xg_data["avg_xg"] if away_xg_data else None,
        home_xga=home_xg_data["avg_xga"] if home_xg_data else None,
        away_xga=away_xg_data["avg_xga"] if away_xg_data else None,
    )

    for k, v in yao_summary.items():
        state = f"{NEON_PINK}阳{RESET}" if v > 0.5 else f"{NEON_CYAN}阴{RESET}"
        bar_filled = int(v * 20)
        bar = f"{GOLD}{'█' * bar_filled}{DIM}{'░' * (20 - bar_filled)}{RESET}"
        print(f"  {DIM}    {k:<5}{RESET} [{bar}] {v:.2f} [{state}]")

    # === Step 5: 64 卦推演 + 决策 + 晶体匹配 ===
    print(f"  {DIM}>{RESET} {NEON_GREEN}[5/5]{RESET} 推演卦象 + 检查经验晶体...")
    hex_result = hexagram.recognize(yao_summary)

    # 检查是否触发已有晶体
    from core.crystallizer import match_crystal
    crystal = match_crystal(hex_result)
    if crystal:
        s = crystal["stats"]
        rc = crystal.get("recurrence_count", 0)
        age_str = ""
        if crystal.get("first_seen"):
            try:
                from datetime import datetime as _dt, timezone as _tz
                fs = _dt.fromisoformat(crystal["first_seen"].replace("Z", "+00:00"))
                if fs.tzinfo is None:
                    fs = fs.replace(tzinfo=_tz.utc)
                days = (_dt.now(_tz.utc) - fs).days
                age_str = f" · 首见 {days}d 前" if days > 0 else " · 首见今日"
            except Exception:
                pass
        # 复用次数越多越可信，给颜色提示
        trust_tag = "验证中"
        if rc >= 5:
            trust_tag = "高复用 ⭐"
        elif rc >= 2:
            trust_tag = "复用中"
        print(f"  {NEON_PINK}    ✦ 触发晶体 [{crystal['crystal_id']}] "
              f"{crystal['outcome']}  历史命中率 {s['rate']*100:.0f}% "
              f"({s['hits']}/{s['matches']}){RESET}")
        print(f"  {NEON_PINK}      已被复用 {rc} 次{age_str} · {trust_tag}{RESET}")

    home_implied = (1/odds["home"]) / (1/odds["home"] + 1/odds["draw"] + 1/odds["away"]) if odds else 0.5
    odds_dict = {**(odds or {}),
                 "home_odd": odds.get("home") if odds else 99,
                 "draw_odd": odds.get("draw") if odds else 99,
                 "away_odd": odds.get("away") if odds else 99,
                 "home_implied": home_implied}
    decision = kongming.make_decision(hex_result, odds_dict)

    # === 输出推演结果 ===
    print(f"\n  {NEON_CYAN}╔═══════════════ 推演结果 ═══════════════╗{RESET}")
    print(f"  {NEON_CYAN}║{RESET}  卦象: {GOLD}{BOLD}{hex_result['hexagram_name']}{RESET}  ({hex_result['bits']})  阳{hex_result['yang_count']}/6")
    print(f"  {NEON_CYAN}║{RESET}  含义: {DIM}{hex_result['football_meaning']}{RESET}")
    print(f"  {NEON_CYAN}║{RESET}  判语: {NEON_YELLOW}{hex_result['verdict']}{RESET}")
    print(f"  {NEON_CYAN}║{RESET}")
    print(f"  {NEON_CYAN}║{RESET}  {NEON_PINK}孔明评:{RESET} {decision['verdict']}")
    print(f"  {NEON_CYAN}║{RESET}")
    print(f"  {NEON_CYAN}║{RESET}  {BOLD}推荐:{RESET}")
    print(f"  {NEON_CYAN}║{RESET}    1X2: {NEON_GREEN}{decision['1x2']}{RESET}  (信心: {decision['confidence']})")
    if odds:
        avg_g = (home_form["goals_for"] + home_form["goals_against"] + away_form["goals_for"] + away_form["goals_against"]) / 10
        ou = "under" if avg_g < 2.5 and odds.get("under_2_5", 99) < 1.85 else "over"
        print(f"  {NEON_CYAN}║{RESET}    2.5: {NEON_GREEN}{ou}{RESET}  (近期场均 {avg_g:.1f} 球)")
    else:
        ou = None
    print(f"  {NEON_CYAN}╚════════════════════════════════════════╝{RESET}\n")

    # === LLM 增强孔明评语（如已配置）===
    llm_text = kongming.llm_verdict(
        hex_result, {"match": match_str}, decision
    )
    if llm_text:
        print(f"  {NEON_PINK}╔═══════════════ 孔明亲笔 ═══════════════╗{RESET}")
        for line in llm_text.strip().split("\n"):
            print(f"  {NEON_PINK}║{RESET}  {line}")
        print(f"  {NEON_PINK}╚════════════════════════════════════════╝{RESET}\n")

    # === 写经验库 ===
    if save:
        record = {
            "exp_id": hashlib.md5(f"{match_str}{time.time()}".encode()).hexdigest()[:8],
            "source": "predict_v1_0_5",
            "timestamp": time.time(),
            "match": match_str,
            "league": league,
            "api_fixture_id": fid,
            "bits": hex_result["bits"],
            "hexagram_name": hex_result["hexagram_name"],
            "verdict": hex_result["verdict"],
            "yao_summary": yao_summary,
            "yang_count": hex_result["yang_count"],
            "predictions": {"1x2": decision["1x2"], "total_2_5": ou},
            "confidence": decision["confidence"],
            "raw_data": {"odds": odds, "h2h": h2h, "cross_validate": cross},
            "actual_result": None,
            "prediction_correct": None,
        }
        DB.parent.mkdir(parents=True, exist_ok=True)
        with open(DB, "a", encoding="utf-8") as f:
            f.write(json.dumps(record, ensure_ascii=False) + "\n")
        print(f"  {DIM}✓ 已写入经验库（待赛后回传）{RESET}\n")

    return record if save else None


def run_demo(match_str: str = None):
    """零配置 demo — 用样本数据展示完整流程
    match_str: 给了则基于队名 hash 生成确定性伪 yao 值 (同比赛每次同结果, 不同比赛不同结果)
    """
    print(f"\n  {NEON_PINK}{'━' * 50}{RESET}")
    print(f"  {BOLD}{NEON_PINK}⚠ DEMO 模式 · 非真实预测{RESET}")
    print(f"  {DIM}用内置样本数据演示 · 配 API_FOOTBALL_KEY 才跑真行情{RESET}")
    print(f"  {NEON_PINK}{'━' * 50}{RESET}\n")

    if match_str:
        import hashlib
        seed = int(hashlib.md5(match_str.encode('utf-8')).hexdigest()[:8], 16)
        def vary(base, idx):
            offset = ((seed >> (idx * 4)) & 0xFF) / 255 * 0.4 - 0.2
            return max(0.1, min(0.9, base + offset))
        sample_yao = {
            "攻防":   round(vary(0.560, 0), 3),
            "士气":   round(vary(0.600, 1), 3),
            "伤停":   round(vary(0.500, 2), 3),
            "主客场": round(vary(0.650, 3), 3),
            "交锋":   round(vary(0.533, 4), 3),
            "赔率":   round(vary(0.608, 5), 3),
        }
        display_match = match_str
    else:
        sample_yao = {
            "攻防": 0.560, "士气": 0.600, "伤停": 0.500,
            "主客场": 0.650, "交锋": 0.533, "赔率": 0.608,
        }
        display_match = "Napoli vs Lazio (样本)"

    print(f"  {BOLD}演示对阵: {display_match}{RESET}\n")
    print(f"  {NEON_GREEN}[6 维爻位]{RESET}")
    for k, v in sample_yao.items():
        state = f"{NEON_PINK}阳{RESET}" if v > 0.5 else f"{NEON_CYAN}阴{RESET}"
        bar = "█" * int(v * 20) + "░" * (20 - int(v * 20))
        print(f"    {k:<5} [{GOLD}{bar}{RESET}] {v:.3f} [{state}]")

    hex_result = hexagram.recognize(sample_yao)
    decision = kongming.make_decision(hex_result, {"home_implied": 0.61})

    print(f"\n  {NEON_GREEN}[卦象]{RESET}")
    print(f"    {GOLD}{BOLD}{hex_result['hexagram_name']}{RESET} 卦  ({hex_result['bits']})  阳爻{hex_result['yang_count']}/6")
    print(f"    {DIM}{hex_result['football_meaning']}{RESET}")
    print(f"    {NEON_YELLOW}{hex_result['verdict']}{RESET}")

    print(f"\n  {NEON_GREEN}[孔明评语]{RESET}")
    print(f"    {NEON_PINK}{decision['verdict']}{RESET}")

    print(f"\n  {NEON_GREEN}[推荐]{RESET}")
    print(f"    1X2: {NEON_GREEN}{BOLD}{decision['1x2']}{RESET} (信心: {decision['confidence']})")

    # If user has LLM configured, also show 孔明亲笔 in demo
    try:
        llm_text = kongming.llm_verdict(hex_result, {"match": display_match}, decision)
        if llm_text:
            print(f"\n  {NEON_PINK}╔═══════════════ 孔明亲笔 ═══════════════╗{RESET}")
            for line in llm_text.strip().split("\n"):
                print(f"  {NEON_PINK}║{RESET}  {line}")
            print(f"  {NEON_PINK}╚════════════════════════════════════════╝{RESET}")
    except Exception:
        pass  # demo shouldn't crash if LLM fails

    print(f"\n  {NEON_PINK}━━━ DEMO 结束 · 以上为确定性伪数据, 非真实预测 ━━━{RESET}")
    print(f"  {DIM}真数据路径: 编辑 .env.example → .env 填 API_FOOTBALL_KEY{RESET}")
    print(f"  {DIM}零成本本地 LLM 路径: 装 Ollama + qwen2.5:7b (参考 README §三档落地){RESET}\n")


def main():
    p = argparse.ArgumentParser()
    p.add_argument("match", nargs="?", default="demo",
                   help="比赛 'Home vs Away' 或 'demo'")
    p.add_argument("--league", default="serie-a")
    p.add_argument("--no-xg", action="store_true")
    p.add_argument("--no-cross", action="store_true")
    p.add_argument("--no-save", action="store_true")
    args = p.parse_args()

    if args.match == "demo":
        run_demo()
    else:
        predict_match(args.match, league=args.league,
                      use_xg=not args.no_xg,
                      use_cross_validate=not args.no_cross,
                      save=not args.no_save)


if __name__ == "__main__":
    main()
