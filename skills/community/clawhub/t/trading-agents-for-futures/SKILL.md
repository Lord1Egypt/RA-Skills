---
name: Trading_Agents_for_Futures
description: |
  期货六维分析数据引擎。两种运行模式：
  (1) 数据模式：python main.py -s RB → 结构化 JSON 指标 + data_gap_report（数据缺口报告 + AI 搜索指令）
  (2) 决策模式：python main.py -s RB --decision → 指标 + 数据来源追溯 + 多空辩论 + 风控 + CIO决策报告
  零 API Key，纯规则引擎。API 缺失时自动生成 search_actions，AI Agent 可按 fillability 回填 ai_fill 槽位。
agent_created: true
---

# Trading_Agents_for_Futures — 期货分析数据引擎

> **你是哪种用户？根据你的身份选择对应模式。**

| 如果你 | 用这个命令 | 你会得到 |
|--------|-----------|---------|
| **是 AI Agent**（Kimi/Claude/GPT-4 等），需要结构化数据自己分析判断 | `python main.py -s RB` | 纯指标 JSON（MA/MACD/RSI/Z-score/净持仓...），无方向判断 |
| **是人类交易者**，需要直接看"多空辩论报告 + 操作建议" | `python main.py -s RB --decision` | 指标数据 + 口语化多空辩论 + 裁判长裁决 + 仓位/止损建议 |

---

## 快速开始

```bash
# 默认：数据模式（给 AI Agent 用）
python main.py -s RB

# 决策模式：辩论 + 风控 + CIO 建议（给人类看）
python main.py -s RB --decision

# 批量分析多个品种
python main.py -s RB,CU,M

# 全市场扫描 38 个品种
python main.py -s ALL
```

执行后输出纯 JSON（字段含义见下文）。首次运行会自动下载约 1 年历史数据，耗时 5~10 分钟；后续秒级。

---

## 输出 JSON 结构

```json
{
  "symbol": "RB",
  "timestamp": "2026-05-14T15:43:59",
  "success": true,
  "analysis_details": {
    "technical_analysis": {
      "close": 3257.0,
      "MA5": 3266.8,
      "MA20": 3192.1,
      "MA60": 3131.7,
      "EMA20": 3207.3,
      "MACD": 37.8,
      "MACD_Signal": 30.8,
      "MACD_Hist": 7.0,
      "RSI14": 70.5,
      "BB_Upper": 3312.0,
      "BB_Middle": 3192.1,
      "BB_Lower": 3072.1,
      "ATR14": 30.2,
      "VOL_MA20": 685669,
      "OI_delta": -49216,
      "trend_20d": "up",
      "change_20d_pct": 5.1,
      "data_points": 245
    },
    "basis_analysis": {
      "spot_price": 3280.0,
      "futures_price": 3260.0,
      "current_basis": -20.0,
      "basis_pct": -0.6,
      "basis_zscore_180d": -0.8,
      "structure": "backwardation"
    },
    "term_structure_analysis": {
      "front_contract": "RB2605",
      "back_contract": "RB2704",
      "front_price": 3150,
      "back_price": 3307,
      "spread": 157,
      "spread_pct": 5.0,
      "structure": "contango"
    },
    "inventory_analysis": {
      "latest_inventory": 520000,
      "inv_change_wow": 0.7,
      "inv_change_mom": -2.3,
      "inv_zscore_180d": 1.6,
      "latest_warehouse_receipt": 82000,
      "wr_change_5d": 1500
    },
    "positioning_analysis": {
      "net_position": -3367,
      "net_change": -3466,
      "concentration_idx": 0.0068,
      "top20_long": 245143,
      "top20_short": 241185,
      "top20_long_pct": 0.5041,
      "top20_members_count": 20
    },
    "news_analysis": {
      "total_news_count": 10,
      "bullish_news_count": 1,
      "bearish_news_count": 0,
      "neutral_news_count": 9,
      "sentiment_ratio": 0.1
    }
  }
}
```

> **输出是纯指标字典，不含任何方向判断、置信度评分、辩论文本。**
> 每个 skill 的本地规则逻辑（`_rule_based_signal`）仍在内部运行但不对外暴露。

---

## 六大分析维度 & 方法论框架

**你是 AI 分析师，以下是你可以用来解读数据的完整方法论。**

---

### 一、技术面分析 (`technical_analysis`)

**数据指标：** close, MA5/MA20/MA60, EMA20, MACD/Signal/Hist, RSI14, BB_Upper/Middle/Lower, ATR14, VOL_MA20, OI_delta, trend_20d, change_20d_pct

**分析框架（你需要做的）：**

1. **均线系统判断：** 价格 > MA20 → 多头格局；价格 < MA20 → 空头格局。MA5 > MA20 > MA60 → 多头排列，趋势强势。MA5 < MA20 < MA60 → 空头排列。
2. **趋势强度评估：** MACD > Signal 且 Hist > 0 → 动能偏多；MACD < Signal 且 Hist < 0 → 动能偏空。change_20d_pct 反映近期趋势方向和幅度。
3. **超买超卖识别：** RSI > 70 → 超买，回调风险；RSI < 30 → 超卖，反弹可能。RSI > 80 视为极度超买/超卖。
4. **布林带位置：** 价格接近 BB_Upper → 高估/阻力；接近 BB_Lower → 低估/支撑。
5. **波动率评估：** ATR14 / close 的比值衡量波动率。>2% 为高波动，<1% 为低波动。
6. **量仓配合：** 价格涨 + 持仓增 → 多头主动；价格涨 + 持仓减 → 空头回补。偏离 5 万手以上视为显著变化。

---

### 二、基差分析 (`basis_analysis`)

**数据指标：** spot_price, futures_price, current_basis, basis_pct, latest_basis, basis_zscore_180d, basis_slope_20d, structure(contango/backwardation/flat)

**分析框架（你需要做的）：**

1. **基差率绝对判断：** basis_pct > 5% → 期货大幅升水(Contango)，现货供应充裕，偏空。basis_pct < -5% → 期货大幅贴水(Backwardation)，现货偏紧，偏多。±2% 以内视为合理区间。
2. **历史分位判断：** Z-score > 2 → 基差处于历史极高（期货升水极端），回归压力大。Z-score < -2 → 历史极低（现货升水极端）。
3. **基差趋势：** slope_20d > 0 → 基差走强（现货相对走强），偏多。slope_20d < 0 → 基差走弱（期货相对走强），偏空。
4. **期限结构与基差联动：** Backwardation + 基差 Z-score 低位 → 现货紧张信号加强。Contango + 基差 Z-score 高位 → 库存充裕信号加强。

---

### 三、期限结构分析 (`term_structure_analysis`)

**数据指标：** structure(contango/backwardation/flat), front_contract/back_contract, front_price/back_price, spread, spread_pct, carry_score, 各合约间价差(spread_xxx)

**分析框架（你需要做的）：**

1. **结构类型判断：** Contango（远月 > 近月）→ 库存充裕、持有成本定价、偏空；Backwardation（近月 > 远月）→ 现货紧张、便利收益 > 持有成本、偏多。
2. **展期收益：** Contango → 多头展期亏损（展期收益为负），空头有利；Backwardation → 多头展期获利（展期收益为正），多头有利。
3. **价差幅度解读：** spread_pct > 5% → 结构信号强烈。spread_pct < 2% → 结构信号弱，市场可能平坦。
4. **Full Carry 理论验证：** 实际价差 > 理论 Full Carry → 存在仓储利润空间，库存意愿强 → 偏空。实际价差 < Full Carry → 供给不足信号 → 偏多。
5. **跨合约价差异常：** 某两个合约间价差异常放大 → 可能存在结构性供需扭曲，需要结合品种特性判断。

---

### 四、库存仓单分析 (`inventory_analysis`)

**数据指标：** latest_inventory(吨), inv_change_wow(%), inv_change_mom(%), inv_zscore_180d, latest_warehouse_receipt(吨), wr_change_5d(吨)

**分析框架（你需要做的）：**

1. **历史分位（Z-score）是核心信号：** Z > 2.5 → 库存历史极高，供给严重过剩，强看空。Z > 1.5 → 偏高，偏空。Z < -2.5 → 库存历史极低，供给紧张，强看多。Z < -1.5 → 偏低，偏多。±0.5 附近 → 供需平衡。
2. **周度变化反映边际变化：** WoW > 15% → 短期供给激增，利空。WoW < -15% → 快速去库，利多。注意节假日和交割前后可能出现的异常值。
3. **月度变化反映趋势：** MoM > 20% → 月度累库趋势，偏空。MoM < -20% → 趋势性去库，偏多。
4. **仓单变化补充验证：** 仓单增加 + 库存增加 → 可交割品充裕，空头交货方便。仓单减少 + 库存低位 → 虚实盘比高，近月逼仓风险。
5. **库存周期理论：** 库存高位 + 价格低位 → 被动去库初期；库存低位 + 价格高位 → 被动累库初期。结合价格判断周期阶段。
6. **投机性库存 vs 真实消费：** 若库存增加伴随价格下跌 → 可能是被动累库（需求弱），信号更偏空。

---

### 五、持仓席位分析 (`positioning_analysis`)

**数据指标：** net_position(手), net_change(手), concentration_idx, top20_long(手), top20_short(手), top20_long_pct, top20_short_pct, data_points, key_players(可选的乾坤/摩根等外资席位标记)

**分析框架（你需要做的）：**

#### A. 蜘蛛网策略 —— 捕捉"聪明钱"动向

基于前 20 名会员持仓变动数据追踪机构资金意图：

1. **蜘蛛网信号判断（核心）：** 
   - 多头增仓 + 空头减仓（dB>0, dS<0）→ **强烈看多**，机构主动进攻
   - 多头减仓 + 空头增仓（dB<0, dS>0）→ **强烈看空**，机构撤离
   - 多空同向 → 需结合净变化量判断。净变化 > +5000 → 偏多；< -5000 → 偏空
2. **净持仓绝对值：** net > 10000 → 机构明显看涨。3000~10000 → 偏多。负值同理反向。
3. **净持仓变化量：** net_change > 8000 → 资金积极做多（强烈信号）。net_change < -8000 → 积极做空。±3000 以内正常波动。

#### B. 聪明钱分析

1. **前 20 会员多空比：** long_pct > 65% → 主力一致看多（注意拥挤风险）。< 35% → 主力一致看空。45%~55% → 多空均衡。
2. **持仓效率（OI/Volume）：** OI/Volume 高 → 机构深度参与，信号可信度↑。OI/Volume 低 → 散户主导，信号噪音多。
3. **关键玩家追踪：** 如果 key_players 字段出现了"乾坤""摩根""永安"等外资或顶级席位，这些席位的动向权重应额外加 0.2x（因为这些席位通常代表产业套保或宏观对冲资金，准确率更高）。

#### C. 持仓集中度分析（HHI指数）

1. **concentration_idx 解读：** > 0.3 → 高集中度，持仓集中在少数席位，方向性风险极大（一方拥挤随时可能反转）。< 0.1 → 高度分散，市场无单边共识。
2. **多空集中度差异：** 如果多头集中度 >> 空头集中度 → 多头拥挤在少数席位，一旦撤退将引发踩踏。空头集中度 >> 多头 → 轧空风险。
3. **集中度趋势：** 集中度连续上升 → 方向共识加强（同向信号）。集中度突然下降 → 主力分歧加大（反转预警）。

#### D. 散户反向策略

1. 如果前 20 会员极端偏多，但成交量萎缩 → 机构锁仓，散户追涨接盘 → **偏空信号**。
2. 如果前 20 会员极端偏空，但成交量萎缩 → 机构锁仓，散户恐慌抛售 → **偏多信号**。
3. 散户席位（成交量小但数量多的席位）动向与前 20 相反 → 反向指标确认。

#### E. 拥挤度风险策略
- 前 20 极度偏多（>70%）+ 价格在60日高位 → 多头拥挤，回调风险↑
- 前 20 极度偏空（<30%）+ 价格在60日低位 → 空头拥挤，轧空风险↑
- 拥挤度 > 0.3 + 持仓量创60日新高 → 极端拥挤信号，应降低仓位

---

### 六、新闻情绪分析 (`news_analysis`)

**数据指标：** total_news_count, bullish_news_count, bearish_news_count, neutral_news_count, sentiment_ratio

**分析框架（你需要做的）：**

1. **情绪比率：** sentiment_ratio > 0.2 → 利多新闻占优势。> 0.5 → 强烈偏多。< -0.2 → 利空。<-0.5 → 强烈偏空。
2. **新闻总量：** total < 5 → 信息不足，此维度权重应降低。> 20 → 信息充裕，可信度高。
3. **中性占比：** neutral > 60% → 市场缺乏明确方向，情绪以观望为主。

---

## 核心原则：诚实比完整更重要

**API 拿不到的，诚实地标出来。能搜的搜，搜不到的不编。**

```
         ┌─ API 命中     ──→ 输出数据，标记 data_source: "api"
数据需求 ─┤
         └─ API 失败      ──→ 生成 data_gap_report ──→ fillable? ──→ AI 搜 → 回填 ai_fill (参与评分)
                                                    ──→ direction_only? ──→ AI 搜 → 回填 ai_fill (×0.30~0.50 降权)
                                                    ──→ 每次搜不到    ──→ 标 status: "empty"，权重保持 0
```

### 硬数据（不能编）

价格、持仓手数、库存吨数、基差数值。**这些数字必须来自 API 或官方来源。** 不能编造。

### 软数据（AI 搜）

新闻事件、政策变化、天气影响、地缘风险、行业开工率。

---

## data_gap_report 工作流（核心）

当 `coverage.available < coverage.total` 时，输出 JSON 的顶层包含 `data_gap_report`：

```json
{
  "data_gap_report": {
    "total_gaps": 2,
    "summary": {"fillable": 1, "direction_only": 1, "not_fillable": 0},
    "gaps": [
      {
        "skill": "news_analysis",
        "skill_cn": "新闻情绪",
        "fillability": "fillable",
        "ai_fill_weight_multiplier": 0.90,
        "search_actions": [
          {"query": "JD 鸡蛋 期货 新闻 2026年5月", "source": "web", "priority": "high"}
        ],
        "ai_fill_schema": {
          "fields": ["bullish_news_count", "bearish_news_count", "sentiment_ratio"],
          "cannot_fill": []
        }
      },
      {
        "skill": "term_structure_analysis",
        "skill_cn": "期限结构",
        "fillability": "direction_only",
        "ai_fill_weight_multiplier": 0.30,
        "search_actions": [
          {"query": "JD 期货 期限结构 contango backwardation", "source": "web", "priority": "high"}
        ],
        "ai_fill_schema": {
          "fields": ["structure"],
          "cannot_fill": ["contracts", "prices", "spread_pct"]
        }
      }
    ]
  }
}
```

### 你（AI Agent）需要做的

1. **解析 `data_gap_report`**，对每个 gap 执行 `search_actions` 中的搜索
2. **按 `ai_fill_schema` 回填**到对应 `analysis_details[skill].ai_fill`：
```json
"ai_fill": {
  "filled_at": "2026-05-18T12:00:00",
  "source": "web_search",
  "fillability_tier": "fillable",
  "weight_multiplier": 0.90,
  "confidence": "high",
  "data": {
    "bullish_news_count": 3,
    "bearish_news_count": 1,
    "sentiment_ratio": 0.2
  },
  "urls": ["https://...来源URL..."],
  "note": "搜索结果摘要"
}
```
3. **`cannot_fill` 中的字段绝不要编造**（如期限结构的 `spread_pct`）
4. **`weight_multiplier` 从 gap 中的 `ai_fill_weight_multiplier` 复制**

---

## AI 搜索执行指南

### 触发条件

当**任何维度**的 `analysis_details` 中出现以下信号时，你（AI Agent）必须立即启动搜索：

| 信号 | 含义 | 行动 |
|------|------|------|
| `"data_source": "insufficient"` | API 有数据但太弱 | 搜索补充，API 和 AI 搜索结果合并输出 |
| `"status": "empty"` | API 完全无数据 | AI 搜索成为该维度唯一数据源 |
| `"soft_data_hint"` 字段存在 | 该维度给了搜索指引 | 按指引关键词搜索 |
| `coverage.available < coverage.total` | 有维度缺失 | 检查缺失维度并搜索 |

### 各品类搜索关键词

| 品类 | 搜索模板 | 重点关注 |
|------|---------|---------|
| 黑色系(RB/HC/I/J/JM) | `{品种名} {月份}月 2026 期货 库存 开工率 政策 检修` | Mysteel、钢厂检修、房地产政策、铁矿石发运 |
| 贵金属(AU/AG) | `沪{金/银} {月份}月 2026 COMEX库存 美联储 地缘 光伏需求` | COMEX/上金所库存、CFTC持仓、避险事件、工业需求 |
| 有色金属(CU/AL/ZN) | `沪{铜/铝/锌} {月份}月 2026 库存 LME 升贴水 矿端` | 三大交易所库存、TC/RC、矿端停产 |
| 农产品(M/RM/Y/CF/SR) | `{豆粕/菜粕/豆油/白糖} {月份}月 2026 进口 天气 库存 USDA` | USDA报告、海关数据、压榨利润、天气模型 |
| 能源化工(SC/FU/MA/TA/PP) | `{品种} {月份}月 2026 开工率 装置检修 港口库存 OPEC` | 装置动态、开工率、港口库存、原油政策 |

### 搜索要求

- 按时间排序，优先 **48 小时内**信息
- **每条标注来源网址和发布日期**
- **绝不编造数字**
- 拿不准的信息，明确标注"未经核实"

### 搜索后输出格式

搜索完成后，将搜索结果合并入对应维度的 JSON：

```json
"inventory_analysis": {
  "data_source": "mixed",
  "api": {
    "status": "N/A",
    "reason": "AKShare 不支持 AG 库存数据"
  },
  "ai_search": {
    "search_query": "沪银 库存 上金所 注册仓单 2026年5月",
    "content_count": 8,
    "key_findings": [
      "上金所白银库存 1,782 吨，环比-3.2%（来源：上金所官网，5月16日）",
      "COMEX 白银库存 11,200 吨（来源：CME Group，5月15日）"
    ],
    "assessment": "库存处于中等偏低水平，对银价构成支撑"
  }
}
```

---

## 数据缺失处理

| 情况 | 处理 |
|------|------|
| API 有数但不足（quality: insufficient） | API 数据 + AI 搜索补充，`data_gap_report` 标记为 `fillable` |
| API 完全无数（status: empty） | `data_gap_report` 标记为 `direction_only` 或 `fillable`，AI 搜索按 `ai_fill_schema` 回填 |
| AI 搜索也找不到 | `ai_fill.data` 留空，`confidence: "low"`，维度降权 |
| 最终仍有维度缺失 | 该维度 `weight × 0`，不参与 scoring |

### fillability 分级

| 级别 | 含义 | AI 搜索后评分权重 | 示例 |
|------|------|-------------------|------|
| `fillable` | 公开信息充足，可补全大部分字段 | ×0.75~0.90 | 新闻情绪(0.90)、基差(0.75) |
| `direction_only` | 只能拿定性方向，Z-score/精确数字不可补 | ×0.30~0.50 | 库存方向(0.50)、期限结构(0.30)、持仓(0.30) |
| `not_fillable` | 保留分类，当前版本所有维度均可搜索 | ×0 | — |

---

## 数据来源标注规范

**输出中每个维度都有数据来源和时效标记。**

| 标记 | 含义 | AI Agent 应对 |
|------|------|---------------|
| `data_source: "api"` | 来自 AkShare 实时数据接口 | 直接使用 |
| `data_source: "api_fallback"` | API 当日不可用，自动回退至前一交易日 | 查看 `data_gap_report`，确认是否需要 AI 搜索验证 |
| `data_source: "api_all_neutral"` | 关键词匹配全部判定为中性 | 按 `data_gap_report` 中的 `search_actions` 搜索补充 |
| `data_source: "insufficient"` | 样本不足 | 按 `ai_fill_schema` 回填到 `ai_fill` 槽位 |
| `data_quality: "stale"` | 数据过期回退 | 辩论中权重自动折半 |
| `data_quality: "low_value"` | 全中性/低质量 | 辩论中权重自动 ×0.3 |

> 所有数字必须是 JSON 原生类型，不能是 numpy/pandas 特殊类型。

---

## 综合决策框架

### 四维动态权重系统

本引擎内部使用**四维动态权重**（品种品类 × 置信度 Sigmoid × 市场状态自适应 × 数据质量折损）：

| 品类 | 核心驱动模块 |
|------|------------|
| 黑色系(RB/HC/I/J/JM) | 库存(1.3x) > 持仓(1.2x) > 技术面(1.0x) |
| 贵金属(AU/AG) | 技术面(1.3x) > 持仓(1.2x) > 新闻(1.1x) |
| 有色金属(CU/AL/ZN/NI) | 期限结构(1.2x) > 基差(1.1x) > 库存(1.1x) |
| 化工(MA/TA/EG/PP等) | 基差(1.2x) > 期限结构(1.2x) > 技术面(1.0x) |
| 农产品(M/RM/Y/CF/SR/JD等) | 库存(1.3x) > 新闻(1.2x) > 基差(1.1x) |
| 能源(SC/FU/LU/PG) | 新闻(1.3x) > 技术面(1.0x) > 期限结构(1.1x) |

### 市场状态自适应加成

- **高波动**（ATR/close > 2%）→ 技术面+10%，新闻情绪+50%
- **趋势市场**（20日有明确方向）→ 技术面+15%
- **低波动/震荡**（ATR/close < 1%）→ 基差+10%，库存+10%

### 数据质量折损（第四维）

回退数据、AI 补全数据自动降权：

| 数据状态 | 权重乘数 |
|---------|---------|
| API 历史回退 | ×0.5 |
| AI 补全 fillable（新闻/基差） | ×0.75~0.90 |
| AI 补全 direction_only（库存方向/期限结构/持仓） | ×0.30~0.50 |
| 完全缺失 | ×0（不参与评分） |

### 决策选择框架

拿到 6 个维度的结构化数据后，你应该：

1. **逐维度评估：** 按上述方法论对每个维度独立判断多空方向和置信度。
2. **加权聚合：** 考虑上述动态权重，不要简单数票数。黑色系的库存维度空头信号比农产品新闻维度多头信号更可信。
3. **分歧度评估：** 如果多空维度数量接近（差距 ≤1），信号不可靠，建议"观望"。
4. **极端信号优先：** 当某个维度出现极端信号（Z-score > 2.5 或 RSI > 80），该维度的权重应该进一步提升。
5. **仓位与风险匹配：** 分歧度越高 → 仓位越低。信号一致度越高 → 可适当加仓。最大仓位不超过 20%。

---

## 风控评估框架 (`--decision` 模式输出中包含 `risk_assessment`)

当运行 `--decision` 模式时，输出 JSON 的 `risk_assessment` 字段包含完整的风控评估结果。你需要理解并整合这些信息：

### 风控输出字段

| 字段 | 含义 |
|------|------|
| `risk_level` | 风险等级：low / medium / high |
| `approval` | 审批状态：approved / conditionally_approved / rejected |
| `max_position_pct` | 风控允许的最大仓位 |
| `max_risk_score` | 综合风险评分（0~3，越高越危险） |
| `risk_factors` | 触发的风险因素列表 |
| `conditions` | 交易条件（必须满足才能执行） |
| `stop_loss_advice` | 止损建议 |
| `position_advice` | 仓位建议 |

### 五维风险扫描

风控引擎从五个维度独立评估风险，你解读时应对每个维度独立关注：

1. **分歧度风险：** 多空分歧 ≥ 50% → 极高风险；30%~50% → 高风险；15%~30% → 可控。分歧度高时即使方向正确也应大幅降低仓位。
2. **信号强度风险：** 综合信号信心 < 20% → 可靠性极低，不应交易；20%~28% → 偏弱，仅适合极小仓位试探。
3. **方向一致性风险：** 多空维度票数接近（差距 ≤ 1）→ 没有共识，强制观望。多空各半时任何单向押注都是赌博。
4. **中性维度风险：** 超过一半维度保持中性 → 信息严重不足，基于不完整信息的决策比不决策更危险。
5. **仓位结构风险：** 做多时需检查库存/期限/持仓等空头核心维度是否同时给出反向信号。如果一个核心维度强烈反向，应降低仓位至少 50%。

### 风控审批规则

| 审批结果 | 含义 | 你的行动 |
|---------|------|---------|
| `approved` | 通过 | 可按正常仓位执行 |
| `conditionally_approved` | 条件批准 | 必须列出交易前置条件（如"必须严格止损""建议分批建仓"），条件不满足则不执行 |
| `rejected` | 否决 | 强制 hold，任何情况下不得建议交易。即使 6 维度全部看涨，风控一票否决也必须服从 |

### 风控总监立场

风控总监独立于交易决策链，**不关心方向，只关心风险**。读取风控报告时你应该：
- 风控否决 = 绝对不交易，这不是建议而是禁令
- 风控降仓 = 无论多头多强烈，仓位不得超过风控上限
- 风控条件 = 必须在你的最终建议中逐条列出并强调

---

## CIO 最终决策框架

在综合 6 维度分析 + 多空辩论 + 风控评估后，你（作为 AI Agent 的决策者角色）需要输出最终决策。参考以下框架：

### 决策输出必须包含

| 要素 | 要求 |
|------|------|
| **方向判断** | long / short / neutral，必须明确，不能模糊 |
| **操作建议** | buy / sell / hold，与方向对应 |
| **信心水平** | 0%~100%，基于加权信号强度和分歧度。**信心 < 25% 时必须建议观望或极低仓位** |
| **建议仓位** | 占资金百分比。分歧度 ≥ 30% → 不超过 5%；分歧度 < 15% + 信号强 → 可到 15% |
| **止损位** | 基于 ATR 或关键支撑/阻力。一般品种 1.5%~3%，高波动品种可放宽到 4% |
| **止盈位** | 参考最近阻力/支撑，或固定盈亏比（≥2:1） |
| **监控要点** | 列出最关键的风险因子和需要持续关注的指标变化 |

### 否决机制（必须遵守）

```
风控 rejection → 最终决策强制 hold，不可覆盖
信心 < 15% → 强制 hold，即使方向明确
仓位超过风控 max_position_pct → 以风控上限为准
```

### 多空辩论报告解读指南

`--decision` 模式输出的 `reasoning` 数组包含完整的多空辩论实录，结构为：

1. **序章** — 以"⚔️ 期货投资决策委员会 | XX 多空辩论实录"开场
2. **逐轮辩论** — 6 个维度依次展开，每个维度有多头/空头代表发言
3. **裁判长裁决** — 综合信号强度 + 分歧度 + 方向
4. **风控审核** — 独立风控评估
5. **CIO 决策** — 方向/仓位/止损/止盈

解读时注意裁判长的用词等级：
- "合上案卷" → 信号明确，可执行
- "犹豫片刻" → 信号偏弱但可辨方向，谨慎执行
- "沉吟片刻" → 方向不明确，建议观望
- "摇头" → 分歧过大，强制观望

---

## 支持的品种代码

| 代码 | 品种 | 交易所 | 代码 | 品种 | 交易所 |
|------|------|--------|------|------|--------|
| RB | 螺纹钢 | SHFE | HC | 热卷 | SHFE |
| CU | 沪铜 | SHFE | AL | 沪铝 | SHFE |
| AU | 沪金 | SHFE | AG | 沪银 | SHFE |
| M | 豆粕 | DCE | RM | 菜粕 | CZCE |
| I | 铁矿石 | DCE | J | 焦炭 | DCE |
| MA | 甲醇 | CZCE | TA | PTA | CZCE |
| SC | 原油 | INE | FU | 燃料油 | SHFE |
| LH | 生猪 | DCE | SR | 白糖 | CZCE |

---

## 注意事项

- 数据时效：期货数据在交易日收盘后更新，分析前确认数据日期
- 持仓数据：前 20 会员持仓 T+1 日公布
- 风险提示：输出结果仅供参考，不构成投资建议
- 缓存位置：所有数据缓存在 `cache/` 目录，删除可重新获取

---

## 分析风格指南

**你的输出形式是"期货投资决策委员会会议实录"——六个分析师依次发言，裁判长最终裁决。**

### 核心语言要求

- **纯中文，绝对禁止任何英文单词、缩写或术语。** 用"远期升水结构"而非"contango"，用"现货升水"而非"backwardation"，用"持仓量"而非"open interest"
- 禁止出现任何 markdown 符号（如 `**`、`#`、`-`），纯文本输出
- 所有结论必须有具体数字支撑，严禁编造数据

### 角色设定

每个分析维度有一个独立角色，在陈述时使用以下身份和语气：

| 角色 | 口头禅 / 特征 | 语气 |
|------|-------------|------|
| **技术面分析师** | "盯着屏幕猛敲键盘" | 语速快，数字密集，"金叉""死叉""超买超卖"张口就来 |
| **基差分析师** | "推了推眼镜" | 严谨克制，每个结论必带基差率或 Z-score 数值 |
| **期限结构分析师** | "翻开跨期价差表" | 冷静派，用 Full Carry 理论说话，爱算展期收益 |
| **库存分析师** | "冷笑一声" | 只认库存周期理论，看 Z 分位定多空，语气傲慢但每个字都有数据 |
| **持仓分析师** | "调出会员持仓排名" | 追踪"聪明钱"，关注前20会员动向，讲究量仓配合 |
| **新闻分析师** | "刷着最新资讯" | 情绪敏感，能从标题里嗅出利多利空，但也坦诚信息不足时不下判断 |
| **裁判长** | "合上案卷" 或 "摇头" 或 "沉吟片刻" | 权威、克制、不站队。综合各方论述做出最终裁决，给出明确的方向、仓位和止损建议 |

### 辩论结构

1. **序章**：以"⚔️ 期货投资决策委员会 | XX 多空辩论实录"开场
2. **分轮辩论**：六个维度依次展开，每个维度先由多头代表发言，再由空头代表发言
3. **裁判裁决**：裁判长综合各方论述，指出最关键的分歧点，给出最终判断
4. **风控审核**：风控总监独立评估风险
5. **CIO 最终决策**：方向、仓位、止损止盈、监控要点

### 裁决原则

- 不简单数票数。黑色系的库存维度空头信号比农产品新闻维度多头信号更可信
- 分歧度过高（多空维度数接近）时，选择观望而非强判方向
- 极端信号（Z-score > 2.5、RSI > 80 等）应被重点强调
- 最终决策必须包含仓位比例和止损位，不能只给方向不给操作
