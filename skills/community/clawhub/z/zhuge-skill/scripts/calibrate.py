"""
权重校准 — 用回传后的命中率反向调整 6 维爻位的权重

工作原理：
1. 拉所有回传后的预测
2. 用线性回归找出哪些维度对实际胜负预测力最强
3. 输出新的权重建议（不自动覆盖，用户手动审查）

用法:
    python scripts/calibrate.py              # 显示建议
    python scripts/calibrate.py --apply      # 写入 weights.json（生效）
"""
import sys
import json
import argparse
from pathlib import Path
from collections import defaultdict

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

from core.welcome import (NEON_CYAN, NEON_PINK, NEON_GREEN, NEON_YELLOW,
                          GOLD, DIM, BOLD, RESET, GRAY, HOT_RED as RED)

DB = ROOT / "data" / "experience.jsonl"
SEED = ROOT / "data" / "seed_experience.jsonl"
WEIGHTS = ROOT / "data" / "weights.json"

DEFAULT_WEIGHTS = {
    "攻防": 0.30, "士气": 0.20, "伤停": 0.05,
    "主客场": 0.15, "交锋": 0.10, "赔率": 0.20,
}


def load_records() -> list:
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


def calibrate(verbose=True, apply=False):
    """简化的相关性分析（不用 numpy，纯 stdlib）"""
    records = [r for r in load_records()
               if r.get("prediction_correct") and r.get("yao_summary")]

    if len(records) < 10:
        if verbose:
            print(f"\n  {NEON_YELLOW}样本不足{RESET}（{len(records)} < 10），无法稳定校准")
            print(f"  {DIM}建议先跑更多预测 + 回传，至少 10 场{RESET}\n")
        return None

    # 对每个维度计算「该维度阳爻 vs 主胜命中」的相关性
    correlations = {}
    for dim in DEFAULT_WEIGHTS.keys():
        # X = 该维度的爻位值（0~1）
        # Y = 1x2 是否命中（0/1）
        # 简化：用 point-biserial correlation
        xs, ys = [], []
        for r in records:
            yao_v = r.get("yao_summary", {}).get(dim)
            pc = (r.get("prediction_correct") or {}).get("1x2")
            if yao_v is not None and pc is not None:
                xs.append(yao_v)
                ys.append(1 if pc else 0)

        if len(xs) < 5:
            correlations[dim] = 0
            continue

        n = len(xs)
        mean_x = sum(xs) / n
        mean_y = sum(ys) / n
        cov = sum((x - mean_x) * (y - mean_y) for x, y in zip(xs, ys)) / n
        var_x = sum((x - mean_x) ** 2 for x in xs) / n
        var_y = sum((y - mean_y) ** 2 for y in ys) / n
        if var_x == 0 or var_y == 0:
            correlations[dim] = 0
        else:
            correlations[dim] = cov / (var_x ** 0.5 * var_y ** 0.5)

    # 把负相关也变成正贡献（绝对值），归一化
    abs_corr = {k: abs(v) for k, v in correlations.items()}
    total = sum(abs_corr.values())
    if total == 0:
        new_weights = DEFAULT_WEIGHTS.copy()
    else:
        new_weights = {k: round(v / total, 3) for k, v in abs_corr.items()}

    if verbose:
        print(f"\n  {NEON_CYAN}╔═══ 权重校准建议 {' ' * 25}═══╗{RESET}")
        print(f"  {NEON_CYAN}║{RESET}  样本: {len(records)} 条已回传记录")
        print(f"  {NEON_CYAN}║{RESET}")
        print(f"  {NEON_CYAN}║{RESET}  {BOLD}维度  → 相关性 → 当前权重 → 建议权重{RESET}")
        for dim, w in DEFAULT_WEIGHTS.items():
            corr = correlations.get(dim, 0)
            new_w = new_weights.get(dim, w)
            arrow = "↑" if new_w > w else ("↓" if new_w < w else "=")
            color = NEON_GREEN if arrow == "↑" else (RED if arrow == "↓" else DIM)
            print(f"  {NEON_CYAN}║{RESET}  {dim:<5}  → {corr:+.3f}  → {w:.2f}  → {color}{new_w:.2f} {arrow}{RESET}")
        print(f"  {NEON_CYAN}║{RESET}")

        if apply:
            WEIGHTS.parent.mkdir(parents=True, exist_ok=True)
            WEIGHTS.write_text(json.dumps(new_weights, ensure_ascii=False, indent=2),
                              encoding="utf-8")
            print(f"  {NEON_CYAN}║{RESET}  {NEON_GREEN}✓ 已写入 data/weights.json{RESET}")
        else:
            print(f"  {NEON_CYAN}║{RESET}  {DIM}（仅显示。--apply 才会生效）{RESET}")
        print(f"  {NEON_CYAN}╚{'═' * 50}╝{RESET}\n")

    return new_weights


def main():
    p = argparse.ArgumentParser()
    p.add_argument("--apply", action="store_true", help="写入 weights.json（默认仅显示）")
    args = p.parse_args()
    calibrate(verbose=True, apply=args.apply)


if __name__ == "__main__":
    main()
