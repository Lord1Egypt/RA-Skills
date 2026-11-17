---
name: xiaoyaoclaw-kb-retriever
description: >
  OpenClaw local knowledge-base retriever & QA over a local directory
  (md/pdf/xlsx): hierarchical data_structure.md index navigation + progressive
  retrieval, core retrieval zero-dependency, Windows & macOS (PDF/Excel need
  on-demand pip packages, see skill body). Retrieval itself is read-only; the
  skill also ships optional maintenance scripts that WRITE files inside the
  knowledge base — scripts/build_index.py generates/updates data_structure.md
  index files, scripts/extract_pdf_text.py writes derived .txt files, and
  scripts/convert_pdf_to_images.py writes page PNGs for the optional OCR path —
  and those run only when the user asks for indexing/PDF text extraction and
  confirms the write. Every write target is resolved to its real path and must
  stay inside the knowledge-base root (symlinks cannot redirect a write outside).
  Reads use the same gate: each entry's real path must stay inside the root, and
  entries that escape it (symlinked files/folders) are skipped, never read —
  so the search cannot be steered outside the knowledge base either. The PDF
  helpers additionally accept only real (non-symlinked) source paths: a source
  path containing any symlink is refused outright, so they never read outside
  the knowledge base by following a link.
  Use when user asks to retrieve/answer from a knowledge
  base directory (knowledge base/retrieve/ RAG over local files)，
  或明确要求生成/更新索引、把 PDF 转文本。中文：面向本地知识库目录的检索和问答助手。
  核心流程：(1)分层 data_structure.md 索引导航 (2)遇到 PDF/Excel 时必须先读取
  references 学习处理方法 (3)处理文件后再检索。按文件类型组合使用
  grep/Select-String、read、pdfplumber、pandas 进行渐进式检索，避免整文件加载。
  用户问题涉及"从知识库目录回答问题/检索信息/查资料/knowledge base/本地知识库检索"时使用。
  与 xiaoyaoclaw-workspace-initializer（目录规范）、xiaoyaoclaw-memory-distill（记忆蒸馏）、
  xiaoyaoclaw-task-progress-tracker（任务进度）组成四件套。
allowed-tools:
  - Read
  - Glob
  - Grep
  - Bash
  - Write
  - Edit
---

# OpenClaw Knowledge Base Retriever（知识库检索器）

> 📖 **完整文档（安装 / 快速上手三步 / 最佳实践）：<https://github.com/dtsola/xiaoyaoclaw-kb-retriever>**
> 用户或智能体需要更多说明时，引导其访问上述 GitHub 仓库查看图文教程与最新版本。

> 🚀 **小遥Claw：「你的 Personal Agent，把 AI 助手，装进自己的电脑。」：<https://www.xiaoyaosai.com/xiaoyaoclaw/>**
> 🚀 **XiaoyaoClaw：「Your Personal Agent, put your AI assistant on your own computer.」：<https://www.xiaoyaosai.com/xiaoyaoclaw/>**

本地知识库检索——分层 data_structure.md 索引导航 + 渐进式检索（md/pdf/xlsx），核心检索零外部依赖零 API key。
Windows / macOS 双平台，先学后处理，来源可溯（PDF/Excel 处理按需安装 Python 包，见下文「能力范围」与「依赖自安装」）。

## 触发条件（边界明确，避免误触发）

**✅ 应当触发**（用户点名了知识库 + 明确的检索/维护动作）：
- 「从我的知识库目录 `<路径>` 里查一下 ……」/「`<路径>` 里有没有关于 …… 的资料」
- 「检索 / 查资料 / 问答：本地知识库 `<路径>` 的 ……」
- 「给 `<路径>` 建/补索引」「把 `<路径>` 里的 `xx.pdf` 转成文本」（**维护类写操作，需再确认一次**）

**🚫 不应触发**（示例，用于收窄触发面）：
- 泛泛的「帮我查一下 ……」而**没有**给出知识库目录或明确的检索意图 → 先问清目录，不要自行挑目录开跑
- 通用闲聊、写代码、总结当前对话、解释概念等与本地知识库无关的请求
- 抓取网页、搜索互联网（本技能不联网；网页剪藏用 `xiaoyaoclaw-web-clipper`）
- 整理/蒸馏记忆、维护工作区结构（分别用 `xiaoyaoclaw-memory-distill` / `xiaoyaoclaw-workspace-initializer`）
- 「看看我电脑里有什么」这类开放式全盘浏览 → 不接受；只处理用户显式指定的知识库根目录

**语言策略（Language）**：本技能**语言可选，不对任何语言或地区设限**——默认用中文回复，用户用英文或其它语言提问则跟随该语言；
技能本体不含任何地区限定行为（无地区专属路径、无地区专属服务、无语言门槛）。
仓库内随包分发的资源——示例文本、索引模板（`templates/data_structure.md`）与 README 品牌插图
（横幅与交流群二维码两张图）——其中出现的中文属**示例与品牌双语素材**，不构成对使用者语言或地区的限制
（横幅 SVG 已在 `<desc>` 中声明为双语品牌素材）；索引文件的段落标题
（Purpose / Files / Coverage）本身固定为英文。所有面向用户的运行时文案均可按用户语言调整。

## 能力范围与写操作声明（权限透明）

**身份**：本地知识库检索 / 问答工具。主流程**只读**——检索 md/pdf/xlsx，不修改任何源文件。

**可选写操作**（均需用户明确要求，或作为检索流程的必要中间步骤）：
- `scripts/build_index.py` → 生成 / 更新 `data_structure.md` 分层索引（写入知识库根目录及各子目录）
- `scripts/extract_pdf_text.py` → 提取 PDF 文本为派生 `.txt` 文件（用法：`--root <知识库根> <pdf> <txt>`；源与目标都按真实路径校验在根内；源 PDF 不动、目标与源同文件即拒绝、目标为链接即拒绝、写入原子替换）
- `scripts/convert_pdf_to_images.py` → 扫描件转图片（OCR 可选路径；用法：`--root <知识库根> <pdf> <输出目录>`；**每一页 PNG 的写目标都单独校验**在根内、非链接、非目录；源 PDF 须为真实路径）

**边界承诺**：
- 不修改任何源文件（md / pdf / xlsx 原样保留）
- **读取同样受同一道边界约束**：`scripts/search_kb.py`（检索 / 列举）对每个候选条目做
  **真实路径校验**（解开符号链接后仍须落在知识库根内），越界的条目**跳过并计数**，
  绝不读取知识库之外的文件；符号链接目录一律不进入遍历
- **被处理的源文件必须是真实路径**：`scripts/extract_pdf_text.py` /
  `scripts/convert_pdf_to_images.py` 只接受**不含任何符号链接**的源 PDF 路径
  （含链接即拒绝并回显真实位置）—— 不做"解开链接再读"，因此不会跟着链接读到知识库之外
- 不联网、不调用外部 API、不发送任何数据
- 写操作产物（txt / 图片 / 索引）**一律位于知识库根目录内**（与源文件同目录），可随时清理；知识库之外不改动任何文件
- 安装 Python 依赖前必须先告知用户并获得确认（见下文「依赖自安装」）

## 知识库目录说明

- 知识库存放在一个根目录下，包含多种文件类型（如 `.md`/`.txt`、`.pdf`、`.xlsx` 等），通常按类型或业务用途拆分为多级子目录。
- 采用**分层目录索引文件**：
  - 根目录有一个 `data_structure.md`，说明主要的「领域目录」及其用途。
  - 每个领域目录下可以有自己的 `data_structure.md`，说明该目录下有哪些子目录/文件，以及各自用途。
  - 更深一层的子目录也可以继续有 `data_structure.md`，形成多级索引树。
- 知识库根目录约定：
  - 默认认为知识库位于当前项目根目录下的 `knowledge/` 目录。
  - 如果用户在对话中明确指定了其他路径（例如“我的知识库在 /data/kb”或“用 ./docs 这个目录作为知识库”），则以用户指定的路径作为根目录。
  - 当默认路径 `knowledge/` 不存在或访问失败时，应向用户确认实际的知识库根目录位置，而不是随意猜测。
- 单个业务文件可能很大：
  - 不要直接用 read 读取整文件
  - 对 PDF、Excel 使用对应 references 文档中的方法进行结构化处理后，再结合 grep/局部读取做精细检索

### 定位 `knowledge` 根目录

- 根目录优先听用户：如果用户给了路径（如 `./docs`、`./knowledge-personal`），直接用用户提供的路径。
- 默认根目录：否则约定根目录为当前项目下的 `knowledge/`。
  - **平台检测（每次检索前先执行）**：用 exec 运行 `$env:OS`（Windows 输出含 "Windows"）或 `uname -s`（macOS 输出 "Darwin"）判定当前平台，后续命令按平台选择模板。
  - 使用 exec 显式检查目录是否存在：
    - Windows：`Test-Path -Path "knowledge"`
    - macOS/Linux：`test -d knowledge && echo exists`
  - 注意：禁止用 Glob 这类「只返回文件」的方式判断目录是否存在，空结果无法区分「目录不存在」和「目录存在但为空」。目录存在性必须通过 exec 的 Test-Path / test -d 确认。
- 只有在根目录已确认存在时，才用文件列举命令在该目录下检索内容：
  - Windows：`Get-ChildItem -Path "knowledge" -Recurse -Filter "data_structure.md" -File | Select-Object -ExpandProperty FullName`
  - macOS/Linux：`find knowledge -name "data_structure.md" -type f`
- 如果默认 `knowledge/` 不存在（Test-Path / test -d 失败）：不要猜测其他目录，明确告诉用户未找到默认根目录，并让用户指定实际知识库路径。

## 关键原则：先学习，再处理

**遇到 PDF 或 Excel 文件时的强制检查清单**：

- [ ] ✅ 已读取对应的 references 文档学习处理方法
- [ ] ✅ 已理解推荐的工具和命令
- [ ] ✅ 已将文件处理（提取/转换）完成
- [ ] ⏭️ 现在可以开始检索

**禁止行为**：
- ❌ 在未读取 references/pdf_reading.md 的情况下直接尝试处理 PDF
- ❌ 在未读取 references/excel_reading.md 的情况下直接尝试处理 Excel
- ❌ 跳过文件处理步骤，直接对原始 PDF/Excel 进行检索

## 工具映射速查（OpenClaw 适配）

| 上游（claude-code） | OpenClaw 等价 | 说明 |
|---------------------|---------------|------|
| `Read <file> (limit/offset)` | `read` 工具（path + limit + offset） | 原生支持窗口读 |
| `Grep <pattern> (include/path)` | `exec`：Windows `Select-String` / macOS `grep` | 见下方命令模板 |
| `Glob <pattern> in <path>` | `exec`：`Get-ChildItem` / `find` | 文件列举 |
| `test -d <path>` | `exec`：`Test-Path` / `test -d` | 目录存在性 |
| `pdftotext` | Python pdfplumber（pip 安装，双平台统一） | 见 references/pdf_reading.md |
| pandas（Excel） | Python pandas（pip 安装，双平台统一） | 见 references/excel_reading.md |

### exec 命令模板（按平台选择）

**搜索文本（替代 Grep）—— 首选本技能自带的安全检索脚本**：

```bash
# 关键词与目录都作为 argv 传入，不经 shell 解析；按字面量匹配；条数有上限
python scripts/search_kb.py <知识库根目录> "<关键词>" --max-hits 50
python scripts/search_kb.py <知识库根目录> --list --max-files 100    # 只列举文件
```

⚠️ **不要用 shell 递归检索作为回退**。`grep -r` / `Get-ChildItem -Recurse` 这类递归
检索会**跟随符号链接**：库内一个指向库外的 `notes.md` 链接，就会把库外文件的内容读进
结果并写进回答 —— 边界形同虚设。`scripts/search_kb.py` 是**唯一**被认可的检索实现：
它逐文件解析真实路径、越界即跳过并计数。

同样不要自己拼 shell 字符串：关键词与目录都是**用户可控文本**，写进
`grep "<关键词>"` / `Select-String -Pattern "<关键词>"` 这类模板时，引号、反引号、
`$()`、`;` 会被当成 shell 语法（命令注入）。

**只列举文件名（不读内容）时**，必须显式排除链接：
- Windows（PowerShell）：`Get-ChildItem -LiteralPath "<dir>" -Recurse -File -Attributes !ReparsePoint | Select-Object -First 100 -ExpandProperty FullName`
- macOS/Linux：`find "<dir>" -type l -prune -o -type f -print | head -100`

**禁止**：`Invoke-Expression` / `iex` / `eval` / `sh -c "$拼接"`；把关键词塞进命令名、
参数名、重定向目标这类结构性位置；用任何**会跟随链接**的递归检索替代 `search_kb.py`。

**检查目录存在（替代 test -d）**：
- Windows：`Test-Path -Path "<dir>"`
- macOS/Linux：`test -d "<dir>" && echo exists`

> ⚠️ 命中结果多时，用 `Select-Object -First` / `head` 限制输出，避免占用大量 token。
> ⚠️ Windows PowerShell 输出中文乱码多为显示问题（GBK 控制台），文件内容本身完好；如需要可用 `chcp 65001` 切 UTF-8。

## 读写范围与权限（先看这里）

**默认只读**：检索、问答、列举文件都只读，不改动知识库任何内容。

**可写操作（仅三项，且必须由用户点名并确认）**：

| 操作 | 写什么 | 触发条件 |
|---|---|---|
| 生成/更新索引 | 各目录下的 `data_structure.md` | 用户明确要求「建/补索引」；跑之前先说清「将写入哪些目录」 |
| PDF 转文本 | 派生的 `.txt` 文件（源 PDF 不动） | 用户明确要求把 PDF 内容落成文本；先说清写入位置；**源 PDF 须为真实路径**（含符号链接即拒绝） |
| PDF 转图片（OCR 可选路径） | 每页 `page_N.png`（源 PDF 不动） | 用户明确要求处理扫描件；先说清写入目录；需先确认安装 `pdf2image` + poppler；**源 PDF 须为真实路径** |

> ⚠️ **索引生成会写盘**：`scripts/build_index.py` 会在知识库各目录**新建/覆盖 `data_structure.md`**（`--force` 时覆盖已有索引）。它不是检索动作，必须由用户点名「建/补索引」后才运行。

**写入硬约束**：只写**知识库根目录内**的文件；不删任何文件；不改知识库之外的文件；写前打印目标路径。
**读取硬约束**：检索 / 列举（`scripts/search_kb.py`）对每个条目按**真实路径**（`realpath`）校验，越界条目跳过并计数，不读知识库之外的文件；待处理的源 PDF 必须是**真实路径**（路径任一段含符号链接即拒绝，不做"解链再读"）。
**符号链接防线（读 + 写同一道闸）**：写入目标与读取目标都按**真实路径**校验，解析符号链接后仍须落在知识库根内，否则拒绝/跳过；遍历时**不进入符号链接目录**；源 PDF 走 `require_real_file()`（含链接直接拒绝）（`scripts/pathguard.py` 统一把关，fail closed）。
**权限对应**：`Read`/`Glob`/`Grep`/`Bash` 用于检索与只读命令；`Write`/`Edit` 仅用于上面三项写操作。本技能不读环境变量、不读凭据、不联网。

## 总体流程

1. 理解用户需求
   - 读用户问题，提取：
     - 主题/领域关键词（如“销售报表”“系统架构”“接口文档”）
     - 时间或范围限定（如“2023 年 Q1”“最近版本”）
     - 需要的输出类型（解释、摘要、具体字段数值等）
   - 确定知识库根目录：
     - 优先检查用户是否在问题中指定了知识库路径。
     - 否则使用默认根目录 `knowledge/`。
     - 若默认根目录不存在或目录结构异常，应向用户询问确认，而不是自行假设。

2. 分层查看目录索引 `data_structure.md`
   - 使用一个「当前工作目录」的概念：
     - 默认从用户指定的知识库根目录开始；如果用户未指定，则使用当前目录。
   - 在当前工作目录下，如果存在 `data_structure.md`：
     - 使用 read 读取该文件的前若干行（例如 limit=300），必要时分段继续读取。
     - 目标：
       - 了解当前目录下有哪些子目录和文件
       - 理解每个子目录/文件的用途说明
     - 基于用户问题，挑选**最相关的若干个子目录或文件**，构成候选集合。
   - 对于候选子目录：
     - 递归进入该子目录，将其作为新的「当前工作目录」，继续查找其中的 `data_structure.md` 并重复上述过程。
     - 在递归过程中，避免一次性深入所有分支，优先沿着与问题最相关的路径向下钻取。
   - 对于候选业务文件（md/文本、PDF、Excel 等）：
     - 在完成必要的目录层级探索后，收集这些文件为最终的**检索目标列表**。
   - 在优先级排序时：
     - 优先选择用途说明与问题主题高度匹配的领域目录和文件
     - 其次考虑时间/版本等约束（如果索引中有体现）
     - 通用说明类文档（如 README.md、总体设计类文档）放在较后优先级

3. 学习文件处理方法（遇到 PDF/Excel 时强制执行）
   - **在处理 PDF 文件前**：
     - **必须先读取** [references/pdf_reading.md](references/pdf_reading.md)（位于本 Skill 目录下，不是 Knowledge 目录下）学习提取方法
     - 重点了解：pdfplumber 提取文本/表格、pypdf 元数据、扫描件处理
   - **在处理 Excel 文件前**：
     - **必须先读取** [references/excel_reading.md](references/excel_reading.md)学习读取方法
     - **必须先读取** [references/excel_analysis.md](references/excel_analysis.md)学习分析方法
     - 重点了解：pandas 读取、列筛选、数据过滤
   - **目的**：确保使用正确的工具和方法，避免盲目检索

4. 按文件类型执行处理和检索
   - 使用刚学到的方法处理文件（提取、转换、结构化）
   - 对每类候选文件，按照下面「Markdown/文本」「PDF」「Excel」策略执行
   - 总原则：
     - 优先从最相关、最精确的文件开始
     - 每个文件内都渐进式地局部检索，避免一次性加载全内容
     - 若当前文件得不到满意信息，切换到下一个候选文件

5. 迭代检索
   - 所有文件类型都使用统一的「多轮迭代检索机制」（见下文公共检索原则）

6. 答案组织与溯源
   - 汇总多轮检索得到的上下文，综合回答用户问题。
   - 尽量：
     - 给出清晰、直接的回答
     - 指出使用过的文件名（必要时包含大致位置，如章节或大概行数/页数）
   - 如果答案基于推断或信息不完全：
     - 明确标注假设与不确定性
     - 提示用户可以补充更具体的文件范围或关键词

## 公共检索原则

### 关键词选择策略
- 从用户问题提取 3-8 个关键词（含可能的英文缩写、同义词、上位/下位词）
- 可组合词组（如 "销售 报表"、"API 接口 超时"）
- 必要时包含业务词、技术术语、常见缩写（如 "uv"、"pv"、"GMV"）

### 搜索基本原则
- 始终指定尽量精准的路径和文件类型过滤，避免搜索整个目录
- pattern 优先尝试问题中的核心名词、术语，再尝试同义词
- 对于每个命中，只读取匹配附近的局部区域（上下若干行）
- 保存「文件名 + 位置信息 + 文本片段」

### 多轮迭代检索机制（最多 5 次）
所有文件类型都采用统一的迭代策略：
1. **迭代控制**
   - 维护「已尝试检索次数」计数，最多 5 次
   - 每次检索后累加计数
2. **每轮迭代流程**
   1. 基于问题生成/更新检索关键词（可包括同义词、扩展词）
   2. 选择尚未充分检索的文件或文件部分
   3. 执行检索（exec 搜索 / read 局部读取 / Python 处理）
   4. 分析获取的上下文片段
   5. 判断是否足够回答问题
3. **终止条件**
   - 找到足够支撑回答的上下文；或
   - 已达到 5 次尝试仍未找到合适信息
4. **信息不足时的处理**
   - 明确告知用户信息缺失或可能不在当前知识库中
   - 提供已找到的最接近信息，并说明不确定性
   - 提示用户可以如何缩小范围（更具体的文件名、关键词、时间范围等）

### 注意事项

- 目录存在性必须通过 exec（Test-Path / test -d）检查，禁止用文件列举命令代替目录存在性判断。
- 使用本 Skill 查询知识库时，禁止使用网络搜索等其他工具获取知识。

## 针对不同文件类型的具体策略

### 1. Markdown / 文本类文件（.md, .txt, .log 等）

1. **候选文件选择**
   - 根据 `data_structure.md` 和文件名、路径判断相关度
   - 优先检索标题和目录类文件（如汇总文档、设计总览）

2. **搜索定位与局部读取**
   - 使用 exec 对指定候选文件执行关键词搜索（Select-String / grep，见命令模板）
   - 对于有匹配的文件，使用 read 仅读取匹配附近的局部区域：
     - 通过 offset 和 limit 控制读取（例如从匹配行附近往前后各读取几十行）
     - 避免整文件读取

3. **特殊处理**
   - 如内容仅是目录/标题，根据链接或小节名继续定位深入内容
   - 应用「多轮迭代检索机制」（见上文公共检索原则）

### 2. PDF 文件检索策略

**工作流**：

1. **首先：读取处理方法指南**
   - 在处理任何 PDF 之前，**必须先读取** [references/pdf_reading.md](references/pdf_reading.md)（位于本 Skill 目录下，不是 Knowledge 目录下）
   - 重点了解：pdfplumber 提取文本/表格、pypdf 元数据、扫描件转图片 + OCR

2. **选择候选 PDF**
   - 根据 `data_structure.md` 中的描述，选择最相关的 1-3 个文件
   - 如果用户指明具体 PDF 文件，则优先使用该文件

3. **在内存里提取并检索（检索期不落盘）**
   - **统一走 Python 路线**（双平台一致）：用 pdfplumber 在进程内提取文本/表格
   - **不要为了一次检索把整份 PDF 落盘**：那是「派生写入」，属于维护动作。
     检索期的做法是**只把命中的片段写进回答**（页码 + 少量上下文），
     提取结果留在内存里，读完即弃
   - 确实需要落盘（例如用户要一份可检索的文本副本）→ 这属于维护动作：
     **先取得用户确认**，再用 `scripts/extract_pdf_text.py --root <知识库根> <pdf> <txt>`
     （脚本会校验源与目标都在根内、目标非链接、不覆盖源文件、原子写入）
   - 如需提取表格，使用 pdfplumber 的 `extract_tables()`，同样在内存里筛选后直接写进回答

4. **对提取结果执行检索**
   - **检索一律走 `scripts/search_kb.py`**：它逐文件解析真实路径、越界（含符号链接）即跳过并计数；
     **不要**用 `grep -r` / `Get-ChildItem -Recurse` 递归搜文本文件（会跟随链接读到库外）
   - 对 PDF 这类二进制文档，先在内存里提取文本再用 Python 做匹配（或先按第 3 步经用户确认落盘后检索）
   - 对于每个命中，提取命中附近范围的上下文（上下数十行或相邻几页）
   - 保存「文件名 + 页码/大致位置 + 文本片段」
   - 应用「多轮迭代检索机制」（见上文公共检索原则）

### 3. Excel 文件检索策略

**工作流**：

1. **首先：读取处理方法指南**
   - 在处理任何 Excel 之前，**必须先读取**：
     - [references/excel_reading.md](references/excel_reading.md) - 学习如何读取工作表（位于本 Skill 目录下，不是 Knowledge 目录下）
     - [references/excel_analysis.md](references/excel_analysis.md) - 学习如何分析数据（位于本 Skill 目录下，不是 Knowledge 目录下）
   - 重点了解：pandas 读取方法、列筛选、数据过滤、聚合操作

2. **选择候选 Excel**
   - 根据 `data_structure.md` 和文件/工作表命名，选择最相关的表
   - 优先选择包含「报表」「统计」「日志」「配置」「映射」等关键词的工作簿/工作表
   - 若用户指明具体 Excel 文件，优先使用该文件

3. **应用学到的方法探索结构**
   - 使用 pandas 读取前 10-50 行（使用 `nrows` 参数限制）
   - 重点掌握：列名/字段名、数据类型（数值、日期、文本）、关键字段
   - 将列名与用户问题比对，识别潜在关键字段（如「收入」「销售额」「error_code」等）

4. **执行数据检索和分析**
   - 使用学到的 pandas 方法进行过滤和聚合（如 `df[df['column'] == value]`）
   - 每次只读取匹配行附近的数据，避免一次性读取整表
   - 如问题包含时间范围，在检索中加入时间过滤
   - 应用「多轮迭代检索机制」（见上文公共检索原则）

## 与其他工具的协同

### PDF 处理
- **在处理 PDF 前必须先读取** [references/pdf_reading.md](references/pdf_reading.md) 学习处理方法
- 统一走 Python：pdfplumber（文本/表格）、pypdf（元数据/加密）、pypdfium2（扫描件转图片）
- 双平台通用安装：`pip install pdfplumber pypdf pypdfium2`

### Excel 处理
- **在处理 Excel 前必须先读取**：
  - [references/excel_reading.md](references/excel_reading.md) - 学习读取方法
  - [references/excel_analysis.md](references/excel_analysis.md) - 学习分析方法
- 使用 pandas 进行数据探索、预览、过滤和分析
- 双平台通用安装：`pip install pandas openpyxl`

### 可选依赖（精确钉版清单 + 用户确认）

- 检索核心**零依赖**；PDF / Excel / 扫描件处理才需要额外包
- **版本精确钉死**在 [`requirements-optional.txt`](requirements-optional.txt)（解析不可信文档时，解析库版本必须确定）：
  `pdfplumber==0.11.10` / `pypdf==7.1.0` / `pypdfium2==5.15.2` / `pandas==3.1.1` / `openpyxl==3.1.5`
- ⚠️ **安装前必须告知用户**：明确提示「将安装以下 Python 包（会修改当前 Python 环境）」，**获得用户确认后才执行**；禁止静默安装
  - PDF：`pip install pdfplumber==0.11.10 pypdf==7.1.0 pypdfium2==5.15.2`
  - Excel：`pip install pandas==3.0.5 openpyxl==3.1.5`
- 遇到 `ModuleNotFoundError` / `ImportError`：按上述白名单+钉版提示用户，确认后安装并重试
- ⚠️ **扫描件 OCR 是可选路径，且要过同一道确认**：仅当 PDF 无文本层且用户明确要求时，才考虑 `pytesseract==0.3.13` + `pdf2image==1.17.0`；它们**还需要系统级依赖**（tesseract / poppler）——必须先把「将安装的 pip 包 + 系统级依赖 + 影响」讲清楚并取得同意，再执行（详见 references/pdf_reading.md）
- 升级依赖须显式改动 `requirements-optional.txt`，不做隐式升级

### 工具使用原则
- **exec**：用于目录存在性检查、关键词搜索（Select-String / grep）、文件列举；始终指定精准路径和过滤条件
- **read**：只用于局部读取文件，始终设置合理的 limit（如 200-500 行）和合适的 offset
- **Python**：用于 PDF/Excel 结构化处理（pdfplumber / pandas），双平台统一
- **对于任何可能很大的文件**：
  - 禁止直接从头读到尾
  - 始终先通过索引、目录、关键词等方式缩小范围后再读

## 回答风格与错误处理

- 回答风格
  - 尽量用用户提问的语言（中文/英文）作答。
  - 先给出结论，再给出简要依据。
  - 如需要，可在后面列出引用的文件和大致位置，例如：
    - 来源：design/api_gateway.md 第 100 行附近
    - 来源：reports/2023_Q1_sales.xlsx Summary 工作表
- 信息缺失或不确定时
  - 明确说明在当前知识库中没有找到完全匹配的信息或只能部分回答。
  - 不臆造事实。
  - 提示用户可以如何帮助缩小范围：
    - 指定更具体的目录/文件
    - 提供更精确的关键词或字段名
    - 指定时间/版本范围
