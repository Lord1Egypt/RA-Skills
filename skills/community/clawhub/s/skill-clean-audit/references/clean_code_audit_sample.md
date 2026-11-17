# Clean Code 审计样例 · aggregate.py → `main()`（合成示例）

> 审计对象：`demo-skill/scripts/aggregate.py` 的 `main()`（下方片段第 15–55 行，约 41 行）
> 判据：A. 理解成本 / B. 修改风险。红=出现即脏优先修，黄=有意的债(注释+可控)，绿=出现即干净。
> 注：本样例为**合成示例脚本**，不对应任何真实项目；片段行号从 1 起，审计证据可直接对照核对。

## 被审计片段（`demo-skill/scripts/aggregate.py`）

```python
 1 │ """Daily usage report aggregator.
 2 │ Builds the daily usage report and writes a summary JSON.
 3 │ """
 4 │ from config import *                      # 隐式导入：符号来源不明
 5 │ import sqlite3, requests
 6 │
 7 │ DB_PATH = "data/usage.db"                 # 模块级全局
 8 │ TZ = "Asia/Shanghai"
 9 │ _PRICING = {}                             # 模块级【可变】全局
10 │
11 │ """Daily usage report aggregator.
12 │ This module collects token usage and emits a per-source summary.
13 │ (legacy header kept for compatibility)"""   # 与顶部 docstring 重复/矛盾
14 │
15 │ def main(argv=None):
16 │     args = _parse_args(argv)
17 │     # T-12: fall back to empty db when missing
18 │     # F-3: skip pricing meta if unavailable
19 │     # T-18: reorder sources after incident review
20 │     rows = _fetch_rows(args.start, args.end, DB_PATH, gap_min=15)  # 魔法数 15
21 │     if not rows:
22 │         print("[WARN] no rows in range")   # 隐藏副作用（打印）
23 │         rows = []
24 │     if args.source == "claude":            # switch-on-type
25 │         try:
26 │             raw = _query(rows, "claude")
27 │         except (sqlite3.Error, OSError):    # 精确的 except
28 │             raw = []
29 │         sid_map = _build_sid_map(rows, "claude")
30 │         total = 0
31 │         for r in raw:                       # 与 codex 分支重复
32 │             total += r["tokens"]
33 │         usage = {"source": "claude", "total": total, "rows": len(raw)}
34 │         _write_outputs(usage, "claude")
35 │     elif args.source == "codex":           # 与 claude 分支几乎逐行相同
36 │         try:
37 │             raw = _query(rows, "codex")
38 │         except (sqlite3.Error, OSError):
39 │             raw = []
40 │         sid_map = _build_sid_map(rows, "codex")
41 │         total = 0
42 │         for r in raw:                       # 重复逻辑（DRY 违反）
43 │             total += r["tokens"]
44 │         usage = {"source": "codex", "total": total, "rows": len(raw)}
45 │         _write_outputs(usage, "codex")
46 │     summary = {
47 │         "generated_at": _now(TZ),
48 │         "period": f"{args.start}..{args.end}",
49 │         "source": usage["source"],
50 │         "total_tokens": usage["total"],
51 │         "row_count": usage["rows"],
52 │     }
53 │     _attach_pricing(summary, _PRICING)      # 修改模块级可变全局
54 │     print(f"report ready: {len(summary)}")  # main 名像查询却偷偷打印
55 │     return summary
```

## A. 理解成本

| # | 清单项 | 命中 | 证据（行） | 说明 |
|---|--------|------|-----------|------|
| A1 | 🔴 符号来源隐式（`import *`） | ✅ 红 | 4 + 调用点 7/8/9/20/46/53 | `DB_PATH`/`TZ`/`_PRICING`/`_now`/`_query`/`_fetch_rows` 等全从 `from config import *` 进来。看到调用无法判断定义在哪个文件，要全局搜。 |
| A2 | 🔴 同一说明多处重复且矛盾 | ✅ 红 | 1–3 vs 11–13 | 顶部 docstring 与第 11 行起的裸字符串字面量重复同一段；后者是死字符串（运行时丢弃），且"legacy header kept"暗示它已无意义却未删。 |
| A3 | 🔴 注释像 changelog（满屏工单号） | ✅ 红 | 17/18/19 | `T-12`/`F-3`/`T-18` 之类 issue-tracker 标签散落 main 体内。新读者要先在脑子里解码这套内部编号体系才懂"这段代码现在归谁管"。 |
| A4 | 🟡 长函数 >40 行但内聚难拆 | ✅ 黄 | 15–55（约 41 行） | 确实长。但"难拆"辩护弱：它本质是顺序编排（解析参数→按源采集→聚合→挂定价元信息→输出），可拆成 `parse_args`/`collect_by_source`/`build_summary`/`attach_pricing`/`write_output`。标黄=暂时可接受，但应排期拆。 |
| A5 | 🟡 魔法数字/字符串未命名 | ✅ 黄 | 20/24/35（`"claude"`/`"codex"`）、20（`gap_min=15`） | `"claude"`/`"codex"` 成本口径字符串出现 2 处；`gap_min=15` 在默认+调用共 2 处。命名常量（`SOURCE_CLAUDE` 等、`GAP_MIN_DEFAULT`）即可消除。 |
| A6 | 🟢 命名即文档 | ✅ 绿（多数） | `_parse_args`(16)/`_build_sid_map`(29)/`raw`(26)/`total`(30) | 多数局部变量名一眼知意图，这一项达标。 |
| A7 | 🟢 显式优于隐式 | ❌ 未达标 | 见 A1/B1 | 行为混入导入的模块级全局（`DB_PATH`/`TZ`/`_PRICING`…），前提与边界不清，故本项不算绿。 |

## B. 修改风险

| # | 清单项 | 命中 | 证据（行） | 说明 |
|---|--------|------|-----------|------|
| B1 | 🔴 模块级可变全局状态控行为 | ✅ 红 | 9 + 53 | main 读并修改 `import *` 灌入的模块全局 `_PRICING`（`_attach_pricing(summary, _PRICING)`）。这些在 import 时由 config 设定，非运行中改，风险比运行期变异低一档，但按清单定义仍属"依赖非局部状态"，标红。 |
| B2 | 🔴 重复逻辑（违反 DRY） | ✅ 红 | 24–34 vs 35–45 | `claude` 与 `codex` 两个分支结构几乎逐行相同（collect→建 sid_map→累加 tokens→写输出），仅适配器名与打印标签不同。约 20 行重复，改一处要同步两处。 |
| B3 | 🔴 裸 `except` 静默吞错 | ⬜ 未命中（好评） | 25–28/37–39 | 所有 `except` 均精确：`(sqlite3.Error, OSError)`(27)(38)。无裸 `except`。本项达标。 |
| B4 | 🟡 有意的 best-effort `except` | ✅ 黄 | 25–28/37–39（单源采集失败回退 `raw = []`） | 单源查询失败只回退空列表不中断整条管线。已有精确 except + 范围可控，属"暂时可接受的债"。 |
| B5 | 🟡 过早抽象出没人复用的接口 | ⬜ 未命中 | — | 拆 `_parse_args`/`_build_sid_map` 属 deliberate 重构，非过早抽象，本项不算。 |
| B6 | 🟢 行为只由入参决定 | ⚠️ 部分达标 | 解析自 `argv`(16) | CLI 工具必然读 argv，但混入导入全局（见 B1），非纯入参驱动，故仅部分达标，不记满绿。 |
| B7 | 🟢 测试覆盖 | ❓ 未核实 | — | 未在本次审计中确认测试存在，留空。 |

## 额外发现（不在清单内，但同属理解成本）

**第 24 行的 `if args.source == "claude": ... elif args.source == "codex":` 是 switch-on-type：**
每加一种数据源，就要在 main 里复制一整段分支（见 B2），且需同步改 2 处。等价 Uncle Bob 气味 **Rigidity/Fragility**——小改动（加源）被迫改多处。可抽成 `COLLECTORS = {"claude": collect_claude, "codex": collect_codex}` 注册表，新增源只改一处。

## 审计评分

- 🔴 红（必须修）：**5** —— A1 import* / A2 重复 docstring / A3 changelog 注释 / B1 全局状态 / B2 DRY 重复分支
- 🟡 黄（可控债）：**3** —— A4 长函数 / A5 魔法量 / B4 best-effort except
- 🟢 绿（已达标）：**1**（A6 命名）+ B3 裸 except 未命中（好评）
- 未核实/未命中：A7、B5、B6、B7

## 结论（按第一性原理）

`main()` 的"脏"集中在**理解成本**一侧：来源隐式（A1）、说明自相矛盾（A2）、注释退化成工单追踪器（A3）、函数过长（A4）。
**修改风险**一侧反而较克制——没有裸 except（B3 好评），重复只在 claude/codex 两分支（B2），全局依赖是 import-time 而非运行中变异（B1）。
优先级建议：先消 A1/A2/A3（几乎零行为风险，纯可读性），再排 B2 合并双分支、A4 拆函数；A5/B4 这类黄项可随改顺手处理。

> 本样例只读不改。若要落地修复，建议另开一轮，按上面优先级逐个 PR。
