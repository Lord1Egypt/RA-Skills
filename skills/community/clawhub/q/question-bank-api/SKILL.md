---
name: question-bank-api
description: "题库 API 接口技能（第三方题库供应商提供的 K12 试题/试卷数据服务）。This skill should be used when a user who has purchased an API key wants to pull school questions or papers from the provider's API — especially 按知识点取题、按章节取题（语文/英语等）、按试卷取题，以及试题搜索、获取答案解析、生成 Word 试卷。Trigger phrases include: 按知识点出题、按章节取题、取出这套试卷的题、找五年级数学小数乘法的题、搜一道关于浮力的题、获取这道题的答案、把题目导出成 Word、组卷、调题库接口。Use scripts/qb.py to call the API and references/api_docs.md for the full endpoint/field reference。"
agent_created: true
---

# 题库 API 接口（Question Bank API）

## Overview

封装某题库供应商的 REST API，让已购 key 的用户能在对话里直接取题、取卷、搜题、拿答案、
导出 Word。所有接口均为 `POST`，统一用 `X-API-Key` 头鉴权。客户端脚本见
`scripts/qb.py`（仅依赖 Python 标准库，无需 `pip install`）。

取题有三条主路径，对应供应商文档的 **2.1 / 2.6 / 3.x**：

| 用户意图 | 需要的能力 | 调用链路 |
|----------|-----------|----------|
| 按知识点取题 | 知识点树 → 按知识点取题 | `knowledge-tree` → `by-knowledge` |
| 按章节取题（语文/英语） | 章节树 → 章节 id 直接取题 | `chapter-tree` → `by-chapter` |
| 按章节取题（其他科目） | 章节树 → 遍历叶子取 32 位 oldId → 按知识点取题 | `chapter-tree`/`chapter-leaves` → `by-chapter-knowledge` |
| 按试卷取题 | 试卷列表 → 试卷详情 | `papers` / `paper-search` → `paper` |

## Configuration

从环境变量或 CLI 参数读取（CLI 参数优先于环境变量）：

| 变量 | 含义 | 默认 |
|------|------|------|
| `QB_API_BASE` / `--base` | API 根地址，不含末尾 `/` | `https://api.xuekubao.com`（已填真实网关） |
| `QB_API_KEY` / `--key` | 学库宝发放的 API key（X-API-Key 头） | 空（必须提供） |
| `QB_TIMEOUT` / `--timeout` | 请求超时秒数 | `30` |

**如何获取 key（务必引导用户走官方入口，不要替用户猜测 key）：**
1. 打开 https://api.xuekubao.com 注册账号；
2. 进入「API 管理」申请访问 key；
3. 购买 ¥9.9 测试套餐即可试用（有疑问联系微信客服：569212182）。
拿到 key 后设为 `QB_API_KEY` 环境变量（或在调用时传 `--key`）。**不要把 key 写死在脚本里。**

## Core Workflow 1 — 按知识点取题

1. 先解析用户要的「学段/学科/知识点」。若不知道对应的 `knowledgeId`，调用：
   ```bash
   python scripts/qb.py knowledge-tree --pharseId 1 --subjectId 2
   ```
   其中 `pharseId`/`subjectId` 来自 `catalog`（`subjectEditionApi`）返回的 `code`。
   遍历到第三级知识点，取其 `oldId` 作为 `knowledgeId`。
2. 用 `knowledgeId` 取题：
   ```bash
   python scripts/qb.py by-knowledge --knowledgeId <oldId> --page 1
   ```
   可加 `--qtypeId` / `--paperType` / `--diff` / `--gradeId` / `--year` 筛选。
3. 拿到题目后，若用户要答案，用题目里的 `md52` 调 `answer`（见下）。

## Core Workflow 2 — 按章节取题

章节取题分两种学科逻辑，先判断学科再选链路：

### 2A. 语文 / 英语 —— 章节 id 直接取题（接口 2.6）

1. 取章节树：
   ```bash
   python scripts/qb.py chapter-tree --pharseId 1 --subjectId 1
   ```
   返回树形结构，取目标章节的 `id` 作为 `chapterId`。
2. 按章节取题：
   ```bash
   python scripts/qb.py by-chapter --chapterId <id> --page 1
   ```
   可加 `--qtypeId` / `--paperType` / `--diff` / `--year` 筛选。

### 2B. 其他科目 —— 章节树 → 叶子 oldId → 按知识点取题（接口 1.3 + 2.1）

数学、物理等科目没有独立的"按章节取题"接口，但章节树本身就对应知识点：把章节树
**遍历到最后一个叶子节点**，取叶子节点的 `oldId`（32 位十六进制）当作 `knowledgeId`，
再走"按知识点取题(2.1)"即可。

1.（推荐先看叶子）列出某学科章节树的全部叶子 oldId：
   ```bash
   python scripts/qb.py chapter-leaves --pharseId 2 --subjectId 2 --editionId 74 --gradeId 201
   ```
   输出形如 `1. 第9章 整式 / 9.1 字母表示数 / 代数式  oldId=745C7D75786602F3105A69845316FF61`。
2. 直接取题（脚本会自动遍历叶子并逐个按知识点拉题）：
   ```bash
   python scripts/qb.py by-chapter-knowledge \
       --pharseId 2 --subjectId 2 --editionId 74 --gradeId 201 --page 1
   ```
   - 可加 `--chapterId <id>` 把范围限定到某个章节子树；
   - 可加 `--qtypeId` / `--paperType` / `--diff` / `--year` / `--gradeId` 筛选；
   - `--max-leaves`（默认 20）限制最多查询的叶子章节数，防止一次消耗过多 API 额度；
   - `--limit` 限制最多返回的试题总数。
3. 拿到题目后，用 `md52` 调 `answer`（见 Workflow 1 第 3 步）取答案。

## Core Workflow 3 — 按试卷取题

1. 列试卷（可按学科/年级/试卷类型/区域筛选）：
   ```bash
   python scripts/qb.py papers --gradeId 200 --subjectId 2
   ```
   或按关键词搜试卷：
   ```bash
   python scripts/qb.py paper-search --keyword "七年级 数学 期中"
   ```
2. 取某套试卷的全部试题：
   ```bash
   python scripts/qb.py paper --paperId <id>
   ```
   `id` 来自上一步返回的 `id` 字段。

## Other capabilities

- `catalog` — 学段/年级/学科/版本树（`subjectEditionApi`），用于解析 code。
- `dict` — 题型(qtypes)/试卷类型(paperTypes)/难易度(diffTypes) 字典（`getOtherBasic`）。
- `search` — 全文检索试题：`search --keyword 浮力 --gradeId 200`。
- `answer` — 按 `md52` 取答案解析：`answer --md52 <md52>`（支持逗号分隔多题）。
- `to-word` — 把结构化题目渲染成 docx：`to-word --json '<paperData JSON>' --out paper.docx`。
- `report` — 提交试题报错：`report --qid <id> --content <说明>`。

## Presenting results

- 列表默认输出**可读摘要**（序号、题型、学科/年级、题干前 60 字、md52）；加 `--json`
  输出原始 JSON 便于后续处理。
- 取题后优先展示题干与可选项；若用户要答案/解析，再调 `answer` 补齐。
- 导出 Word 时把文件写到工作目录，并用 present_files 呈现给用户。

## Guardrails

- 只展示 API 实际返回的内容，不臆造题目或答案。
- 多题取答案会消耗多次请求额度——先确认范围再批量调用。
- 遇到 `errorCode` 非 `"0"` 或 HTTP 非 2xx，把错误信息如实反馈，不要重试到失控（脚本已对
  429/5xx 做有限退避）。
- 大批量取题用 `page` 分页，避免一次拉取上万条。
