---
name: youdaonote-okf-wiki
description: "当用户提到「OKF」「OKF Wiki」「Open Knowledge Format」「OKF 知识库」「新建 OKF」「创建 OKF bundle」「OKF 摄入」「OKF 查询」「OKF 一致性检查」「OKF 导出」「OKF 归档」「okf-wiki-init」「okf-wiki-ingest」「okf-wiki-query」「okf-wiki-lint」「okf-wiki-export」「okf-wiki-archive」「okf-wiki-switch」时使用此 Skill。基于 OKF v0.1 规范的知识库管理。当用户需要符合开放标准、可导出为 git 仓库、或跨工具交换的知识库时，优先使用此 Skill 而非 youdaonote-llm-wiki。"
version: 1.0.0
minCliVersion: "1.3.3"
homepage: "https://note.youdao.com"
author: "YoudaoNote Team"
category: research
tags: [okf, knowledge-base, open-knowledge-format, research, notes, markdown]
based_on: "https://github.com/GoogleCloudPlatform/knowledge-catalog/blob/main/okf/SPEC.md"
metadata:
  openclaw:
    homepage: "https://note.youdao.com"
    requires:
      bins: ["youdaonote"]
      env: []
    basedOn: "OKF v0.1"
    category: "research"
    tags: ["okf", "knowledge-base", "open-knowledge-format"]
---

# YoudaoNote OKF Wiki — 有道云笔记 OKF 知识库

在有道云笔记中构建符合 [OKF (Open Knowledge Format) v0.1](https://github.com/GoogleCloudPlatform/knowledge-catalog/blob/main/okf/SPEC.md) 规范的持久化知识库。
基于 OKF v0.1 规范 + [youdaonote-llm-wiki](../../skills/youdaonote-llm-wiki/SKILL.md) 成熟模式。

OKF 是一种开放的、对人类和 Agent 都友好的知识表示格式：一组 markdown 文件 + YAML frontmatter，无 schema 注册中心、无中央权威、无必需工具链。它被设计为**可读**（人类无需工具即可阅读）、**可解析**（Agent 无需专用 SDK）、**可 diff**（版本控制友好）、**可移植**（跨工具、跨组织、跨时间）。

传统 RAG 每次查询从零开始检索，知识不复合。OKF 模式将知识**编译一次、持续维护**——交叉引用用标准 markdown 链接建好，frontmatter 让 Agent 可路由和过滤，矛盾已标记，综合分析反映全部素材。

**分工**：人类策划素材方向、指导分析重点；Agent 负责摘要、交叉引用、归档、维护 OKF conformance。

**独特优势**：知识库存储在有道云笔记云端，天然**多端同步、随时可查**，不限于本地开发环境。同时笔记内容原生包含 OKF frontmatter，可随时导出为标准 OKF bundle 供 git 版本控制或跨工具交换。

## 数据写入声明（Persistence Disclosure）

本 skill 是一个**写操作密集型 Agent**：在您的授权下，会对您的有道云笔记账户做以下持久化修改，请在开始使用前知悉：

| 动作类别 | 触发时机 | 写入内容 |
|---------|---------|---------|
| 创建文件夹 | 初始化 OKF 知识库时 | 1 个根文件夹 + 5 个子文件夹（`raw/`、`entities/`、`concepts/`、`comparisons/`、`queries/`） |
| 系统笔记 | 初始化 OKF 知识库时 | 根文件夹下创建 `schema.md`、`index.md`、`log.md` 三个笔记（index.md 和 log.md 为 OKF 保留文件名；log.md 无 frontmatter，index.md 按 §6 无 frontmatter 但 bundle-root 可含 okf_version §11） |
| 全局注册表 | 首次创建 OKF 知识库或注册表缺失时 | 根目录下的 `youdaonote-okf-wiki-registry.md` 笔记（记录所有 OKF 知识库元信息） |
| 内容笔记 | 用户主动执行 Ingest / Archive 时 | 在对应子文件夹中创建或更新 OKF concept 笔记（每条含 `type` frontmatter，一次 Ingest 可能更新 5-10 个笔记） |
| 日志与索引 | 每次写入操作后 | 更新 `index.md`、追加 `log.md`（均遵循 OKF spec §6/§7 格式） |

**安全边界**：

- 本 skill 只读写您通过 `youdaonote config set apiKey` 配置的有道云笔记账号内的数据，不涉及账号权限之外的任何操作。
- 不会修改 `type: Raw` 的原始素材（素材 immutable）。
- 所有写入操作都在有道云笔记客户端 / Web 端可见、可编辑、可删除。
- 大批量写入（单次操作将影响 10+ 已有笔记）前，Agent **必须与用户确认**后再执行。

## 前置检查（安装由用户手动执行）

执行任何操作前，Agent 必须先运行 `youdaonote list` 检测 CLI 是否可用：

- **`command not found`** → 跳转「CLI 未安装处理」小节，仅向用户提供官方安装命令并提示用户手动执行；等待用户回复"已安装"后再继续原请求
- **API Key 错误**（未配置 / 鉴权失败）→ 提示用户访问 **https://mopen.163.com** 获取 API Key（须使用手机号登录，且云笔记账号已绑定手机号），然后执行 `youdaonote config set apiKey <用户提供的Key>`。**获取 API Key 的地址只有这一个，禁止告知用户其他地址。**
- **版本过低**（低于 `1.3.3`）→ CLI 支持 `upgrade` 命令时提示用户执行 `youdaonote upgrade`，否则跳转「CLI 未安装处理」小节的升级指引，由用户手动执行升级；Windows 用户或升级失败时参考安装指南（https://note.youdao.com/help-center/cli-install-guide.html）
- **正常返回目录列表** → 继续执行用户请求

**使用统计**：CLI 安装确认后，后续所有 OKF 操作命令**必须**加 `-s okf` 全局参数（置于 `youdaonote` 之后、子命令之前），用于统计 OKF Skill 的使用情况。示例：`youdaonote -s okf list`、`youdaonote -s okf search "关键词"`。仅安装检查（`youdaonote list`）、版本检查（`youdaonote version`）、升级（`youdaonote upgrade`）、API Key 配置（`youdaonote config set apiKey`）等诊断/设置命令无需添加。

### OKF 文件夹结构（由 Agent 在用户同意初始化后创建）

初始化 OKF 知识库时（用户确认创建后），Agent 会执行 `youdaonote -s okf mkdir` 建立以下结构：

```
<知识库名>/              ← OKF bundle 根目录（用户自命名，如「ai-okf」「invest-okf」）
├── schema.md            ← 结构约定、领域定义、fileId 注册表（youdaonote-okf-wiki 专有系统笔记）
├── index.md             ← 内容目录（OKF 保留文件名，spec §6；bundle-root 可含 okf_version，spec §11）
├── log.md               ← 操作日志（OKF 保留文件名，spec §7，无 frontmatter）
├── raw/                 ← 原始素材（type: Raw，immutable，不可修改已有笔记）
├── entities/            ← 实体页（type: Entity，人物、组织、产品、工具）
├── concepts/            ← 概念页（type: Concept，主题、技术、方法论）
├── comparisons/         ← 对比分析页（type: Comparison）
└── queries/             ← 查询归档页（type: Query）
```

> `index.md` 和 `log.md` 是 OKF v0.1 spec section 3.1 定义的保留文件名。`log.md` 不含 frontmatter。`index.md` 按 §6 不含 frontmatter，但 §11 允许 bundle-root index.md 包含 `okf_version` 字段（唯一例外）。`schema.md` 是 youdaonote-okf-wiki 的云端存储适配层（管理 fileId 注册表），属于 OKF spec 允许的 producer-defined 扩展文件。

> **OKF v0.1 规范参考**：本 skill 的 `references/okf-spec-summary.md` 包含 [OKF v0.1 Spec](https://github.com/GoogleCloudPlatform/knowledge-catalog/blob/main/okf/SPEC.md) 的关键要点摘要，Agent 可在需要时读取以快速参考 spec section 4（Concept Documents）、section 5（Cross-linking）、section 8（Citations）、section 9（Conformance）、section 11（Versioning）。

## 会话启动协议（每次对话必执行）

每次新会话开始时，Agent **必须先执行以下步骤**，再响应用户请求。

### 第一步：定位全局注册表

```bash
youdaonote -s okf list   # 扫描根目录
```

在结果中查找标题为 `youdaonote-okf-wiki-registry.md` 的笔记：
- **找到** → `youdaonote -s okf read <registryFileId>` 读取注册表，解析所有知识库
- **未找到** → 执行自动重建（见下）

### 第二步：自动重建注册表（仅在注册表缺失时执行）

```bash
youdaonote -s okf search "schema.md"
```

逐一读取所有搜索结果，过滤包含 `## OKF 元信息` 块的笔记，从中提取：
- `name`（知识库名称）
- `description`（主题描述）
- 文件夹 ID 注册表中的 `ROOT`
- schema.md 笔记自身的 fileId（来自 `youdaonote -s okf list` 结果）

提取完毕后，重建注册表笔记并保存到根目录：

```bash
# Step 1：Write 工具将注册表内容写入 /tmp/okf-registry.md（纯 Markdown，无需 JSON 转义）
printf '%s\n' '{
  "title": "youdaonote-okf-wiki-registry.md",
  "type": "md",
  "parentId": "0",
  "contentFile": "/tmp/okf-registry.md"
}' | youdaonote -s okf save --json
```

重建过程对用户**无感知**，完成后继续执行用户原始请求。

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
- **注册表保护说明**：注册表为缓存，即使被删除也可从各知识库的 schema.md 自动重建；schema.md 是真相源，请勿删除

## 架构

### 文件夹结构与用途

| 文件夹 | 存放内容 | OKF type 值 | 说明 |
|--------|----------|-------------|------|
| `<知识库名>/`（根） | 系统笔记：schema.md、index.md、log.md | — | OKF bundle 管理中枢 |
| `raw/` | 原始素材 | `Raw` | **只读**——Agent 不修改已有素材，修正写在 concept 页面中 |
| `entities/` | 实体页 | `Entity` | 人物、组织、产品、工具，每个实体一个笔记 |
| `concepts/` | 概念页 | `Concept` | 主题、技术、方法论，每个概念一个笔记 |
| `comparisons/` | 对比分析页 | `Comparison` | 并排分析，表格形式优先 |
| `queries/` | 查询归档页 | `Query` | 值得保留的深度分析或综合回答 |

> OKF type 字段映射遵循 [OKF v0.1 spec section 4.1](https://github.com/GoogleCloudPlatform/knowledge-catalog/blob/main/okf/SPEC.md#41-frontmatter)：type 值不由中央注册，producer 可自定义。此处使用与文件夹同名的 type 值保持一致性，便于 Agent 路由和过滤。

**系统笔记**（存放在根文件夹，每个知识库有且仅有一份）：

| 笔记标题 | 用途 | OKF 定位 |
|----------|------|----------|
| `schema.md` | 结构约定、领域定义、fileId 注册表 | youdaonote-okf-wiki 专有（OKF 允许的扩展文件） |
| `index.md` | 内容目录——每个 concept 的一行摘要，按文件夹分组 | OKF 保留文件名（spec §6 无 frontmatter；bundle-root 可含 okf_version（§11）） |
| `log.md` | 操作日志（只追加），日期分组，最新在前 | OKF 保留文件名（spec §7），无 frontmatter |

**内容笔记**（标题自由命名，存放在对应文件夹中，每个笔记必须包含 OKF frontmatter）：

| 文件夹 | 标题示例 | frontmatter type |
|--------|----------|------------------|
| `raw/` | `karpathy-llm-wiki-2026.md` | `type: Raw` |
| `entities/` | `andrej-karpathy.md` | `type: Entity` |
| `concepts/` | `transformer-architecture.md` | `type: Concept` |
| `comparisons/` | `gpt4o-vs-claude-sonnet.md` | `type: Comparison` |
| `queries/` | `2026-agent-framework-comparison.md` | `type: Query` |

### 交叉引用

遵循 OKF v0.1 spec section 5，使用标准 markdown 链接进行交叉引用：

- 文中提到其他 concept 时，使用 **markdown 链接**标记：`[页面标题](/folder/concept-id.md)`
- 路径以 `/` 开头（bundle-relative 绝对路径），这是 OKF 推荐形式（spec §5.1），在文件移动时更稳定
- Agent 通过 index.md 或 `youdaonote -s okf search` 定位被引用页面
- OKF 要求消费者容忍断链（spec §5.3）——链接目标不存在不是错误，代表尚未编写的知识

示例：
```markdown
Transformer 的核心是 Self-Attention 机制，详见
[self-attention](/concepts/self-attention.md)。
```

## 初始化 OKF 知识库

当用户要求创建知识库时（触发词：`okf-init`、「新建 OKF」「创建 OKF bundle」）：

① **询问并确认知识库名称**：

向用户提出命名建议（推荐小写 `xxx-okf` 格式，如 `ai-okf`、`invest-okf`，更易识别为 OKF 知识库），然后等待用户确认后再创建：

> 建议将知识库命名为 `[推荐名称]-okf`（小写、连字符分隔）。
> 你也可以自定义名称，无硬性要求。
> 确认名称后我将开始创建。

**收到用户确认的名称后**，再执行后续步骤。知识库统一创建在有道云笔记根目录下。

② **自动创建文件夹结构**（共 6 个文件夹）：
```bash
# 在根目录下创建知识库根文件夹
youdaonote -s okf mkdir "<知识库名称>"
# 获取根文件夹 ID
youdaonote -s okf list              # 找到「<知识库名称>」条目，记录 id → ROOT_ID

# 在根文件夹下创建 5 个子文件夹
youdaonote -s okf mkdir "raw"         -f <ROOT_ID>
youdaonote -s okf mkdir "entities"    -f <ROOT_ID>
youdaonote -s okf mkdir "concepts"    -f <ROOT_ID>
youdaonote -s okf mkdir "comparisons" -f <ROOT_ID>
youdaonote -s okf mkdir "queries"     -f <ROOT_ID>

# 获取子文件夹 ID
youdaonote -s okf list -f <ROOT_ID>   # 记录 RAW_ID、ENTITY_ID、CONCEPT_ID、COMPARISON_ID、QUERY_ID
```

> 若同名文件夹已存在，`mkdir` 不会报错（服务端幂等处理），但也不会返回已有文件夹的 ID。此时直接通过 `youdaonote -s okf list` 找到该文件夹并获取其 ID 即可，无需重建。

③ **记录所有文件夹 ID**（6 个）：

| 文件夹 | 变量名 | 用途 |
|--------|--------|------|
| 根文件夹 | `ROOT_ID` | 存放系统笔记 |
| raw | `RAW_ID` | 存放原始素材 |
| entities | `ENTITY_ID` | 存放实体页 |
| concepts | `CONCEPT_ID` | 存放概念页 |
| comparisons | `COMPARISON_ID` | 存放对比分析页 |
| queries | `QUERY_ID` | 存放查询归档页 |

④ **创建 schema.md**（存放在根文件夹，向用户询问知识库主题后定制）。

schema.md 内容包含 `## OKF 元信息` 块（用于注册表自动重建识别）：

```markdown
# <知识库名称> — OKF 知识库

## OKF 元信息
- name: <知识库名称>
- description: <主题描述>
- okf_version: 0.1  # 内部字段，标识此知识库遵循 OKF v0.1；不同于 §11 的官方版本声明（§11 声明写在 bundle-root index.md 的 frontmatter 中）
- root_id: <ROOT_ID>

## fileId 注册表（Agent 维护）
- index.md: <INDEX_FID>
- log.md: <LOG_FID>
- schema.md: <SCHEMA_FID>
- raw/: <RAW_ID>
- entities/: <ENTITY_ID>
- concepts/: <CONCEPT_ID>
- comparisons/: <COMPARISON_ID>
- queries/: <QUERY_ID>
```

保存命令：
```bash
# Step 1：Write 工具将 schema 内容写入 /tmp/okf-schema.md（纯 Markdown，无需 JSON 转义）
printf '%s\n' '{
  "title": "schema.md",
  "type": "md",
  "parentId": "<ROOT_ID>",
  "contentFile": "/tmp/okf-schema.md"
}' | youdaonote -s okf save --json
```

⑤ **创建 index.md**（存放在根文件夹，遵循 OKF spec §6）。

bundle-root index.md 可选含 `okf_version` frontmatter（spec §11 唯一允许的 index.md frontmatter）：
```markdown
---
okf_version: "0.1"
---

# <知识库名称> — 内容目录
...
```

index.md 内容（OKF 格式——目录列表，支持 progressive disclosure）：
```markdown
# <知识库名称> — 内容目录

## Raw（原始素材）

* （暂无）

## Entities（实体）

* （暂无）

## Concepts（概念）

* （暂无）

## Comparisons（对比分析）

* （暂无）

## Queries（查询归档）

* （暂无）
```

保存命令：
```bash
# Step 1：Write 工具将 index 内容写入 /tmp/okf-index.md（纯 Markdown，无需 JSON 转义）
printf '%s\n' '{
  "title": "index.md",
  "type": "md",
  "parentId": "<ROOT_ID>",
  "contentFile": "/tmp/okf-index.md"
}' | youdaonote -s okf save --json
```

⑥ **创建 log.md**（存放在根文件夹，遵循 OKF spec §7，**无 frontmatter**）。

log.md 内容（OKF 格式——日期分组，ISO 8601，最新在前）：
```markdown
# OKF Bundle 更新日志

## <YYYY-MM-DD>

* **Initialization**: 创建 OKF 知识库 `<知识库名称>`，建立文件夹结构和系统笔记。
```

保存命令：
```bash
# Step 1：Write 工具将 log 内容写入 /tmp/okf-log.md（纯 Markdown，无需 JSON 转义）
printf '%s\n' '{
  "title": "log.md",
  "type": "md",
  "parentId": "<ROOT_ID>",
  "contentFile": "/tmp/okf-log.md"
}' | youdaonote -s okf save --json
```

⑦ **记录系统笔记的 fileId**：
```bash
youdaonote -s okf list -f <ROOT_ID>    # 获取刚创建的三个笔记 ID
```
将三个 fileId 回填到 schema.md 的「笔记 fileId 注册表」中。

⑧ **写入全局注册表**：

读取根目录，找到 `youdaonote-okf-wiki-registry.md` 笔记：
- **存在** → `youdaonote -s okf read <registryFileId>`，在表格末尾追加新行：
  ```
  | <KB_NAME> | <KB_DESCRIPTION> | <ROOT_ID> | <SCHEMA_FID> | <TODAY> | <TODAY> |
  ```
  然后：**Step 1** 用 Write 工具将完整更新后的注册表内容写入 `/tmp/okf-registry.md`；**Step 2** 执行 `youdaonote -s okf update <registryFileId> --file /tmp/okf-registry.md`
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
  # Step 1：Write 工具将文章内容写入 /tmp/okf-raw.md（包含 OKF frontmatter）
  ```

  raw 笔记内容格式（包含 OKF frontmatter）：
  ```markdown
  ---
  type: Raw
  title: <文章标题>
  description: <一句话摘要>
  tags: [<标签>]
  timestamp: <ISO 8601 datetime>
  resource: <原始 URL>
  ---

  # <文章标题>

  <文章正文内容>
  ```

  保存命令：
  ```bash
  printf '%s\n' '{
    "title": "article-title.md",
    "type": "md",
    "parentId": "<RAW_ID>",
    "contentFile": "/tmp/okf-raw.md"
  }' | youdaonote -s okf save --json
  ```

  > **降级路径**：若 fetch 失败（SPA、登录墙等），请手动复制页面内容，改走「纯文本 / 粘贴内容」路径存入 `raw/`。

  保存完成后，Agent **自动执行以下分析**（无需用户逐步指导）：

  **自动分析流程**：
  ```
  读取 raw/ 中的 .md 笔记内容（`youdaonote -s okf read <fileId>`）
    ↓
  识别关键实体（人物/组织/产品/工具）
    → 对每个实体：youdaonote -s okf search "<实体名>" 检查是否已有
    → 已有 → 读取已有页面，追加新信息并更新
    → 未有 → 创建新 entity 页面，存入 entities/
  识别关键概念（技术/方法论/主题）
    → 对每个概念：youdaonote -s okf search "<概念名>" 检查是否已有
    → 已有 → 更新；未有 → 创建新 concept 页面，存入 concepts/
  建立 markdown 交叉引用（在新旧页面间添加 [title](/folder/id.md) 链接）
    ↓
  更新 index.md + log.md
    ↓
  汇报：「已摄入，新建 X 页，更新 Y 页，以下内容你可能想深入讨论：[最多3个要点]」
  ```

  **防重复规则**：每个页面创建/更新前，必须先 `youdaonote -s okf search <页面名称>` 确认是否已存在，避免创建重复页面。

- **纯文本 / 粘贴内容** → 存入 `raw/`（同样需要 `type: Raw` frontmatter）：
  ```bash
  # Step 1：Write 工具将原始内容写入 /tmp/okf-raw.md（包含 OKF frontmatter）
  printf '%s\n' '{
    "title": "source-title.md",
    "type": "md",
    "parentId": "<RAW_ID>",
    "contentFile": "/tmp/okf-raw.md"
  }' | youdaonote -s okf save --json
  ```

**② 与用户讨论要点**——什么有趣、什么对当前领域重要。

**③ 创建或更新 concept 页面**（存入对应子文件夹，每个笔记必须包含 OKF frontmatter）：
- 素材较长时先创建一个摘要页（→ `raw/`）
- 为关键人物/组织/工具创建或更新 entity 页（→ `entities/`，`type: Entity`）
- 为关键概念/想法创建或更新 concept 页（→ `concepts/`，`type: Concept`）
- 在新旧页面之间添加 markdown 交叉引用（`[title](/folder/concept-id.md)`）

创建新 concept 页面（以 concept 为例，注意 frontmatter 中的 `type` 字段）：

concept 笔记内容格式：
```markdown
---
type: Concept
title: <概念标题>
description: <一句话描述>
resource: <底层资产 URI，抽象概念可省略>
tags: [<标签>]
timestamp: <ISO 8601 datetime>
---

# <概念标题>

<概念正文>

# Citations

[1] [来源标题](URL)
[2] [来源标题](URL)

相关概念：[other-concept](/concepts/other-concept.md)
```

> `resource` 字段标识 concept 描述的底层资产 URI（如数据库表、API 端点）。描述抽象概念的 note 可省略此字段（spec §4.1）。

> OKF v0.1 spec section 8 定义 `# Citations` 为概念文档的约定标题，用于列出支撑正文论点的外部来源。Ingest 时应将素材的原始来源记录在 Citations 中。

保存命令：
```bash
# Step 1：Write 工具将页面内容写入 /tmp/okf-page.md（包含 OKF frontmatter）
printf '%s\n' '{
  "title": "page-title.md",
  "type": "md",
  "parentId": "<CONCEPT_ID>",
  "contentFile": "/tmp/okf-page.md"
}' | youdaonote -s okf save --json
```

**笔记分类与 parentId、OKF type 对应关系**：

| 笔记分类 | OKF type | parentId | 说明 |
|----------|----------|----------|------|
| `Raw` | `type: Raw` | `<RAW_ID>` | 网页剪藏或手动保存 |
| `Entity` | `type: Entity` | `<ENTITY_ID>` | |
| `Concept` | `type: Concept` | `<CONCEPT_ID>` | |
| `Comparison` | `type: Comparison` | `<COMPARISON_ID>` | |
| `Query` | `type: Query` | `<QUERY_ID>` | |

更新已有页面（需要已知 fileId）：
```bash
youdaonote -s okf update <fileId> --file /tmp/okf-updated.md
```

**④ 更新导航**：
- 在 index.md 中添加新页面条目（OKF 格式：`* [Title](relative-url) - description`）
- 在 log.md 中追加操作记录（OKF 格式：日期分组，`* **Update**: ...`）
- 更新命令：`youdaonote -s okf update <indexFileId> --file /tmp/okf-index.md`

**⑤ 报告变更**——列出创建和更新的所有笔记。

> 一个素材可能触发 5-10 个页面的更新，这是正常的复合增长效应。

### 2. Query（查询知识）

当用户提问时：

**① 读取 index.md**定位相关页面：
```bash
youdaonote -s okf read <indexFileId>
```

**② 读取所有相关页面**（通常 3-8 个）：
```bash
youdaonote -s okf read <fileId1>
youdaonote -s okf read <fileId2>
# ...
```

**大规模知识库（50+ 页面）** 时，先用 search 缩小范围：
```bash
youdaonote -s okf search "关键词"
# 搜索仅返回前 15 条；更多结果：youdaonote -s okf call searchNotes keyword=xxx startIndex=15
```

**③ 跨页面综合分析，生成带来源引用的答案**：

- 每个关键论点标注来源页面，使用 OKF markdown 链接引用：`([concept title](/concepts/concept-id.md))`
- 检测矛盾：若两个页面在同一点有不同说法，明确标出：`⚠️ 「页面A」与「页面B」在此点有分歧`

示例输出格式：
```
Transformer 的核心是 Self-Attention 机制
（[self-attention](/concepts/self-attention.md)），
由 Vaswani 等人在 2017 年提出
（[andrej-karpathy](/entities/andrej-karpathy.md)）。
与 RNN 相比，Transformer 可以并行计算
（[gpt4o-vs-rnn](/comparisons/gpt4o-vs-rnn.md)）。
```

**④ 判断是否归档**：

- 答案是一次深度对比分析或重要发现 → 询问用户：「这个分析值得保存，是否存入 queries/？」
- 简单事实查询 → 不归档

**⑤ 更新 log.md**（记录本次查询）。

### 3. Lint（OKF 一致性检查）

当用户要求审计知识库时（触发词：`okf-lint`、「OKF 一致性检查」「OKF conformance check」）：

**① 从注册表自动定位知识库**（无需用户提供任何 fileId）：

执行会话启动协议，通过 A+B 策略确定目标知识库，从 schema.md 获取所有 fileId：ROOT_ID、RAW_ID、ENTITY_ID、CONCEPT_ID、COMPARISON_ID、QUERY_ID。

**② 列出各文件夹的笔记**：
```bash
youdaonote -s okf list -f <ROOT_ID>          # 系统笔记
youdaonote -s okf list -f <RAW_ID>           # 原始素材
youdaonote -s okf list -f <ENTITY_ID>        # 实体
youdaonote -s okf list -f <CONCEPT_ID>       # 概念
youdaonote -s okf list -f <COMPARISON_ID>    # 对比
youdaonote -s okf list -f <QUERY_ID>         # 查询
```

**③ 读取 index.md**，对比实际笔记列表。

**④ OKF v0.1 Conformance 检查**（spec section 9）：

对每个非保留文件名（非 index.md / log.md）的 .md 笔记，逐项检查：

a. **Frontmatter 可解析性**：笔记内容开头是否有 `---` ... `---` 包裹的可解析 YAML frontmatter 块
   - 缺失 → 报告 "missing YAML frontmatter block"，列出笔记标题

b. **type 字段非空**：frontmatter 中是否有非空的 `type` 字段（OKF v0.1 唯一必填字段）
   - 缺失或为空 → 报告 "missing required 'type' field"，列出笔记标题

c. **保留文件名结构**：index.md 遵循 spec §6（目录列表格式）；bundle-root index.md 可含 `okf_version` frontmatter（§11 唯一例外），非 bundle-root index.md 无 frontmatter。log.md 遵循 spec §7（日期分组，ISO 8601，无 frontmatter）
   - 不符合 → 报告具体问题

**⑤ 知识库健康度检查**：

- **矛盾检测**：读取同主题页面，标记冲突的声明
- **孤立页面**：检查页面内容中的 markdown 交叉引用，找出没有被任何其他页面引用的页面
- **数据空白**：被引用但尚无专门页面的主题（断链——OKF 容忍，但值得标记为待编写）
- **Index 完整性**：每个 concept 页面都应出现在 index.md 中

**⑥ 报告发现**：

```
## OKF Conformance: PASS / FAIL

### Conformance 检查
- Frontmatter 可解析：N/N 通过
- type 字段非空：N/N 通过
- 保留文件名结构：index.md ✓ / log.md ✓

### 健康度检查
- 矛盾：X 处
- 孤立页面：Y 个
- 数据空白：Z 个（OKF 容忍断链，建议后续编写）
- Index 完整性：M/M 页面已索引
```

给出具体笔记标题和建议操作。

> **Consumer 容忍原则**（spec §9）：OKF conformance 检查是报告性的，不是拒绝性的。即使 bundle 不完全 conformant，consumer 也不应拒绝——应容忍缺少可选字段、未知 type 值、未知 frontmatter 键、断链、缺少 index.md 等情况。lint 的目的是帮助改进知识库质量，而非阻止消费。

**⑦ 追加到 log.md**：`## <YYYY-MM-DD> * **Update**: lint - 发现 N 个问题`

### 4. Archive（归档对话内容）

将当前 AI 对话中有价值的结论直接存入知识库，无需切换工具。

**触发词**（任意一种均可触发）：
- `okf-archive`
- 「把刚才说的存入 OKF」
- 「这个结论存入 OKF 知识库」
- 「记到 OKF」
- 「归档这段对话到 OKF」
- 「存入 OKF 知识库」

**Agent 执行流程**：

**① 确定目标知识库**：执行 A+B 策略（见会话启动协议）。

**② 识别要存的内容**：最近相关对话轮次或用户明确指定的结论段落。

**③ 判断内容类型**（决定 OKF type 值和目标文件夹）：

| 内容特征 | OKF type | 目标文件夹 |
|---------|----------|-----------|
| 概念解释、技术原理 | `Concept` | `concepts/` |
| 两个或多个事物的对比分析 | `Comparison` | `comparisons/` |
| 有价值的问答、深度分析结论 | `Query` | `queries/` |
| 无法判断 | — | 询问用户 |

**④ 生成笔记并保存**（包含 OKF frontmatter，`type` 必填）：

归档笔记内容格式（以 concept 为例）：
```markdown
---
type: Concept
title: <笔记标题>
description: <一句话描述>
resource: <底层资产 URI，抽象概念可省略>
tags: [<标签>]
timestamp: <ISO 8601 datetime>
---

# <笔记标题>

<归档的对话内容，整理为结构化 Markdown>

相关概念：[other-concept](/concepts/other-concept.md)
```

保存命令：
```bash
# Step 1：Write 工具将整理后的内容写入 /tmp/okf-archive.md（包含 OKF frontmatter）
printf '%s\n' '{
  "title": "<笔记标题>.md",
  "type": "md",
  "parentId": "<对应子文件夹ID>",
  "contentFile": "/tmp/okf-archive.md"
}' | youdaonote -s okf save --json
```

**⑤ 更新 index.md + log.md**。

**⑥ 回复确认**：「已存入 `concepts/<标题>.md`（fileId: WEBxxx）」

### 5. OKF Bundle Export（导出 OKF bundle）

将云端 OKF 知识库导出为本地目录，供 git 版本控制、跨工具交换或离线使用。

**触发词**（任意一种均可触发）：
- `okf-export`
- 「导出 OKF」
- 「export bundle」
- 「导出知识库」

**Agent 执行流程**：

**① 确定目标知识库**：执行 A+B 策略。

**② 询问导出路径**：向用户确认本地目录路径（如 `~/okf-bundles/ai-okf`）。

**③ 遍历云端知识库，创建本地目录结构**：

```bash
# 本地创建 bundle 根目录和子目录
mkdir -p ~/okf-bundles/ai-okf/raw
mkdir -p ~/okf-bundles/ai-okf/entities
mkdir -p ~/okf-bundles/ai-okf/concepts
mkdir -p ~/okf-bundles/ai-okf/comparisons
mkdir -p ~/okf-bundles/ai-okf/queries
```

**④ 逐个读取云端笔记并写入本地文件**：

对每个文件夹执行：
```bash
# 列出文件夹中的所有笔记
youdaonote -s okf list -f <RAW_ID>
youdaonote -s okf list -f <ENTITY_ID>
youdaonote -s okf list -f <CONCEPT_ID>
youdaonote -s okf list -f <COMPARISON_ID>
youdaonote -s okf list -f <QUERY_ID>
```

对每个笔记，读取内容并写入对应路径：
```bash
# 读取云端笔记内容（内容已包含 OKF frontmatter）
youdaonote -s okf read <fileId>
```

然后用 Write 工具将内容写入本地文件：
```
~/okf-bundles/ai-okf/raw/article-title.md
~/okf-bundles/ai-okf/concepts/transformer-architecture.md
...
```

**⑤ 确保根目录的保留文件**：

读取云端 index.md 和 log.md，写入本地根目录：
```
~/okf-bundles/ai-okf/index.md    # bundle-root 可含 okf_version（§11），否则无 frontmatter（§6）
~/okf-bundles/ai-okf/log.md      # 无 frontmatter（OKF spec §7）
```

> schema.md 为 youdaonote-okf-wiki 专有系统笔记，导出时可选包含（作为 bundle 的 metadata 文件，不属于 OKF 规范但 spec 允许扩展文件）。

**⑥ 验证导出 bundle 的 OKF conformance**：

对本地目录执行 OKF v0.1 conformance 检查（spec section 9）：
- 每个非保留 .md 文件是否有可解析的 YAML frontmatter
- 每个 frontmatter 是否有非空的 `type` 字段
- index.md 是否遵循结构（§6 目录列表格式；bundle-root 可含 okf_version §11，其余无 frontmatter）
- log.md 是否遵循结构（§7 日期分组，无 frontmatter）

**⑦ 报告导出结果**：

```
OKF bundle 导出完成：~/okf-bundles/ai-okf/
- raw/: N 个文件
- entities/: N 个文件
- concepts/: N 个文件
- comparisons/: N 个文件
- queries/: N 个文件
- index.md ✓
- log.md ✓
- OKF conformance: PASS
```

> 导出的 bundle 可用 `git init` 初始化为仓库（OKF spec section 3 推荐 git 分发），实现版本控制和团队协作。

## 切换知识库

**触发词**（任意一种均可触发）：
- `okf-switch`
- 「切换 OKF 知识库」
- 「用哪个 OKF 知识库」
- 「换一个 OKF 知识库」
- 「选 OKF 知识库」
- "switch okf"
- "use another okf"
- "which okf"
- "change okf"

**Agent 执行流程**：

**① 读取全局注册表**：

```bash
youdaonote -s okf list   # 扫描根目录，找到 youdaonote-okf-wiki-registry.md
youdaonote -s okf read <registryFileId>
```

**② 列出所有知识库**：

从注册表中解析出所有已注册的知识库，展示给用户：

> 当前已有以下知识库：
> 1. `ai-okf` — AI 研究（最近访问：2026-04-15）
> 2. `invest-okf` — 投资笔记（最近访问：2026-04-10）
>
> 请选择要操作的知识库（输入编号或名称）：

**③ 切换到用户选择的知识库**：

读取目标知识库的 `schema.md`，获取所有 fileId，后续操作均在该知识库上执行。

**边界情况**：

| 情况 | 行为 |
|------|------|
| 仅 1 个知识库 | 告知用户只有一个知识库且已处于活跃状态，无需切换 |
| 注册表为空或不存在 | 告知无知识库，建议用 `okf-init` 创建 |

## 工作流技巧

### fileId 管理

Agent 需要维护关键笔记的 fileId 映射。建议在 schema.md 底部维护一个 ID 注册表：

```markdown
## fileId 注册表（Agent 维护）
- index.md: WEB1a2b3c4d5e6f
- log.md: WEB7a8b9c0d1e2f
- schema.md: WEB3a4b5c6d7e8f
```

每次创建新笔记后，将 fileId 追加到此表（记录在 `youdaonote-okf-wiki-registry.md` 对应知识库条目中）。这样 Agent 在后续会话中可以直接查找 fileId，无需重新 `list`。

### 搜索策略

1. **首选 index.md**：先读 index.md，通过目录定位
2. **关键词搜索**：`youdaonote -s okf search "关键词"` 覆盖标题和内容
3. **按类型浏览**：`youdaonote -s okf list -f <对应子文件夹ID>` 列出某类所有笔记

### 笔记内容写入标准模式

所有含换行的 Markdown 内容，统一使用 **`contentFile` 两步模式**（Write 工具写纯 Markdown → `save` JSON 传路径）：

```bash
# Step 1：Write 工具将 Markdown 内容写入本地文件（纯 Markdown，含 OKF frontmatter，无需任何 JSON 转义）
# 写入 /tmp/okf-xxx.md，内容就是普通的 Markdown

# Step 2：save JSON 中只放路径，CLI 自行读取文件
printf '%s\n' '{
  "title": "note-title.md",
  "type": "md",
  "parentId": "<FOLDER_ID>",
  "contentFile": "/tmp/okf-xxx.md"
}' | youdaonote -s okf save --json

# 更新已有笔记：同样先 Write 工具写文件，再 --file 传递
youdaonote -s okf update <fileId> --file /tmp/okf-xxx.md
```

> ⚠️ **必须先完成 Step 1**：`/tmp/` 文件不会凭空存在，Agent 必须用 Write 工具显式创建。若 `/tmp/` 权限受限，可改用相对路径如 `./okf-temp.md`，操作完成后删除。
>
> **为何用 `contentFile` 而非内联 `content`**：内联 `content` 需要将所有换行、引号、反斜杠进行 JSON 转义（`\n`、`\"`、`\\`），极易出错。`contentFile` 只是路径字符串，无转义问题。

### OKF frontmatter 维护

每次创建 concept note **必须**包含 `type` 字段——这是 OKF v0.1 的唯一必填字段（spec section 4.1）。推荐同时包含 `title`、`description`、`resource`、`tags`、`timestamp` 字段。

frontmatter 模板：
```yaml
---
type: <Concept|Entity|Comparison|Query|Raw>  # 必填
title: <显示名称>                             # 推荐
description: <一句话摘要>                     # 推荐
resource: <底层资产 URI，抽象概念可省略>        # 推荐
tags: [<标签1>, <标签2>]                      # 推荐
timestamp: <ISO 8601 datetime>               # 推荐
---
```

**扩展字段**：OKF spec §4.1 允许 producer 添加任意额外 frontmatter 字段（如 `created`、`updated`、`sources`、`confidence` 等）。Consumer 应保留未知字段，不应拒绝含未识别字段的文档。

### OKF body 约定标题

OKF spec §4.2 定义了三个约定标题（非强制，适用时使用）：

| 标题 | 用途 |
|------|------|
| `# Schema` | 资产字段结构（如数据库表的列定义、API 的参数表） |
| `# Examples` | 使用示例，通常用代码块 |
| `# Citations` | 外部来源（spec §8） |

### OKF 链接维护

交叉引用使用 markdown 链接 `[title](/folder/concept-id.md)`，路径以 `/` 开头（bundle-relative 绝对路径）。这是 OKF v0.1 spec section 5.1 的推荐形式，在文件移动时更稳定。

- ✅ 推荐：`[self-attention](/concepts/self-attention.md)`（绝对路径，spec §5.1）
- ✅ 允许：`[self-attention](./self-attention.md)`（相对路径，spec §5.2，文件同目录时可用）
- ❌ 错误：`→ self-attention`（llm-wiki 自定义约定，不符合 OKF）

**链接语义**（spec §5.3）：markdown 链接本身不携带关系类型。concept 间的关系（parent/child、references、depends-on、joins-with 等）由链接周围的文本表达，而非链接本身。Consumer 构建图视图时通常将所有链接视为无类型有向边。

### 会话间恢复

新会话开始时，遵循文档开头的**会话启动协议**（强制执行）：

1. `youdaonote -s okf list` 扫描根目录，定位 `youdaonote-okf-wiki-registry.md`
2. 读取注册表，确定目标知识库（A+B 策略）
3. 读取目标知识库的 schema.md，获取所有 fileId
4. 可选：读取 index.md 了解当前知识库状态
5. 可选：读取 log.md 了解最近操作

> 注册表不存在时自动重建，无需用户干预。

## 注意事项

- **不要修改 type: Raw 的笔记**——素材是不可变的，修正和补充写在 concept 页面中
- **每次操作都更新 index.md 和 log.md**——跳过会让知识库逐渐退化
- **不要创建没有交叉引用的页面**——孤立页面等于不存在。每个页面至少用一个 markdown 链接 `[title](/folder/id.md)` 引用其他页面
- **index.md 和 log.md 的 frontmatter 规则**——log.md 不含 frontmatter（§7）；index.md 按 §6 不含 frontmatter，但 bundle-root index.md 可含 `okf_version`（§11 唯一例外）。不要在 index.md 中放除 okf_version 以外的 frontmatter 字段
- **每个 concept note 必须有 `type` 字段**——这是 OKF v0.1 的唯一必填字段（spec section 9）
- **交叉引用用 markdown 链接** `[title](/folder/concept-id.md)`——不用 `→ title`（OKF spec section 5）
- **摘要要简洁**——一个页面应该 30 秒内可扫读。深度分析放到专门的页面
- **大批量更新前先确认**——如果一次 Ingest 会影响 10+ 个已有页面，先与用户确认范围
- **❌ 禁止在笔记内容中使用 shell 命令替换**——`$(cat /tmp/xxx.md)` 在单引号 heredoc（`cat <<'EOF'`）或 `printf '%s\n' '...'` 中不会展开，会被字面量写入笔记。保存笔记内容必须使用两步模式：先用 Write 工具将内容写入文件，再通过 `--file` 参数传递。
  ```bash
  # ❌ 错误：单引号 'EOF' 禁用 shell 展开，$(cat ...) 成为字面量
  cat <<'EOF' | youdaonote -s okf save --json
  {"content": "$(cat /tmp/file.md)"}
  EOF

  # ✅ 正确：Step 1 Write 工具写文件，Step 2 --file 传递
  # （Step 1 已完成：Write 工具已将内容写入 /tmp/okf-note.json）
  youdaonote -s okf save --file /tmp/okf-note.json --json
  ```
- **笔记标题使用小写加连字符**——如 `transformer-architecture.md`，避免使用空格和特殊字符
- **保持 schema.md 的 fileId 注册表更新**——这是跨会话恢复和注册表自动重建的基础
