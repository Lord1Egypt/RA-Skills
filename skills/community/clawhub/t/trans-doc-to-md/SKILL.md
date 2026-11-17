---
name: trans-doc-to-md
version: "3.0.1"
description: >-
  Convert PDFs, Lexiang document links, or prepared Markdown packages into faithful
  bilingual Markdown work packages. Preserves source paragraphs, local image paths
  and order, and rich document structure; uses a generic article profile or strict
  PDF-rich profile as appropriate. Outputs source.md, optional images/, meta.json,
  and a final Markdown file named from the original title. Publishing is delegated
  to upload-markdown-to-lexiang; this skill contains no upload implementation.
  将 PDF、乐享文档链接或已准备好的 Markdown 工作包转换为保真的双语 Markdown 工作包。
requires:
  skills:
    - name: upload-markdown-to-lexiang
      version: ">=1.1.0,<2.0.0"
---

# Trans Doc to Markdown（保真双语文档工作包）

处理三类输入：PDF、乐享文档链接、Prepared Markdown Package。输出保真的双语 Markdown
工作包；如需发布，统一复用 `upload-markdown-to-lexiang`，本 Skill 不实现上传。

开始前先读 [references/lessons-learned.md](references/lessons-learned.md) 的 P0 教训。

## 适用边界

- PDF：论文、报告、信息图的文字、图表、表格与卡片提取和双语化。
- 乐享文档链接：解析正文、下载 assets 图片并双语化。
- Prepared Markdown Package：消费已经准备好的 `source.md`、可选 `images/`、`meta.json`。
- 不负责网页付费墙、视频、播客抓取。
- 不负责乐享上传实现；发布只能调用公共 uploader Skill。

## 统一工作包契约

每个输入都先归一化为独立工作目录：

```text
<work-dir>/
├── source.md          # 必需；不可变的原文完整性校验基准
├── images/            # 可选；source.md 引用的本地图片
├── meta.json          # 必需；标准元数据
└── <原文标题>.md      # 最终双语 Markdown
```

`source.md` 一旦形成即只读。清洗、重排、翻译必须写入草稿或最终文件，禁止覆盖
`source.md`；最终校验始终以它为基准。最终文件名取 `meta.json.title` 的原文标题，仅对
路径分隔符等文件系统非法字符做必要替换，不使用摘要标题或译名。

`meta.json` 标准字段：

```json
{
  "title": "Original Document Title",
  "source_url": "https://example.com/original",
  "source_title": "Original Document Title",
  "source_type": "pdf",
  "language": "en",
  "parent_id": "optional-lexiang-parent-entry-id"
}
```

- `title`：最终 Markdown 文件名和默认发布标题的原文标题。
- `source_url`：原始来源 URL；纯本地文件可用 `file://` URL 或空字符串。
- `source_title`：来源显示标题，通常与 `title` 相同。
- `source_type`：保留真实来源类型，支持 `article`、`youtube`、`podcast`、`pdf`、
  `lexiang` 或通用的 `prepared-markdown`。
- `language`：检测到的 BCP 47 语言标签，如 `en`、`zh-CN`。
- `parent_id`：可选；发布到乐享时的父条目 ID。

提取器可以保留 `entry_id`、`space_id`、`images.json`、`parsed_raw.md`、`paper.pdf`
等扩展字段或旁路产物，但不能替代上述标准字段。

## 工作流总览

```text
PDF ───────────┐
               ├─ 提取/归一化工作包 ─┐
乐享文档链接 ──┘                      ├─ 语言检测 → 通用清洗 → 翻译 → 校验
Prepared Markdown Package ────────────┘

PDF 使用 pdf-rich profile；乐享与 Prepared Markdown 默认使用 generic profile。
只有确认乐享来源本质是富 PDF 报告时，才显式切换为 pdf-rich。
```

任务清单：

```text
- [ ] Step 0 读取 P0 教训并识别输入模式
- [ ] Step 1 提取或预检统一工作包
- [ ] Step 2 检测 source.md 语言
- [ ] Step 3 通用清洗（写新文件，不改 source.md）
- [ ] Step 4 仅 pdf-rich：图片、富元素、TOC 与标题层级处理
- [ ] Step 5 翻译并生成 <原文标题>.md
- [ ] Step 6 按 profile 校验
- [ ] Step 7 可选：调用公共 uploader
```

## Step 1 — 按输入模式分流

### A. 乐享文档链接

```bash
python3 scripts/lexiang_fetch.py "<乐享URL或entry_id>" --out-dir out/my-doc
# assets 失败时可补下原 PDF
python3 scripts/lexiang_fetch.py "<entry_id>" --out-dir out/my-doc --download-pdf
```

脚本生成 `source.md`、`images/`、`images.json`、`parsed_raw.md` 和 `meta.json`。
`[IMAGE]...[/IMAGE]` 与行内 `![](/assets/...)<image_ocr>` 仅用于定位并下载图片；
`source.md` 只保留 `![](images/...)` 引用，**不得**附带 OCR 标签、图片描述或衍生表格。
检查并补齐标准 meta 字段，随后冻结 `source.md`。图片对账要求：

```text
images.json 条目数 == downloaded=true 数 == source.md 本地图片引用数
```

### B. 本地或 URL PDF

```bash
curl -L -o out/my-doc/paper.pdf "<PDF URL>"
python3 scripts/pdf_extract.py out/my-doc/paper.pdf --text --out-dir out/my-doc
python3 scripts/pdf_extract.py out/my-doc/paper.pdf --thumbs --out-dir out/my-doc
```

结合 `paper.txt` 与逐页图表裁剪装配出 `source.md`，写入标准 `meta.json` 后冻结
`source.md`。文字与图片分两条路径，详见
[references/extraction.md](references/extraction.md)。

### C. Prepared Markdown Package

从语言检测和通用清洗直接开始，不运行提取器。预检：

1. 工作目录内有非空 `source.md` 和合法 `meta.json`。
2. `meta.json` 包含 `title/source_url/source_title/source_type/language`；
   `parent_id` 可选；`source_type` 保留真实来源类型，未知来源才使用
   `prepared-markdown`。
3. `source.md` 中每个本地图片路径都位于工作目录内且文件存在。
4. `images/` 可不存在；没有本地图片时这是合法状态。
5. 不改写 `source.md`，不把已清洗稿反向覆盖为校验基准。

## Step 2 — 语言检测

对所有模式统一读取 `source.md` 前 500 个正文字符，忽略 Markdown 标记、图片和 HTML
注释。中文字符占比 ≥30% 视为中文；否则按检测语言翻译为中英对照。把结果写入
`meta.json.language`。

## Step 3 — 通用清洗

所有模式都执行，但结果写入临时草稿：

- 保留每个源文正文段落，不摘要、不改写英文侧。
- 保留本地 Markdown 图片的路径和先后顺序；alt 可翻译。
- `[IMAGE]...[/IMAGE]` 及紧随图片的 `<image_ocr>...</image_ocr>` 是提取元数据，
  只用于定位和下载图片；最终文档仅保留本地图片引用。禁止附带图片标题、图片描述、
  OCR 原文、OCR 翻译或根据 OCR 另行重建的表格，除非这些内容本来就是图片块之外的
  独立正文。
- 保留链接、列表、表格、引用与代码。
- 清除明确的解析噪音；任何可能属于正文的内容宁可保留。
- 表示“约”的裸 `~` 改为 `≈`；代码、行内代码和 URL 不改。
- 普通货币金额直接写 `$`，不得转义成 `\$`；只有真实数学公式才按公式策略处理。
- 标题使用单行双语格式；普通文章不要求 Contents/TOC。

翻译格式见 [references/translation.md](references/translation.md)。

## Step 4 — 仅 `pdf-rich` 的专项处理

Prepared Markdown 和普通乐享文章默认跳过本步骤。PDF 富文档执行：

1. 逐页扫描并裁剪全部图表，处理一页多图；对账实际图表数与本地图片引用数。
2. 重建统计卡、定义卡、多列信息图、样式化表格；见
   [references/rich-elements.md](references/rich-elements.md)。
3. 清理页眉页脚和 LaTeX 脚注残留。
4. 严格重排标题层级。
5. 源文存在 Contents/TOC 时逐项保持完整标题、真实类别和页码格式。

`pdf-rich` 校验 profile 要求严格 TOC/标题结构；若 PDF 确实没有 TOC，应使用
`generic`，不要伪造目录来满足校验。

## Step 5 — 翻译与装配

默认由当前模型按 3000–5000 字符逐块翻译。备选仅在用户明确要求且配置
`GEMINI_API_KEY` 时使用本 Skill 唯一副本：

```bash
python3 scripts/translate_gemini.py draft.md "<原文标题>.md"
```

硬性要求：

- 英文原文完整保留，后接中文译文。
- 标题单行双语：`## English / 中文`。
- 列表逐项单行双语：`- English item / 中文条目`；不受句末标点影响，禁止英文列表与中文列表分组堆叠。
- 本地图片 path 原样保留且顺序不变，alt 可翻译。
- 图片块只输出图片引用，不输出 `[IMAGE]` 元数据、`<image_ocr>`、OCR 译文或衍生表格。
- 非公式场景中的美元符号写为 `$`，禁止写成 `\$`。
- 不在章节标题前添加 `---`。
- 最终文件必须命名为 `<meta.title>.md`。

## Step 6 — 校验

普通文章、Prepared Markdown 和默认乐享模式：

```bash
python3 scripts/bilingual_validate.py source.md "<原文标题>.md" \
  --profile generic --json
```

PDF 富文档严格模式：

```bash
python3 scripts/bilingual_validate.py source.md "<原文标题>.md" \
  --profile pdf-rich --raw-source parsed_raw.md --json
```

兼容按章节校验：

```bash
python3 scripts/bilingual_validate.py source.md "<原文标题>.md" \
  --section "Mechanical Properties" --profile generic
```

`generic` 始终校验源文段落与本地图片路径/顺序；仅当源文存在 TOC 时运行 TOC
专项校验。`pdf-rich` 继续运行严格 TOC 和标题结构校验。成功/失败退出码分别为 0/1；
`--json` 始终输出含 `status/ok/profile/scope/error` 的 JSON。

## Step 7 — 可选发布（只调用公共 uploader）

先按公共 Skill 的定位规则获得 `<uploader-root>`，并检查 CLI 契约：

```bash
python3 "<uploader-root>/scripts/lexiang_upload.py" --version
# cli_api 必须为 "1"
```

使用统一工作包上传：

```bash
python3 "<uploader-root>/scripts/lexiang_upload.py" upload \
  --work-dir "out/my-doc" --md "<原文标题>.md" \
  --meta-file meta.json --parent-from-meta --source-from-meta \
  --name-suffix " 中英对照" --pin --json
```

预览而不上传：

```bash
python3 "<uploader-root>/scripts/lexiang_upload.py" upload \
  --work-dir "out/my-doc" --md "<原文标题>.md" \
  --parent-id dry-run --dry-run --json
```

禁止在本 Skill 增加上传脚本、认证逻辑或逐块 MCP 上传代码。两个 Skill 仅通过
`meta.json`、`images/` 和最终 `.md` 文件组合。

## 交付自检

- `source.md` 未被修改，是最终校验的唯一原文基准。
- `meta.json` 标准字段齐全，最终文件使用原文标题命名。
- 所有源文段落完整保留，没有摘要替代。
- 所有源文本地图片路径不变、顺序不变、文件存在。
- 图片块仅保留图片引用，无图片元数据、OCR 文本、OCR 译文或衍生内容。
- 全文无非必要的 `\$`；普通金额统一使用 `$`。
- `generic` 对无 TOC 普通文章可通过；有 TOC 时标题保持完整。
- `pdf-rich` 已完成图表、富元素、TOC 和标题层级专项检查。
- 校验命令退出码为 0；JSON 中 `ok=true`。
- 上传能力完全来自 `upload-markdown-to-lexiang`。

## 脚本职责

| 脚本 | 职责 |
|---|---|
| `scripts/lexiang_fetch.py` | 仅获取乐享正文与 assets；处理 `[IMAGE]` 与行内 asset，剔除 OCR 元数据 |
| `scripts/pdf_extract.py` | 仅提取 PDF 文字、缩略图与裁剪图片 |
| `scripts/bilingual_validate.py` | 按 generic/pdf-rich 校验双语产物 |
| `scripts/translate_gemini.py` | 可选 Gemini 翻译，本 Skill 仅此一份 |

## 依赖

- 乐享 fetch：标准库及现有读取凭证。
- PDF：`pymupdf`、`Pillow`、`numpy`。
- Gemini 备选：`requests`、`GEMINI_API_KEY`。
- 发布：独立 Skill `upload-markdown-to-lexiang`，`cli_api=1`。
