---
name: worldcup-2026-analysis
description: "2026世界杯/足球比赛量化分析与预测引擎。基于Elo评级+Dixon-Coles泊松+蒙特卡洛模拟，结合网页搜索获取最新赛果/伤病/赔率进行实时校准。提供单场胜平负预测、比分概率、小组出线概率、淘汰赛晋级概率、爆冷分析、赔率价值检测。当用户要求分析足球比赛、预测结果、查看晋级/出线概率、对比球队实力、检测赔率价值、查询世界杯赛程比分赔率、或提到足球/世界杯/欧冠/英超/五大联赛等赛事分析时使用。"
metadata:
  version: "2.1.1"
  openclaw:
    emoji: "⚽"
    requires:
      bins: ["python3"]
    credentials:
      - id: "odds-api-key"
        name: "The Odds API Key"
        description: "可选。免费赔率 API (https://the-odds-api.com)，用于批量价值扫描。单场赔率可由网页搜索替代，无 key 不影响核心功能。"
        env: "ODDS_API_KEY"
      - id: "football-data-api-key"
        name: "football-data.org API Key"
        description: "可选。赛果校准的 API backup (https://www.football-data.org，免费档)。主路径为网页搜索，仅搜索不可用时兜底。"
        env: "FOOTBALL_DATA_API_KEY"
---

# 世界杯 2026 量化分析

专业足球比赛量化分析工具，**提供可验证的分析框架，而非投注建议**。

核心理念（v2.1）：**模型本地计算 + 网页搜索实时校准**。实时数据（赛果/伤病/阵容/赔率）由 agent 的网页搜索能力获取，不依赖付费 API；搜索到的信息经结构化后喂入引擎，驱动 Elo/攻防数据/修正因子的更新。

| 模块 | 文件 | 能力 | 依赖 |
|------|------|------|------|
| 预测引擎 | `scripts/prediction_engine.py` | Elo+DC泊松+蒙特卡洛+市场融合 | 无（纯本地） |
| 搜索校准器 | `scripts/calibrate.py` | 搜索结果→Elo/攻防/分组更新 | 网页搜索（agent 自带） |
| 赔率提供器 | `scripts/odds_provider.py` | 批量比赛盘/夺冠盘/价值扫描 | `ODDS_API_KEY`（可选） |

## 核心能力

1. **单场分析**：Elo-xG耦合 + Dixon-Coles比分矩阵 + 主场xG乘数 + 修正因子 → 胜平负 + 最可能比分
2. **市场融合**：搜索单场赔率 → 去vig隐含概率 → 模型70%+市场30%融合（显著降低Brier）
3. **小组出线**：4队单循环蒙特卡洛（含东道主主场）→ 出线/头名/名次分布
4. **淘汰赛晋级**：常规时间 + 加时/点球折算（不预测点球比分）
5. **晋级路径**：单队多阶段蒙特卡洛推演
6. **爆冷分析**：三层判据（风格克制+状态变量+赛制红利）→ 爆冷概率+等级
7. **赔率价值**：模型 vs 市场偏差≥3%标记 + 半Kelly仓位
8. **搜索校准**：网页搜索最新赛果 → FIFA风格Elo更新 + EWMA攻防数据更新

## 标准工作流（每次预测前执行）

### 第 0 步：搜索校准（关键！预测准确度的最大来源）

用网页搜索获取自上次校准以来的最新信息：

1. **搜索最新赛果**（如 `World Cup 2026 results yesterday scores` / `世界杯 比分 昨天`），将结果结构化为 JSON：
```json
{
  "source": "ESPN 2026-06-12 搜索结果",
  "results": [
    {"home": "墨西哥", "away": "南非", "home_goals": 2, "away_goals": 0, "neutral": false}
  ]
}
```
2. 运行 `python3 scripts/calibrate.py results.json` → 自动更新 Elo（K=30+净胜球放大+东道主加成）和攻防数据（EWMA α=0.30，近期状态主导）
   - **搜索不可用时的 backup**：`python3 scripts/calibrate.py --from-api [起日] [止日]` 从 football-data.org 拉赛果（需 `FOOTBALL_DATA_API_KEY`，英文队名经 `data/team_names.json` 自动映射，映射失败的场次如实跳过）
3. **搜索球队情报**（如 `"队名" injury lineup news`）：核心伤缺/内讧/轮换 → 转化为修正因子或 `match_context`
4. **搜索本场赔率**（如 `"A vs B" odds 1x2`）：拿到三个小数赔率备用

**红线**：搜索结果必须有来源；搜不到就如实说明并跳过该步，**绝不编造比分/伤病/赔率**。

### A. 单场比赛分析
1. 完成第 0 步校准
2. `engine = FootballPredictionEngine(data_dir='../data')`
3. `engine.predict(a, b, corrections={...}, is_knockout=布尔, home='a'/'b'/None)`
   - `home` 仅东道主真主场传值（美/加/墨），中立场传 None（主场已是 xG 乘数，勿再叠加概率修正）
   - `corrections` 放搜索到的伤病/状态情报（参考 `data/corrections.json` 16 项库）
4. 如搜到赔率：`mk = engine.odds_to_probability(o1, ox, o2)` → `engine.blend_with_market(pred['final'], mk)` 作为最终输出概率
5. 按「单场分析」格式输出，注明数据截止时间，结尾附风险提示

### B. 小组出线概率
1. 分组未填充时：搜索官方分组 → `python3 scripts/calibrate.py --groups groups.json`（必须注明 source）
2. `engine.simulate_group([4队], simulations=50000, home_teams=['美国','加拿大','墨西哥'])`

### C. 淘汰赛晋级
- 单场：`engine.knockout_advance_prob(a, b, corrections, home)`
- 全路径：`stages=[{'name':'16强','win_prob':0.62},...]` → `engine.monte_carlo_path(team, stages)`

### D. 爆冷分析
1. 搜索两队近期情报填 `match_context`：`is_first_match` / `is_last_group_match` / `rotation_risk`(强队轮换) / `expansion_format` / `internal_strife`(内讧) / `key_injury` / `slow_starter`
2. `engine.upset_analysis(a, b, match_context)` → 三层修正 + Tier 等级

### E. 赔率价值检测
- 单场（推荐，无需 key）：搜索赔率 → `odds_to_probability` → `engine.value_detection(model, market, 3.0)` + `engine.kelly(prob, odds)`
- 批量（需 `ODDS_API_KEY`）：`OddsProvider().value_scan(engine, predictions)` / `get_outright_winner()`

### F. 赛后复盘
结果回填 `logs/prediction_log.md`，`engine.brier_score(predicted, outcome)` 量化校准，每 10 场复盘平均分。

## 数据文件

- `data/elo_ratings.json`：48 队 Elo（初始估值，**由搜索校准持续更新**，自动 .bak 备份）
- `data/team_stats.json`：48 队场均进球/失球（EWMA 滚动更新）
- `data/corrections.json`：16 项修正因子库（含 2026 专属 7 项）
- `data/world_cup_schedule.json`：赛制骨架（分组为事实型数据，搜索后经 `--groups` 写入，不预填）
- `logs/calibration_log.md`：每次校准的来源、赛果、Elo 变动（自动生成）

## 输出格式

### 单场分析
```
⚽ [A] vs [B] | [赛事] | [日期] | 数据截止: [校准时间]
📊 Elo [A] vs [B]（差[gap]）| xG [A] [值] / [B] [值]
📈 模型: 胜 x% | 平 x% | 负 x%
💹 市场融合后: 胜 x% | 平 x% | 负 x%（搜索赔率 [o1/ox/o2]）
✏️ 修正: [因子] ±x%（来源: [搜索情报]）
🎯 最可能比分: [比分1] / [比分2] / [比分3]
💡 关键洞察: [一句话]
⚠️ 本分析基于统计模型，不构成投注建议。
```

### 爆冷分析
```
🔥 [强队] vs [弱队] | 爆冷分析
📊 Elo差 [gap] | 基础爆冷 x%（弱队胜）/ x%（平）
✏️ 三层修正: 风格 +x% | 状态 ±x% | 赛制 +x%
📈 调整后: 弱队胜 x% | 平 x% | 综合爆冷值 x% | [Tier X]
💡 关键因素: [1-3个核心变量]
⚠️ 本分析基于统计模型，不构成投注建议。
```

## 红线

- 绝不直接建议投注，只提供分析框架
- 绝不伪造数据：所有计算经代码执行；**赛果/伤病/赔率/分组等事实型数据必须来自可溯源的搜索结果，搜不到就如实说明**
- 校准必须注明来源（`source` 字段强制）
- 绝不隐瞒偏差：模型 vs 市场大偏差时标注不确定性
- 每次分析结尾必须附风险提示；输出注明数据截止时间
- 不预测点球大战比分（仅给晋级概率）

## 模型说明（v2.1 准确度改进）

1. **Dixon-Coles 修正**（ρ=-0.10）：独立泊松系统性低估 0-0/1-1，τ 修正抬升低比分平局——足球建模标准做法
2. **Elo→xG 耦合**（强度 0.25）：Elo 差距直接调整期望进球；概率空间 Elo 权重相应降至 0.15 避免双重计算
3. **主场优势 = xG 乘数**（×1.10）：替代扁平概率修正，强弱对话中效果自适应
4. **市场融合**（默认 30%）：市场赔率聚合了全市场信息，融合可显著降低 Brier
5. **EWMA 攻防更新**（α=0.30）：近 3 场状态主导，比静态赛前均值更贴近临场
6. **搜索驱动情报**：伤病/轮换/内讧等无法量化建模的变量，由 agent 搜索后经修正因子进入模型

## 版本历史

- **2.1.1**：新增赛果校准 API backup（football-data.org + 队名映射表 `data/team_names.json`）；搜索仍为主路径
- **2.1.0**：OpenClaw 适配；移除 26worldcup.cn API 依赖（`data_provider.py` → 搜索驱动的 `calibrate.py`）；Dixon-Coles / Elo-xG 耦合 / 主场 xG 乘数 / 市场融合 / EWMA 校准
- **2.0.0**：三 skill 整合（football-match-analysis + world-cup-2026-odds + worldcup26-api），去 Coze 耦合
