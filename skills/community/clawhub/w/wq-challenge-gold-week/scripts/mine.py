#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
mine.py —— 挖矿流水线:生成候选 → 回测 → 三道门筛选 → keeper 入池(对应 SKILL.md §③⑤)

流水线:
1. 读 wq_workspace/arsenal_usa.json(先跑 bootstrap.py 生成)
2. 按公开骨架批量生成候选表达式(SKILL.md §3.1 / §3.2):
       group_rank( ts_rank( 分子/分母 , 窗口 ) , 分组 )
   - 分子:fundamental / analyst 两类字段按关键词粗筛(利润/现金流/营收/分析师预期等)
   - 分母:close / assets / equity / cap / sales(§3.2 分母杠杆表,只用武器库里实测存在的)
   - 窗口:63 / 126 / 252(长窗压 turnover 救 Fitness,§3.3)
   - 分组:industry / subindustry(§3.5)
3. K=2 并发 POST /simulations,每 8 秒轮询到 COMPLETE(平台硬约定,绝不加速)
4. 三道门:is.sharpe ≥ 1.25、is.fitness ≥ 1.0、checks 无 FAIL
5. 过门者拉 /alphas/{id}/recordsets/pnl 差分成日收益,与池内已有 keeper 算 Pearson,
   max |corr| < 0.9 才入 pool.jsonl(池内多样性;提交时另有更严的 <0.70 线,见 submit_daily.py)

健壮性:
- 已试过的表达式记 wq_workspace/tried.txt,跨次运行去重
- 429 按 Retry-After 退避;401 自动重认证一次(wq_common 统一处理)
- Ctrl-C 中断安全:tried / pool 都是随评随追加落盘,再跑即续

用法:
    python scripts/mine.py               # 默认本次最多回测 20 条
    python scripts/mine.py --limit 50    # 自定义本次回测条数
"""

import argparse
import json
import random
import sys
import time

from wq_common import (
    ARSENAL_PATH,
    BASE,
    WORKSPACE,
    FITNESS_MIN,
    MAX_CONCURRENCY,
    POLL_INTERVAL,
    POOL_PATH,
    SHARPE_MIN,
    CORR_POOL_MAX,
    BrainSession,
    alpha_failed_checks,
    append_jsonl,
    ensure_workspace,
    get_alpha,
    get_daily_returns,
    load_jsonl,
    load_tried,
    mark_tried,
    max_abs_corr,
)

# ---------------------------------------------------------------------------
# 搜索空间 —— 你的分叉点(SKILL.md §5.8)
#
# 首次运行会把默认搜索空间写入 wq_workspace/recipes.json。
# 默认值人人相同(共同的起步);但从 Day 2 起,你应该根据"自己的命中数据"编辑它:
# 换关键词、加分母、开新窗口、写自定义模板——**每个人的 recipes.json 演化路径不同,
# 挖出的因子就不同**。这个文件(连同你的活页手册)才是本 skill 真正的产出。
# ---------------------------------------------------------------------------

DEFAULT_RECIPES = {
    "_readme": "这是你的分叉点:默认值=公共起步;请按你的命中数据迭代它(方法见 SKILL.md 第⑤章,尤其 5.8)。改完直接重跑 mine.py 即生效。",
    "numerator_keywords": ["income", "profit", "earn", "ebit",
                            "cashflow", "cash_flow", "fcf", "ocf",
                            "revenue", "sales",
                            "eps", "est_", "estimate", "forecast"],
    "numerator_categories": ["fundamental", "analyst"],
    "max_numerators": 24,
    "denominators": ["close", "assets", "equity", "cap", "sales"],
    "windows": [63, 126, 252],
    "groups": ["industry", "subindustry"],
    "extra_templates": [
        "// 自定义表达式模板,占位符:{num} {den} {w} {g}。示例(去掉本行注释后生效):",
        "// group_rank(ts_rank({num}/{den}*{num2}/{den2}, {w}), {g})  —— 双腿相乘(§3.4 第一式)"
    ]
}
# 最全预设:认知不够、不想手工调网的用户一键用它(python scripts/mine.py --preset full)。
# 空间更大(窗口全档/三级分组/6 分母/40 分子)+ 两个已启用的组合模板(§3.4 第一、二式)。
# 代价:全空间从 ~240 条涨到 ~2000+ 条,靠 --limit 分天推进,tried.txt 记进度。
FULL_RECIPES = {
    "_readme": "最全预设(--preset full 生成)。它仍是'公共起步'——真正的分叉靠你此后按命中数据修剪/扩展它:砍掉低命中的窗口、加你发现的好分母、写你自己的模板。",
    "numerator_keywords": ["income", "profit", "earn", "ebit", "ebitda", "margin",
                            "cashflow", "cash_flow", "fcf", "ocf",
                            "revenue", "sales", "book", "dividend",
                            "eps", "est_", "estimate", "forecast", "guidance"],
    "numerator_categories": ["fundamental", "analyst"],
    "max_numerators": 40,
    "denominators": ["close", "assets", "equity", "cap", "sales", "enterprise_value"],
    "windows": [20, 63, 126, 252, 504],
    "groups": ["industry", "subindustry", "sector"],
    "extra_templates": [
        "group_rank(ts_rank({num}/{den}*{num2}/{den2}, {w}), {g})",
        "0.5*rank({num}/{den})+0.5*rank({num2}/{den2})"
    ]
}
RECIPES_PATH = WORKSPACE / "recipes.json"

def apply_preset(name):
    """--preset starter|full:重写 recipes.json(已有的自定义会先备份为 .bak)。"""
    ensure_workspace()
    preset = DEFAULT_RECIPES if name == "starter" else FULL_RECIPES
    if RECIPES_PATH.exists():
        bak = RECIPES_PATH.with_suffix(".json.bak")
        bak.write_text(RECIPES_PATH.read_text())
        print(f"[preset] 原 recipes.json 已备份 → {bak}")
    RECIPES_PATH.write_text(json.dumps(preset, ensure_ascii=False, indent=2))
    print(f"[preset] 已应用 '{name}' 搜索空间 → {RECIPES_PATH}")

def load_recipes():
    """读取(首次则生成)你的个人搜索空间。这里是'同一起点、不同演化'的技术落点。"""
    ensure_workspace()
    if not RECIPES_PATH.exists():
        RECIPES_PATH.write_text(json.dumps(DEFAULT_RECIPES, ensure_ascii=False, indent=2))
        print(f"[分叉点] 已生成默认搜索空间 → {RECIPES_PATH}")
        print("         从 Day 2 起,请根据你的命中率数据编辑它(或让你的 AI 按模板 C 的复盘结论改)。")
    r = json.loads(RECIPES_PATH.read_text())
    for k, v in DEFAULT_RECIPES.items():   # 新版本字段兜底,旧 recipes 文件不失效
        r.setdefault(k, v)
    return r

SIM_TIMEOUT = 900          # 单条回测最长等待(秒),超时放弃该条继续后面的


def build_candidates(arsenal):
    """分子 × 分母 × 窗口 × 分组 的笛卡尔积,套进公开骨架。搜索空间来自你的 recipes.json。"""
    R = load_recipes()
    NUMERATOR_KEYWORDS = tuple(R["numerator_keywords"])
    NUMERATOR_CATEGORIES = tuple(R["numerator_categories"])
    MAX_NUMERATORS = int(R["max_numerators"])
    DENOMINATORS = list(R["denominators"])
    WINDOWS = list(R["windows"])
    GROUPS = list(R["groups"])
    fields_by_cat = arsenal.get("fields_by_category", {})

    # 全部字段 id 集合(用来确认分母真的存在于武器库)
    all_ids = set()
    for items in fields_by_cat.values():
        for f in items:
            fid = f["id"] if isinstance(f, dict) else str(f)
            if fid:
                all_ids.add(fid)

    # 分母:只保留武器库里实测存在的
    denoms = [d for d in DENOMINATORS if d in all_ids]
    missing = [d for d in DENOMINATORS if d not in all_ids]
    if missing:
        print(f"[提示] 以下分母字段不在你的武器库里,已跳过:{missing}")
    if not denoms:
        print("[错误] 五个分母字段一个都不可用,无法按 §3.2 组网。请检查 arsenal_usa.json。")
        sys.exit(1)

    # 分子:fundamental/analyst 里按关键词粗筛,按覆盖率降序取前 MAX_NUMERATORS 个
    numerators = []
    for cat in NUMERATOR_CATEGORIES:
        for f in fields_by_cat.get(cat, []):
            fid = f["id"] if isinstance(f, dict) else str(f)
            desc = (f.get("description", "") if isinstance(f, dict) else "")
            cov = (f.get("coverage") if isinstance(f, dict) else None) or 0.0
            text = f"{fid} {desc}".lower()
            if fid and any(k in text for k in NUMERATOR_KEYWORDS):
                numerators.append((fid, cov))
    numerators.sort(key=lambda x: -x[1])
    numerators = [fid for fid, _ in numerators[:MAX_NUMERATORS]]

    if not numerators:
        print("[错误] fundamental/analyst 类里没筛到任何分子字段。"
              "可能账号 tier 未解锁这两类数据,或需调整 NUMERATOR_KEYWORDS。")
        sys.exit(1)

    print(f"[候选生成] 分子 {len(numerators)} 个 × 分母 {len(denoms)} 个 × "
          f"窗口 {len(WINDOWS)} 个 × 分组 {len(GROUPS)} 个")

    exprs = []
    for num in numerators:
        for den in denoms:
            if num == den:      # sales/sales 之类无意义比率,跳过
                continue
            for w in WINDOWS:
                for g in GROUPS:
                    exprs.append(f"group_rank(ts_rank({num}/{den}, {w}), {g})")

    # 你的自定义模板(recipes.json 的 extra_templates,// 开头的行是注释)
    custom = [t for t in R.get("extra_templates", []) if isinstance(t, str) and not t.strip().startswith("//")]
    if custom:
        rnd = random.Random(20260102)
        for t in custom:
            for _ in range(min(60, len(numerators) * 2)):   # 每个模板抽样填充,防爆炸
                try:
                    e = t.format(num=rnd.choice(numerators), den=rnd.choice(denoms),
                                 num2=rnd.choice(numerators), den2=rnd.choice(denoms),
                                 w=rnd.choice(WINDOWS), g=rnd.choice(GROUPS))
                    exprs.append(e)
                except (KeyError, IndexError):
                    print(f"[提示] 自定义模板占位符有误,跳过:{t[:60]}")
                    break
        print(f"[候选生成] 自定义模板 {len(custom)} 个已并入(你的分叉在生效)")

    # 固定种子打散:让有限的 --limit 覆盖多个"分子家族",而不是死磕第一个分子;
    # 种子固定 → 每次运行顺序一致,配合 tried.txt 逐步推进整张网
    random.Random(20260101).shuffle(exprs)
    print(f"[候选生成] 全空间 {len(exprs)} 条表达式(去重前)")
    return exprs


def sim_payload(expr, arsenal):
    """构造 POST /simulations 请求体(设置与 SKILL.md Day 0 示例一致)。"""
    return {
        "type": "REGULAR",
        "settings": {
            "instrumentType": arsenal.get("instrument_type", "EQUITY"),
            "region": arsenal.get("region", "USA"),
            "universe": arsenal.get("universe", "TOP3000"),
            "delay": arsenal.get("delay", 1),
            "decay": 4,
            "neutralization": "INDUSTRY",
            "truncation": 0.08,
            "pasteurization": "ON",
            "unitHandling": "VERIFY",
            "nanHandling": "OFF",
            "language": "FASTEXPR",
            "visualization": False,
        },
        "regular": expr,
    }


def launch_sim(bs, expr, arsenal):
    """POST /simulations,成功返回轮询用的 Location URL;失败返回 None。"""
    r = bs.post(f"{BASE}/simulations", json=sim_payload(expr, arsenal))
    loc = r.headers.get("Location")
    if r.status_code in (200, 201) and loc:
        return loc
    print(f"  [提交失败] HTTP {r.status_code}:{r.text[:200]}")
    return None


def load_pool_basis(bs):
    """读 pool.jsonl 里已有 keeper 的日收益(算池内相关的基准);顺带返回已入池 alpha 集合。"""
    pool = load_jsonl(POOL_PATH)
    basis, alpha_ids = [], set()
    if pool:
        print(f"[池] pool.jsonl 已有 {len(pool)} 个 keeper,加载其日收益作相关基准 …")
    for entry in pool:
        aid = entry.get("alpha_id")
        if not aid or aid in alpha_ids:
            continue
        alpha_ids.add(aid)
        rets = get_daily_returns(bs, aid)   # 有本地缓存,通常不打 API
        if rets:
            basis.append(rets)
    return basis, alpha_ids


def evaluate(bs, expr, sim_result, pool_basis, stats):
    """回测 COMPLETE 后:过三道门 → 算池内相关 → 决定是否入池。"""
    alpha_id = sim_result.get("alpha")
    if not alpha_id:
        print(f"  [异常] 回测完成但没有 alpha id:{str(sim_result)[:150]}")
        return

    alpha = get_alpha(bs, alpha_id)
    is_ = alpha.get("is") or {}
    sharpe = is_.get("sharpe")
    fitness = is_.get("fitness")
    turnover = is_.get("turnover")
    fails = alpha_failed_checks(alpha)

    head = f"  alpha={alpha_id}  Sharpe={_fmt(sharpe)}  Fitness={_fmt(fitness)}  Turnover={_fmt(turnover)}"

    # 三道门(SKILL.md §4.2):Sharpe ≥ 1.25、Fitness ≥ 1.0、checks 无 FAIL
    if sharpe is None or sharpe < SHARPE_MIN:
        print(f"{head}  → 淘汰(Sharpe < {SHARPE_MIN})")
        return
    if fitness is None or fitness < FITNESS_MIN:
        print(f"{head}  → 淘汰(Fitness < {FITNESS_MIN};可试更长窗口降换手,§3.3)")
        return
    if fails:
        print(f"{head}  → 淘汰(checks FAIL:{fails})")
        return

    # 池内相关:与已有 keeper 的日收益算 Pearson,max |corr| < 0.9 才入池
    rets = get_daily_returns(bs, alpha_id)
    if not rets:
        print(f"{head}  → 过了三道门但拉不到 PnL,暂不入池")
        return
    corr = max_abs_corr(rets, pool_basis)
    if corr >= CORR_POOL_MAX:
        print(f"{head}  → 过三道门,但与池内相关 {corr:.2f} ≥ {CORR_POOL_MAX},不入池(克隆无价值,§5.5)")
        return

    settings = alpha.get("settings") or {}
    entry = {
        "alpha_id": alpha_id,
        "expression": expr,
        "sharpe": sharpe,
        "fitness": fitness,
        "turnover": turnover,
        "universe": settings.get("universe", "TOP3000"),
        "region": settings.get("region", "USA"),
        "neutralization": settings.get("neutralization", "INDUSTRY"),
        "max_corr_in_pool": round(corr, 4),
        "created_at": time.strftime("%Y-%m-%d %H:%M:%S"),
    }
    append_jsonl(POOL_PATH, entry)      # 随评随写盘,Ctrl-C 不丢
    pool_basis.append(rets)             # 新 keeper 立刻成为后续候选的相关基准
    stats["keepers"] += 1
    print(f"{head}  → ✅ KEEPER 入池(池内相关 {corr:.2f})")


def _fmt(v):
    return f"{v:.2f}" if isinstance(v, (int, float)) else "N/A"


def main():
    ap = argparse.ArgumentParser(description="BRAIN alpha 挖矿流水线(先跑 bootstrap.py)")
    ap.add_argument("--limit", type=int, default=20,
                    help="本次最多回测多少条候选(默认 20;分数瓶颈在质量不在数量)")
    ap.add_argument("--preset", choices=["starter", "full"], default=None,
                    help="重置搜索空间:starter=精简起步 / full=最全网(不会调参也能吃满空间)")
    args = ap.parse_args()
    if args.preset:
        apply_preset(args.preset)

    ensure_workspace()
    if not ARSENAL_PATH.exists():
        print(f"[错误] 找不到 {ARSENAL_PATH}。请先跑:python scripts/bootstrap.py")
        sys.exit(1)
    arsenal = json.loads(ARSENAL_PATH.read_text())

    print("=" * 62)
    print(f"挖矿流水线:region={arsenal.get('region')} universe={arsenal.get('universe')} "
          f"并发=K{MAX_CONCURRENCY} 轮询={POLL_INTERVAL}s")
    print("=" * 62)

    # 候选生成 + tried.txt 去重
    exprs = build_candidates(arsenal)
    tried = load_tried()
    todo = [e for e in exprs if e not in tried][:args.limit]
    print(f"[去重] 已试过 {len(tried)} 条;本次将回测 {len(todo)} 条(--limit {args.limit})")
    if not todo:
        print("本轮网格已全部试过。请扩大搜索空间(换分子关键词/加窗口/加分组),"
              "参考 SKILL.md §5.2 覆盖率纪律。")
        return

    bs = BrainSession()
    pool_basis, _ = load_pool_basis(bs)

    stats = {"launched": 0, "complete": 0, "failed": 0, "keepers": 0}
    queue = list(todo)
    inflight = []   # [{expr, loc, started}]

    try:
        while queue or inflight:
            # 补满并发槽(严格 ≤ K=2,绝不绕过)
            while queue and len(inflight) < MAX_CONCURRENCY:
                expr = queue.pop(0)
                print(f"\n[启动 {stats['launched'] + 1}/{len(todo)}] {expr}")
                mark_tried(expr)           # 启动即记 tried:中断也不重复烧回测额度
                loc = launch_sim(bs, expr, arsenal)
                stats["launched"] += 1
                if loc:
                    inflight.append({"expr": expr, "loc": loc, "started": time.time()})
                else:
                    stats["failed"] += 1

            if not inflight:
                continue

            time.sleep(POLL_INTERVAL)      # 8 秒轮询,尊重平台

            for job in inflight[:]:
                r = bs.get(job["loc"])
                data = r.json() if r.status_code == 200 and r.text.strip() else {}
                status = data.get("status", "")
                if status == "COMPLETE":
                    inflight.remove(job)
                    stats["complete"] += 1
                    evaluate(bs, job["expr"], data, pool_basis, stats)
                elif status in ("FAIL", "ERROR"):
                    inflight.remove(job)
                    stats["failed"] += 1
                    msg = data.get("message") or str(data)[:150]
                    print(f"  [回测失败] {job['expr']}\n    原因:{msg}")
                elif time.time() - job["started"] > SIM_TIMEOUT:
                    inflight.remove(job)
                    stats["failed"] += 1
                    print(f"  [超时放弃] {job['expr']}(>{SIM_TIMEOUT}s)")
                # 其余状态(排队/运行中)继续等下一轮
    except KeyboardInterrupt:
        print("\n[中断] Ctrl-C。已评估的结果均已落盘(tried.txt / pool.jsonl),再跑即续。")

    print("\n" + "=" * 62)
    print(f"本轮小结:启动 {stats['launched']} 条,完成 {stats['complete']} 条,"
          f"失败/超时 {stats['failed']} 条,新增 keeper {stats['keepers']} 个")
    pool_total = len(load_jsonl(POOL_PATH))
    print(f"候选池累计:{pool_total} 个(见 {POOL_PATH})")
    print("下一步:python scripts/submit_daily.py  (每日精提,人工确认)")
    print()
    print("💡 迭代提示(这才是本 skill 的核心玩法,见 SKILL.md §5.8):")
    print(f"   你的搜索空间在 {RECIPES_PATH} —— 可改:分子关键词 / 分母 / 窗口 / 分组 /")
    print("   自定义表达式模板(占位符 {num} {den} {num2} {den2} {w} {g},双腿相乘、rank blend 随便写)。")
    print("   根据本轮命中数据修剪低产方向、扩展高产方向;不想调参就一键最全网:")
    print("   python scripts/mine.py --preset full")


if __name__ == "__main__":
    main()
