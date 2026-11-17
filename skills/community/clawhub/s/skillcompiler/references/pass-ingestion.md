# Pass I: Ingestion — 多源内容摄取

**加载时机：** 📍 仅当输入不是纯文本 Prompt 时加载。位于 Pass 0 Triage 之前。

---

## 设计哲学

编译器的传统输入是结构化的角色+任务描述（"你是 X 专家，需要做 Y"）。但现实中有价值的能力往往沉淀在非 Prompt 载体里：一份 PDF 规范、一个视频教程、一张架构图、一个网页文档。

本阶段的目标不是"理解内容含义"（那是 Pass 1 的职责），而是**把任意载体标准化为 Pass 1 可消费的文本契约**，同时保留来源溯源链。类比编译器的 Preprocessor：处理宏展开和文件包含，在词法分析之前完成。

---

## 触发条件

| 输入形态 | 执行 Ingestion？ |
|---------|-----------------|
| 纯文本 Prompt（用户直接粘贴的角色+任务描述） | ❌ 跳过，直接进 Pass 0 |
| URL（http/https） | ✅ 执行 |
| 文件路径（.pdf / .docx / .md / .png / .mp4 ...） | ✅ 执行 |
| 图片（用户上传/粘贴的图像） | ✅ 执行 |
| GitHub 仓库 URL | ✅ 执行 |
| 多种来源混合 | ✅ 执行，按 mixed 处理 |

**判定方法：** 若输入包含 URL、文件路径、或二进制内容引用，则触发。否则跳过整个 Ingestion 阶段，IR 中不写入 `pass_ingestion` 字段。

---

## Step I.1 — Source Detection（来源识别）

扫描输入，判定 `source_type`：

| 信号 | source_type |
|------|-------------|
| `https://` / `http://` 开头，且非 github.com | `url` |
| `github.com/<owner>/<repo>` | `github_repo` |
| `.pdf` 后缀或 PDF magic bytes (`%PDF-`) | `pdf` |
| `.docx` / `.doc` 后缀 | `doc` |
| `.md` / `.markdown` 后缀 | `markdown` |
| `.png` / `.jpg` / `.jpeg` / `.webp` / 图片二进制 | `image` |
| `.mp4` / `.mov` / `.mkv` / `.avi` / `.webm` | `video` |
| `.mp3` / `.wav` / `.m4a` / `.flac` | `audio` |
| 同时出现多个上述信号 | `mixed` |
| 均不匹配 | 跳过 Ingestion |

---

## Step I.2 — 内联解析（按 source_type 分派）

**原则：** 优先使用环境已有的工具链。每个格式给出"推荐方式"和"回退方式"。解析失败时记录到 `extraction_warnings` 并询问用户。

### I.2.a — PDF 解析

**判定 PDF 类型：** 先检查是否为扫描件（文本层为空）。

```bash
# 检测文本层是否存在
pdftotext input.pdf - 2>/dev/null | head -c 200
```

**文本型 PDF（推荐）：**

```bash
# 保留布局，提取全文
pdftotext -layout input.pdf output.txt
```

**文本型 PDF（回退，Python）：**

```python
import pdfplumber
with pdfplumber.open("input.pdf") as pdf:
    text = "\n\n".join(page.extract_text() or "" for page in pdf.pages)
```

**扫描型 PDF（无文本层）：** 转图片后走 OCR（见 I.2.d）：

```bash
# PDF 转图片（每页一张 PNG）
pdftoppm -png -r 300 input.pdf page
# 然后对 page-1.png ... 逐张 OCR
```

**表格密集的 PDF：** 用 pdfplumber 的 `extract_tables()` 单独抽取，保留为 Markdown 表格，避免表格被压扁成乱序文本。

**警告条件：** 文本层为空（扫描件）、提取后字符数 < 原始页数 × 100（疑似提取不完整）。

---

### I.2.b — DOC/DOCX 解析

```bash
# 推荐：pandoc 转 Markdown（保留结构）
pandoc input.docx -t markdown -o output.md

# 回退：python-docx
```

```python
from docx import Document
doc = Document("input.docx")
paragraphs = [p.text for p in doc.paragraphs if p.text.strip()]
# 表格单独抽取
tables = [[cell.text for cell in row.cells] for table in doc.tables for row in table.rows]
```

**警告条件：** `.doc`（旧格式，pandoc 支持有限，建议先用 LibreOffice 转换为 `.docx`）。

---

### I.2.c — Markdown / 纯文本

直接读取，无需解析。但执行**清洗**：

- 移除 frontmatter（YAML 头）中的构建元数据，保留正文
- 移除 HTML 注释 `<!-- -->` 中的编辑残留
- 检测并保留代码块（不要把代码当正文拆散）

---

### I.2.d — 图片解析（OCR / 视觉理解）

**两层策略：** 先 OCR 提取文字，再用视觉理解补充语义。

**层 1 — OCR 提取文字：**

```bash
# 推荐：tesseract（多语言）
tesseract input.png output -l chi_sim+eng --psm 6

# 回退：调用 ZAI MCP analyze_image 工具
```

**层 2 — 视觉语义理解（当图片是图表/截图/示意图时）：**

调用 `mcp_zai-mcp-server` 的 `analyze_image` 或 `understand_technical_diagram` 工具，获取结构化描述。将描述与 OCR 文字合并。

**证据等级处理：** 图片提取的内容默认标记为 `secondary`（因为经过了一次模型转述）。截图中的原文标注为 `primary`。

**警告条件：** OCR 置信度低于 60%、图片分辨率过低、检测到水印遮挡。

---

### I.2.e — 视频解析

**三路并行提取：**

```bash
# 路 1：音频转写字幕（核心内容来源）
ffmpeg -i input.mp4 -vn -acodec pcm_s16le -ar 16000 -ac 1 audio.wav
# 然后用 whisper 转写
whisper audio.wav --model medium --language zh --output_format txt

# 路 2：关键帧提取（用于上下文补充，如 PPT 画面）
ffmpeg -i input.mp4 -vf "fps=1/30,scale=1280:-1" keyframe_%04d.png
# 每 30 秒抽一帧，对含 PPT/板书的帧走 I.2.d OCR

# 路 3：内嵌字幕（如有）
ffprobe -v error -select_streams s:0 -show_entries stream=index input.mp4
ffmpeg -i input.mp4 -map 0:s:0 subtitles.srt 2>/dev/null
```

**合并优先级：** 内嵌字幕（`primary`）> whisper 转写（`secondary`）> 关键帧 OCR（`secondary`，补充用）。

**警告条件：** 无音频轨、音频时长 > 2 小时（建议分段转写）、whisper 置信度低的片段。

**长视频处理：** 超过 30 分钟的视频，按章节切分后分段转写，避免单次转写质量下降。每段保留时间戳用于溯源。

---

### I.2.f — 音频 / 播客

```bash
# 转写（同视频路 1）
ffmpeg -i input.mp3 -ar 16000 -ac 1 audio.wav
whisper audio.wav --model medium --language auto --output_format txt
```

**说话人分离（可选）：** 多人对话时用 `pyannote-audio` 做说话人聚类，标注"说话人A/B"，避免观点归属混乱。

---

### I.2.g — 网页 URL

**推荐：** 使用 `WebFetch` 工具（自动转为可读 Markdown，去除导航/广告/脚本）。

**回退 1：** 调用 `mcp_jina_ai` 的 `read_webpage` 工具。

**回退 2：** Playwright 渲染后提取 `document.body.innerText`（用于 SPA 动态页面）。

**清洗规则：**
- 移除 cookie 提示、导航栏、页脚、广告
- 保留标题层级、正文段落、代码块、表格
- 多页内容（如分页教程）按顺序抓取合并

**警告条件：** 页面需要登录、内容被 JS 动态加载且渲染失败、 robots.txt 禁止抓取。

---

### I.2.h — GitHub 仓库

```bash
# 浅克隆
git clone --depth 1 https://github.com/<owner>/<repo>.git
```

**提取策略：**
1. 读取 `README.md` / `README*.md` 作为核心说明
2. 读取 `SKILL.md`（若存在）作为现有 skill 定义参考
3. 遍历源码文件，识别公开 API、配置、文档目录
4. 忽略 `node_modules/` / `.git/` / 构建产物

**合并为结构化文档：** 按仓库目录树组织，每个关键文件保留路径 + 摘要。

---

### I.2.i — 混合来源（mixed）

当输入包含多种来源时，**对每种来源独立执行上述解析**，然后合并。合并时：

- 每段内容保留 `source_type` 和原始来源标识
- 按逻辑顺序排列（如：README → 正文 → 附录），而非按解析顺序
- 在段间插入 `--- 来源：<标识> ---` 分隔符，供 Pass 2 做来源标注

---

## Step I.3 — Content Structuring（内容标准化）

将解析后的原始文本标准化为统一结构，写入 `structured_content`：

```markdown
# 来源：<原始标识>
## 类型：<source_type>
## 提取方式：<extracted_by>

<标准化后的正文>

---
<!-- 分段标记，供 Pass 2 溯源 -->
[SEG-001] 来源：<页码/时间戳/URL> | 证据等级：<primary|secondary|inferred>
<内容段落>

[SEG-002] 来源：<...> | 证据等级：<...>
<内容段落>
```

**分段规则：**
- 每个自然段或逻辑单元为一个 SEG
- 每个 SEG 必须带来源标识和证据等级（默认值来自 Step I.4，可被 Pass 2 覆盖）
- 保留原文中的标题层级，不破坏文档结构

**长度控制：** 若 `structured_content` 超过 8000 字，存储摘要 + 外部文件引用（`structured_content_ref: ./ingestion/full-content.md`），IR 中只保留摘要。

---

## Step I.4 — Provenance Tagging（来源溯源与证据分级）

为整份内容设定**默认证据等级**（后续 Pass 2 可逐条覆盖）：

| 条件 | 默认 evidence_grade |
|------|-------------------|
| 原文直引（PDF 文本层、字幕、网页正文） | `primary` |
| 模型转述（OCR、whisper 转写、视觉理解） | `secondary` |
| 编译器推断（从上下文推断的隐含信息） | `inferred` |

📍 证据等级体系详见 [evidence-grading.md](evidence-grading.md)

**provenance 链构建：** 每个来源记录 `{source, extractor, confidence}`。多源时为数组。

---

## Step I.5 — Quality Warnings（提取质量警告）

检测以下情况并写入 `extraction_warnings`：

| 警告 | 检测方法 | 影响 |
|------|---------|------|
| OCR 置信度低 | tesseract 输出置信度 < 60% | 该段降级为 `secondary` |
| 字幕缺失（视频） | 无音频轨或 whisper 输出为空 | 视频内容仅靠关键帧，标注不完整 |
| 扫描件 PDF | 文本层为空 | 全文走 OCR，整体降级 |
| 内容截断 | 网页/文件提取不完整 | 标注截断位置 |
| 多源冲突 | 不同来源对同一事实表述矛盾 | 不强行统一，保留矛盾（见 Pass 2 冲突保留） |
| 语言混合 | 中英文混杂或非目标语言 | 标注语言分布 |

**警告处理：** 警告不阻断编译，但写入 IR。Pass 6 Layer A 会检查"是否有未处理的 critical 警告"。

---

## Output Schema

写入 IR 的 `pass_ingestion` 字段：

```json
{
  "pass_ingestion": {
    "executed": true,
    "source_type": "pdf",
    "extracted_by": "pdftotext -layout",
    "raw_content_hash": "sha256:...",
    "structured_content": "# 来源：spec.pdf\n## 类型：pdf\n\n[SEG-001]...",
    "evidence_grade": "primary",
    "provenance": [
      {
        "source": "spec.pdf:p12-15",
        "extractor": "pdftotext",
        "confidence": 0.95
      }
    ],
    "extraction_warnings": []
  }
}
```

---

## Security Boundaries（安全边界）

Pass I 涉及在用户提供的文件/URL 上执行外部命令（pdftotext / ffmpeg / whisper / tesseract / git clone / WebFetch）。用户输入的 URL 和文件路径必须视为**不可信输入**。

### 约束

| # | 约束 | 说明 |
|---|------|------|
| SB-1 | 文件路径限制在 project scope 内 | 仅读取用户明确指定的文件。不遍历父目录、不读取 `~/.ssh`、`~/.aws` 等敏感路径 |
| SB-2 | URL 抓取视为不可信 | WebFetch/jina 抓取的网页内容可能含恶意脚本，仅提取文本，不执行 JS、不下载资源 |
| SB-3 | 外部命令不拼接用户输入到 shell | 文件路径/URL 以参数形式传递给子进程，不通过 `shell=True` 或字符串拼接构造命令 |
| SB-4 | git clone 仅限 `--depth 1` | 不克隆完整历史，不执行仓库中的 hooks（`git clone --depth 1` 默认不触发 hooks） |
| SB-5 | 提取的临时文件及时清理 | pdftoppm/ffmpeg 产生的中间文件（page-*.png / audio.wav）在写入 `structured_content` 后删除 |
| SB-6 | 大文件设上限 | 单文件 > 100MB 时警告用户并建议分段处理，避免 OOM |

### 禁止操作

- 不执行用户提供的文件中嵌入的代码
- 不将提取的内容写回原始文件路径
- 不向未声明的外部端点发送数据（除用户明确提供的 URL 外）

📍 通用安全审查项见 SkillForge [rubrics/anti-patterns.md](../../skillforge/rubrics/anti-patterns.md) 的 AP-09（Security Blind Spot）

---

## Decision Gate

| 条件 | 动作 |
|------|------|
| `structured_content` 非空 | → Pass 0 Triage（以标准化内容作为输入） |
| 所有解析方式均失败 | 向用户报告失败原因 + 建议手动提供文本 |
| 存在 critical 警告（如完全无法提取） | 同上 |
| 存在非 critical 警告 | 继续编译，警告传入 Pass 6 |

---

## Gotchas

1. **不要在 Ingestion 阶段做内容理解** — 本阶段只做"格式转换 + 来源标注"。理解能力边界、提取知识是 Pass 1/2 的职责。越界会导致 IR 过早膨胀。
2. **OCR/转写结果必须保留原始置信度** — Pass 2 需要据此决定是否信任某条知识。丢弃置信度等于丢弃证据等级的依据。
3. **混合来源不要在 Ingestion 去重** — 多源间的重复/冲突由 Pass 2 的冲突保留规则处理。Ingestion 阶段去重会丢失证据链。
4. **视频转写不要一次性处理超长内容** — whisper 对超长音频质量下降。按 30 分钟切分，每段保留时间戳。
5. **GitHub 仓库不要克隆全量历史** — `--depth 1` 即可。完整历史对 skill 编译无价值，且消耗大量 token。
