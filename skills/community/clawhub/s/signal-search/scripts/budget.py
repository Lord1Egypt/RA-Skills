"""scripts/budget.py - token 预算 + 早停 + 缓存读写接口（§5.11 / B4）。"""

import json
import os
from typing import Dict

TIER_DEFAULTS = {
    "L0": 2000,
    "L1": 8000,
    "L2": 30000,
    "L3": 100000,
}
CONFIG_PATH = os.path.join(
    os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "config.json"
)


def _load_tier_defaults() -> Dict[str, int]:
    try:
        with open(CONFIG_PATH, "r", encoding="utf-8") as f:
            return json.load(f).get("tier_defaults", TIER_DEFAULTS)
    except Exception:
        return TIER_DEFAULTS


def monitor(token_used: int, budget: int) -> Dict[str, bool]:
    """软上限；over=True 时调用方停手并标 exhausted=False。"""
    return {"over": token_used >= budget}


def estimate(query: str, tier: str, n_subqs: int = 0) -> int:
    """按档位默认预算做线性修正（P1-5）：查询越长、子问题越多，预算越高；封顶不出界。

    - 长度系数：0.6 + min(len(query)/200, 1.4) → 区间 [0.6, 2.0]
    - 子问题系数：1 + 0.15 * n_subqs
    - 上限：档位默认预算的 3 倍，避免异常长查询撑爆预算
    """
    tier_cfg = _load_tier_defaults().get(tier, {})
    base = tier_cfg.get("budget", 8000) if isinstance(tier_cfg, dict) else tier_cfg
    # 长度系数以 ~0.75 为基线（贴近旧 0.85 默认），随查询长度线性上升，封顶 1.75
    length_factor = 0.75 + min(len(query or "") / 300.0, 1.0)
    subq_factor = 1.0 + 0.15 * max(0, int(n_subqs))
    est = base * length_factor * subq_factor
    return int(min(est, base * 3))


# 缓存接口见 cache.Cache（不再在此处留 NotImplementedError 占位，避免误导调用方，S6 清理）
