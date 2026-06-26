# Stockquant — A 股交易一站式 Skill

> **A 股短线波段（T+1 隔日 / 1~3 天持仓）+ 持仓 T+0 对冲 + 个股深度分析的一站式工具**。Python 负责数据采集 / 过滤 / 打分 / 规则判决 / 对象化 hint 矩阵；LLM 只读末尾 `═══ ## NEXT_STEP ═══` 区块（`[STATE] / [DATA] / [TASK]`），按模板推导决策。

**入口契约 / 默认命令 / CLI 参数见 `SKILL.md`**（38 行入口卡片）。

本 README 聚焦**策略原理 + 文本流程图 + 实现细节**，供维护者与想理解策略逻辑的进阶用户阅读。

---

## 功能总览

| 子命令 | 用途 | 入口 |
|---|---|---|
| **PICK_BUY 选股** | T+1 短线候选 + 仓位 + 风控建议 | `stockquant.py --capital X --market main` |
| **SELL 持仓策略** | 当前持仓的 sell/buy/NO_OP 决策（11 档 regime + T+0 对冲） | `stockquant.py sell-plan code:qty/avail@cost ...` |
| **ANALYZE 个股分析** | 多维原始数据 + 解读框架（用户问"X 怎么样"时使用）| `stockquant.py analyze 600519 茅台 ...` |

三个功能**共享同一套数据源 + 缓存 + 容错层**（详见 §共用基础设施），策略逻辑各自独立。

---

## 设计哲学：Progressive Disclosure

> Python 扛所有确定性工作，LLM 只看**动态生成的 focused 指令**，attention 不被无关信息稀释。

```
┌────── Python 内部（LLM 不读源码 / README）──────┐
│ 数据采集 → 规则过滤 → 打分 → 仓位 → 标签        │
└────────────────────┬────────────────────────────┘
                     ▼ LLM 只看 ~2 KB
┌─── ═══ ## NEXT_STEP ═══（三段式 focused）──────┐
│  [STATE]  时段 / 数据质量 / should_terminate    │
│  [DATA]   表 / 矩阵 / 软区间 (含 🟢🟡🔴 标签)   │
│  [TASK]   S1~Sn 过程化决策框架                   │
└─────────────────────────────────────────────────┘
```

数据降级 / 候选 0 处置 / 数据质量门禁 / 失败案例教训 → 全部由 Python **运行时**渐进披露在对应输出段，**不在 SKILL.md / README 里堆**。

---

# § 1. 选股（PICK_BUY）

## 1.1 文本流程图

```
全市场 5000+ 只
       ▼
┌────────── 引擎 C 板块滞涨股 ──────────────────────────┐
│ Step1: 板块榜按近 5 日涨幅排序，取 Top5 热板          │
│ Step2: 拉每个板块成分股 + 个股 N 日涨幅                │
│ Step3: 板块内涨幅后 40% 的滞涨股 → C 候选              │
└──────────────────────────────────────────────────────┘
┌────────── 引擎 D 主力资金累积 ────────────────────────┐
│ Step1: 全市场翻页拉多日资金流（5d / 10d 累计）         │
│ Step2: 5 日累计净流入 > 0 + 收盘 ≥ MA20 ≥ MA40 ≥ MA60  │
│ Step3: 健康换手 (2~10%) + 量比 + 行业过滤 → D 候选     │
└──────────────────────────────────────────────────────┘
┌────────── 引擎 E 60 日箱体突破 ───────────────────────┐
│ Step1: 全市场（默认随机 sample=500，防 WAF）           │
│ Step2: 60 日 K 线 → 箱体振幅 < 25% (窄箱)              │
│ Step3: 现价位于箱体 80% 上方 + 放量突破 → E 候选       │
└──────────────────────────────────────────────────────┘
       ▼ 三引擎合池
┌── _unified_score 6 维 + 市场延迟 + 策略 bonus ────────┐
│ 资金面 25 + 量价 20 + 位置 15 + 板块 15 + 市值 10 + 换手 10 = 100 │
│ + market_delta (-10 ~ +5)  + strategy_bonus            │
└──────────────────────────────────────────────────────┘
       ▼ 排序 + sector dedup（同行业最多 2 只）
┌── _apply_llm_hints 4 类标签 ──────────────────────────┐
│ 🔴 reject_reasons    → 移出 PASS, 入 REJECT_LIST        │
│ 🟡 soft_warnings     → 保留, LLM S2.5 必须 elaborate    │
│ 🟢 boost_reasons     → 重排序加分                       │
│    next_day_prob     → high / mid / low 档              │
└──────────────────────────────────────────────────────┘
       ▼ 仓位计算 _build_allocation_plan
┌──────────────────────────────────────────────────────┐
│ 固定 10000 元/只 → round_lot 100 整倍 → 累计 ≤ capital │
│ 单手 > 半仓自动跳过下一只                              │
│ 输出 📎PICKED:000001|000002|... 强制签名行              │
└──────────────────────────────────────────────────────┘
       ▼
[STATE] + [DATA] PASS_TOP10 + [TASK] S1~S6 → LLM 决策
```

## 1.2 六引擎设计（2026-05 重构）

旧策略 **A（涨停分歧低吸）/ B（跌停反弹）** 实盘验证为低期望值博傻链，已下线。当前 **六引擎独立 screen → 合池 → 统一打分 → sector dedup → 仓位计算**。

| 引擎 | 默认 | 思路 | 关键信号 | 期望盈亏特征 |
|---|:---:|---|---|---|
| **C 板块滞涨股** | ✅ | 热板内涨幅排后 40% 的"跟随者" | `laggard_gap` | **胜率高、收益小**；赌板块热度溢出补涨 |
| **D 主力资金累积** ⚠️ | ❌ | 多日资金流入+均线多头（**实盘复盘为派发末期形态，默认关闭**） | `main_inflow_5d / ma_aligned` | 假信号集中在顶部；建议改用 F2 |
| **E 60 日箱体突破** | 可选 | 长期窄箱+放量突破上沿 | `box_range_pct / box_position_pct` | **大级别启动**；赌横盘后大波 |
| **F1 缩量横盘+首日突破** | ✅ | 10日盘整±3%，今日量比1.2~2.5、涨1~4%、站上MA20 | `pct_10d / volume_ratio / ma20` | 捕捉 Day-1；避开 Day-3 追涨 |
| **F2 主力悄悄吸筹** | ✅ | 5d资金累积≥0.3%流通市值+价格**未**启动（不满足均线多头） | `main_inflow_ratio_pct / pct_5d` | D 的前置状态；T-3~T-5 建仓区 |
| **F3 板块异动初动** | ✅ | 板块今日Top5且过去5d不在Top10 → 选板块内未启动成员 | `sector_pct_today / sector_pct_5d / pct_5d` | 板块轮动 Day-1；避开 Day-3 追 |

**容错**：任一引擎失败（API 异常 / 限流 / 无候选）**不影响其他引擎**（顶层 try/except 各自兜住），降级到剩余引擎继续。

## 1.3 统一打分 `_unified_score`（0~100）

| 维度 | 权重 | 取值逻辑 |
|---|---:|---|
| 资金面 | 0~25 | 今日 `main_inflow` + `main_inflow_5d` 趋势 |
| 量价健康 | 0~20 | `volume_ratio` 1.0~2.5 健康，>4 巨量反扣分 |
| 位置 | 0~15 | `distance_from_ma20` 绝对值越小越好；越过 12% **直接 reject** |
| 板块热度 | 0~15 | `industry` 是否在当日 Top5 热板 |
| 流通市值 | 0~10 | 20~200 亿为健康区间 |
| 换手率 | 0~10 | `turnover` 2~10% 为健康区间 |

**市场延迟** `_market_context_delta`：根据 `sh_pct / gem_pct` 全局调分（大盘强势 +3 / 弱势 -6 / 重挫 -10）。

**策略特化 bonus**（小范围加分）：
- **C**：`laggard_gap` 越大 +bonus；板块 Top3 +3
- **D**：`main_inflow_pct_5d` 高 +bonus；多头排列 +5（D 默认关闭）
- **E**：`box_range_pct` 越窄 +bonus；`volume_ratio > 2` +5
- **F1/F2/F3**：策略命中即附带独立 bonus；同一只股命中 ≥2 策略时置信度升为 `HIGH`

最终 `score = clip(main_6dim + market_delta + strategy_bonus, 0, 100)`。

## 1.4 LLM Hints（4 类标签）

| 类别 | 含义 | 触发例 |
|---|---|---|
| `reject_reasons` 🔴 | 硬剔除（移 PASS → REJECT_LIST）| `over_extended` (`distance_from_ma20 > 12`) / `volume_panic` (`volume_ratio > 5`) |
| `soft_warnings` 🟡 | 软提示（保留但 LLM 二次复核）| `bad_news:计提资产减值`（公告利空命中）|
| `boost_reasons` 🟢 | 加分项（重排序，不影响 pass）| `strong_money_accum` (D 强多日流入)、`tight_box` (E 窄箱)|
| `next_day_prob` | 次日触及止盈档位 | `high / mid / low` |

**分离不变量**：reject 代号永远不进 `soft_warnings`；soft 代号永远不进 `reject_reasons`（防止语义漂移）。

LLM 在 `[TASK]` S2.5 风险复核必须**逐票**对 PASS_TOP10 输出风险表，🔴 直接 HIGH 不进 Top5；🟡 必须 elaborate 风险；只有 🟢 (boost≥2 + prob=high + 无 warn) 才能直接进 Top5。

## 1.5 证据卡 + 形态 + 置信度（2026-05 新增）

每个最终候选打印在 `## 证据卡 / 形态 / 置信度 (每只必读)` 章节：

| 字段 | 说明 |
|---|---|
| `pattern_labels` | 8 种形态标签：`breakout_initial` / `silent_accumulation` / `sector_initial_move` / `bottom_first_rally` / `gravestone_after_run` / `low_vol_consolidation` / `distribution_top` / `overheated_chase` |
| `evidence_card` | `bullish` / `bearish` / `uncertain` 三列中文信号，**禁止只读看多一边** |
| `confidence_label` | `HIGH`（≥2策略共振）/ `MED`（单策略+多看多）/ `LOW`（看空≥看多）/ `CONFLICTED`（F1+F2互斥） |
| `must_verify_before_buy` | 买入前必验项（分时量价背离、大单监控 + 策略特定检查） |
| `devil_advocate_questions` | 自我挑战题，逐条回答后再决定 |

**LLM 决策铁律**：`CONFLICTED` 放弃 → `LOW` 不入场 → `MED` 需 bullish ≥ 2×bearish → `HIGH` 完成 must_verify 才建仓。

---

# § 2. 持仓策略（SELL）

## 2.1 文本流程图（11 档 regime 第一命中）

```
                    ┌── 时段闸门 ──┐
持仓输入 ┐          │ 非交易时段?    │ → MARKET_CLOSED → NO_OP（盘外不操作）
 - qty   │          │ 14:55+尾盘?    │ → CLOSE_RUSH    → 现价/bid1 全卖（赶尾盘流动性）
 - avail │          ├── 风险闸门 ──┤
 - cost  │          │ 浮亏 ≤ -4%?    │ → DEEP_LOSS     → bid1 全卖（止损）
         │          │ 14:30+ 浮亏<-1%│ → TAIL_EXIT     → 现价 全卖（尾盘止损）
现价 ────┤ → 分类 → ├── 趋势闸门 ──┤
振幅/ATR │          │ 浮盈≥5% & MA↑ │ → TREND_UP      → 高位 +2~+5% 双档减半
量比     │          │ 浮盈≥2% & MA↑ │ → HIGH_BAND     → 高位 +1~+3% 单档减1/3
主力流入 │          │ MA↓ + 量比≥1.5│ → TREND_DOWN    → bid1 全卖（破位止损）
MA趋势   │          ├── 震荡闸门 ──┤
         │          │ ATR≥1.5 振幅≥5│ → OSC_LARGE     → ±(1~2)% 双边对冲
         │          │ ATR≥0.8 振幅≥2│ → OSC_SMALL     → ±(0.3~0.5)% 单档对冲
         │          │ ATR<0.5?       │ → FLAT_DEAD     → NO_OP（死水不动）
         │          ├── 抄底闸门 ──┤
         │          │ 浮亏-3~0%, MA↑│ → LOW_DIP       → -1~-2% 单档加仓
         └─→        └── catch-all ─→ HOLD            → NO_OP
```

**第一命中**：从上往下扫，命中即停（时段闸最优先，catch-all 最后）。这保证 14:55 尾盘的票一定走 `CLOSE_RUSH`，浮亏 -5% 的票一定走 `DEEP_LOSS`，不会被后面的震荡闸劫持。

## 2.2 11 档 regime 触发条件

| Regime | 触发条件（`profit_pct = (price-cost)/cost*100`） | 默认动作 | 设计意图 |
|---|---|---|---|
| `MARKET_CLOSED` | now < 09:30 / now > 15:00 / 非交易日 | NO_OP | 盘外不操作 |
| `CLOSE_RUSH` | 14:55 ≤ now < 15:00 | 现价/bid1 全卖 | 赶尾盘流动性，免隔夜 |
| `DEEP_LOSS` | profit_pct ≤ -4% | bid1 全卖 | 重亏止损，不在乎价位 |
| `TAIL_EXIT` | now ≥ 14:30 且 profit_pct < -1% | 现价 全卖 | 尾盘小亏出清，不留过夜 |
| `TREND_UP` | profit ≥ 5% & ma5 up | +2~+5% 双档减半 | 高位浮盈大，分两档兑现 |
| `HIGH_BAND` | profit ≥ 2% & ma5 up | +1~+3% 单档减 1/3 | 浮盈中等，少量兑现保留主仓 |
| `TREND_DOWN` | ma5 down & vol_ratio ≥ 1.5 | bid1 全卖 | 破位+放量，止损 |
| `OSC_LARGE` | ATR ≥ 1.5% & 振幅 ≥ 5% | ±(1~2)% 双边对冲 | 大幅震荡，T+0 反复做差 |
| `OSC_SMALL` | ATR ≥ 0.8% & 振幅 ≥ 2% | ±(0.3~0.5)% 单档对冲 | 小幅震荡，紧密价差 |
| `FLAT_DEAD` | ATR < 0.5% & 振幅 < 1.5% | NO_OP | 死水不动，做差也赚不到手续费 |
| `LOW_DIP` | profit -3~0% & ma5 up & inflow ≥ 0 | -1~-2% 单档加仓 | 强势趋势中浅跌，加仓抄底 |
| `HOLD` | catch-all | NO_OP | 不在任何明确档，保守不动 |

## 2.3 关键定价逻辑

### 止损类（`DEEP_LOSS / TAIL_EXIT / TREND_DOWN / CLOSE_RUSH`）

直接挂 `bid1`（现价 × 0.995）或 `current` 保成交，**不在乎价位**，只求当天出清。`bid1` 比对手价低 0.5%，几乎瞬时成交；不挂跌停板是为了避开尾盘瞬时跌停撤单的风险。

### 趋势减仓类（`TREND_UP / HIGH_BAND`）

高位浮挂卖单等更好价。Python 给 `upper_pct_range`（如 `(2.0, 5.0)`）软区间，LLM 二次微调：

- **强势**（主力净流入 > 0 & 量比 ≥ 1.5）→ 偏区间 hi 端（+5%）等延续
- **弱势**（流入<0 或 量比<1）→ 偏 lo 端（+2%）早成交

不直接给固定值是因为同一档 regime 下，"强趋势" vs "震荡末端" 的合理报价能差 2~3%。

### 震荡对冲类（`OSC_LARGE / OSC_SMALL`） — T+0 核心

在现价**上下对称**挂卖+买单赚价差，**买入 qty 默认 = 卖出 qty**（持仓中性，不改变仓位规模）：

```
                持仓  N 股
                  │
    ┌─────────────┼─────────────┐
    ▼ 卖出 K 股                  ▼ 买入 K 股
sell @ +1.5%  ── 收回 P*K*1.015 ─┐
                                │ 一卖一买，差价 ≈ 3%
                                │ 覆盖手续费 ~0.8% 后净赚 ~2.2%/轮
                                │ 持仓数量 N 不变
buy  @ -1.5%  ── 支出 P*K*0.985 ─┘
```

**为什么 sell_qty = buy_qty？** 保持净持仓不变 = T+0 性质：今天买的明天才能卖，所以**今天的卖单只能用昨天的 avail（T+1 可卖）**，今天的买单不影响今天的 avail（明天才能卖）。一卖一买配对后，明天 avail 变化 = -K + 0 = -K（少了今天卖出的部分），但仓位规模不变。

**Python 强制差价校验**：`min(sell_pct) - max(buy_pct) ≥ fee_floor_pct`（默认 0.8%）。

```
合规: sell @ +1.5%, buy @ -1.5% → 差价 3% ≥ 0.8% ✅
违规: sell @ +0.3%, buy @ -0.3% → 差价 0.6% < 0.8% ❌ exit 2
```

差价小于 0.8% 的对冲单会被拒绝，因为成交后扣完手续费净亏，不如不做。

### 抄底加仓类（`LOW_DIP`）

浅跌（profit -3 ~ 0%）且趋势未破（ma5 up + inflow ≥ 0）时，单边买入等反弹。Python 给 `lower_pct_range = (-2, -1)`，LLM 在区间内挑具体 pct。

### NO_OP 类（`HOLD / FLAT_DEAD / MARKET_CLOSED`）

本回合不动；下次轮询时重判。`HOLD` 是 catch-all 兜底，避免无规则 regime 误下单。

## 2.4 两阶段流水

```
┌─── Phase 1（Python 出建议）─────────────────────────────┐
│ python sell-plan 000949:1200/800@7.97 002324:500/500@17.11 │
│       ▼                                                  │
│ Python:                                                  │
│   1. 批量拉行情 + 日 K → 算 ATR / 振幅 / MA / 量比       │
│   2. _classify_regime 11 档第一命中 → 每只一个 regime   │
│   3. _suggest_orders 默认建议 (qty = round_lot(target/price)) │
│   4. 输出 6 段:                                          │
│      [STATE] [HOLDINGS_DATA] [REGIME_CLASSIFY (含默认 --order)] │
│      [REGIME_RULES] [CADENCE_HINT] [TASK]               │
└──────────────────────────────────────────────────────────┘
       ▼
LLM 默认拷贝 [REGIME_CLASSIFY] 表中"默认建议 --order"列
（特殊情况按 S2/S3 微调 pct/qty 或 override 到防御档）
       ▼
┌─── Phase 2（Python 验证 + 出 ORDER）───────────────────┐
│ python sell-plan <同样持仓 tokens> \                    │
│   --order 000949:sell:100@+1.5 \                        │
│   --order 000949:buy:100@-1.5 \                         │
│   --order 002324:sell:500@bid1 \                        │
│   --override 002324=DEEP_LOSS:K线跌破年线               │
│       ▼                                                  │
│ Python 强制 6 关校验:                                    │
│   ① T+1 锁: sum_sell ≤ avail                            │
│   ② 100 整数倍: qty % 100 == 0                          │
│   ③ pct 在 regime 软区间内                              │
│   ④ sell_frac ≤ regime cap (如 OSC_LARGE 0.5)           │
│   ⑤ buy_frac ≤ regime cap                               │
│   ⑥ 双边差价 ≥ fee_floor_pct (默认 0.8%)                │
│       ▼ 通过                                             │
│ 输出:                                                    │
│   [ACTION_PLAN] 中文自然语言:                            │
│     "卖出 100 股 @ 10.15 元 (现价+1.5%, 单笔 1015 元)"    │
│   --- 机器签名 ---                                       │
│   📍ORDER:000949:SELL:100@10.15                         │
│   📍ORDER:000949:BUY:100@9.85                           │
│   📍ORDER:002324:SELL:500@10.18                         │
│   📍ORDER_TOTAL:orders=3                                │
│       ▼ 失败 → ❌ 详情 + exit 2                          │
│ LLM 改 --order 重跑                                      │
└──────────────────────────────────────────────────────────┘
       ▼
顶层模块消费 📍ORDER 行下单（skill 不参与下单流程）
```

**为什么分两阶段？** Phase 1 让 LLM 看清每只持仓的 regime + 软区间，**默认采纳建议**就行；Phase 2 把 LLM 拼好的方案做硬验证，避免 LLM 拍脑袋绕过 T+1 / 100 整倍 / 差价 / regime 范围。Python 是最后一道关。

**override 白名单**：仅允许 LLM 把 regime 覆盖到**更保守档**（防御档：`HOLD / FLAT_DEAD / MARKET_CLOSED / DEEP_LOSS / TAIL_EXIT / TREND_DOWN / CLOSE_RUSH`），不允许激进化。理由：LLM 可能基于 K 线/资金面看出 Python 没看到的破位信号，应允许它"宁紧勿松"；但不允许它跳到 OSC_LARGE 多挂单博 T+0。

## 2.5 资金充足性由顶层保证

**skill 不验证 cash**。理由：

- skill 是模块化的，不应假设调用方账户余额
- 顶层 Agent / 钱包模块持有完整资金视图，能算"还能买多少"
- skill 给的是"建议下单 X 股 @ Y 元"，由顶层决定要不要、能不能下

`--target-yuan`（默认 10000）只控**单笔总价**，不是总资金限额。10 元/股 → 1000 股/笔；100 元/股 → 100 股/笔；目标是手续费占比 < 0.05%。

---

# § 3. 个股分析（ANALYZE）

## 3.1 文本流程图

```
查询: "600519" / "茅台" / "比亚迪" / "002594" ...
       ▼ search 模糊匹配 → 6 位代码
       ▼ 同码 dedup, 未匹配名末尾回显
       ▼ 6 维并行拉取（线程池）
┌──────────────────────────┬──────────────────────────┐
│ ① 基本面                  │ ② 实时行情                │
│   - 行业 / 概念            │   - 现价 / 涨跌 / 振幅    │
│   - 流通市值 / PE / PB     │   - 量比 / 换手 / 主力流入 │
├──────────────────────────┼──────────────────────────┤
│ ③ 日 K 序列 (默认 120 日)  │ ④ 15 分钟 K (默认 32 根)  │
│   - MA5/10/20/60 排列      │   - 60m_trend            │
│   - 60 日位置分位           │   - 15m_end_strength      │
│   - tape (放量/缩量) 形态  │   - 盘中突破/破位 标记     │
├──────────────────────────┼──────────────────────────┤
│ ⑤ 资金面                  │ ⑥ 板块 + 公告             │
│   - 今日/5日/10日累计      │   - 板块排名 + 共振       │
│   - 主力/大单/中小单分层   │   - 7日公告 + bad-news 扫描│
└──────────────────────────┴──────────────────────────┘
       ▼ 拼装多段 markdown
═══ ANALYSIS_HINT (LLM 解读指南) ═══
  [多维交叉原则] 趋势 × 节奏 × 驱动 三维联动验证
  [各数据块怎么看] 字段 → 意义映射
  [未来走势分析三步走] 定性 → 节奏 → 驱动
  [常见用户意图回答套路] "能不能买" / "怎么看" / "对比"
  [硬纪律] 禁止脑算 / 引用具体字段
       ▼
LLM 按 hint 框架结合用户 prompt 分析（不出买卖结论）
```

## 3.2 多维数据来源 + 拉取耗时

| 维度 | 接口 | 耗时 | 关键字段 |
|---|---|---:|---|
| 基本面 | EM clist + 单股详情 | ~0.3s | industry / pe / float_mv |
| 实时行情 | EM ulist (批量) → Sina fallback | ~0.5s | price / pct / vol_ratio / turnover / main_inflow |
| 日 K 序列 | EM kline | ~0.5s/股 | ma5/10/20/60 / 分位 / tape 形态 |
| 15 分钟 K | EM kline (period=15) | ~0.5s/股 | 60m_trend / 15m_end_strength |
| 资金面 | EM zjlx + 多日资金流榜 | ~0.5s | 5d/10d 累计 / 主力分层 |
| 板块 | EM bk_industry rank + 个股 industry | ~0.3s | 板块排名 / 板块涨幅 |
| 公告 | EM ann + 关键词 bad-news 扫描 | ~1s/股 | 7 日公告 / 7 日内 bad-news 命中 |

**单只全量分析** ~3-4 秒；**3 只并行** ~5-6 秒。`--no-news` 跳过公告 + bad-news 扫描可节省 ~1s/股。

## 3.3 解读框架（ANALYSIS_HINT，渐进披露）

ANALYZE **不出买卖结论**，只在输出末尾给 LLM 一段解读框架。三步分析：

1. **定性**（日 K 趋势）：MA 排列 + 60 日位置分位 + 经典形态 → 上涨 / 下跌 / 震荡
2. **节奏**（15min 级别）：当前在 启动 / 加速 / 顶背离 / 高位震荡 / 破位 哪一段
3. **驱动**（资金 + 板块 + 公告）：动能可持续性 + 风险事件

### 各数据块怎么读

| 数据块 | 关键阈值 / 形态 |
|---|---|
| 基本 | PE 极端值 (>80 或 <0) 是风险信号 |
| 行情 | 换手率 <1% 滞涨、2~5% 健康、>10% 过热；量比 >2 资金关注异常 |
| 日 K | MA 多头排列 (5>10>20>60) + 站上 MA20 = 强势；60 日位置 >80% 高位、<20% 低位 |
| 15m K | 放量突破 15min 前高 = 动能上；跌破 15min 低点 = 动能下；尾盘 14:30 后放量 = 次日延续 |
| 资金面 | 今日 + 5d + 10d 三档连续正 = 主力真建仓；只今日正 5d/10d 负 = 短线 |
| 板块 | 板块 Top10 + 个股跟涨 = 强势共振；板块强个股弱 = 掉队；板块弱个股强 = 龙头(风险集中)|
| 公告 | 问询函 / 减持 / 业绩预警 / 立案调查 → 直接 avoid |

## 3.4 常见用户意图回答套路

ANALYZE 的 hint 内嵌了套路，LLM 照抄即可：

| 用户问 | 回答结构 |
|---|---|
| **能不能买 X** | [支持多的证据] / [支持空的证据] / [中性] 三类证据分别列出；不给买卖硬结论让用户权衡 |
| **X 走势怎么看** | (1) 定性一句话；(2) 近 N 日关键行为(突破/回踩/放量)；(3) 支撑/阻力位 (MA20, 60日高/低, 密集成交区)；(4) 触发场景: 站稳 X 看 Y / 跌破 X 看 Z |
| **持有的能不能拿** | 趋势未破 + 公告无利空 + 资金未大流出 = 可持；任一破坏 = 减仓预警 |
| **对比 X 和 Y** | 逐维度打分(趋势/节奏/驱动/公告)对比表，突出差异项 |

### 硬纪律

- 禁止脑算均线 / 涨跌幅 / 分位，全部引用 Python 输出的具体数值
- 所有结论必须给依据（引用具体字段 + 数值），不做无依据的定性判断
- 用户没明说时间周期就默认"短中期 1-4 周"视角

---

# § 共用基础设施

## 数据源（东方财富免费接口为主）

| 端点 | 用途 | 稳定性 |
|---|---|---|
| `push2.eastmoney.com/api/qt/clist/get` | 全市场 clist / 板块榜 / 多日资金流 | ⚠️ 翻页多时偶发 WAF 软限流 |
| `push2.eastmoney.com/api/qt/ulist.np/get` | 批量行情（按代码集）| 稳定 |
| `push2.eastmoney.com/api/qt/stock/get` | 指数 quote | 稳定 |
| `push2his.eastmoney.com/api/qt/stock/kline/get` | 日 K / 15 分钟 K | 稳定 |
| `np-anotice-stock.eastmoney.com/api/security/ann` | 公告（bad-news 扫描）| 稳定 |

**备用**：`hq.sinajs.cn/list=` —— EM ulist 挂时自动降级，少 3 项（换手 / 量比 / 主力流向）。

## 容错层级（fail-soft）

1. **单只 K 线拉失败** → ThreadPool 内 try/except → 该股 `drops["no_kline"]` 跳过，**batch 不中断**
2. **单个策略崩溃**（C/D/E 任一）→ `recommend` 顶层 try/except 各自兜住 → `pool_x = []` + `meta["warnings"]` 追加 → 其他两引擎照常
3. **全部策略空候选** → "0 候选 terminate success" 分支，打印漏斗诊断（每层过滤了多少）
4. **EM clist 整挂** → 降级 Sina，`meta["data_source"] = "sina_fallback"`，打分质量降低但不阻塞
5. **盘中实时全失败** → 严格模式禁用 stale cache 回退 → `[STATE]` 打 `🛑 critical_intraday_stale_denied` + `should_terminate=true`，**禁止用昨日 cache 替代今日 T+1 决策**

## HTTP 重试 + 缓存

- **关键请求** (`_get_json`)：3 次重试，退避 0.8s / 1.6s / 3.2s
- **非关键** (`_get_json_fast_fail`)：1 次快速重试 0.3s，失败立即空返
- **缓存 TTL**：池子/行情 5 min、大盘 3 min、板块 rank 5 min、K 线 5 min、公告 1 h、板块成分股 24 h
- **自动 GC**：每次 CLI 启动扫 `cache/YYYYMMDD/`，删 7 天前目录；磁盘稳定 ~20 MB

## 请求数 & 性能（`brief` 一次完整调用）

| 阶段 | 请求数 | 说明 |
|---|---:|---|
| 大盘 + 板块榜 | ~5 | 稳定 |
| 策略 C（Top5 板块 × 成分股 × K 线）| ~300~400 | 中等压力 |
| 策略 D（多日资金流翻页）| ~15~20 | 低 |
| 策略 E（全市场 K 线，默认 sample=500）| ~500 | **最大压力** |
| bad-news 扫描（final picks）| ~30 | 低 |
| **合计** | **~900~1000** | 单次 ~3~8 秒 |

如果对限流敏感，走 `--strategy C,D` 跳过 E 降到 ~350 次。

## CLI 入口（含工程调试）

### LLM 默认入口（自动转 `brief`）

```sh
python stockquant.py --capital 10000 --market main --top 30
```

首个 token 不是已知子命令时，`_cli_main` 自动前插 `brief`。

### 工程调试子命令

| 子命令 | 用途 |
|---|---|
| `market` | 指数大盘快照 |
| `sector-rank --type industry/concept --top N` | 板块涨幅榜 |
| `screen-c` / `screen-d` / `screen-e` | 单策略筛选（不打分，debug 用）|
| `recommend` | 完整筛 + 打分 + 仓位（`brief` 的核心段）|
| `brief` | 聚合三段 + NEXT_STEP（**LLM 主入口**）|
| `eval [--date]` | 评估历史推荐（次日 OHLC 对比止盈/止损）|
| `stats [--days 30]` | 聚合 N 日胜率 / 盈亏比 |
| `intraday-track [--date]` | 当日已推荐 vs 实时行情中途检查 |
| `quote <code...>` | 实时现价（JSON 输出）|
| `kline <code> [--period day/week/month] [--count N]` | K 线原始数据 |
| `search <关键词>` | 按中文名 / 拼音搜索代码 |
| `allocate --codes ... --capital N` | 2nd-pass 仓位表（LLM 重排后调）|
| `sell-plan <code:qty/avail@cost> ...` | 持仓策略（**SELL 主入口**）|
| `analyze <query> ...` | 个股分析（**ANALYZE 主入口**）|

**设计意图**：LLM 走 `brief` / `sell-plan` / `analyze` 三个主入口；其他子命令给维护者调试 / 回测 / 排错用。

## 每日日志（3 路落盘，回测 + 事后分析）

每次 `recommend` / `brief` 调用（非交易日跳过）同步写 3 个 JSONL：

| 文件 | 每行内容 | 用途 |
|---|---|---|
| `logs/recommend/YYYYMMDD.jsonl` | 每只 final pick（~45 列）| `evaluate_recommendations` T+1 胜率 |
| `logs/candidates/YYYYMMDD.jsonl` | Top-50 打分候选（含 `is_final_pick`）| "为什么漏了涨停股" 回测 |
| `logs/market/YYYYMMDD.jsonl` | session snapshot (market_ctx / funnel / sector / warnings) | 关联市场状态分层评估 |

**磁盘占用**：3 路合计 ~40 MB / 年。已加入 `.gitignore`。

---

# 常见问题（FAQ）

**Q: 今天候选 0 只？**
看输出顶部"选股漏斗"段：
- **热板 0 个** → 板块榜接口限流（非关键，丢热板 bonus）
- **C 0 只** → 无 5 日涨幅 Top5 板块 / 滞涨股被其他过滤砍光（看 `C_stage1_drops`）
- **D 0 只** → 5 日主力净流入>0 的股过少 / 被均线/换手过滤
- **E 0 只** → 全市场无符合 60 日箱体（`no_kline` 占比高 = 被限流）
- **NEXT_STEP `should_terminate=true`** → 整体不宜入场，LLM 直接 terminate success

**Q: 跑 E 被 ban 一半，部分数据还能用么？**
能。`get_daily_klines_batch` 每个 future 独立 try/except，拿到的数据**即便后续 ban 也保留**且缓存。E 策略遇空 kline 就 `drops["no_kline"] += 1; continue`，不中断。

**Q: 降级到 Sina 后质量掉多少？**
损失 3 维（`volume_ratio` / `turnover` / `main_inflow`），打分区分度下降但排序仍有效。日志 `meta["data_source"] = "sina_fallback"` 可事后过滤。

**Q: C 和 D 策略买点本质区别？**
- **C**：板块热度已确立后，找**板块内滞涨**跟随者 → T+1 赚溢出补涨
- **D**：主力**多日持续**流入，均线已多头 → T+1 赌趋势延续
- 前者赌轮动（短期），后者赌持续（中期）。C 胜率高但收益小，D 收益大但假信号多。

**Q: SELL 的 OSC 对冲为什么 sell_qty 必须 = buy_qty？**
保持净持仓不变 = T+0 的核心。卖出用昨天的 avail（T+1 可卖），买入今天不可卖（明天才能 sell）。一卖一买配对后明天 avail 恢复，仓位规模不变；只赚价差，不改变方向暴露。如果 sell_qty > buy_qty，本质就变成"减仓"了，应该走 TREND_UP / HIGH_BAND 不是 OSC。

**Q: SELL 为什么不接 `--cash`？**
skill 是模块化工具，不假设调用方账户余额。顶层 Agent 持有完整资金视图（持仓 + 可用 + 委托冻结），能算"还能买多少"。skill 给"建议下单 X 股 @ Y 元 (单笔总价 Z 元)"，由顶层决定要不要 / 能不能下。

**Q: ANALYZE 为什么不给买卖结论？**
ANALYZE 是用户主动查询路径（"X 怎么样"），不是自动决策路径（PICK_BUY/SELL）。给买卖结论会让用户产生"AI 推荐"的依赖错觉，不符合用户主导的设计原则。skill 只给 raw 数据 + 解读框架，让用户自己结合 prompt 形成判断。

**Q: 盘前 / 周末 / 节假日跑会怎样？**
- **盘前 (工作日 09:30 前)**：正常，数据为 T-1 日完整收盘快照
- **周末 / 节假日**：自动识别，用上一交易日收盘快照，输出 ⚠️ 警告，**跳过日志写入**（避免 eval 污染）
- **`session_not_for_entry`**：09:30~09:45 / 11:30 后 / 14:55 后 → `[STATE]` 标记不宜下单，LLM 直接 terminate success

**Q: 日志文件大么？**
3 路合计 ~40 MB/年，不清理也无压力。已 `.gitignore`。

---

# 免责声明

- 本 skill 为量化筛选 + 持仓策略工具，输出 **仅供参考**，不构成投资建议
- A 股市场风险复杂，任何策略都可能失败
- 用户须自行承担交易结果
- 建议初次使用小仓位验证，熟悉策略脾气后再加仓
