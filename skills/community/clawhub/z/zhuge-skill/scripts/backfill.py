"""
经验回传 — 拉取实际比赛结果，回写经验库，计算命中率

工作流：
1. 扫描经验库所有 actual_result == null 的记录
2. 跳过赛前 3 小时内的（结果未必出来）
3. 调 API-Football 拉真实结果
4. 计算 prediction_correct
5. 写回经验库
6. 输出本次回传统计

用法：
    python scripts/backfill.py              # 单次回传
    python scripts/backfill.py --loop 30    # 每 30 分钟循环一次（守护进程模式）
"""
import sys
import json
import time
import argparse
import os
from pathlib import Path
from datetime import datetime, timezone, timedelta

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

DB = ROOT / "data" / "experience.jsonl"
SEED = ROOT / "data" / "seed_experience.jsonl"


def _load_db() -> list:
    """合并种子 + 用户库"""
    records = []
    for path in [SEED, DB]:
        if path.exists():
            with open(path, encoding="utf-8") as f:
                for line in f:
                    if line.strip():
                        try:
                            records.append(json.loads(line))
                        except Exception:
                            pass
    return records


def _save_db(records: list):
    """覆盖写用户库（种子库不动）"""
    DB.parent.mkdir(parents=True, exist_ok=True)
    # 只保存非种子记录（user 自己的预测）
    seed_ids = set()
    if SEED.exists():
        with open(SEED, encoding="utf-8") as f:
            for line in f:
                if line.strip():
                    try:
                        seed_ids.add(json.loads(line)["exp_id"])
                    except Exception:
                        pass
    user_records = [r for r in records if r.get("exp_id") not in seed_ids]
    with open(DB, "w", encoding="utf-8") as f:
        for r in user_records:
            f.write(json.dumps(r, ensure_ascii=False) + "\n")


def _fetch_actual_result(api_fid: int) -> dict:
    """从 API-Football 拿真实结果"""
    if not os.getenv("API_FOOTBALL_KEY"):
        return None
    try:
        import requests
        r = requests.get("https://v3.football.api-sports.io/fixtures",
                         headers={"x-apisports-key": os.getenv("API_FOOTBALL_KEY")},
                         params={"id": api_fid}, timeout=15)
        if not r.ok:
            return None
        data = r.json().get("response", [])
        if not data:
            return None
        m = data[0]
        status = m["fixture"]["status"]["short"]
        if status not in ("FT", "AET", "PEN"):  # 未结束
            return None
        gh = m["goals"]["home"] or 0
        ga = m["goals"]["away"] or 0
        return {
            "home_goals": gh,
            "away_goals": ga,
            "winner": "home" if gh > ga else ("away" if gh < ga else "draw"),
            "total_goals": gh + ga,
            "status": status,
        }
    except Exception as e:
        try:
            from scripts.error_log import log_error
            log_error("fetch_actual_result", e, {"api_fid": api_fid})
        except Exception:
            pass
        return None


def _check_correct(prediction: dict, actual: dict) -> dict:
    """判定预测是否正确"""
    correct = {}
    if "1x2" in prediction:
        correct["1x2"] = (prediction["1x2"] == actual["winner"])
    if "total_2_5" in prediction:
        is_over = actual["total_goals"] > 2.5
        correct["total_2_5"] = (
            (prediction["total_2_5"] == "over" and is_over) or
            (prediction["total_2_5"] == "under" and not is_over)
        )
    if "score" in prediction:
        actual_score = f"{actual['home_goals']}:{actual['away_goals']}"
        scores = prediction["score"]
        if isinstance(scores, str):
            scores = [scores]
        correct["score"] = (actual_score in scores)
    # 综合命中率（任一维度命中算半成功）
    if correct:
        correct["any"] = any(correct.values())
        correct["all"] = all(correct.values())
    return correct


def backfill_once(verbose: bool = True) -> dict:
    """单次回传"""
    records = _load_db()
    pending = [r for r in records
               if r.get("actual_result") is None
               and r.get("api_fixture_id")]

    if verbose:
        print(f"\n  扫描经验库：{len(records)} 条总记录，{len(pending)} 条待回传\n")

    backfilled = 0
    correct_count = {"1x2": 0, "total_2_5": 0, "any": 0, "all": 0}
    total_checked = 0

    for r in pending:
        fid = r.get("api_fixture_id")
        actual = _fetch_actual_result(fid)
        if not actual:
            if verbose:
                print(f"  ⏳ {r.get('match','?')} 结果未出（fixture={fid}）")
            continue

        r["actual_result"] = actual
        prediction = r.get("predictions", {})
        correctness = _check_correct(prediction, actual)
        r["prediction_correct"] = correctness
        r["backfilled_at"] = datetime.now(timezone.utc).isoformat()

        backfilled += 1
        total_checked += 1
        for k in correct_count:
            if correctness.get(k):
                correct_count[k] += 1

        if verbose:
            mark = "✓" if correctness.get("1x2") else "✗"
            print(f"  {mark} {r.get('match','?'):40} 预测={prediction.get('1x2','?')} "
                  f"实际={actual['winner']:5} 比分={actual['home_goals']}-{actual['away_goals']}")

    if backfilled > 0:
        _save_db(records)

    # 统计累积命中率
    all_with_result = [r for r in records if r.get("prediction_correct")]
    cumulative = {"1x2": 0, "total_2_5": 0, "any": 0}
    for r in all_with_result:
        c = r["prediction_correct"]
        for k in cumulative:
            if c.get(k):
                cumulative[k] += 1
    n = max(1, len(all_with_result))

    if verbose:
        print(f"\n  本次回传：{backfilled} 条")
        if total_checked > 0:
            print(f"  本次命中率：1x2 {correct_count['1x2']}/{total_checked} "
                  f"({100*correct_count['1x2']/total_checked:.0f}%)")
        print(f"  累计命中率：1x2 {cumulative['1x2']}/{n} ({100*cumulative['1x2']/n:.0f}%) "
              f"| 大小球 {cumulative['total_2_5']}/{n} ({100*cumulative['total_2_5']/n:.0f}%)")
        print()

    return {
        "backfilled": backfilled,
        "checked": total_checked,
        "this_round": correct_count,
        "cumulative": cumulative,
        "total_records": len(records),
    }


def loop_backfill(interval_minutes: int = 30):
    """守护进程模式 — 每 N 分钟跑一次"""
    print(f"  守护模式启动：每 {interval_minutes} 分钟扫描一次")
    print(f"  按 Ctrl+C 停止\n")
    while True:
        try:
            backfill_once(verbose=True)
            time.sleep(interval_minutes * 60)
        except KeyboardInterrupt:
            print("\n  停止守护进程")
            break
        except Exception as e:
            try:
                from scripts.error_log import log_error
                log_error("backfill_loop", e, {"interval_min": interval_minutes})
            except Exception:
                pass
            print(f"  ERR: {e}（30 秒后重试）")
            time.sleep(30)


def main():
    p = argparse.ArgumentParser()
    p.add_argument("--loop", type=int, default=0,
                   help="守护模式间隔（分钟），0=单次")
    args = p.parse_args()

    if args.loop > 0:
        loop_backfill(args.loop)
    else:
        backfill_once()


if __name__ == "__main__":
    main()
