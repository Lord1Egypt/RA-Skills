# XHS Knowledge Base

本文件定义「知识库」核心能力：把每次分析、选题、发布、回复、复盘中的有效信息，沉淀成可检索、可复用、可追踪的结构化记录。

目标不是存一堆日志，而是让后续决策能快速回答三个问题：
- 这类内容之前怎么做的
- 哪些动作有效、哪些动作失败
- 下一次应该直接复用什么

知识库的固定位置如下：

- 总览入口：`knowledge-base/README.md`
- 细分记录目录：`knowledge-base/accounts/`、`knowledge-base/topics/`、`knowledge-base/patterns/`、`knowledge-base/actions/`、`knowledge-base/reviews/`
- git 策略：细分记录默认本地保存，`.gitignore` 忽略这些运行中积累的 md 文件，只保留目录骨架和总览入口纳入版本管理

## 0. 总原则

- 只存“可复用信息”，不做流水账。
- 优先结构化字段，少写长段描述。
- 结论要带证据指针：来源笔记、帖子 URL、截图、时间点、操作结果。
- 分析结果和动作记录分开存，避免一个条目里混杂太多层次。
- 如果知识库暂时不可写，先完成用户任务，再返回一份结构化摘要，后续补记。

## 1. 目录与数据结构

先遵循目录分层，再决定具体字段。

### 1.1 目录分层

- `knowledge-base/README.md`
  - 只放总览、当前重点、固定索引、搜索提示
  - 不在这里堆大段流水账
- `knowledge-base/accounts/`
  - 账号定位、账号诊断、竞品主页分析
- `knowledge-base/topics/`
  - 选题候选、争议点、标题骨架、内容方向
- `knowledge-base/patterns/`
  - 爆款结构、封面层级、互动机制、可复用 pattern
- `knowledge-base/actions/`
  - 发布、回复、下载、抓取、复刻等操作记录
- `knowledge-base/reviews/`
  - 结果复盘、失败原因、回退策略、下次修正

### 1.2 建议的数据结构

建议把知识库拆成 5 类记录：

1. `account`
   - 账号定位、人设、内容支柱、风格约束
2. `topic`
   - 选题候选、适用场景、争议点、标题模板
3. `pattern`
   - 可复用的爆款结构、互动钩子、封面层级、评论机制
4. `action`
   - 具体操作记录：分析、发布、回复、下载、复刻
5. `review`
   - 结果复盘：什么有效、什么无效、下次如何调整

### 1.3 通用字段

每条记录建议至少包含：

```yaml
id: 2026-03-19-confirmation-comment-hook
type: pattern
status: active # active | deprecated | experimental
created_at: 2026-03-19T10:20:00+08:00
updated_at: 2026-03-19T10:45:00+08:00
source:
  kind: xhs_post # xhs_post | notification | publish_flow | manual
  url: "https://www.xiaohongshu.com/explore/..."
  account: "账号名"
  note_id: "可选"
summary: "一句话结论"
evidence:
  - "截图或快照说明"
  - "关键字段或页面状态"
tags:
  - drama-watch
  - title-hook
confidence: medium # low | medium | high
next_action: "下一次要怎么用"
```

### 1.4 分类型字段

- `account`
  - `audience`
  - `content_pillars`
  - `tone_rules`
  - `red_lines`
- `topic`
  - `problem`
  - `angle`
  - `supporting_signals`
  - `risk_level`
- `pattern`
  - `title_template`
  - `cover_template`
  - `body_template`
  - `cta_template`
  - `fit_conditions`
- `action`
  - `task_type`
  - `input`
  - `steps_taken`
  - `result`
  - `blocker`
- `review`
  - `what_worked`
  - `what_failed`
  - `why`
  - `fix_next_time`

## 2. 笔记模板

### 2.1 分析记录模板

适用于首页推荐流分析、账号分析、选题灵感。

```markdown
---
id: 2026-03-19-taipingnian-argument-patterns
type: review
status: active
created_at: 2026-03-19T10:20:00+08:00
source_url: https://www.xiaohongshu.com/explore/...
account: 账号名
tags: [topic, hook, pattern]
---

# 结论
一句话写清楚这次分析最重要的发现。

# 证据
- 关键帖子 / 账号
- 关键标题或封面特征
- 互动信号

# 可复用点
- 标题模板
- 封面结构
- 正文节奏
- 评论区触发词

# 风险
- 容易踩线的地方
- 不适合复用的部分

# 下一步
- 下一次直接复用什么
- 下一次要避免什么
```

### 2.2 动作记录模板

适用于发布、回复、下载、抓取、复刻等执行动作。

```markdown
---
id: 2026-03-19-publish-taipingnian-note
type: action
status: active
created_at: 2026-03-19T10:30:00+08:00
task_type: publish
input: "太平年剧情讨论"
result: success
---

# 动作
做了什么，按时间顺序写 3-5 条。

# 结果
成功 / 失败 / 部分成功。

# 关键阻塞
如果失败，卡在哪一步。

# 复用建议
下次同类任务优先怎么做。
```

### 2.3 文件命名模板

为了方便 agentic search，细分记录建议按“日期 + brief”命名：

```text
knowledge-base/accounts/2026-03-19-drama-watch-positioning.md
knowledge-base/topics/2026-03-19-taipingnian-argument-hooks.md
knowledge-base/patterns/2026-03-19-confirmation-comment-hook.md
knowledge-base/actions/2026-03-19-publish-taipingnian-note.md
knowledge-base/reviews/2026-03-19-reply-flow-retrospective.md
```

命名原则：

- 日期放最前，方便按时间排序
- brief 保留账号名、主题词、动作词或结论词，方便全文检索
- 一份文件只记录一个核心结论或一次完整动作

## 3. 更新时机

建议在以下节点写入知识库：

1. 任务前
   - 先读 `knowledge-base/README.md`
   - 再检索历史记录，避免重复试错
2. 任务中
   - 当出现新结论、新结构、新封面模板、新风险信号时，立刻记一条临时记录
3. 任务后
   - 每次完成分析、发布、回复、复刻后补写结果
4. 失败后
   - 失败原因、回退策略、可替代路径必须单独记
5. 周期复盘时
   - 把临时记录合并成稳定 pattern，过期内容降级或废弃

## 4. 检索方式

检索目标是“快速找到能直接用的东西”，不是盲目全文翻找。

### 4.1 推荐检索维度

- 按账号：`account = xxx`
- 按主题：`tags contains drama-watch`
- 按类型：`type = pattern | review | action`
- 按状态：`status = active`
- 按风险：`risk_level = high`
- 按结果：`result = success` 或 `blocker exists`

### 4.2 推荐检索顺序

1. 先读 `knowledge-base/README.md` 的“当前重点”和“固定索引”
2. 再找最近 7-14 天的同类记录
3. 再找同账号、同主题记录
4. 再找同结构 pattern
5. 最后才看历史失败记录

### 4.3 返回格式

检索结果建议返回：
- 匹配条数
- 最相关的 3 条
- 每条的可复用点
- 当前任务可直接采用的动作建议

## 5. 写入规则

- 一条记录只解决一个问题。
- 结论必须可执行，避免“感觉不错”这种模糊表述。
- 证据优先保留摘要，不保留大段原文。
- 同类条目重复出现时，先更新旧条目，再新增条目。
- 对已验证失效的 pattern 标记为 `deprecated`，不要直接删除。

## 6. 失败降级

如果知识库不可用或写入失败：

1. 先完成当前用户任务，不阻塞主流程
2. 返回一份结构化摘要，至少包含：
   - 结论
   - 证据
   - 动作
   - 风险
   - 下一步
3. 标记这次记录待补写
4. 若连续两次无法写入，停止尝试，提示用户当前知识库存储不可用
5. 若仅细分记录目录写入失败，但 `knowledge-base/README.md` 可写，则先把摘要挂到总览入口的“待整理”区域

如果检索失败：

1. 退回到当前会话上下文
2. 用最近一次分析结果作为临时知识
3. 标记“未命中知识库”，避免误以为历史不存在

## 7. 与其他能力的衔接

- 首页推荐流分析：优先沉淀 `pattern` 和 `topic`
- 账号分析：优先沉淀 `account` 和 `review`
- 选题灵感：优先沉淀 `topic`
- 发布与回复：优先沉淀 `action`
- 爆款笔记复刻：优先沉淀 `pattern`，再补 `review`

总览入口的职责：

- 保留当前账号的固定定位摘要
- 链接最近高价值的细分记录
- 记录当前最值得复用的 3-5 条 pattern
- 标出“待整理”的临时结论，避免丢失

## 8. 最小可执行输出

当需要把知识库结果直接给用户时，建议输出：

1. `结论`
2. `可复用规则`
3. `风险点`
4. `下一步动作`

这样可以保证分析结果既能被人读懂，也能被后续流程直接消费。
