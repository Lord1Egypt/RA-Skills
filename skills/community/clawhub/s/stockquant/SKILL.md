---
name: stockquant
description: "A股量化一站式：选股 + 持仓策略 + 个股分析（代码/名称查询，返回行情+日K+15分钟K+资金面+板块+公告）。Python 出数据+hint，LLM 按 [TASK] 推导决策。"
---

# Stockquant Skill

A 股一站式：**选股 / 持仓策略 / 个股分析**。Python 只出**数据 + 对象化 hint 矩阵**，LLM 按 `[TASK]` 过程化推导决策。

> ⛔ **严禁 read_file 本脚本源码 / README**（6000+ 行，浪费 context）；下面子命令复制即可。
> ⏱️ **所有 stockquant 命令必须带 `timeout_sec=300`**（全流程含网络重试约 60~200s，默认 60s 会超时）。若引擎检测到你漏填仍会自动钳到 300s，建议显式写明。

## 六大策略引擎

| 引擎 | 思路 | 适用场景 | 默认启用 |
|---|---|---|:---:|
| **C 板块滞涨股** | 近 5 日板块涨幅 Top5 × 板块内涨幅后 40% 的滞涨股 | 板块轮动第二波补涨 | ✅ |
| **D 主力资金累积** ⚠️ | 5 日累计主力净流入>0 + 均线多头 + 健康换手 | （**反指信号 / 过拟合后期形态**，默认关闭） | ❌ |
| **E 60 日箱体突破** | 60 日窄箱（<25%）+ 放量突破箱体上沿 | 长期横盘后大级别启动 | 可选 |
| **F1 缩量横盘+首日突破** | 10 日盘整±3% + 今日量比 1.2~2.5、涨 1~4%、站上 MA20 | 捕捉启动 Day-1（避开追涨） | ✅ |
| **F2 主力悄悄吸筹** | 5 日资金累积净流入 ≥ 0.3% 流通市值 + 5d 横盘 + **不**满足均线多头 | 主力吸筹中期（D 的前置状态） | ✅ |
| **F3 板块异动初动** | 板块今日涨幅 Top5 且**过去 5 日**不在 Top10 + 选板块内未启动成员 | 板块轮动 Day-1（避开 Day-3 追涨） | ✅ |

> ⚠️ **D 为何被默认关闭**：历史回测 + 实盘复盘发现 D 的"经典信号"（资金+均线+换手共振）实际是**主力派发末期**的形态，往往出现在行情顶部。F2 是 D 的前置形态（主力吸筹中期），更有 alpha。用户可用 `--strategy C,D,E` 显式启用 D。

## 置信度 + 证据卡 + 魔鬼代言人

每个最终候选自动附带：

- **pattern_labels**：命中的 8 个经典形态标签（`breakout_initial`/`silent_accumulation`/`sector_initial_move`/`bottom_first_rally`/`gravestone_after_run`/`low_vol_consolidation`/`distribution_top`/`overheated_chase`）
- **evidence_card**：`bullish` / `bearish` / `uncertain` 三列中文信号（**禁止只读一边**）
- **confidence_label**：`HIGH`（≥2 策略共振）/ `MED`（单策略 + 多看多）/ `LOW`（看空≥看多）/ `CONFLICTED`（F1+F2 互斥）
- **must_verify_before_buy**：买入前必验项（含分时量价、大单监控、策略特定检查）
- **devil_advocate_questions**：自我挑战题，必须逐条回答后再下决定

**LLM 决策铁律**：
1. `CONFLICTED` 直接放弃
2. `LOW` 默认不入场
3. `MED` 需 `bullish ≥ 2 * bearish` 才考虑
4. `HIGH` 也要完成 `must_verify_before_buy` 才建仓

## 子命令

### 1. 选股（PICK_BUY）

```sh
python ${SKILL_DIR}/stockquant/scripts/stockquant.py recommend --capital <元> --market all --top 8
```

默认同跑 **C / F1 / F2 / F3**（不含 D、E）。读输出 `═══ ## NEXT_STEP ═══`：`[STATE] / [DATA] / [TASK]`，按 `[TASK]` S1~S6 执行。状态位 `should_terminate` / `session_not_for_entry` 命中即 terminate，不入场。**重点读 `## 证据卡 / 形态 / 置信度` 章节**，不要只看 Top-N 表。

> 🚫 **禁止跳过 S1~S6 直接 terminate**：脚本输出 `[TASK_TLDR]` 段写明"第一个 action 不得是 terminate/show_output，必须先输出 S1 硬约束矩阵"。`[TASK]` S 段较长会被截断，TLDR 短而硬，必须遵守。
> ⚠️ **数据降级闸**：若 NEXT_STEP 里出现 `S-1.【数据降级告知】`，第一个 action 必须是 `ask_user`，不得静默进入 S0。

参数速查：`--capital`(默认 10000)  `--market`(main/all/gem/star/sh/sz，默认 all)  `--top`(默认 **8**，刻意偏小让 LLM 有足够注意力逐一验证)  `--strategy`(C,D,E,F1,F2,F3 任意子集；默认 `C,F1,F2,F3`)。其他阈值已固化。

> **策略原理 / 三引擎流程图 / 统一打分公式** 见 `README.md` §选股（PICK_BUY）。

### 2. 持仓策略（SELL）

```sh
python ${SKILL_DIR}/stockquant/scripts/stockquant.py sell-plan \
  <code>:<qty>/<avail>@<cost> [...]
# 例：sell-plan 000949:1200/800@7.97 002324:500/500@17.11
```

参数：`qty`=总持仓 / `avail`=T+1 可卖 / `cost`=成本价（全部必填）；`--target-yuan`(默认 10000，单笔目标总价 ≈1万元控手续费占比)。

读输出 `═══ SELL_PLAN Phase 1/2 ═══`：`[REGIME_CLASSIFY]` 表已给每只**默认建议 --order**，按 `=== NEXT_STEP ===` 提示走即可（默认拷贝 → 必要时按 S2/S3 微调或 override → 调 Phase 2 验证）。

> **策略原理 / 11 档 regime 流程图 / 震荡对冲 / 止损定价逻辑** 见 `README.md` §持仓策略（SELL）。

### 3. 个股分析（ANALYZE）—— 用户主动查询

```sh
python ${SKILL_DIR}/stockquant/scripts/stockquant.py analyze <query> [<query>...]
# 例：analyze 600519 茅台 比亚迪 002594
```

查询词：6 位代码 / 中文名（完整或简称，`茅台` → `贵州茅台`）。一次可传多只，同码自动 dedup，未匹配名回显在末尾不阻断。**LLM 不要传任何 flag**，参数已固化。

输出：大盘背景 + 每只个股的多维原始数据（基本/行情/日K/15分K/资金/板块/公告），末尾一段 `═══ ANALYSIS_HINT ═══` 给出解读框架。LLM 照着 hint 结合用户 prompt 分析即可；Python 不给买卖结论。

> **数据维度 / 解读框架 / 常见用户意图回答套路** 见 `README.md` §个股分析（ANALYZE）。

### 4. Tushare Token 管理（按需调用，见 HINT 指令）

```sh
python ${SKILL_DIR}/stockquant/scripts/stockquant.py tushare-token --set <TOKEN>
python ${SKILL_DIR}/stockquant/scripts/stockquant.py tushare-token --skip
python ${SKILL_DIR}/stockquant/scripts/stockquant.py tushare-token --status
python ${SKILL_DIR}/stockquant/scripts/stockquant.py tushare-token --clear
```
