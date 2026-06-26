---
name: caidawei-cdw--brainstorming-for-travel
description: "在旅游需求模糊时，用对话一步一步澄清并给出可行方案；预算充足时用 FlyAI CLI（search-hotels / search-poi / search-flight）辅助酒店、景点与机票扫描。全程中文。用户已说清的目的地/时间/预算等直接采用；未说清时优先用天数与预算收敛。触发：不知道去哪、帮我规划、查酒店机票景点、只有大概预算/假等。"
metadata:
  agent:
    type: skill
    runtime: shell
  openclaw:
    emoji: "🧳"
    priority: 85
    intents:
      - travel_planning
      - travel_brainstorming
      - destination_recommendation
      - flight_search
      - hotel_search
      - poi_search
    patterns:
      - "(不知道去哪 | 去哪里玩 | 旅游规划 | 旅行计划 | 帮我规划| 推荐.*地方)"
      - "(五一 | 国庆 | 春节 | 元旦 | 假期| 放假).*(去哪 | 旅游 | 旅行 | 玩)"
      - "(查酒店 | 查机票 | 查景点 | 预算.*旅游 | 多少钱.*去)"
      - "(只有.*天 | 有.*假 | 想去.*玩)"
---

# 模糊旅游需求澄清与方案

## 何时使用

用户旅游意图**不完整或很泛**，需要先澄清再给方案。若约束已齐，可直接出方案并视情况调用 FlyAI。**不要**在缺少目的地、入住离店日期、出发城市等硬条件时盲目跑 CLI。

## 核心原则（对齐 brainstorming）

- **一次只问一个**关键问题；能做成**选择题**时优先选择题。
- **先读用户原话**：目的地、日期、人数、预算、禁忌、节奏等**已写明则直接采信**。
- **用天数与预算双锚**：目的地或主题不清时，先用**出行天数**缩小范围；再用**总预算/人均预算**区分档次与可行区域（紧预算 vs 宽松）。
- **全程简体中文**回复。

## 预算驱动方案

预算是收敛「交通 + 住宿 + 玩乐」的核心杠杆，澄清或推断时注意：

1. **问清口径**：总预算还是人均；是否含往返大交通与住宿；大致几晚。
2. **粗拆再搜**：在数字明确后，将预算拆成**每晚住宿上限**（`search-hotels` 的 `--max-price`）、**机票扫描上限**（`search-flight` 的 `--max-price`），剩余视为市内交通与门票弹性；若用户只给总包，先按「几晚 + 往返机票预留」反推每晚上限，并在回复里说明假设，便于用户纠正。
3. **方案表述**：优先推荐**预算内**组合；若用户预算偏紧，明确标出「可能需提高预算或改日期/目的地」的项。

## 判断：是否还要澄清

| 情况 | 做法 |
|------|------|
| 目的地 + 时间窗口 + 天数 + 预算 + 出发地（查机票时需要）已齐 | 可直接方案，并按下列步骤调用 FlyAI |
| 只有天数和预算 | 补问区域/兴趣；同时用预算缩小住宿与交通档次预期 |
| 几乎只有「随便」 | 先问**天数或假期窗口**，再问**预算档位**，再问兴趣（选择题） |

## 建议澄清顺序（可跳过已明确的项）

1. **时间与天数**：固定日期或可浮动；共几晚。
2. **预算与口径**：总额/人均、是否含机票与酒店星级预期。
3. **出发地与目的地**：城市级名称，供 `search-flight` 与 `search-hotels`。
4. **主题与禁忌**：自然/城市/亲子等；体力与高反等。
5. **交通偏好**：对方案影响大时再问。

## 方案阶段

- 信息仍偏少：先给 **2～3 个方向**，每个写清**预算档位与取舍**。
- 信息已齐：给出日程级概要；若已执行 FlyAI，用**真实 CLI 结果**支撑酒店/机票/景点建议，并注明查询条件与日期。

---

## FlyAI：何时调用

在至少具备 **目的地城市名、入住/离店日期、出发城市（查机票时）** 后再执行。用户未指定景点时，可用 `search-poi` 的热门档位作参考。

**SSL**：若遇证书校验失败，在命令前加环境变量：`NODE_TLS_REJECT_UNAUTHORIZED=0`（仅作绕过手段，知悉安全风险）。

### Step 1：搜索酒店

```bash
NODE_TLS_REJECT_UNAUTHORIZED=0 flyai search-hotels \
  --dest-name "[目的地]" \
  --check-in-date [入住日期] \
  --check-out-date [离店日期] \
  --max-price [预算上限] \
  --sort rate_desc
```

| 参数 | 说明 |
|------|------|
| `--dest-name` | 目的地城市（必填） |
| `--check-in-date` | 入住日期 YYYY-MM-DD |
| `--check-out-date` | 离店日期 YYYY-MM-DD |
| `--max-price` | 每晚最高价格（与上文预算拆分一致） |
| `--hotel-stars` | 星级筛选，如 `"4,5"` |
| `--sort` | `rate_desc` 评分优先 / `price_asc` 价低到高 |
| `--poi-name` | 附近景点名称 |

### Step 2：搜索景点（可选）

用户指定关键词时：

```bash
NODE_TLS_REJECT_UNAUTHORIZED=0 flyai search-poi \
  --city-name "[目的地]" \
  --keyword "[景点关键词]"
```

用户未指定时，用热门参考：

```bash
NODE_TLS_REJECT_UNAUTHORIZED=0 flyai search-poi \
  --city-name "[目的地]" \
  --poi-level 5
```

### Step 3：机票价格扫描（`search-flight`）

单日查询示例：

```bash
NODE_TLS_REJECT_UNAUTHORIZED=0 flyai search-flight \
  --origin "{出发城市}" \
  --destination "{目的地}" \
  --dep-date {出发日期} \
  --back-date {返回日期} \
  --journey-type {1=直飞/不填=含中转} \
  --sort-type 3
```

| 参数 | 说明 |
|------|------|
| `--origin` | 出发城市（必填） |
| `--destination` | 目的地城市 |
| `--dep-date` | 出发日期 YYYY-MM-DD |
| `--back-date` | 返回日期 YYYY-MM-DD |
| `--journey-type` | `1` 仅直飞，`2` 仅中转，不填为全部 |
| `--sort-type` | `3` 价格从低到高 |
| `--dep-hour-start` / `--dep-hour-end` | 出发时段 0–23 |
| `--max-price` | 价格上限（与预算一致时填入） |

**批量扫描策略**：

1. 根据用户允许的日期范围，列出候选**出发日期**。
2. 对每个出发日期，返程日期 = 出发日期 + **行程天数**（与用户确认的天数一致）。
3. 对每个组合调用 `search-flight`，记录**当日最低价**及对应航班摘要。
4. 汇总成「哪几天出发相对便宜」，再结合酒店 `max-price` 与总预算做推荐。

---

## 禁止

- 不要一次抛多个澄清问题。
- 不要忽略用户已声明的预算与日期。
- **无 CLI 或调用失败时**：明确说明，降级为**经验型方案**，不编造具体价格与余票。
