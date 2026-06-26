"""
经验结晶引擎 — 把分散预测提炼为可复用的「晶体」

工作原理：
1. 扫描经验库所有已回传的记录
2. 用维度组合分桶（卦象 + 关键爻位区间）
3. 当某桶累积 ≥ N 场且命中率 ≥ X%，提炼为「晶体」
4. 晶体可应用于未来预测（加权 / 否决 / 增强）
5. 晶体可导出共享（共同进化）

晶体格式（v2 schema）：
{
  "crystal_id": "xtl-abc123",              # 稳定去重 key（pattern key）
  "version": "v2",
  "trigger": {
    "hexagram": "履",
    "yang_count_min": 5,
    "yao_constraints": {"赔率": [0.55, 1.0]}
  },
  "outcome": "1x2=home",
  "stats": {
    "matches": 12,                         # 训练样本数（来源记录）
    "hits": 10,
    "rate": 0.833,
    "ci_95": [0.65, 0.95]
  },
  "discovered_at": "2026-04-17T...",
  "first_seen": "2026-04-17T...",          # 本晶体首次生成/观测时间
  "last_seen": "2026-04-21T...",           # 最近一次被 match_crystal 命中的时间
  "recurrence_count": 7,                   # 被实战复用的次数（非训练样本数）
  "tags": ["football"]
}
"""
import json
import hashlib
import time
from pathlib import Path
from typing import Dict, List, Optional
from collections import defaultdict
from datetime import datetime, timezone

ROOT = Path(__file__).resolve().parent.parent
DB = ROOT / "data" / "experience.jsonl"
SEED = ROOT / "data" / "seed_experience.jsonl"
CRYSTALS_LOCAL = ROOT / "data" / "crystals_local.jsonl"
CRYSTALS_SHARED = ROOT / "data" / "crystals_shared.jsonl"


# 结晶阈值
MIN_SAMPLES = 3       # 至少 N 场才能结晶
MIN_HIT_RATE = 0.60   # 命中率 ≥ 60% 才算晶体
CONFIDENCE_Z = 1.96   # 95% 置信区间


def _find_existing(crystal_id: str) -> Optional[Dict]:
    """在本地晶体库里查已有的同 ID 晶体（用来保留 first_seen / recurrence_count）"""
    if not CRYSTALS_LOCAL.exists():
        return None
    with open(CRYSTALS_LOCAL, encoding="utf-8") as f:
        for line in f:
            if line.strip():
                try:
                    c = json.loads(line)
                    if c.get("crystal_id") == crystal_id:
                        return c
                except Exception:
                    pass
    return None


def _load_records() -> list:
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


def _wilson_ci(hits: int, n: int, z: float = CONFIDENCE_Z):
    """Wilson 置信区间（小样本更准）"""
    if n == 0:
        return (0, 0)
    p = hits / n
    denom = 1 + z**2 / n
    center = (p + z**2 / (2 * n)) / denom
    spread = z * ((p * (1 - p) + z**2 / (4 * n)) / n)**0.5 / denom
    return (max(0, center - spread), min(1, center + spread))


def crystallize(verbose=True, write=True) -> List[Dict]:
    """从历史回传记录中提炼晶体。
    write=False 时只计算不写入（预览用），保留既有 crystals_local.jsonl 不变。"""
    records = [r for r in _load_records()
               if (r.get("prediction_correct") or {}).get("1x2") is not None]

    if len(records) < MIN_SAMPLES:
        if verbose:
            print(f"  样本不足（{len(records)} < {MIN_SAMPLES}），无法结晶")
        return []

    # 按 (卦象, 阳爻数) 分桶
    buckets = defaultdict(list)
    for r in records:
        key = (r.get("hexagram_name"), r.get("yang_count"),
               r.get("predictions", {}).get("1x2"))
        buckets[key].append(r)

    crystals = []
    for (hex_name, yang, sel), group in buckets.items():
        if len(group) < MIN_SAMPLES:
            continue
        hits = sum(1 for r in group if r["prediction_correct"]["1x2"])
        rate = hits / len(group)
        if rate < MIN_HIT_RATE:
            continue

        ci_lo, ci_hi = _wilson_ci(hits, len(group))

        cid = f"xtl-{hashlib.md5(f'{hex_name}{yang}{sel}'.encode()).hexdigest()[:8]}"
        now_iso = datetime.now(timezone.utc).isoformat()
        existing = _find_existing(cid)
        crystal = {
            "crystal_id": cid,
            "version": "v2",
            "trigger": {
                "hexagram": hex_name,
                "yang_count": yang,
            },
            "outcome": f"1x2={sel}",
            "stats": {
                "matches": len(group),
                "hits": hits,
                "rate": round(rate, 3),
                "ci_95": [round(ci_lo, 3), round(ci_hi, 3)],
            },
            "discovered_at": now_iso,
            "first_seen": (existing or {}).get("first_seen", now_iso),
            "last_seen": (existing or {}).get("last_seen", now_iso),
            "recurrence_count": (existing or {}).get("recurrence_count", 0),
            "tags": ["football"],
        }
        crystals.append(crystal)

    if write:
        CRYSTALS_LOCAL.parent.mkdir(parents=True, exist_ok=True)
        with open(CRYSTALS_LOCAL, "w", encoding="utf-8") as f:
            for c in crystals:
                f.write(json.dumps(c, ensure_ascii=False) + "\n")

    if verbose:
        mode = "已存入 data/crystals_local.jsonl" if write else "DRY-RUN 未写入"
        print(f"  发现 {len(crystals)} 个晶体（{mode}）")
        for c in crystals[:5]:
            print(f"    [{c['crystal_id']}] {c['trigger']['hexagram']}卦 阳{c['trigger']['yang_count']}/6 → "
                  f"{c['outcome']}  命中率 {c['stats']['rate']*100:.0f}% "
                  f"({c['stats']['hits']}/{c['stats']['matches']})")

    return crystals


def load_crystals() -> List[Dict]:
    """加载所有晶体（本地 + 共享）"""
    crystals = []
    for path in [CRYSTALS_LOCAL, CRYSTALS_SHARED]:
        if path.exists():
            with open(path, encoding="utf-8") as f:
                for line in f:
                    if line.strip():
                        try:
                            crystals.append(json.loads(line))
                        except Exception:
                            pass
    return crystals


def match_crystal(hex_result: Dict) -> Optional[Dict]:
    """检查推演结果是否触发某个晶体（命中时回写 last_seen / recurrence_count 到本地库）"""
    crystals = load_crystals()
    matched = []
    for c in crystals:
        t = c["trigger"]
        if t.get("hexagram") and t["hexagram"] != hex_result.get("hexagram_name"):
            continue
        if t.get("yang_count") is not None and t["yang_count"] != hex_result.get("yang_count"):
            continue
        matched.append(c)

    if not matched:
        return None

    best = max(matched, key=lambda c: c["stats"]["rate"])
    _record_recurrence(best["crystal_id"])
    # 返回更新后的副本（让调用方拿到最新 recurrence_count）
    best = dict(best)
    best["last_seen"] = datetime.now(timezone.utc).isoformat()
    best["recurrence_count"] = best.get("recurrence_count", 0) + 1
    return best


def _record_recurrence(crystal_id: str) -> None:
    """晶体被 match 命中时，更新本地库里的 last_seen 和 recurrence_count。
    不动 crystals_shared.jsonl（那是从公共池拉来的，只读）。"""
    if not CRYSTALS_LOCAL.exists():
        return
    now_iso = datetime.now(timezone.utc).isoformat()
    try:
        lines = CRYSTALS_LOCAL.read_text(encoding="utf-8").splitlines()
    except Exception:
        return
    updated = False
    out = []
    for line in lines:
        line = line.strip()
        if not line:
            continue
        try:
            c = json.loads(line)
        except Exception:
            out.append(line)
            continue
        if c.get("crystal_id") == crystal_id:
            c["last_seen"] = now_iso
            c["recurrence_count"] = c.get("recurrence_count", 0) + 1
            c.setdefault("first_seen", c.get("discovered_at", now_iso))
            updated = True
        out.append(json.dumps(c, ensure_ascii=False))
    if updated:
        CRYSTALS_LOCAL.write_text("\n".join(out) + "\n", encoding="utf-8")
