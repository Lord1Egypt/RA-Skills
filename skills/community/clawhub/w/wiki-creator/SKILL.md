---
name: "wiki-creator"
description: "Builds and maintains a global, project-independent knowledge wiki from user-uploaded documents using Karpathy's native LLM Wiki paradigm (zero vectors, zero chunks, single-page units, two-level topic/page index). Invoke when user uploads documents and asks to 'create wiki / build wiki / compile knowledge base', says 'update wiki / add new materials', asks 'search wiki / look up X / use wiki / 用wiki查', or asks for 'wiki health check / lint'. When a knowledge question is asked and a wiki exists, ALWAYS check the wiki FIRST before web search. Does NOT use vector retrieval."
---

# Wiki Creator

基于 Karpathy 原生 LLM Wiki 范式的全局知识库管理技能。**零向量、零 chunk、以完整 Wiki 单页为知识单元**，两级索引（主题层 + 页面层）为符号表，前向 `[[wikilink]]` 支撑多跳推理。

## 1. 范式红线（不可违反）

- **单页为单元**：一个实体 / 概念 = 一个 markdown 文件，目标长度 < 1500 字。
- **两级索引只读**：`index.md` 和 `topics/*.md` 由脚本生成，LLM 与用户**均不得手动编辑**。
- **环境自适应**：Wiki 根目录按运行环境自动选择——编程助手（Trae / VS Code / Cursor 等有"当前项目"概念）放项目内 `<project>/.wiki-creator/`，**与项目绑定**；办公智能体（无项目概念）放全局 `~/.wiki-creator/`（通用路径，不绑定特定产品名）。脚本自动探测，可用 `--root` 覆盖（详见 §2）。
- **raw 只读**：`raw/` 是唯一可信源，LLM 不修改 raw 文件，只读取并产出 wiki 页面。
- **每条断言必有来源**：页面正文每条事实必须标注源文件 + 章节，无来源由 lint 标红，防 LLM 幻觉。
- **矛盾不自动覆盖**：新资料与已有页冲突时**只标记到 `.conflicts.md`**，等用户裁决，绝不静默覆盖。
- **LLM 不擅自改 SCHEMA.md**：主题清单的增删改必须经用户确认。
- **主题永不合并**；仅当某主题页面数 > 1000 时由 lint 建议拆分，用户决策。

## 2. Wiki 根目录（环境自适应）

脚本自动探测 Wiki 根目录，规则：

1. **编程助手环境**（Trae / VS Code / Cursor 等有"当前项目"概念）：从 cwd 向上查找项目标记（`.git` / `.vscode` / `.trae` / `package.json` / `pyproject.toml` / `Cargo.toml` / `go.mod` 等），命中则用 `<project-root>/.wiki-creator/`，**与项目绑定**。
2. **办公智能体环境**（无项目概念）：用全局 `~/.wiki-creator/`（通用路径，不绑定特定产品名，各办公智能体共用）。
3. 任何场景都可用 `--root <path>` 显式覆盖。

> **LLM 判断当前环境**：若运行在 Trae/VS Code/Cursor 这类编程助手中且 cwd 位于某项目内（有上述标记），走**项目模式**；若在办公智能体中或 cwd 无项目标记，走**全局模式**。首次创建时若拿不准，问用户"这份 Wiki 放项目里还是放全局？"。

### 目录结构（两种模式共用，仅根路径不同）

```
<project-root>/.wiki-creator/      # 项目模式（建议加入 .gitignore）
~/.wiki-creator/                  # 全局模式（通用，不绑定特定产品）
├── raw/                           # 原始资料（只读，唯一可信源）
└── wiki/
    ├── SCHEMA.md                  # 知识库约束配置（用户可编辑）
    ├── index.md                   # 顶层索引：主题清单（脚本生成，只读）
    ├── topics/                    # 主题层：每主题一个索引文件（脚本生成，只读）
    ├── pages/                     # Wiki 单页（按主题分目录）
    │   └── <topic>/<slug>.md
    ├── .manifest.json             # 哈希缓存 + 编译记录（脚本维护）
    ├── .graph.json                # 实体→页面、页面→源文件映射（脚本维护）
    └── .backlinks.json            # 反向链接索引（脚本维护）
```

> Windows 上 `~` 解析为 `C:\Users\<用户名>`。
> **项目模式**：`.wiki-creator/` 含生成产物，建议加入项目 `.gitignore`；`raw/` 是否入库看团队是否需要共享原始资料。

## 3. 触发条件

| 用户意图 | 触发工作流 |
|---|---|
| 上传文档后说"创建 wiki / 建 wiki / 编译知识库" | 创建工作流（§4.1） |
| "更新 wiki / 增量编译 / 加入新资料" | 更新工作流（§4.2） |
| "查一下 / 搜一下 / wiki 里有没有提到 X / 用 wiki 查 / 使用 wiki" | 查询工作流（§4.3） |
| **任何知识性问题**，且 wiki 已存在 | **先查 Wiki（§4.3），再考虑公网搜索** |
| "体检 wiki / 检查知识库 / 健康检查" | Lint 工作流（§4.4） |

## 4. 四条工作流（精简版，详细见 references/）

### 4.1 创建 Wiki（首次）

1. 用户上传文件 → Agent 把文件**复制**到 `raw/`（不是移动）。路径由环境探测决定：项目模式放 `<project>/.wiki-creator/raw/`，全局模式放 `~/.wiki-creator/raw/`。
2. 执行 `python scripts/init_wiki.py` → 创建 `wiki/` 骨架 + SCHEMA.md 草稿。
3. LLM 通读所有 raw 文件（用 `parse_raw.py` 解析），归纳主题清单，写入 SCHEMA.md 草稿，**交用户确认 / 编辑**（主题边界、主题清单、实体类型、风格）。
4. 用户确认后，执行 `python scripts/diff.py` → 输出 `new` 清单（首次全部为 new）。
5. 逐文件：LLM 提炼实体 → 查 `.graph.json`（首次为空）→ 按 SCHEMA 模板建页，每页 frontmatter 标 `topic`。
6. 执行 `python scripts/build_index.py` → 生成 `index.md` + `topics/*.md` + 反链 + graph + manifest。
7. 输出编译报告：建了哪些主题、哪些页、悬空链接、建议补什么资料。

### 4.2 更新 Wiki（增量）

1. 用户加新文件 / 改旧文件到 `raw/`，说"更新 wiki"。
2. `python scripts/diff.py` → 输出 `new` + `changed` 清单 + 受影响已有页清单。
3. 逐文件编译 → 走 §6 级联三步（merge / ref-only / conflict）。
4. 若新资料催生新主题，LLM 在报告中提出"建议新增主题 X"，**经用户确认后**写入 SCHEMA.md，再编译相关页。
5. `python scripts/build_index.py` 刷新索引 + 反链 + graph + manifest。
6. 报告：新增页、更新页、主题变更、冲突待裁决项。

### 4.3 查询

> **核心原则：当用户提出知识性问题且 Wiki 已存在时，必须先查 Wiki，再考虑公网搜索。** Wiki 中的内容是经过结构化编译的可信知识，优先级高于公网搜索结果。

#### 查询标准流程（三步递进，禁止跳步）

```
Step 1: 读 wiki/index.md          ← 入口！永远是第一个动作
        ↓ 从主题清单 + 摘要判断属于哪个/哪些主题
Step 2: 读 topics/<topic>.md      ← 该主题所有页面 + 摘要
        ↓ 按摘要判断相关页
Step 3: 读 pages/<topic>/<slug>.md ← 页面全文
        ↓ 沿 [[wikilink]] 多跳推理（按需，≤3 跳）
        ↓
        作答，引用 [[页面]] + 源文件
```

#### 三条强制规则

1. **入口永远是 `index.md`，不是 `ls pages/` 或 `ls topics/`。** index.md 是脚本自动生成的顶层索引，包含所有主题 + 摘要 + 页面数，一次读取即可定位主题。直接 `ls` 目录是错误的查询方式——你无法从文件名判断内容相关性。

2. **逐层缩小范围，禁止整库加载。** 先读 index.md（主题层）→ 只读命中主题的 topics/*.md（页面层）→ 只读命中页面的全文。不要把所有页面都读进 context。

3. **Wiki 优先于公网搜索。** 当用户问一个知识性问题（定义、概念、架构、原理等），先检查本地 Wiki 是否有相关主题。如果 Wiki 中有答案，直接引用；如果 Wiki 中没有，再转向 WebSearch。不要在 Wiki 有答案的情况下浪费公网搜索。

#### 常见错误（必须避免）

| 错误行为 | 正确行为 |
|---------|---------|
| `ls pages/` 盲扫目录 | 读 `index.md` 按主题摘要定位 |
| 跳过 index.md 直接读 topics/ | index.md → topics/ → pages/ 逐层递进 |
| 用户说"用 wiki 查"仍然去 WebSearch | 立即进入 §4.3 查询流程 |
| 整库加载所有页面 | 只读命中主题和页面 |

详细见 `references/query-mode.md`。

### 4.4 健康检查（Lint）

1. 用户说"体检 wiki"。
2. `python scripts/lint.py` 结构扫描，输出：
   - 孤立页（零入链）/ 悬空链接 / 缺失页面 / 缺失交叉引用
   - 无来源断言 / 主题孤儿（topic 不在 SCHEMA）/ 主题过大（>1000 页）
3. LLM 语义层检查（基于 lint 清单 + 抽样读页）：矛盾 / 过时 / 数据缺口 / 主题归类错误。
4. 输出体检报告 + 建议。

## 5. Wiki 单页规范

每页路径 `pages/<topic>/<slug>.md`，结构：

```markdown
---
title: Transformer
topic: deep-learning
entity_type: 概念
aliases: [Transformer 架构]
sources: [raw/paper-a.pdf]
schema_version: v3
---
# Transformer

## 摘要
（1-2 句话，供主题索引抓取）

## 定义
...

## 关键论点
- ...

## 证据 / 来源
- 出自 [[attention]] 机制；原文见 raw/paper-a.pdf §3

## 关联
- 基础：[[attention]], [[positional-encoding]]
- 对比：[[rnn]], [[cnn-nlp]]
- 应用：[[bert]], [[gpt]]
```

强约束：
- `## 摘要` 最多 2 句。
- wikilink 统一用 **kebab-case 英文 slug**（`[[large-language-model]]`），页面文件名 = slug.md，中文走 `aliases`。
- 单页 < 1500 字，超出拆分实体。
- `topic` 必须命中 SCHEMA.md 主题清单中的 slug，否则 lint 报错。
- 每条事实必须标注来源（文件名 + 章节）。

详细规范见 `references/page-authoring.md`，模板见 `assets/page-template.md`。

## 6. 级联更新（受控三步）

- **定位**：`diff.py` 查 `.graph.json`，输出受影响已有页清单。
- **分类**：LLM 对每页判断 `merge`（增量改写）/ `ref-only`（仅加来源行）/ `conflict`（矛盾，**不覆盖，写 `.conflicts.md`**）。
- **限流**：单次受影响页更新上限 20 页；超出分批，报告提示"还有 N 页待级联，请说'继续更新'"。

详细见 `references/cascade-update.md`。

## 7. 脚本调用清单

| 脚本 | 何时调用 | 输出 |
|---|---|---|
| `scripts/init_wiki.py` | 首次创建 / 重建骨架 | `wiki/` 目录 + SCHEMA 草稿 |
| `scripts/parse_raw.py <file>` | 编译前解析 raw 文件 | stdout 输出干净 markdown |
| `scripts/diff.py` | 编译前 | new/changed 清单 + 受影响页清单 |
| `scripts/build_index.py` | 编译后 | index.md + topics/*.md + manifest + graph + backlinks |
| `scripts/lint.py` | 健康检查 | 结构问题清单 |

所有脚本均接受 `--root <wiki-root>` 参数（默认由 `_root.detect_wiki_root()` 探测：项目模式 `<project>/.wiki-creator/`，全局模式 `~/.wiki-creator/`），返回 JSON 或 markdown。LLM 调用时若默认探测不符预期，应显式传 `--root`。

## 8. 上下文管理

- **编译期**：单次 context 只放"当前文件解析文本 + 相关已有页清单 + SCHEMA"，不整库加载。单页 < 1500 字。级联单次 ≤ 20 页。
- **查询期**：两级索引天然限流——`index.md`（主题层）→ `topics/*.md`（页面层）→ 具体页全文。

## 9. 渐进式加载

- 元数据（name + description）常驻，约 100 词。
- 本 SKILL.md 正文 < 5k 词，只放核心流程。
- `references/` 按需加载：级联时才读 `cascade-update.md`，查询时才读 `query-mode.md`，写页时才读 `page-authoring.md`，配 SCHEMA 时才读 `schema-guide.md`。
- 脚本可不读入 context，直接 `python` 执行。

## 10. 强约束总览（LLM 必须遵守）

1. **不走向量**——遇到"语义搜索 / 相似度"不触发本技能。
2. **不手编索引**——`index.md` / `topics/*.md` / `.manifest.json` / `.graph.json` / `.backlinks.json` 由脚本维护。
3. **不擅自改 SCHEMA**——主题增删改必须经用户确认。
4. **不静默覆盖矛盾**——`conflict` 写 `.conflicts.md` 等裁决。
5. **不写无来源断言**——每条事实必须有文件名 + 章节。
6. **不混用 slug 风格**——wikilink 一律 kebab-case 英文。
7. **不超单页长度**——> 1500 字拆分实体。
8. **不跨环境混存**——同一份 Wiki 只用同一个根目录（项目模式 `<project>/.wiki-creator/` 或全局模式 `~/.wiki-creator/`），不把项目 Wiki 写到全局、也不把全局 Wiki 写到项目。脚本默认自动探测，LLM 不确定时问用户。
