---
name: tdoc-docx
version: 1.0.0
description: >
  Word 文档全能处理技能 | Complete Word Document Processing Skill.
  支持创建、读取、编辑、转换 Word 文档 | Create, read, edit, convert Word documents.
  支持 .docx/.doc 格式、中文公文格式、表格、图片、tracked changes、评论 |
  Supports .docx/.doc, Chinese gov format, tables, images, tracked changes, comments.
  触发词：Word、文档、docx、doc、公文、报告、转PDF.
metadata:
  openclaw:
    emoji: 📄
    requires:
      bins:
        - python3
        - uv
    install:
      - id: uv-env
        kind: uv
        path: .
        bins: [create_docx.py, read_docx.py, edit_docx.py, convert_docx.py, diff_docx.py, word_count.py]
---

# TDoc DOCX — Word 文档全能处理技能

## 概述

提供对 `.docx` / `.doc` 文件的**完整生命周期**管理：

| 能力 | 说明 | 脚本 |
|------|------|------|
| **创建** | 从零创建专业 Word 文档（含中文公文格式） | `create_docx.py` |
| **读取** | 提取文本、表格、图片、元数据 | `read_docx.py` |
| **编辑** | JSON 规则批量编辑 / XML 层面精细操作 | `edit_docx.py` + `office/` |
| **转换** | docx↔pdf、doc→docx、docx→markdown | `convert_docx.py` |
| **差异** | 生成两版本间的 Unified Diff 报告 | `diff_docx.py` |
| **评论** | 添加评论、回复、tracked changes | `comment.py` |
| **分析** | 文档摘要、关键词提取、字数统计 | `word_count.py` + AI |

## 自动触发场景

当用户请求以下任务时，**自动使用此 skill**：
- 创建 Word 文档、公文、报告、总结、方案
- 读取/分析/提取 Word 文档内容
- 编辑/修改现有 Word 文档
- 将 Word 转换为 PDF 或其他格式
- 对比两个文档的差异
- 对文档添加评论或修订
- 统计文档字数、分析文档摘要

**关键词识别：**
- "Word"、"文档"、"docx"、"doc"
- "公文"、"报告"、"总结"、"方案"、"材料"
- "转PDF"、"转换"、"格式转换"
- "编辑"、"修改"、"对比"、"差异"
- "评论"、"批注"、"修订"
- "字数"、"摘要"、"关键词"、"总结要点"

### ⚠️ 核心路由原则（必读）

> **路由决策树仅适用于「创建文档」这一个环节。** 文档一旦创建完成（无论是通过路径 A 通用创建还是路径 B 垂类模板创建），后续所有操作**一律使用 `scripts/` 下的工具脚本**，不再走模板流程。

```
用户请求
  │
  ├─ 「创建」新文档 → 走路由决策树（路径 A 通用 / 路径 B 垂类模板）
  │
  └─ 对「已有」文档进行操作 → 直接使用 scripts/ 工具脚本
      ├─ 编辑/修改  → edit_docx.py（JSON 规则）或 XML 编辑（office/unpack → 修改 → pack）
      ├─ 读取/提取  → read_docx.py
      ├─ 格式转换   → convert_docx.py
      ├─ 差异对比   → diff_docx.py
      ├─ 评论/修订  → comment.py + XML 编辑
      └─ 字数/分析  → word_count.py + AI
```

> 💡 **典型场景**：用户先让你用红头模板创建了一份文件，然后又要求「把 A 改成 B」——此时应该用 `edit_docx.py` 编辑已有文件，而不是重新跑一遍创建脚本。

## 安装

> ⚠️ **首次使用本 skill 前必须先安装依赖，否则脚本会报 ModuleNotFoundError！**

**方式1：一键安装（推荐）**

```bash
cd {baseDir}
./install.sh
```

**方式2：手动安装**

```bash
# 使用 pip
pip3 install -r {baseDir}/requirements.txt

# 或使用 uv（更快）
uv pip install -r {baseDir}/requirements.txt
```

**核心 Python 依赖（必装）：**

| 包名 | 最低版本 | 用途 |
|------|----------|------|
| `python-docx` | 1.1.0 | 创建/读取/编辑 DOCX |
| `reportlab` | 4.0 | DOCX→PDF 基础转换 |
| `defusedxml` | 0.7.0 | 安全 XML 解析 |
| `lxml` | 5.0 | XSD 验证 |

**系统级依赖（必装，`install.sh` 会自动安装）：**

| 工具 | 用途 | 手动安装方式 |
|------|------|-------------|
| LibreOffice | 高保真 PDF 转换、DOC→DOCX、接受修订 | macOS: `brew install --cask libreoffice`<br>Linux: `sudo apt install libreoffice` |
| pandoc | 高级文本提取 | macOS: `brew install pandoc`<br>Linux: `sudo apt install pandoc` |
| Poppler | DOCX→图片 (pdftoppm) | macOS: `brew install poppler`<br>Linux: `sudo apt install poppler-utils` |
| antiword | .doc 文件读取 | macOS: `brew install antiword`<br>Linux: `sudo apt install antiword` |

> 💡 **推荐使用 `./install.sh` 一键安装**，脚本会自动检测系统并安装以上所有依赖。

---

## 一、创建文档

### ⚡ 路由决策树（仅用于创建文档）

> **本决策树仅在「创建新文档」时使用。** 对已有文档的编辑、转换、对比等操作请直接使用 `scripts/` 工具脚本（参见上方「核心路由原则」）。

创建文档时，**必须按以下决策树选择执行路径**：

```
用户请求创建文档
  │
  ├─ Step 1: 意图识别 — 是否匹配垂类模板？
  │   │
  │   ├─ ✅ 匹配垂类模板（公文、合同等专业文档）
  │   │   └─ → 路径 B：垂类模板创建流程
  │   │       ① 读取 {baseDir}/templates/<模板名>/rules.md
  │   │       ② 按 rules.md 规范，用 Python 脚本创建文档
  │   │       ③ 不使用 create_docx.py 的内置 style
  │   │
  │   └─ ❌ 不匹配垂类模板（通用文档）
  │       └─ → 路径 A：通用创建流程
  │           │
  │           ├─ Step 2: 用户是否上传/提供了 Markdown 文件？
  │           │   │
  │           │   ├─ ✅ 有 Markdown → 路径 A1：CLI 方式（--from-markdown）
  │           │   └─ ❌ 无 Markdown → 路径 A2：Python API 方式（⭐ 默认推荐）
  │           │
  │           └─ 选择风格: default / business / academic
  │
  └─ 输出文档
```

> **核心原则**：除非用户明确上传了 Markdown 文件要求基于 MD 创建，否则一律使用 **Python API 方式**（直接调用 `DocxCreator`）创建文档。

---

### 路径 A：通用创建（非垂类文档）

适用于：一般报告、总结、方案、商务文档、学术论文等**无特定行业格式规范**的文档。

#### 路径 A2：Python API 方式（⭐ 默认推荐）

> **这是默认的创建方式。** 当用户没有上传 Markdown 文件时，直接编写 Python 脚本调用 `DocxCreator` 类创建文档。

```python
import sys
sys.path.insert(0, "{baseDir}/scripts")
from create_docx import DocxCreator

creator = DocxCreator(style='default')  # 可选: default/business/academic
creator.add_title("文档标题")
creator.add_heading1("一、第一章")
creator.add_paragraph("正文内容")
creator.add_paragraph("详细说明...", bold_prefix="（一）小标题。")
creator.add_table(["列1", "列2"], [["A", "B"], ["C", "D"]])
creator.add_image("chart.png", width=400, caption="图1")
creator.add_empty_line()
creator.add_page_break()
creator.save("output.docx")
```

**DocxCreator 可用方法：**

| 方法 | 说明 |
|------|------|
| `add_title(text)` | 居中大标题 |
| `add_author(text)` | 居中署名（支持 `\\n` 换行） |
| `add_heading1(text)` | 一级标题 |
| `add_heading2(text)` | 二级标题 |
| `add_paragraph(text, bold_prefix=None)` | 正文段落（可选加粗前缀） |
| `add_table(headers, rows, col_widths=None)` | 表格 |
| `add_image(path, width=None, caption=None)` | 图片 |
| `add_empty_line()` | 空行 |
| `add_page_break()` | 分页符 |
| `save(filepath)` | 保存文档 |

**支持的通用风格 (`style`)：**

| 风格 | 说明 | 适用场景 |
|------|------|----------|
| `default` | 默认现代风格（微软雅黑/Arial） | 通用文档 |
| `business` | 商务风格（简洁、专业） | 商业方案、合同 |
| `academic` | 学术论文格式（宋体/Times New Roman） | 论文、学术报告 |

> ⚠️ **注意**：`gov` 风格仍然保留在 DocxCreator 中，但当识别到公文类意图时，应走**路径 B 垂类模板流程**，按 rules.md 规范用 Python 精确创建，而非简单调用 `style='gov'`。

#### 路径 A1：从 Markdown 创建（CLI 方式）

> **仅当用户明确上传了 Markdown 文件**（如 `.md` 文件）时才使用此路径。

```bash
# 从 Markdown 转换（自动识别标题层级）
python3 {baseDir}/scripts/create_docx.py --from-markdown input.md --output output.docx

# 带署名
python3 {baseDir}/scripts/create_docx.py --from-markdown input.md --output output.docx \
  --author "某某单位\n2026年3月11日" --style default

# 指定模板风格
python3 {baseDir}/scripts/create_docx.py --from-markdown input.md --output output.docx --style business
```

**Markdown 格式规范：**

```markdown
# 文档大标题

## 一、一级标题

### （一）二级标题

正文段落内容。

**1. **带加粗前缀的段落

- 列表项会转为段落
```

---

### 路径 B：垂类模板创建（专业文档）

> **当意图识别到用户需要创建符合特定行业/领域格式规范的文档时，必须走此路径。**

#### 垂类意图识别关键词

| 垂类模板 | 触发关键词 | 模板路径 |
|---------|-----------|---------|
| **公文** | 公文、通知、请示、批复、报告、函、纪要、意见、决定、命令、公报、议案 | `{baseDir}/templates/official_document/rules.md` |
| **红头文件** | 红头、红头文件、红头文档、红头模板 | `{baseDir}/templates/red_head/rules.md` |
| *(扩展)* | *(未来可添加更多垂类模板)* | `{baseDir}/templates/<模板名>/rules.md` |

#### 垂类创建流程（三步法）

**第一步：读取规范**

```
读取 {baseDir}/templates/<模板名>/rules.md
```

该文件包含该垂类文档的完整格式规范：字体、字号、行距、页边距、层级编号、标点规则等。

**第二步：按规范用 Python 创建**

根据 rules.md 中的详细规范（含页面设置、字体对照表、段落格式、代码片段等），直接使用 `python-docx` API 编写 Python 脚本创建文档。

> ⚠️ **不使用** `create_docx.py` 的内置 style，因为垂类规范比内置 style 更严格精确。所有字体、字号、行距、页边距等参数均以对应 rules.md 为准。

**第三步：格式检查**

按 rules.md 末尾的格式检查清单逐项确认。

#### 已有垂类模板

| 模板 | 目录 | 规范文件 | 说明 |
|------|------|---------|------|
| 党政机关公文 | `templates/official_document/` | `rules.md` | 依据 GB/T 9704-2012，涵盖通知、请示、批复、报告、函等全部公文类型 |
| 红头文件 | `templates/red_head/` | `rules.md` + `src/red_head_document.py` | 红头文件模板，含发文机关标志、红色分隔线、版记区域等完整红头要素，基于模板 py 文件 + 搜索素材生成 |

> 💡 **扩展方式**：新增垂类模板只需在 `templates/` 下创建新目录，添加 `rules.md` 规范文件，并在上方的意图识别表中注册即可。

---

### 附：XML 层面创建（docx-js，高级用法）

如需使用 Node.js `docx` 库创建高度定制化文档（如复杂嵌套表格、精确页面布局），可安装：`npm install -g docx`

> **注意**：本 skill 推荐优先使用 Python API，docx-js 仅在需要极端定制时作为备选。

**docx-js 关键规则：**
- 设置页面大小：A4 (11906×16838 DXA)、US Letter (12240×15840 DXA)
- 永不使用 `\n`，用 Paragraph 分段
- 永不使用 unicode bullets，用 `LevelFormat.BULLET`
- 表格必须同时设置 `columnWidths` 和 cell `width`
- ImageRun 必须指定 `type`
- 使用 `ShadingType.CLEAR`（非 SOLID）

---

## 二、读取文档

```bash
# 基本文本提取
python3 {baseDir}/scripts/read_docx.py document.docx

# 指定输出格式
python3 {baseDir}/scripts/read_docx.py document.docx --format json
python3 {baseDir}/scripts/read_docx.py document.docx --format markdown
python3 {baseDir}/scripts/read_docx.py document.docx --format text

# 提取特定内容
python3 {baseDir}/scripts/read_docx.py document.docx --extract text
python3 {baseDir}/scripts/read_docx.py document.docx --extract tables
python3 {baseDir}/scripts/read_docx.py document.docx --extract metadata
python3 {baseDir}/scripts/read_docx.py document.docx --extract images

# 批量处理
python3 {baseDir}/scripts/read_docx.py ./docs_folder --batch --format json --output results.json

# 输出到文件
python3 {baseDir}/scripts/read_docx.py document.docx --format markdown --output output.md
```

**输出格式说明：**

| 格式 | 特点 | 适用场景 |
|------|------|----------|
| `text` | 纯文本，段落分隔 | 快速预览 |
| `json` | 结构化数据 | 程序处理 |
| `markdown` | Markdown 格式 | 文档转换 |

---

## 三、编辑文档

### 方式1：JSON 规则编辑（简单场景）

```bash
python3 {baseDir}/scripts/edit_docx.py input.docx output.docx edits.json
```

**编辑规则格式 (edits.json)：**

```json
{
  "description": "修改说明",
  "replacements": [
    {
      "search": "旧文本",
      "replace": "新文本",
      "style": "highlight"
    }
  ],
  "additions": [
    {
      "after": "在此文本之后",
      "text": "添加的文本",
      "style": "bold"
    }
  ]
}
```

**支持的样式：**

| 样式 | 效果 |
|------|------|
| `replace` | 直接替换 |
| `highlight` | 黄色高亮 |
| `delete` | 删除线+高亮 |
| `bold` | 加粗 |
| `underline` | 下划线 |

### 方式2：XML 层面精细编辑（高级场景）

适用于需要 tracked changes、精确格式保留的场景。

**步骤 1：解包**
```bash
python3 {baseDir}/scripts/office/unpack.py document.docx unpacked/
```

**步骤 2：编辑 XML**

直接编辑 `unpacked/word/document.xml`。使用 Edit 工具进行字符串替换，**不要写 Python 脚本**。

**Tracked Changes 语法：**

```xml
<!-- 插入 -->
<w:ins w:id="1" w:author="Claude" w:date="2026-03-11T00:00:00Z">
  <w:r><w:t>插入的文本</w:t></w:r>
</w:ins>

<!-- 删除 -->
<w:del w:id="2" w:author="Claude" w:date="2026-03-11T00:00:00Z">
  <w:r><w:delText>删除的文本</w:delText></w:r>
</w:del>

<!-- 最小化编辑: 仅标记变化部分 -->
<w:r><w:t>期限为</w:t></w:r>
<w:del w:id="1" w:author="Claude" w:date="...">
  <w:r><w:delText>30</w:delText></w:r>
</w:del>
<w:ins w:id="2" w:author="Claude" w:date="...">
  <w:r><w:t>60</w:t></w:r>
</w:ins>
<w:r><w:t>天。</w:t></w:r>
```

**添加评论：**
```bash
python3 {baseDir}/scripts/comment.py unpacked/ 0 "评论内容"
python3 {baseDir}/scripts/comment.py unpacked/ 1 "回复内容" --parent 0
```

**步骤 3：打包**
```bash
python3 {baseDir}/scripts/office/pack.py unpacked/ output.docx --original document.docx
```

### 接受所有修订

```bash
python3 {baseDir}/scripts/accept_changes.py input.docx output.docx
```

---

## 四、格式转换

```bash
# DOCX 转 PDF
python3 {baseDir}/scripts/convert_docx.py input.docx --to pdf --output output.pdf

# DOCX 转 Markdown
python3 {baseDir}/scripts/convert_docx.py input.docx --to markdown --output output.md

# DOC 转 DOCX（需要 LibreOffice）
python3 {baseDir}/scripts/convert_docx.py input.doc --to docx --output output.docx

# DOCX 转图片（需要 LibreOffice + Poppler）
python3 {baseDir}/scripts/convert_docx.py input.docx --to images --output ./pages/
```

**转换支持矩阵：**

| 源格式 | 目标格式 | 工具 | 说明 |
|--------|----------|------|------|
| .docx | .pdf | LibreOffice | ⭐ 高保真，保留表格/字体/排版 |
| .docx | .pdf | reportlab | 基础转换，仅适合纯文本文档 |
| .docx | .md | python-docx | 结构化提取 |
| .doc | .docx | LibreOffice | 需要 soffice |
| .docx | images | LibreOffice+Poppler | 逐页转图片 |

> 💡 **推荐**：DOCX→PDF 优先使用 LibreOffice 命令：`soffice --headless --convert-to pdf --outdir 输出目录 input.docx`

---

## 五、差异对比

```bash
# 生成 Unified Diff 报告
python3 {baseDir}/scripts/diff_docx.py old.docx new.docx --output diff_report.md

# 输出到终端
python3 {baseDir}/scripts/diff_docx.py old.docx new.docx
```

---

## 六、文件获取

```bash
# 从上传获取最新文件
bash {baseDir}/scripts/fetch_file.sh upload output.docx

# 从本地路径
bash {baseDir}/scripts/fetch_file.sh ~/Documents/report.docx output.docx

# 从 URL 下载
bash {baseDir}/scripts/fetch_file.sh https://example.com/file.docx output.docx

# 从 SFTP
bash {baseDir}/scripts/fetch_file.sh sftp://user@host:/path/file.docx output.docx
```

---

## 七、文档分析

### 文档摘要

对文档内容进行智能分析，提取核心信息：

- **提取文档主要观点** — 识别文档中的核心论述和结论
- **生成简短摘要** — 将长文档浓缩为 2-3 句话的概要描述
- **列出关键要点** — 从文档中提炼 3-5 条最重要的信息点

### 关键词提取

自动识别文档中的关键信息：

- **找出重要名词/术语** — 提取文档中的专业术语、人名、机构名等
- **识别主题** — 判断文档所属领域和讨论的核心主题
- **提取关键信息** — 发现文档中的关键数据、日期、金额等结构化信息

### 字数统计

```bash
# 统计文档字数（输出到终端）
python3 {baseDir}/scripts/word_count.py document.docx

# 输出为 JSON 格式（方便程序处理）
python3 {baseDir}/scripts/word_count.py document.docx --format json

# 同时输出前 N 字预览
python3 {baseDir}/scripts/word_count.py document.docx --preview 200
```

**统计指标：**

| 指标 | 说明 |
|------|------|
| 总字符数（含空格） | 文档全部字符计数 |
| 总字符数（不含空格） | 去除空格后的字符计数 |
| 中文字数 | 仅中文汉字数量 |
| 英文单词数 | 英文单词计数 |
| 数字串数 | 数字（连续数字算一个） |
| 标点符号数 | 中英文标点计数 |
| 段落数 | 文档段落总数 |
| 预估页数 | 按 A4 纸估算页数 |

### 输出格式

向用户呈现文档分析结果时，应包含以下信息：

- **文档类型和页数** — 如"docx 文档，约 4 页"
- **主要内容摘要** — 2-3 句话概述文档核心内容
- **关键要点（3-5 条）** — 文档中最重要的信息点
- **建议的后续操作** — 如"可进一步编辑第三条款"、"建议添加签名栏"等

> 💡 **使用方式**：先用 `word_count.py` 获取字数统计和文本内容，再结合 AI 能力生成摘要和关键词。

---

## XML 编辑参考

### Schema 合规

- **`<w:pPr>` 元素顺序**: `<w:pStyle>`, `<w:numPr>`, `<w:spacing>`, `<w:ind>`, `<w:jc>`, `<w:rPr>` 最后
- **空白保留**: 有前/后空格的 `<w:t>` 必须设置 `xml:space="preserve"`
- **RSIDs**: 8 位十六进制（如 `00AB1234`）
- **在 `<w:del>` 内**: 用 `<w:delText>` 替代 `<w:t>`

### 智能引号

```xml
<w:t>这里&#x2019;是引号：&#x201C;你好&#x201D;</w:t>
```

| 实体 | 字符 |
|------|------|
| `&#x2018;` | ' 左单引号 |
| `&#x2019;` | ' 右单引号/撇号 |
| `&#x201C;` | " 左双引号 |
| `&#x201D;` | " 右双引号 |

### 评论标记

```xml
<!-- 评论标记是 w:p 的直接子元素，不在 w:r 内部 -->
<w:commentRangeStart w:id="0"/>
<w:r><w:t>被评论的文本</w:t></w:r>
<w:commentRangeEnd w:id="0"/>
<w:r><w:rPr><w:rStyle w:val="CommentReference"/></w:rPr><w:commentReference w:id="0"/></w:r>
```

### 常见陷阱

- **替换整个 `<w:r>` 元素**: tracked changes 替换整个 run，不在 run 内部注入标签
- **保留 `<w:rPr>` 格式**: 复制原 run 的格式到新 run
- **删除整段时**: 必须在 `<w:pPr><w:rPr>` 中添加 `<w:del/>`
- **图片**: 添加到 `word/media/`，注册 relationship 和 content type

---

## 依赖

| 依赖 | 用途 | 必需 |
|------|------|------|
| `python-docx` | 创建/读取/编辑 DOCX | ✅ |
| `reportlab` | DOCX→PDF 基础转换 | ✅ |
| `defusedxml` | 安全 XML 解析 | ✅ |
| `lxml` | XSD 验证 | ✅ |
| `LibreOffice` | 高保真 PDF 转换、DOC↔DOCX、接受修订 | ✅ |
| `pandoc` | 高级文本提取 | ✅ |
| `Poppler` | DOCX→图片 (pdftoppm) | ✅ |
| `antiword` | .doc 文件读取 | ✅ |

> 所有依赖均通过 `./install.sh` 一键安装。

---

## 故障排除

### "ModuleNotFoundError: python-docx"
```bash
cd {baseDir} && ./install.sh
```

### "No replacements made"（编辑时）
文本不完全匹配。先用 `read_docx.py` 预览准确文本。

### 中文字体乱码（PDF 转换）
确保系统安装中文字体：
- macOS: 系统自带 PingFang
- Linux: `sudo apt install fonts-noto-cjk`
- Windows: 微软雅黑已预装

### LibreOffice 相关
DOC→DOCX 和接受修订功能需要 LibreOffice：
- macOS: `brew install --cask libreoffice`
- Linux: `sudo apt install libreoffice`
