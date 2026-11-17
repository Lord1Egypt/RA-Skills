#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
bootstrap.py —— 参赛链路自检 + 武器库探测(对应 SKILL.md §② / Day 0)

做什么:
1. 从环境变量读凭证,POST /authentication 认证(HTTP Basic,期望 201)——链路自检第一关
2. 分页拉 GET /data-fields(instrumentType=EQUITY, region=USA, delay=1, universe=TOP3000)
3. GET /operators 拉当前账号实际解锁的算子
4. 按 category 汇总,写入 wq_workspace/arsenal_usa.json(后续 mine.py 只用这份实测清单)
5. 打印武器库摘要:每类字段数、算子数、关键算子解锁情况

为什么要先跑它:字段/算子按账号 tier 逐级解锁,"别猜,实测"(SKILL.md §2 核心原则)。
每次 tier 变化后请重跑一次,覆盖旧清单。

用法:
    export BRAIN_EMAIL="你的注册邮箱"
    export BRAIN_PASSWORD="你的登录密码"
    python scripts/bootstrap.py

依赖:requests、numpy(见 scripts/README.md)。
"""

import json
import sys
import time
from collections import defaultdict

from wq_common import (
    ARSENAL_PATH,
    BASE,
    BrainSession,
    ensure_workspace,
    paginate,
)

# 探测口径(与 SKILL.md §2.7 提示词模板一致)
REGION = "USA"
UNIVERSE = "TOP3000"
DELAY = 1
INSTRUMENT_TYPE = "EQUITY"

# 摘要里点名检查的"地标算子":骨架必需的 + 已知常被 tier 锁的
LANDMARK_OPERATORS = [
    ("rank", "横截面排序(几乎所有因子外层)"),
    ("ts_rank", "时序分位(骨架第②层)"),
    ("group_rank", "组内排序(骨架第③层)"),
    ("group_neutralize", "组内中性化"),
    ("ts_decay_linear", "线性衰减平滑(降 turnover 利器)"),
    ("ts_zscore", "时序 z-score"),
    ("vec_stddev", "向量标准差(低 tier 常被锁)"),
    ("vec_avg", "向量均值(低 tier 常被锁)"),
]


def fetch_fields(bs):
    """分页拉全 /data-fields(SKILL.md §2.2 的翻页方式)。"""
    params = {
        "instrumentType": INSTRUMENT_TYPE,
        "region": REGION,
        "delay": DELAY,
        "universe": UNIVERSE,
    }
    print(f"[2/4] 分页拉取 /data-fields(region={REGION}, universe={UNIVERSE}, "
          f"delay={DELAY}, instrumentType={INSTRUMENT_TYPE})…")
    fields = paginate(bs, f"{BASE}/data-fields", params=params)
    print(f"      共 {len(fields)} 个字段。")
    return fields


def fetch_operators(bs):
    """GET /operators:返回当前账号可用算子列表。"""
    print("[3/4] 拉取 /operators …")
    r = bs.get(f"{BASE}/operators")
    r.raise_for_status()
    data = r.json()
    # 返回可能是裸列表,也可能包在 results 里,两种都兼容
    ops = data.get("results", data) if isinstance(data, dict) else data
    print(f"      共 {len(ops)} 个算子。")
    return ops


def _cat_name(raw):
    """category 实测可能是字符串,也可能是 {'id','name'} 对象——统一成字符串。"""
    if isinstance(raw, dict):
        return raw.get("id") or raw.get("name") or "unknown"
    return raw or "unknown"


def build_arsenal(fields, operators):
    """整理成 arsenal_usa.json 的结构(比 SKILL.md §2.6 略丰富:保留描述/覆盖率供 mine.py 粗筛)。"""
    fields_by_category = defaultdict(list)
    for f in fields:
        fields_by_category[_cat_name(f.get("category"))].append({
            "id": f.get("id"),
            "description": f.get("description", ""),
            "type": f.get("type", ""),
            "coverage": f.get("coverage"),
            "dataset": (f.get("dataset") or {}).get("id"),
        })
    # 每类按覆盖率降序,低覆盖字段自然沉底(低覆盖易 Sharpe 虚高,SKILL.md §2.2)
    for cat in fields_by_category:
        fields_by_category[cat].sort(key=lambda x: -(x["coverage"] or 0.0))

    ops_clean = []
    for o in operators:
        if isinstance(o, dict):
            ops_clean.append({
                "name": o.get("name"),
                "category": _cat_name(o.get("category", "")),
                "scope": o.get("scope", []),
                "definition": o.get("definition", ""),
                "level": o.get("level", ""),
            })
        else:  # 极端情况:只给了名字字符串
            ops_clean.append({"name": str(o), "category": "", "scope": [],
                              "definition": "", "level": ""})

    return {
        "generated_at": time.strftime("%Y-%m-%d %H:%M:%S"),
        "region": REGION,
        "universe": UNIVERSE,
        "delay": DELAY,
        "instrument_type": INSTRUMENT_TYPE,
        "fields_by_category": dict(fields_by_category),
        "operators": ops_clean,
    }


def print_summary(arsenal):
    """打印武器库摘要:每类字段数、算子分布、地标算子解锁情况。"""
    print()
    print("=" * 62)
    print("武器库摘要(你账号当前 tier 的实测结果)")
    print("=" * 62)

    print(f"\n◆ 数据字段(region={REGION} / universe={UNIVERSE} / delay={DELAY})")
    total = 0
    for cat, items in sorted(arsenal["fields_by_category"].items(),
                             key=lambda kv: -len(kv[1])):
        total += len(items)
        tops = ", ".join(x["id"] for x in items[:3] if x["id"])
        print(f"  {cat:<14s} {len(items):>5d} 个   例:{tops}")
    print(f"  {'合计':<14s} {total:>5d} 个")

    ops = arsenal["operators"]
    by_cat = defaultdict(int)
    for o in ops:
        by_cat[o.get("category") or "unknown"] += 1
    print(f"\n◆ 算子(共 {len(ops)} 个,按类别)")
    for cat, n in sorted(by_cat.items(), key=lambda kv: -kv[1]):
        print(f"  {cat:<22s} {n:>4d} 个")

    names = {o.get("name") for o in ops}
    print("\n◆ 关键算子解锁情况(骨架必需 + 常见 tier 锁)")
    for name, note in LANDMARK_OPERATORS:
        mark = "已解锁 ✓" if name in names else "未解锁 ✗(tier 锁,升级后重跑本脚本)"
        print(f"  {name:<18s} {mark}   —— {note}")

    missing_core = [n for n, _ in LANDMARK_OPERATORS[:3] if n not in names]
    if missing_core:
        print(f"\n  [警告] 骨架核心算子缺失:{missing_core},mine.py 的模板将无法回测。")
    else:
        print("\n  骨架 group_rank(ts_rank(SIGNAL, 窗口), 分组) 所需算子齐全,可以开挖。")


def main():
    print("=" * 62)
    print("WorldQuant BRAIN 参赛链路自检 + 武器库探测(bootstrap)")
    print("=" * 62)

    print("[1/4] 认证:POST /authentication(HTTP Basic)…")
    bs = BrainSession()   # 凭证缺失/认证失败会打印中文指引并退出
    print("      认证成功(HTTP 201),会话已建立。")

    fields = fetch_fields(bs)
    operators = fetch_operators(bs)

    print("[4/4] 写入武器库清单 …")
    ensure_workspace()
    arsenal = build_arsenal(fields, operators)
    ARSENAL_PATH.write_text(json.dumps(arsenal, ensure_ascii=False, indent=2))
    print(f"      已写入 {ARSENAL_PATH}")

    print_summary(arsenal)

    print("\n下一步:python scripts/mine.py --limit 20  (开始挖矿)")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n[中断] 已手动停止。")
        sys.exit(130)
