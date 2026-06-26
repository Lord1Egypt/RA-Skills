# Stream Digest Implementation Plan

## 1. 背景与目标

`zsxq-digest` 当前已经具备：
- token-first 采集
- browser fallback 采集
- 去重与 cursor
- 简单日报渲染

下一阶段目标不是继续强化“严格今天更新”，而是新增一个更实用的输出模式：

> **分星球信息流摘要（stream digest）**

该模式强调：
- 分星球展示最近更新
- 默认忠实还原原始内容
- 重点展开少量代表性条目
- 其余内容做高密度压缩展示
- 所有条目保留可点击 URL
- 尽量保留完整中间字段，方便后续定制化开发

## 2. 产品定位

### 默认定位
`stream digest` 默认是：
- **高效的信息整理器**
- 不是强主观评论器
- 不是重度策展编辑器
- 不是严格日历日报生成器

### 默认输出目标
用户在 2~4 分钟内应完成：
1. 快速查看每个星球最近的代表性更新
2. 直接读到少量重点条目的主体内容
3. 快速浏览剩余条目并判断是否点开原文

## 3. 设计原则

### P1. 保真优先
默认不输出过强的价值判断文案，例如：
- “为什么值得看”
- “建议动作”

排序可以在内部存在，但默认不显性展示主观解释。

### P2. 结构优先于评论
通过结构编排提高可读性：
- 分星球
- 重点展开
- 其余压缩
- 保留 URL

### P3. 默认保留更多字段
public skill 的默认实现应保留充分中间字段，以便用户后续自行扩展：
- 重新排序
- 自定义摘要
- 增加行业偏好
- 增加更强的 AI 分析层

### P4. 不假装采集完整
如果 browser 模式只能抓到可见预览，应明确标注：
- `is_truncated`
- `source_mode=browser`
- `source_confidence=low|medium`

### P5. 动态展开，宁缺毋滥
每个星球默认展开 **1~3 条重点内容**，而不是强制放满 3 条。

## 4. 非目标（当前阶段不做）

当前版本不追求：
- 严格 today-only 过滤
- 全自动详情页补抓所有长文
- 默认启用 LLM 对所有条目做重写或评论
- 默认做强风格化策展语言
- 默认依赖浏览器二跳抓详情页

这些都保留为后续增强方向，而不是 MVP 的硬要求。

## 5. 输出形态设计

## 5.1 顶部总览
输出以下信息：
- 覆盖星球列表
- 每个星球采集条数
- 数据来源（token/browser）
- 是否含截断内容
- 当前口径：最近可见更新 / 最近信息流，不是严格今天

示例：
- 覆盖星球：学不完根本学不完、睡前消息的编辑们
- 数据来源：token + browser fallback
- 输出口径：最近可见更新（非严格今日）
- 捕获限制：部分长文仅保留可见预览

## 5.2 按星球分块
每个星球一个 section。

建议 Markdown 结构：
- `## 🪐 星球名`
- `### 重点展开`
- `### 其余更新`

## 5.3 重点展开区
每个星球动态选择 1~3 条代表性内容。

每条包含：
- 标题 / 首句
- 作者（如有）
- 时间（如有）
- 点赞 / 评论（如有）
- 正文摘录（大段）
- 原文 URL

### 重点展开的正文策略
- 默认显示 400~900 字
- 优先保留前 2~4 段
- 超长则以：`（下略，见原文）` 收尾
- 如果采集源本身不完整，则显示：`（受限于当前可见预览，正文可能已截断）`

注意：
- 默认不显示“为什么值得看”
- 默认不显示“建议动作”

## 5.4 其余更新区
剩余条目使用紧凑格式。

每条包含：
- 标题 / hook
- 1~2 句摘要
- 点赞 / 评论（如有）
- 原文 URL

目标：
- 尽量保信息
- 尽量少占长度
- 保留点击入口

## 5.5 尾部速览（可选）
可选增加：
- `## 快速浏览索引`
- 按星球列出本次全部标题列表

这部分不是 MVP 必需，但可作为消息过长时的退化输出。

## 6. 星球类型分流

为兼顾不同内容形态，stream digest 需要支持轻量分流。

## 6.1 长文 / 分析型星球
例如：
- 学不完根本学不完

特点：
- 单条内容较长
- 原创分析较多
- 适合重点展开正文

策略：
- 更偏向正文长度与内容完整度排序
- 重点展开区可更长
- 紧凑区保留短摘要 + URL

## 6.2 问答 / 讨论型星球
例如：
- 睡前消息的编辑们

特点：
- 问题与回答结构较重要
- 互动量（点赞/评论）可作为价值信号
- 可能夹杂外链，但核心仍是讨论串

策略：
- 优先考虑互动量与问答完整度
- 如果存在问题 + 回答主体，应优先展开
- 点赞 / 评论应在默认输出中展示

## 6.3 外链 / 线索池型内容
如果某些星球主要为新闻线索与外链集合，则：
- 默认仍可按“重点展开 + 其余更新”输出
- 但中间数据结构应保留 `topic_cluster` 扩展位
- 后续允许用户自行改造成“议题聚类模式”

默认 MVP 不把“聚类模式”做成强制主路径。

## 7. 数据模型设计

当前 normalized item 已有：
- `circle_name`
- `item_id`
- `url`
- `published_at`
- `author`
- `title_or_hook`
- `content_preview`
- `content_type`
- `engagement_hint`
- `signals`
- `priority`

说明：
- `content_type` 在现有实现中仍可保留，用于兼容旧流水线
- 但 stream digest 不应过度依赖它做强排序结论
- 在新方案中，更推荐把它视为 `guessed_type` / 弱信号，而不是高置信业务标签

stream digest 阶段建议扩展为：

```json
{
  "item_id": "string|null",
  "circle_name": "string",
  "author": "string",
  "published_at": "string|null",
  "title_or_hook": "string",
  "content_preview": "string",
  "detail_excerpt": "string",
  "detail_truncated": true,
  "detail_chars": 520,
  "content_type": "analysis|qa|resource|event|chat|other",
  "guessed_type": "analysis|qa|resource|event|chat|other",
  "engagement_hint": {
    "likes": 12,
    "comments": 4
  },
  "signals": ["original-analysis"],
  "stream_score": 41,
  "summary_mode": "full|compact",
  "is_question": false,
  "is_answer": false,
  "is_elite": false,
  "is_pinned": false,
  "has_images": false,
  "has_links": true,
  "source_mode": "token|browser",
  "source_confidence": "high|medium|low",
  "is_truncated": false,
  "topic_cluster": "optional"
}
```

### 字段说明
- `detail_excerpt`：重点展开区实际使用的正文摘录
- `detail_truncated` / `is_truncated`：标记正文是否不完整
- `detail_chars`：摘录字符数
- `stream_score`：内部排序分数，不默认展示给用户
- `summary_mode`：决定该条进入重点展开还是其余更新
- `is_question` / `is_answer`：为问答型星球预留
- `is_elite` / `is_pinned`：平台原生强信号，优先保留
- `has_images` / `has_links`：客观内容特征，便于低依赖排序
- `guessed_type`：弱分类结果，仅作辅助，不应主导排序
- `source_confidence`：体现当前内容完整度
- `topic_cluster`：预留给后续议题聚类扩展

## 8. 排序与选择逻辑

注意：
- 排序逻辑存在
- 但默认不向用户展示“为什么值得看”文案

## 8.1 默认内部排序信号

### A. 平台原生强信号
高优先级加分：
- `is_elite=true`
- `is_pinned=true`

### B. 内容完整度
加分：
- 有较长正文
- 能提取多段内容
- 有清晰标题与主体

### C. 互动量
加分：
- `likes`
- `comments`

对于问答/讨论型星球，可提高评论权重。

### D. 客观内容特征
加分：
- `has_links=true`
- `has_images=true`

### E. 采集质量
加分：
- `source_mode=token`
- `source_confidence=high`

减分：
- 仅标题
- 仅外链无说明
- 仅预览且明显过短

说明：
- `content_type` / `guessed_type` 只作为弱辅助信号
- MVP 不依赖其做大幅基础分差，避免误分类破坏排序

## 8.2 建议评分公式（MVP）
使用简单、可解释、可直接落地的整数评分。

注意：
- 不再依赖 `content_type` 做大幅基础分差
- 优先使用更客观的原生信号、正文长度、互动量、采集质量

建议公式：

### 平台原生信号
- `is_elite=true`: +30
- `is_pinned=true`: +20

### 正文长度
- `detail_excerpt >= 500`: +12
- `detail_excerpt >= 280`: +8
- `detail_excerpt >= 120`: +4

### 互动量（分阶梯而非直接封顶）
- likes > 50: +10
- likes > 20: +7
- likes > 5: +4
- comments > 30: +14
- comments > 10: +10
- comments > 3: +6

### 客观特征
- `has_links=true`: +5
- `has_images=true`: +5

### 质量修正
- `source_mode=token` and `source_confidence=high`: +8
- `source_mode=browser` and `source_confidence=medium`: +2
- `source_mode=browser` and `source_confidence=low`: -4

### 截断修正
- 若 `is_truncated=true`: 0（不加分，但不直接惩罚）

### 弱辅助信号（可选，低权重）
- `guessed_type=qa|analysis|resource`: +2

### 弱内容降分
- 仅外链标题且无正文说明: -8
- 明显闲聊: -10

## 8.3 重点展开选择规则
- 按星球分组
- 每组按 `stream_score` 排序
- 选择前 1~3 条为 `summary_mode=full`
- 若本组总体质量较弱，只选择 1 条或 2 条，不强行放满 3 条
- 其余设为 `summary_mode=compact`
- 支持星球级 `weight_overrides`，用于实现轻量定制，例如：

```json
{
  "睡前消息的编辑们": {
    "comments_multiplier": 3.0,
    "likes_multiplier": 1.5
  }
}
```

该机制用于把“问答/讨论型星球更看重评论量”的规则真正落到工程里，而不是只停留在说明文字中。

## 9. 采集与中间层设计

## 9.1 Token 模式
目标：
- 优先拿结构化字段
- 尽量保留 author / time / likes / comments
- 若 API 字段允许，尽量保留更多正文文本到 `detail_excerpt`

当前基线脚本：
- `scripts/collect_from_session.py`

需要增强：
1. `normalize_topic()` 增加 `detail_excerpt`
2. 增加 `source_mode=token`
3. 增加 `source_confidence`
4. 增加 `is_question` / `is_answer`
5. 增加 `is_elite` / `is_pinned`（若 API 可见）
6. 增加 `has_images` / `has_links`
7. 增加 `stream_score` 所需字段

### Token 截断判断（MVP）
采用保守策略：
- 若 API 仅返回预览字段（如 `text_preview` / 短文本），缺少完整 `text`，标记 `is_truncated=true`
- 若正文明显以省略形式结束，也标记 `is_truncated=true`
- token 模式并不天然等于完整正文，仍需诚实暴露 `source_confidence`

## 9.2 Browser 模式
目标：
- 在 token 不稳定时提供可用 fallback
- 尽量保留可见卡片正文
- 尽量标记内容是否截断

当前基线脚本：
- `scripts/collect_from_browser.py`

需要增强：
1. 从原始 browser capture 中透传更多字段
2. 根据 DOM / 文本特征标记 `is_truncated`
3. 生成 `detail_excerpt`
4. 设置 `source_mode=browser`
5. 给出 `source_confidence=medium|low`

### Browser 截断判断（MVP）
采用保守策略：
- 文本以 `...` 结尾 → 可能截断
- 存在明显“查看详情 / 展开全文”提示 → 可能截断
- 文本很短但 URL 指向 article/topic → 低置信度

不做复杂的自动详情页跳转。

## 9.3 去重层
现有：
- `scripts/dedupe_and_state.py`

当前不需要大改，保持：
- cursor 去重
- TTL 控制
- bounded state

stream digest 只消费去重后的 items。

## 10. 渲染器设计

## 10.1 新增独立渲染器（推荐）
新增：
- `scripts/render_stream_digest.py`

原因：
- 与 `digest_updates.py` 解耦
- 不污染当前简单日报模式
- 更适合快速迭代布局与格式

## 10.2 输入
输入为 normalized item JSON：
- 直接接受 `collect_from_session.py` / `collect_from_browser.py` 输出
- 或接受去重后的 `new_items.json`

## 10.3 输出
输出 Markdown，默认结构：

```md
# 知识星球信息流摘要
- 覆盖星球：...
- 数据来源：...
- 输出口径：最近可见更新（非严格今日）

## 🪐 学不完根本学不完
### 重点展开
#### 1. 标题
- 作者：...
- 时间：...
- 互动：👍 12 / 💬 4
> 正文大段摘录
> 第二段
> （下略，见原文）
- 原文：URL

### 其余更新
- 标题：一句话摘要（👍 x / 💬 y）
  - URL

## 🪐 睡前消息的编辑们
...
```

## 10.4 长度控制
为避免消息过长，renderer 需要支持：
- `--full-per-circle`：默认 3，允许自动实际输出更少
- `--full-max-chars`：默认 800
- `--compact-max-items`：可选，限制紧凑区最多展示多少条
- `--omit-overview`：可选，给后续嵌入式调用留空间

## 11. Pipeline 设计

## 11.1 保持现有 pipeline
现有：
- `scripts/run_digest_pipeline.py`

可继续保留，用于老的日报模式。

## 11.2 新增 stream pipeline
新增：
- `scripts/run_stream_pipeline.py`

流程：
1. collect（token / browser）
2. dedupe（可选）
3. enrich for stream（计算 `stream_score` / `summary_mode`）
4. render stream digest

### 为什么新增独立 pipeline
- 避免把 `run_digest_pipeline.py` 变成多模式大杂烩
- 让 stream 模式拥有更清晰的入参和输出

## 11.3 enrich 层设计
新增：
- `scripts/enrich_stream_items.py`

职责：
- 计算 `detail_excerpt`
- 标记 `is_truncated`
- 计算 `stream_score`
- 决定 `summary_mode`
- 应用星球级 `weight_overrides`
- 输出统计信息（如 full blocks / compact items / circles count）

这样 renderer 只负责展示，不负责业务判断。

## 12. 建议代码结构

在当前 skill 目录下新增 / 调整如下：

```text
skills/public/zsxq-digest/
├── SKILL.md
├── README.md
├── .gitignore
├── references/
│   ├── stream-digest-layout-v1.md
│   └── stream-digest-implementation-plan.md
├── scripts/
│   ├── collect_from_session.py          # 增强字段保留
│   ├── collect_from_browser.py          # 增强截断/置信度
│   ├── dedupe_and_state.py              # 保持
│   ├── digest_updates.py                # 保持旧日报模式
│   ├── enrich_stream_items.py           # 新增：stream enrich/score/select
│   ├── render_stream_digest.py          # 新增：分星球信息流渲染
│   ├── run_digest_pipeline.py           # 保持旧模式
│   ├── run_stream_pipeline.py           # 新增：stream 模式一键入口
│   ├── export_groups_config.py          # 保持
│   ├── run_browser_bootstrap.py         # 保持
│   └── ...
└── state/
    └── (gitignored runtime state)
```

## 13. 技术栈

## 13.1 默认技术栈（MVP）
- **Python 3.9+**
- Python 标准库：
  - `argparse`
  - `json`
  - `pathlib`
  - `subprocess`
  - `urllib`
  - `typing`
  - `collections`
- Node.js 脚本（仅用于现有 browser/CDP 辅助）
- OpenClaw browser tooling（仅用于运行时 browser fallback）

### 原则
MVP 不引入重量级第三方依赖，理由：
- 更适合 public skill 发布
- 安装负担更小
- 维护成本更低
- 与现有 skill 架构一致

## 13.2 可选增强技术栈（非默认）
后续可选扩展，但不纳入默认 MVP：
- LLM 编排层（用于更强的精华选择 / 聚类 / 重写）
- 更强的浏览器详情页补抓
- 更复杂的 topic cluster 聚类器

这些都应设计成可选增强，而不是 public 默认必需能力。

## 14. CLI 设计建议

## 14.1 enrich_stream_items.py

示例：

```bash
python3 scripts/enrich_stream_items.py \
  /tmp/zsxq-new.json \
  --output /tmp/zsxq-stream.json \
  --full-per-circle 3 \
  --full-max-chars 800
```

## 14.2 render_stream_digest.py

示例：

```bash
python3 scripts/render_stream_digest.py \
  /tmp/zsxq-stream.json \
  --output /tmp/zsxq-stream.md
```

## 14.3 run_stream_pipeline.py

Token 模式：

```bash
python3 scripts/run_stream_pipeline.py \
  --source token \
  --token-file state/session.token.json \
  --groups-file state/groups.json \
  --cursor state/cursor.json \
  --full-per-circle 3 \
  --full-max-chars 800 \
  --print-digest
```

Browser 模式：

```bash
python3 scripts/run_stream_pipeline.py \
  --source browser-file \
  --browser-input browser-capture.json \
  --cursor state/cursor.json \
  --full-per-circle 3 \
  --full-max-chars 800 \
  --print-digest
```

## 15. 实施分期

## Phase 1：方案落地（当前阶段）
- 固化本设计文档
- 评审并形成终版
- 不写业务代码

## Phase 2：MVP coding
- 新增 `enrich_stream_items.py`
- 新增 `render_stream_digest.py`
- 新增 `run_stream_pipeline.py`
- 增强 `collect_from_session.py`
- 增强 `collect_from_browser.py`

交付目标：
- 可从真实采集结果生成一版分星球信息流摘要

## Phase 3：文档接入
- 更新 `README.md`
- 更新 `SKILL.md`
- 把 stream digest 作为新的推荐输出模式之一

## Phase 4：增强（后续）
- 可选 topic cluster
- 可选 LLM 编排增强
- 可选浏览器详情页补抓
- 可选消息长度自适应压缩

## 16. 风险与规避

### 风险 1：消息过长
规避：
- 动态 1~3 条展开
- 可设置 `--full-max-chars`
- 可设置 compact 条数限制

### 风险 2：browser 只能拿到短预览
规避：
- 明确 `is_truncated`
- 不假装是完整正文

### 风险 3：问答型星球与长文型星球混用同一模板导致效果差
规避：
- 在 enrich 层保留星球类型与问答字段
- 默认模板统一，但允许后续微分流

### 风险 4：过早引入 LLM 让 public skill 变重
规避：
- LLM 增强保持 optional
- 默认 MVP 只用 stdlib + 现有链路

## 17. 验收标准

当 MVP 完成后，应满足：

### A. 阅读效率
用户在 15~30 秒内能明确：
- 每个星球这一轮主要有什么内容
- 哪几条被重点展开
- 剩余内容大致是什么

### B. 信息保真
用户能明确区分：
- 原始摘录
- 截断预览
- 紧凑摘要

### C. 可点击性
所有展示条目都能精准跳转到原始 URL。

### D. 可扩展性
开发者拿到中间 JSON 后，可以轻松：
- 改排序
- 改布局
- 改字段
- 加 AI 层

## 18. 当前推荐结论

建议采用以下终版方向：
- **默认模式：忠实还原的分星球信息流摘要**
- **默认风格：少评论、少主观解释、多原文摘录**
- **架构方案：collect -> dedupe -> enrich_stream_items -> render_stream_digest**
- **代码策略：新增独立 stream pipeline，不污染现有日报 pipeline**
- **技术策略：默认仅使用 Python stdlib + 现有 browser/token 链路，LLM 增强保持 optional**

这是当前最稳、最适合 public skill、也最方便后续继续定制化开发的实现路径。
