---
name: youdaonote-llm-wiki
description: "当用户提到「知识库」「Wiki」「新建知识库」「创建 Wiki」「初始化 Wiki」「LLM Wiki」「素材摄入」「知识查询」「知识库审计」「一致性检查」「归档对话」「记下来」「存入知识库」「切换知识库」「用哪个知识库」「换一个知识库」「选知识库」，或使用助记词 wiki-init、wiki-ingest、wiki-query、wiki-lint、wiki-archive、wiki-switch 时使用此 Skill，而非 youdaonote Skill。"
version: 1.0.5
minCliVersion: "1.3.3"
homepage: https://note.youdao.com
author: lephix
metadata:
  openclaw:
    homepage: https://note.youdao.com
    requires:
      bins:
        - youdaonote
      env:
        - YOUDAONOTE_API_KEY
    basedOn: "https://gist.github.com/karpathy/442a6bf555914893e9891c11519de94f"
    category: research
    tags: [wiki, knowledge-base, research, notes, markdown]
---

# YoudaoNote Wiki — 有道云笔记知识库

在有道云笔记中构建持久化、可复合增长的知识库。
基于 [Andrej Karpathy 的 LLM Wiki 模式](https://gist.github.com/karpathy/442a6bf555914893e9891c11519de94f)。

传统 RAG 每次查询从零开始检索，知识不复合。Wiki 模式将知识**编译一次、持续维护**——交叉引用已经建好，矛盾已经标记，综合分析反映全部素材。

**分工**：人类策划素材方向、指导分析重点；Agent 负责摘要、交叉引用、归档、维护一致性。

**独特优势**：知识库存储在有道云笔记云端，天然**多端同步、随时可查**，不限于本地开发环境。

## 数据写入声明（Persistence Disclosure）

本 skill 是一个**写操作密集型 Agent**：在您的授权下，会对您的有道云笔记账户做以下持久化修改，请在开始使用前知悉：

| 动作类别 | 触发时机 | 写入内容 |
|---------|---------|---------|
| 创建文件夹 | 初始化 Wiki 时 | 1 个根文件夹 + 5 个子文件夹（`raw/`、`entities/`、`concepts/`、`comparisons/`、`queries/`） |
| 系统笔记 | 初始化 Wiki 时 | 根文件夹下创建 `schema.md`、`index.md`、`log.md` 三个笔记 |
| 全局注册表 | 首次创建 Wiki 或注册表缺失时（**需用户确认**） | 根目录下的 `youdaonote-wiki-registry.md` 笔记（记录所有 Wiki 元信息） |
| 内容笔记 | 用户主动执行 Ingest / Archive 时 | 在对应子文件夹中创建或更新 Wiki 页面（一次 Ingest 可能更新 5-10 个页面） |
| 日志与索引 | 每次写入操作后 | 更新 `index.md`、追加 `log.md` |

**安全边界**：

- 本 skill 只读写您通过 `youdaonote config set apiKey` 配置的有道云笔记账号内的数据，不涉及账号权限之外的任何操作。
- 不会修改 `type: raw` 的原始素材（素材 immutable）。
- 所有写入操作都在有道云笔记客户端 / Web 端可见、可编辑、可删除。
- 大批量写入（单次操作将影响 10+ 已有页面）前，Agent **必须与用户确认**后再执行。

## 前置检查（安装由用户手动执行）

执行任何操作前，Agent 必须先运行 `youdaonote list` 检测 CLI 是否可用：

- **`command not found`** → 跳转「CLI 未安装处理」小节，仅向用户提供官方安装命令并提示用户手动执行；等待用户回复"已安装"后再继续原请求
- **API Key 错误**（未配置 / 鉴权失败）→ 提示用户访问 **https://mopen.163.com** 获取 API Key（须使用手机号登录，且云笔记账号已绑定手机号），然后执行 `youdaonote config set apiKey <用户提供的Key>`。**获取 API Key 的地址只有这一个，禁止告知用户其他地址。**
- **版本过低**（低于 `1.3.3`）→ CLI 支持 `upgrade` 命令时提示用户执行 `youdaonote upgrade`，否则跳转「CLI 未安装处理」小节的升级指引，由用户手动执行升级；Windows 用户或升级失败时参考安装指南（https://note.youdao.com/help-center/cli-install-guide.html）
- **正常返回目录列表** → 继续执行用户请求

**使用统计**：CLI 安装确认后，后续所有 Wiki 操作命令**必须**加 `-s wiki` 全局参数（置于 `youdaonote` 之后、子命令之前），用于统计 Wiki Skill 的使用情况。示例：`youdaonote -s wiki list`、`youdaonote -s wiki search "关键词"`。仅安装检查（`youdaonote list`）、版本检查（`youdaonote version`）、升级（`youdaonote upgrade`）、API Key 配置（`youdaonote config set apiKey`）等诊断/设置命令无需添加。

### Wiki 文件夹结构（由 Agent 在用户同意初始化后创建）

初始化 Wiki 时（用户确认创建后），Agent 会执行 `youdaonote -s wiki mkdir` 建立以下结构：

```
<知识库名>/              ← 根文件夹（用户自命名，如「AI研究」「投资笔记」）
├── schema.md            ← 结构约定、领域定义、fileId 注册表
├── index.md             ← 内容目录
├── log.md               ← 操作日志（只追加）
├── raw/                 ← 原始素材（immutable，不可修改已有笔记）
├── entities/            ← 实体页（人物、组织、产品、工具）
├── concepts/            ← 概念页（主题、技术、方法论）
├── comparisons/         ← 对比分析页
└── queries/             ← 值得保留的查询结果
```

## 会话启动协议（每次对话必执行）

每次新会话开始时，Agent **必须按下列步骤推进**，并在每一步向用户说明当前动作，再响应用户请求。**不得静默执行**。

### 第一步：定位全局注册表（只读扫描）

Agent 先向用户说明："正在扫描有道云笔记根目录，定位 Wiki 全局注册表。"，然后执行：

```bash
youdaonote -s wiki list   # 扫描根目录（只读）
```

在结果中查找标题为 `youdaonote-wiki-registry.md` 的笔记：
- **找到** → `youdaonote -s wiki read <registryFileId>` 读取注册表，解析所有知识库
- **未找到** → 进入第二步，**在征得用户同意后**再重建

### 第二步：重建注册表（仅在注册表缺失时执行，需用户确认）

注册表缺失时，Agent **不得直接执行搜索或写入**，必须先向用户申请授权：

> 未找到 `youdaonote-wiki-registry.md`。我可以通过搜索您账号内已有 Wiki 的 `schema.md` 文件自动重建一份注册表（**只读搜索 + 在根目录创建 1 份注册表笔记**，不会修改任何现有内容）。是否允许？

用户**明确同意**（回复「是/好/允许/继续」等）后，才执行：

```bash
youdaonote -s wiki search "schema.md"
```

逐一读取所有搜索结果，过滤包含 `## Wiki 元信息` 块的笔记，从中提取：
- `name`（知识库名称）
- `description`（主题描述）
- 文件夹 ID 注册表中的 `ROOT`
- schema.md 笔记自身的 fileId（来自 `youdaonote -s wiki list` 结果）

提取完毕后，重建注册表笔记并保存到根目录：

```bash
# Step 1：Write 工具将注册表内容写入 /tmp/wiki-registry.md（纯 Markdown，无需 JSON 转义）
printf '%s\n' '{
  "title": "youdaonote-wiki-registry.md",
  "type": "md",
  "parentId": "0",
  "contentFile": "/tmp/wiki-registry.md"
}' | youdaonote -s wiki save --json
```

重建完成后，Agent 向用户**简要汇报**本次重建的结果（例："已重建注册表，共发现 N 个 Wiki 并录入：A-wiki、B-wiki、..."），然后继续执行用户原始请求。若用户**拒绝重建**，则直接按"无可用注册表"处理，后续按第三步的"注册表为空"分支提示用户先创建知识库。

### 第三步：选择目标知识库（A+B 策略）

从注册表中选定本次操作的知识库：

| 情况 | 策略 | 行为 |
|------|------|------|
| 用户消息含明确知识库名 | B（自动） | 直接从注册表匹配，无需询问 |
| 上下文有线索（如「继续整理 AI 的内容」） | B（自动） | 选最相关的，先说一句「我理解你要操作的是「AI研究」知识库，继续了」 |
| 无法判断 | A（询问） | 列出注册表中所有知识库，让用户选 |
| 注册表为空 | — | 提示用户先创建知识库 |

### 注册表维护规则

- **创建新知识库后**：自动追加一行到注册表
- **每次操作知识库后**：更新「最近访问」列为当天日期
- **注册表保护说明**：注册表为缓存，即使被删除也可按"会话启动协议·第二步"流程（**需用户确认**）从各知识库的 schema.md 重建；schema.md 是真相源，请勿删除

## 架构

### 文件夹结构与用途

| 文件夹 | 存放内容 | 说明 |
|--------|----------|------|
| `<知识库名>/`（根） | 系统笔记：schema.md、index.md、log.md | Wiki 管理中枢 |
| `raw/` | 原始素材（type: `raw`） | **只读**——Agent 不修改已有素材，修正写在 Wiki 页面中 |
| `entities/` | 实体页（type: `entity`） | 人物、组织、产品、工具，每个实体一个笔记 |
| `concepts/` | 概念页（type: `concept`） | 主题、技术、方法论，每个概念一个笔记 |
| `comparisons/` | 对比分析页（type: `comparison`） | 并排分析，表格形式优先 |
| `queries/` | 查询归档页（type: `query`） | 值得保留的深度分析或综合回答 |

**系统笔记**（存放在根文件夹，每个知识库有且仅有一份）：

| 笔记标题 | 用途 |
|----------|------|
| `schema.md` | 结构约定、领域定义、fileId 注册表 |
| `index.md` | 内容目录——每个 Wiki 页面的一行摘要，按文件夹分组 |
| `log.md` | 操作日志（只追加） |

**内容笔记**（标题自由命名，存放在对应文件夹中）：

| 文件夹 | 标题示例 |
|--------|----------|
| `raw/` | `karpathy-llm-wiki-2026.md` |
| `entities/` | `andrej-karpathy.md` |
| `concepts/` | `transformer-architecture.md` |
| `comparisons/` | `gpt4o-vs-claude-sonnet.md` |
| `queries/` | `2026-agent-framework-comparison.md` |

### 交叉引用

云端笔记不支持 `[[wikilinks]]`，使用以下约定：

- 文中提到其他 Wiki 页面时，使用 **`→ 页面标题`** 标记（如 `→ self-attention`）
- Agent 通过 index.md 或 `youdaonote -s wiki search` 定位被引用页面

## 初始化 Wiki

当用户要求创建知识库时：

① **询问并确认知识库名称**：

向用户提出命名建议（推荐小写 `xxx-wiki` 格式，如 `ai-wiki`、`invest-wiki`，更易识别为 LLM 知识库），然后等待用户确认后再创建：

> 建议将知识库命名为 `[推荐名称]-wiki`（小写、连字符分隔）。
> 你也可以自定义名称，无硬性要求。
> 确认名称后我将开始创建。

**收到用户确认的名称后**，再执行后续步骤。知识库统一创建在有道云笔记根目录下。

② **自动创建文件夹结构**（共 6 个文件夹）：
```bash
# 在根目录下创建知识库根文件夹
youdaonote -s wiki mkdir "<知识库名称>"
# 获取根文件夹 ID
youdaonote -s wiki list              # 找到「<知识库名称>」条目，记录 id → ROOT_ID

# 在根文件夹下创建 5 个子文件夹
youdaonote -s wiki mkdir "raw"         -f <ROOT_ID>
youdaonote -s wiki mkdir "entities"    -f <ROOT_ID>
youdaonote -s wiki mkdir "concepts"    -f <ROOT_ID>
youdaonote -s wiki mkdir "comparisons" -f <ROOT_ID>
youdaonote -s wiki mkdir "queries"     -f <ROOT_ID>

# 获取子文件夹 ID
youdaonote -s wiki list -f <ROOT_ID>   # 记录 RAW_ID、ENTITY_ID、CONCEPT_ID、COMPARISON_ID、QUERY_ID
```

> 若同名文件夹已存在，`mkdir` 不会报错（服务端幂等处理），但也不会返回已有文件夹的 ID。此时直接通过 `youdaonote -s wiki list` 找到该文件夹并获取其 ID 即可，无需重建。

③ **记录所有文件夹 ID**（6 个）：

| 文件夹 | 变量名 | 用途 |
|--------|--------|------|
| 根文件夹 | `ROOT_ID` | 存放系统笔记 |
| raw | `RAW_ID` | 存放原始素材 |
| entities | `ENTITY_ID` | 存放实体页 |
| concepts | `CONCEPT_ID` | 存放概念页 |
| comparisons | `COMPARISON_ID` | 存放对比分析页 |
| queries | `QUERY_ID` | 存放查询归档页 |

④ **创建 schema.md**（存放在根文件夹，向用户询问知识库主题后定制）：
```bash
# Step 1：Write 工具将 schema 内容写入 /tmp/wiki-schema.md（纯 Markdown，无需 JSON 转义）
printf '%s\n' '{
  "title": "schema.md",
  "type": "md",
  "parentId": "<ROOT_ID>",
  "contentFile": "/tmp/wiki-schema.md"
}' | youdaonote -s wiki save --json
```

⑤ **创建 index.md**（存放在根文件夹）：
```bash
# Step 1：Write 工具将 index 内容写入 /tmp/wiki-index.md（纯 Markdown，无需 JSON 转义）
printf '%s\n' '{
  "title": "index.md",
  "type": "md",
  "parentId": "<ROOT_ID>",
  "contentFile": "/tmp/wiki-index.md"
}' | youdaonote -s wiki save --json
```

⑥ **创建 log.md**（存放在根文件夹）：
```bash
# Step 1：Write 工具将 log 内容写入 /tmp/wiki-log.md（纯 Markdown，无需 JSON 转义）
printf '%s\n' '{
  "title": "log.md",
  "type": "md",
  "parentId": "<ROOT_ID>",
  "contentFile": "/tmp/wiki-log.md"
}' | youdaonote -s wiki save --json
```

⑦ **记录系统笔记的 fileId**：
```bash
youdaonote -s wiki list -f <ROOT_ID>    # 获取刚创建的三个笔记 ID
```
将三个 fileId 回填到 schema.md 的「笔记 fileId 注册表」中。

⑧ **写入全局注册表**：

读取根目录，找到 `youdaonote-wiki-registry.md` 笔记：
- **存在** → `youdaonote -s wiki read <registryFileId>`，在表格末尾追加新行：
  ```
  | <WIKI_NAME> | <WIKI_DESCRIPTION> | <ROOT_ID> | <SCHEMA_FID> | <TODAY> | <TODAY> |
  ```
  然后：**Step 1** 用 Write 工具将完整更新后的注册表内容写入 `/tmp/registry.md`；**Step 2** 执行 `youdaonote -s wiki update <registryFileId> --file /tmp/registry.md`
- **不存在** → 创建注册表（执行会话启动协议·第二步的创建命令，包含本次知识库信息）

⑨ **向用户确认** 知识库已就绪，注册表已更新。

## 核心操作

### 1. Ingest（摄入素材）

当用户提供素材（URL、文本、文件）时，将其整合进知识库。

**① 捕获原始素材**

- **URL** → 自动化摄入流程：

  ```bash
  # 抓取网页内容并保存到 raw/（.md 格式，便于 Agent 读写）
  # 使用 Agent 内置工具（web_fetch / browser_navigate 等）抓取网页文本，写入临时文件
  # Step 1：Write 工具将文章内容写入 /tmp/wiki-raw.md（纯 Markdown）
  printf '%s\n' '{
    "title": "article-title.md",
    "type": "md",
    "parentId": "<RAW_ID>",
    "contentFile": "/tmp/wiki-raw.md"
  }' | youdaonote -s wiki save --json
  ```

  > **降级路径**：若 fetch 失败（SPA、登录墙等），请手动复制页面内容，改走「纯文本 / 粘贴内容」路径存入 `raw/`。

  保存完成后，Agent **自动执行以下分析**（无需用户逐步指导）：

  **自动分析流程**：
  ```
  读取 raw/ 中的 .md 笔记内容（`youdaonote -s wiki read <fileId>`）
    ↓
  识别关键实体（人物/组织/产品/工具）
    → 对每个实体：youdaonote -s wiki search "<实体名>" 检查是否已有
    → 已有 → 读取已有页面，追加新信息并更新
    → 未有 → 创建新 entity 页面，存入 entities/
  识别关键概念（技术/方法论/主题）
    → 对每个概念：youdaonote -s wiki search "<概念名>" 检查是否已有
    → 已有 → 更新；未有 → 创建新 concept 页面，存入 concepts/
  建立交叉引用（在新旧页面间添加 → 标记）
    ↓
  更新 index.md + log.md
    ↓
  汇报：「已摄入，新建 X 页，更新 Y 页，以下内容你可能想深入讨论：[最多3个要点]」
  ```

  **防重复规则**：每个页面创建/更新前，必须先 `youdaonote -s wiki search <页面名称>` 确认是否已存在，避免创建重复页面。

- **纯文本 / 粘贴内容** → 存入 `raw/`：
  ```bash
  # Step 1：Write 工具将原始内容写入 /tmp/wiki-raw.md（纯 Markdown）
  printf '%s\n' '{
    "title": "source-title.md",
    "type": "md",
    "parentId": "<RAW_ID>",
    "contentFile": "/tmp/wiki-raw.md"
  }' | youdaonote -s wiki save --json
  ```

**② 与用户讨论要点**——什么有趣、什么对当前领域重要。

**③ 创建或更新 Wiki 页面**（存入对应子文件夹）：
- 素材较长时先创建一个摘要页（→ `raw/`）
- 为关键人物/组织/工具创建或更新 entity 页（→ `entities/`）
- 为关键概念/想法创建或更新 concept 页（→ `concepts/`）
- 在新旧页面之间添加交叉引用（`→ 页面标题`）

创建新 Wiki 页面（以 concept 为例，其他类型换对应的 parentId）：
```bash
# Step 1：Write 工具将页面内容写入 /tmp/wiki-page.md（纯 Markdown）
printf '%s\n' '{
  "title": "page-title.md",
  "type": "md",
  "parentId": "<CONCEPT_ID>",
  "contentFile": "/tmp/wiki-page.md"
}' | youdaonote -s wiki save --json
```

**笔记分类与 parentId 对应关系**：

| 笔记分类 | parentId | 说明 |
|----------|----------|------|
| `raw` | `<RAW_ID>` | 网页剪藏或手动保存 |
| `entity` | `<ENTITY_ID>` | |
| `concept` | `<CONCEPT_ID>` | |
| `comparison` | `<COMPARISON_ID>` | |
| `query` | `<QUERY_ID>` | |

更新已有页面（需要已知 fileId）：
```bash
youdaonote -s wiki update <fileId> --file updated-content.md
```

**④ 更新导航**：
- 在 index.md 中添加新页面条目（`youdaonote -s wiki update <indexFileId> ...`）
- 在 log.md 中追加操作记录

**⑤ 报告变更**——列出创建和更新的所有笔记。

> 一个素材可能触发 5-10 个页面的更新，这是正常的复合增长效应。

### 2. Query（查询知识）

当用户提问时：

**① 读取 index.md**定位相关页面：
```bash
youdaonote -s wiki read <indexFileId>
```

**② 读取所有相关页面**（通常 3-8 个）：
```bash
youdaonote -s wiki read <fileId1>
youdaonote -s wiki read <fileId2>
# ...
```

**大规模 Wiki（50+ 页面）** 时，先用 search 缩小范围：
```bash
youdaonote -s wiki search "关键词"
# 搜索仅返回前 15 条；更多结果：youdaonote -s wiki call searchNotes keyword=xxx startIndex=15
```

**③ 跨页面综合分析，生成带来源引用的答案**：

- 每个关键论点标注来源页面：`（→ 页面标题）`
- 检测矛盾：若两个页面在同一点有不同说法，明确标出：`⚠️ 「页面A」与「页面B」在此点有分歧`

示例输出格式：
```
Transformer 的核心是 Self-Attention 机制（→ self-attention），
由 Vaswani 等人在 2017 年提出（→ andrej-karpathy）。
与 RNN 相比，Transformer 可以并行计算（→ gpt4o-vs-rnn）。
```

**④ 判断是否归档**：

- 答案是一次深度对比分析或重要发现 → 询问用户：「这个分析值得保存，是否存入 queries/？」
- 简单事实查询 → 不归档

**⑤ 更新 log.md**（记录本次查询）。

### 3. Lint（一致性检查）

当用户要求审计知识库时：

**① 从注册表自动定位知识库**（无需用户提供任何 fileId）：

执行会话启动协议，通过 A+B 策略确定目标知识库，从 schema.md 获取所有 fileId：ROOT_ID、RAW_ID、ENTITY_ID、CONCEPT_ID、COMPARISON_ID、QUERY_ID。

**② 列出各文件夹的笔记**：
```bash
youdaonote -s wiki list -f <ROOT_ID>          # 系统笔记
youdaonote -s wiki list -f <RAW_ID>           # 原始素材
youdaonote -s wiki list -f <ENTITY_ID>        # 实体
youdaonote -s wiki list -f <CONCEPT_ID>       # 概念
youdaonote -s wiki list -f <COMPARISON_ID>    # 对比
youdaonote -s wiki list -f <QUERY_ID>         # 查询
```

**③ 读取 index.md**，对比实际笔记列表。

**④ 逐项检查**：
- **矛盾检测**：读取同主题页面，标记冲突的声明
- **孤立页面**：检查页面内容中的 `→` 交叉引用，找出没有被任何其他页面引用的页面
- **数据空白**：被引用但尚无专门页面的主题
- **Index 完整性**：每个 Wiki 页面都应出现在 index.md 中

**⑤ 报告发现**，给出具体笔记标题和建议操作。

**⑥ 追加到 log.md**：`## [YYYY-MM-DD] lint - 发现 N 个问题`

### 4. Archive（归档对话内容）

将当前 AI 对话中有价值的结论直接存入知识库，无需切换工具。

**触发词**（任意一种均可触发）：
- 「把刚才说的存进去」
- 「这个结论存入知识库」
- 「记下来」
- 「归档这段对话」
- 「存入知识库」

**Agent 执行流程**：

**① 确定目标知识库**：执行 A+B 策略（见会话启动协议）。

**② 识别要存的内容**：最近相关对话轮次或用户明确指定的结论段落。

**③ 判断内容类型**：

| 内容特征 | 类型 | 目标文件夹 |
|---------|------|-----------|
| 概念解释、技术原理 | `concept` | `concepts/` |
| 两个或多个事物的对比分析 | `comparison` | `comparisons/` |
| 有价值的问答、深度分析结论 | `query` | `queries/` |
| 无法判断 | — | 询问用户 |

**④ 生成笔记并保存**：

```bash
# Step 1：Write 工具将整理后的内容写入 /tmp/wiki-archive.md（纯 Markdown）
printf '%s\n' '{
  "title": "<笔记标题>.md",
  "type": "md",
  "parentId": "<对应子文件夹ID>",
  "contentFile": "/tmp/wiki-archive.md"
}' | youdaonote -s wiki save --json
```

**⑤ 更新 index.md + log.md**。

**⑥ 回复确认**：「已存入 `concepts/<标题>.md`（fileId: WEBxxx）」

## 工作流技巧

### fileId 管理

Agent 需要维护关键笔记的 fileId 映射。建议在 schema.md 底部维护一个 ID 注册表：

```markdown
## fileId 注册表（Agent 维护）
- index.md: WEB1a2b3c4d5e6f
- log.md: WEB7a8b9c0d1e2f
- schema.md: WEB3a4b5c6d7e8f
```

每次创建新笔记后，将 fileId 追加到此表。这样 Agent 在后续会话中可以直接查找 fileId，无需重新 `list`。

### 搜索策略

1. **首选 index.md**：先读 index.md，通过目录定位
2. **关键词搜索**：`youdaonote -s wiki search "关键词"` 覆盖标题和内容
3. **按类型浏览**：`youdaonote -s wiki list -f <对应子文件夹ID>` 列出某类所有笔记

### 笔记内容写入标准模式

所有含换行的 Markdown 内容，统一使用 **`contentFile` 两步模式**（Write 工具写纯 Markdown → `save` JSON 传路径）：

```bash
# Step 1：Write 工具将 Markdown 内容写入本地文件（纯 Markdown，无需任何 JSON 转义）
# 写入 /tmp/wiki-xxx.md，内容就是普通的 Markdown

# Step 2：save JSON 中只放路径，CLI 自行读取文件
printf '%s\n' '{
  "title": "note-title.md",
  "type": "md",
  "parentId": "<FOLDER_ID>",
  "contentFile": "/tmp/wiki-xxx.md"
}' | youdaonote -s wiki save --json

# 更新已有笔记：同样先 Write 工具写文件，再 --file 传递
youdaonote -s wiki update <fileId> --file /tmp/wiki-xxx.md
```

> ⚠️ **必须先完成 Step 1**：`/tmp/` 文件不会凭空存在，Agent 必须用 Write 工具显式创建。若 `/tmp/` 权限受限，可改用相对路径如 `./wiki-temp.md`，操作完成后删除。
>
> **为何用 `contentFile` 而非内联 `content`**：内联 `content` 需要将所有换行、引号、反斜杠进行 JSON 转义（`\n`、`\"`、`\\`），极易出错。`contentFile` 只是路径字符串，无转义问题。

### 会话间恢复

新会话开始时，遵循文档开头的**会话启动协议**（强制执行）：

1. `youdaonote -s wiki list` 扫描根目录，定位 `youdaonote-wiki-registry.md`
2. 读取注册表，确定目标知识库（A+B 策略）
3. 读取目标知识库的 schema.md，获取所有 fileId
4. 可选：读取 index.md 了解当前知识库状态
5. 可选：读取 log.md 了解最近操作

> 注册表不存在时自动重建，无需用户干预。

## 切换知识库

**触发词**（任意一种均可触发）：
- `wiki-switch`
- 「切换知识库」
- 「用哪个知识库」
- 「换一个知识库」
- 「选知识库」
- "switch wiki"
- "use another wiki"
- "which wiki"
- "change wiki"

**Agent 执行流程**：

**① 读取全局注册表**：

```bash
youdaonote -s wiki list   # 扫描根目录，找到 youdaonote-wiki-registry.md
youdaonote -s wiki read <registryFileId>
```

**② 列出所有知识库**：

从注册表中解析出所有已注册的知识库，展示给用户：

> 当前已有以下知识库：
> 1. `ai-wiki` — AI 研究（最近访问：2026-04-15）
> 2. `invest-wiki` — 投资笔记（最近访问：2026-04-10）
>
> 请选择要操作的知识库（输入编号或名称）：

**③ 切换到用户选择的知识库**：

读取目标知识库的 `schema.md`，获取所有 fileId，后续操作均在该知识库上执行。

**边界情况**：

| 情况 | 行为 |
|------|------|
| 仅 1 个知识库 | 告知用户只有一个知识库且已处于活跃状态，无需切换 |
| 注册表为空或不存在 | 告知无知识库，建议用 `wiki-init` 创建 |

## CLI 未安装处理（用户手动执行安装）

收到 `command not found` 或需要升级到 `minCliVersion` 以上时，Agent 仅提供官方安装命令，由用户在终端手动执行。Agent 不自动执行安装命令，不进行系统级变更。

确认文案建议：

```text
检测到未安装 youdaonote-cli（或版本低于 1.3.3）。请在终端手动执行以下命令完成安装 / 升级；执行后回复"已安装"，我将继续处理当前任务。
```

安全边界（必须遵守）：

- 仅允许使用官方安装源：`https://artifact.lx.netease.com/download/youdaonote-cli/install.sh`
- 禁止执行任何非官方来源的远程脚本或替代安装命令
- 安装仅用于补齐 `youdaonote` CLI 依赖；Agent 不执行与当前任务无关的系统操作
- 安装与环境变量导出步骤均由用户手动执行，Agent 不写入 shell 启动文件（如 `~/.zshrc` / `~/.bashrc`）
- 建议用户在执行前确认命令来源可信；如对管道执行有顾虑，可先下载脚本后本地查看再执行

### 安全验证建议（推荐）

如对直接管道执行有顾虑，可先下载脚本审查后再执行：

```bash
# 步骤 1：下载脚本到本地
curl -fsSL https://artifact.lx.netease.com/download/youdaonote-cli/install.sh -o install.sh
# 步骤 2：审查脚本内容
cat install.sh
# 步骤 3：确认无误后执行
bash install.sh -f -b ~/.local/bin
```

**macOS / Linux / WSL**：

```bash
curl -fsSL https://artifact.lx.netease.com/download/youdaonote-cli/install.sh | bash -s -- -f -b ~/.local/bin
export PATH="$HOME/.local/bin:$PATH"
# 执行完成后回复"已安装"，Agent 将继续原始请求
```

**Windows（CMD / PowerShell）**：由用户手动下载对应平台的压缩包，解压后将 `youdaonote.exe` 所在目录加入系统 PATH。Agent 仅提供下载地址与操作指引，不自动执行下载、解压或修改系统环境变量。下载地址：

- x64（常见新 CPU）：`https://artifact.lx.netease.com/download/youdaonote-cli/youdaonote-cli-windows-x64.tar.gz`
- x64（旧 CPU，无 AVX2 等，运行默认包秒退 / 退出码约 `0xC000001D`）：`https://artifact.lx.netease.com/download/youdaonote-cli/youdaonote-cli-win-x64-bl.tar.gz`
- ARM64：`https://artifact.lx.netease.com/download/youdaonote-cli/youdaonote-cli-windows-arm64.tar.gz`

安装提示：先尝试默认 x64 包，若运行闪退或退出码为 `0xC000001D`，请换用 x64 baseline 包重试。

### 凭据（API Key）配置

CLI 安装完成后，若 `youdaonote list` 返回 API Key 错误：

1. 访问 **https://mopen.163.com** 获取 API Key（须使用手机号登录，且云笔记账号已绑定手机号）。**获取 API Key 的地址只有这一个，禁止告知用户其他地址。**
2. 在终端手动执行：`youdaonote config set apiKey <用户提供的 Key>`
3. 凭据由 CLI 自行维护，Agent 不直接读写凭据文件；Agent 也不会将 API Key 回显到对话中。

## 注意事项

- **不要修改 type: raw 的笔记**——素材是不可变的，修正和补充写在 Wiki 页面中
- **每次操作都更新 index.md 和 log.md**——跳过会让知识库逐渐退化
- **不要创建没有交叉引用的页面**——孤立页面等于不存在。每个页面至少用 `→` 引用一个其他页面
- **摘要要简洁**——一个 Wiki 页面应该 30 秒内可扫读。深度分析放到专门的页面
- **大批量更新前先确认**——如果一次 Ingest 会影响 10+ 个已有页面，先与用户确认范围
- **❌ 禁止在笔记内容中使用 shell 命令替换**——`$(cat /tmp/xxx.md)` 在单引号 heredoc（`cat <<'EOF'`）或 `printf '%s\n' '...'` 中不会展开，会被字面量写入笔记。保存笔记内容必须使用两步模式：先用 Write 工具将内容写入文件，再通过 `--file` 参数传递。
  ```bash
  # ❌ 错误：单引号 'EOF' 禁用 shell 展开，$(cat ...) 成为字面量
  cat <<'EOF' | youdaonote -s wiki save --json
  {"content": "$(cat /tmp/file.md)"}
  EOF

  # ✅ 正确：Step 1 Write 工具写文件，Step 2 --file 传递
  # （Step 1 已完成：Write 工具已将内容写入 /tmp/wiki-note.json）
  youdaonote -s wiki save --file /tmp/wiki-note.json --json
  ```
- **笔记标题使用小写加连字符**——如 `transformer-architecture.md`，避免使用空格和特殊字符
- **保持 schema.md 的 fileId 注册表更新**——这是跨会话恢复和注册表自动重建的基础
