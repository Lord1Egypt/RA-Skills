---
name: video_finder_search
description: "搜索影片：Query Rewrite 扩展标签、Multi Search 多引擎并行搜索（subagent 并发）、Result Merge 加权去重排序。触发：搜片、找片、搜索、搜一搜"
---

# search — 影片搜索

三层架构：Query Rewrite → Multi Search → Result Merge，基于用户偏好自动筛选排序。

## 前置条件

- **称呼约定**：`{{{user}}}` 为占位符
- **依赖**：`video_finder_preferences`（读取 `preferences.json`）
- **依赖**：`video_finder_proxy`（站点可达性探测）

---

## Layer 1: Query Rewrite（查询改写与标签扩展）

### 输入

用户原始关键词 + `preferences.json` 中的偏好数据。

### Step 1: 转译（中 → 英）

中文关键词先转英文，非中文直接进入 Step 2。

```
"金发护士" → "blonde nurse"
"学生妹"   → "schoolgirl"
```

### Step 2: 语义概念扩展

对每个核心词，沿多维度扩展关联标签：

```
"blonde nurse" 的扩展:

  📌 直译/同义       blonde nurse, blond nurse, blonde medical
  🏥 场景/地点       hospital, clinic, medical office, exam room
  🎭 类型/分类       medical, cosplay, roleplay, uniform, costume
  👤 角色/身份       nurse, doctor, patient, medical student
  🎬 行为/动作       examination, checkup, treatment, bedside
  👗 视觉/外观       nurse outfit, scrubs, white uniform, stethoscope, blonde hair
```

扩展维度：

| 维度 | 说明 | 示例（金发护士） |
|------|------|-----------------|
| 直译/同义 | 中译英 + 近义词 | blonde nurse, blond nurse, blonde medical |
| 场景 | 在哪里发生 | hospital, clinic, medical office, exam room |
| 类型 | 内容分类标签 | medical, cosplay, roleplay, uniform |
| 角色 | 涉及的人物身份 | nurse, doctor, patient |
| 行为 | 发生的动作 | examination, checkup, treatment |
| 视觉 | 外观特征 | nurse outfit, scrubs, white uniform, blonde hair |

### Step 3: 偏好注入

读取 `preferences.json`，将每个字段注入查询的不同位置：

```
preferences.json
├─ source_type: "欧美 amateur"     → 注入 Q1-Q4 作为必带词 "amateur"
├─ preferred_sites: ["xvideos",   → 注入 Q1-Q3 site: 前缀
│                    "eporner"]
├─ site_priority: ["xvideos",     → xvideos 作为 Q2/Q3 首选站点
│                  "eporner"]
├─ quality_min: "1080p"           → 注入 Q4 作为 "1080p" / "hd"
├─ duration_min_seconds: 300      → 不在查询层面注入，在 Layer 3 评分时一票否决
├─ tag_weights: {                 → 取权重 ≥ 3 的标签，与语义扩展词取交集
│     "amateur": 12,              →   注入 Q2/Q4 做加权
│     "homemade": 10,             → 例: amateur ✓ (匹配 source_type)
│     "natural tits": 8,          →     homemade ✓, euro ✓
│     "euro": 7,
│     "blonde": 6,
│     "young": 5, ...}
├─ author_weights: {              → 权重 ≥ 2 的作者注入 Q2/Q4
│     "CreatorName": 4 }
├─ exclude_tags: ["黑皮", "old",  → 注入 Q3 加 "-" 前缀排除（硬排除，不受权重影响）
│   "milf", "复古", ...]
└─ tag_weights 中权重 ≤ 0 的标签  → 注入 Q3 加 "-" 前缀排除
```

**注入逻辑详解**：

| 偏好字段 | 注入位置 | 注入方式 |
|---------|---------|---------|
| `source_type` | Q1-Q4 全部 | 作为必带词直接拼入查询 |
| `preferred_sites` | Q1-Q3 | Q1: `site:a OR site:b`，Q2/Q3: `site:首选` |
| `quality_min` | Q4 | 转为标签词 `1080p` / `hd` / `4k` 拼入 |
| `tag_weights`（权重 ≥ 3） | Q2, Q4 | 取与语义扩展词有语义关联的子集，散列拼入 |
| `tag_weights`（权重 ≤ 0） | Q3 | 等同于硬排除，加 `-` 前缀 |
| `exclude_tags` | Q3 | 每个前面加 `-`（硬排除，不受权重影响） |
| `author_weights`（权重 ≥ 2） | Q2, Q4 | 若作者名与场景相关则加入 |
| `duration_min_seconds` | — | **不注入查询**，留到 Layer 3 一票否决 |

### Step 4: 生成查询变体

```
原始输入:   "金发护士"
语义扩展:   blonde nurse, hospital, medical, cosplay, roleplay, uniform
偏好注入:
  source_type  → "amateur"（必带）
  sites       → site:xvideos.com, site:eporner.com
  tag_weights（≥3）→ euro, homemade, real couple, natural tits（与 nurse/cosplay 语义相关）
  排除         → -black -mature -granny -milf -jav -ssbbw（tag_weights≤0 + exclude_tags）
  quality     → hd, 1080p

↓ 生成 4 个查询变体:

Q1（宽）:  site:xvideos.com OR site:eporner.com amateur "blonde nurse"
           └─site范围──┘ └source_type┘ └─核心直译词（精准匹配）─┘

Q2（中）:  site:xvideos.com amateur blonde nurse medical hospital cosplay euro homemade
           └首选站点┘ └source_type┘ └──语义扩展──┘ └关联tag_weights≥3┘

Q3（窄）:  site:xvideos.com "blonde nurse" hospital amateur -black -mature -granny -milf -jav
           └首选站点┘ └─精准匹配─┘ └场景┘ └─source─┘ └──排除（tag_weights≤0 + exclude_tags）──┘

Q4（泛）:  blonde nurse amateur medical cosplay roleplay homemade real couple hd
           └核心词┘ └source┘ └───────语义扩展 + tag_weights≥3────────┘
```

### 查询生成规则

| 变量 | 生成策略 |
|------|---------|
| Q1（宽） | `site:站点1 OR site:站点2` + source_type + 核心直译词（引号包裹） |
| Q2（中） | `site:首选站点` + source_type + 核心词 + 场景词 + 类型词 |
| Q3（窄） | `site:首选站点` + 核心词 + 场景词 + source_type + 排除标签加 `-` 前缀 |
| Q4（泛） | 无 site 限制，核心词 + source_type + 类型词 + 角色词 + 偏好高频标签 |

### 语义扩展示例

```
"金发护士"    → blonde nurse, hospital, medical, cosplay, roleplay, uniform
"女仆"        → maid, french maid, cleaning, domestic, servant, apron, costume
"瑜伽"        → yoga, flexible, yoga pants, stretching, fitness, gym, workout
"学生"        → schoolgirl, student, classroom, college, uniform, teen, dorm
"人妻"        → wife, married, milf, cheating, housewife, mature, kitchen
"户外"        → outdoor, public, park, beach, nature, car, forest, garden
```

---

## Layer 2: Multi Search（多引擎并行搜索）

### 并行策略

启动 **N 个 subagent** 同时搜索，N = 参与引擎数（默认 5 个，站内搜索动态增减）。

```
                    ┌─ subagent: Google ────── 用 Q1-Q4 搜，返回结果列表
                    │
Layer 1 产出的 ─────┼─ subagent: DuckDuckGo ─── 用 Q1-Q4 搜，返回结果列表
4 个查询变体        │
(Q1, Q2, Q3, Q4)   ├─ subagent: Bing ───────── 用 Q1-Q4 搜，返回结果列表
                    │
                    ├─ subagent: Yandex ─────── 用 Q1-Q4 搜，返回结果列表
                    │
                    └─ subagent: 站内搜索 ───── 直连 preferred_sites 站点搜
```

- **全部同时启动**，不等待彼此
- 每个 subagent 收到完整上下文（全部查询变体 + 偏好数据 + 代理配置）
- 设置总超时 = 30s，超时的 subagent 结果丢弃

### 各引擎 subagent 任务模板

```
你是搜索子代理，负责用 [引擎名] 搜索影片。

查询变体:
  Q1: {query1}
  Q2: {query2}
  Q3: {query3}
  Q4: {query4}

用户偏好:
  source_type: {source_type}
  preferred_sites: {preferred_sites}
  quality_min: {quality_min}
  duration_min_seconds: {duration_min_seconds}
  exclude_tags: {exclude_tags}
  tag_weights: {tag_weights}

任务:
  对每个 Q 用 web_fetch 执行搜索，提取结果链接列表。
  
  然后逐个获取链接详情页，**自主决定**用 web_fetch 还是 browser:
    - web_fetch 优先 → 直接提取标题、时长、画质、标签
    - 若返回内容为空 / JS 占位符 / 反爬 → 切换 browser 渲染后提取
    - 若 browser 也失败 → 仅保留搜索摘要信息，标记 incomplete

  返回: JSON 数组，最多 20 条。去重 + 无结果则返回空数组。
  超时: 30 秒。
```

### 站内搜索 subagent 特殊处理

站内搜索直接抓取各站点搜索页面，不经过搜索引擎：

```
搜索目标站点: {preferred_sites}
  web_fetch: {site}/?k={原始关键词}
  提取视频卡片列表 → 解析标题/时长/画质/URL
```

### 引擎容错

| 情况 | 处理 |
|------|------|
| subagent 超时（> 30s） | 结果丢弃，不影响其他 |
| subagent 返回空 | 正常，该引擎无结果 |
| subagent 报错 | 忽略，继续等其他的 |
| 全部 subagent 超时/失败 | 告知用户"搜索受限，换关键词试试" |

### 汇总

所有 subagent 返回后，将结果列表合并 → 交给 Layer 3。

---

## Layer 3: Result Merge（结果合并去重排序）

### Step 1: 合并

将所有引擎 × 查询变体产出的结果汇入一个列表。

### Step 2: 去重

| 维度 | 策略 |
|------|------|
| URL 完全匹配 | 直接去重，保留首次出现的 |
| 标题相似度 > 85% | 视为重复，保留信息更全的那条 |
| 同一站点 + 相同时长 | 高度疑似重复，合并 |

### Step 3: 评分排序

每条结果计算 `score`，满分 100：

```
base_score = 50

加分项:
  + title 匹配 tag_weights 中的标签       每个 +权重值 (无上限)
  + title 匹配 author_weights 中的作者    每个 +权重值 (无上限)
  + 画质 ≥ quality_min                          +10
  + 时长在 10-30 分钟区间                         +5
  + 来源站在 preferred_sites 中                 +5
  + 来源站在 site_priority 前两位               +3

减分项:
  - title 匹配 tag_weights 中权重 ≤ 0 的标签     一票否决 (-100)
  - title 命中 exclude_tags                   每个 -10 (无下限)
  - 时长 < duration_min_seconds                   一票否决 (-100)
  - 画质 < quality_min                             -15

最终 score = clamp(base_score + 加分 - 减分, 0, 100)
```

### Step 4: 排序输出

按 `score` 降序排列，截取 Top 15。

### Step 5: 标签被动增益

搜索完成后，对展示给用户的结果中出现的标签，在 `tag_weights` 中 +1：

```
for tag in top_results.flatMap(tags):
  tag_weights[tag] = (tag_weights[tag] || 0) + 1   ← 被动增益
```

> 此操作在搜索会话结束时由 orchestrator 写回 `preferences.json`。

---

## 结果展示

```
{{{user}}}，搜到以下结果：

🔝 最佳匹配:
1️⃣ [标题] — 来源站 — ⏱ 时长 — 🎬 画质 — ⭐ 匹配度 95

📋 其他:
2️⃣ [标题] — 来源站 — ⏱ 时长 — 🎬 画质 — ⭐ 88
3️⃣ [标题] — 来源站 — ⏱ 时长 — 🎬 画质 — ⭐ 82
...

→ 用户选定 → 交给 video_finder_download
→ 用户不满意 → 换关键词，回到 Layer 1 重新生成查询变体
```

## 页面内容获取

Subagent 在拿到搜索结果链接后，**自主判断**用哪个工具获取详情：

```
搜索结果链接
  │
  ├─ web_fetch 直连
  │   ├─ 返回有效 HTML → 解析标题/时长/画质/标签 ✅
  │   ├─ 返回空 / 403 / 反爬 → 切代理重试
  │   └─ 返回 JS 占位符（如 XVideos、Pornhub 等 SPA 站点）
  │       └─ 自动切换 browser 渲染 → 截图 + 提取 ✅
  │
  └─ browser 也失败 → 仅保留搜索结果摘要，标记 incomplete ⚠️
```

**不需要在主流程中手动判断** — 每个 subagent 自己决定，因为不同引擎搜出的站点不同（Google 可能出 XVideos JS 页、站内搜索可能直接出静态页）。

