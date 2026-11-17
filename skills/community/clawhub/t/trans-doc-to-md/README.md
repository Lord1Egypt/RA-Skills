# trans-doc-to-md

> 将 **PDF、乐享文档链接或已准备好的 Markdown 工作包**，转换为**保真的双语（中英对照）Markdown 工作包**。
> 保留源文段落、本地图片路径与顺序、富文档结构；翻译默认由当前模型完成。
> 发布到乐享的能力**不在本 Skill 内**——统一复用独立的 `upload-markdown-to-lexiang` Skill。

| 项 | 值 |
|---|---|
| **Skill 名** | `trans-doc-to-md` |
| **版本** | `3.0.1` |
| **上游依赖** | `upload-markdown-to-lexiang`（仅发布时使用，`cli_api=1`） |

---

## ✨ 能力概览

处理三类输入，统一归一化为「保真双语 Markdown 工作包」：

| 输入类型 | 说明 | Profile |
|---|---|---|
| **PDF** | 论文、报告、信息图的文字 / 图表 / 表格 / 卡片提取与双语化 | `pdf-rich` |
| **乐享文档链接** | 解析正文、下载 assets 图片并双语化 | `generic` |
| **Prepared Markdown Package** | 消费已准备好的 `source.md` + 可选 `images/` + `meta.json` | `generic` |

**不负责**：

- 网页付费墙、视频、播客抓取
- 乐享上传实现（发布只能调用公共 uploader Skill）

---

## 📦 统一工作包契约

每个输入都先归一化为一个独立工作目录：

```text
<work-dir>/
├── source.md          # 必需；不可变的原文完整性校验基准（只读）
├── images/            # 可选；source.md 引用的本地图片
├── meta.json          # 必需；标准元数据
└── <原文标题>.md      # 最终双语 Markdown
```

**核心规则**：

- `source.md` 一旦形成即**只读**。清洗、重排、翻译必须写入草稿或最终文件，禁止覆盖 `source.md`；最终校验始终以它为基准。
- 最终文件名取 `meta.json.title` 的原文标题，仅对路径分隔符等文件系统非法字符做必要替换，不使用摘要标题或译名。

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

| 字段 | 含义 |
|---|---|
| `title` | 最终 Markdown 文件名和默认发布标题的原文标题 |
| `source_url` | 原始来源 URL；纯本地文件可用 `file://` 或空字符串 |
| `source_title` | 来源显示标题，通常与 `title` 相同 |
| `source_type` | 保留真实来源类型：`article` / `youtube` / `podcast` / `pdf` / `lexiang` / `prepared-markdown` |
| `language` | 检测到的 BCP 47 语言标签，如 `en`、`zh-CN` |
| `parent_id` | 可选；发布到乐享时的父条目 ID |

> 提取器可保留 `entry_id`、`space_id`、`images.json`、`parsed_raw.md`、`paper.pdf` 等扩展字段或旁路产物，但不能替代上述标准字段。

---

## 🔄 工作流总览

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

---

## 🚀 快速上手

### A. 乐享文档链接

```bash
python3 scripts/lexiang_fetch.py "<乐享URL或entry_id>" --out-dir out/my-doc
# assets 失败时可补下原 PDF
python3 scripts/lexiang_fetch.py "<entry_id>" --out-dir out/my-doc --download-pdf
```

脚本生成 `source.md`、`images/`、`images.json`、`parsed_raw.md` 和 `meta.json`。
`source.md` 只保留 `![](images/...)` 引用，**不得**附带 OCR 标签、图片描述或衍生表格。图片对账要求：

```text
images.json 条目数 == downloaded=true 数 == source.md 本地图片引用数
```

### B. 本地或 URL PDF

```bash
curl -L -o out/my-doc/paper.pdf "<PDF URL>"
python3 scripts/pdf_extract.py out/my-doc/paper.pdf --text --out-dir out/my-doc
python3 scripts/pdf_extract.py out/my-doc/paper.pdf --thumbs --out-dir out/my-doc
```

结合 `paper.txt` 与逐页图表裁剪装配出 `source.md`，写入标准 `meta.json` 后冻结 `source.md`。

### C. Prepared Markdown Package

从语言检测和通用清洗直接开始，不运行提取器。预检：

1. 工作目录内有非空 `source.md` 和合法 `meta.json`。
2. `meta.json` 包含 `title/source_url/source_title/source_type/language`；`parent_id` 可选。
3. `source.md` 中每个本地图片路径都位于工作目录内且文件存在。
4. `images/` 可不存在；没有本地图片时这是合法状态。
5. 不改写 `source.md`，不把已清洗稿反向覆盖为校验基准。

---

## 🌐 翻译规则（要点）

- **英文原文完整保留**，后接中文译文；不摘要、不改写英文侧。
- **标题单行双语**：`## English Title / 中文标题`（禁止中文另起一行）。
- **列表逐项单行双语**：`- English item / 中文条目`；禁止先列全部英文再列全部中文。
- **正文按句末标点判断**：有明确句末标点 → 英文一段、中文一段；无句末标点（标签 / 指标 / 短语）→ 同一行 `English / 中文`。
- **术语全局统一**：先建术语表，整篇沿用同一译法。
- 本地图片 path 原样保留且顺序不变，alt 可翻译。
- 图片块只输出图片引用，不输出 `[IMAGE]` 元数据、`<image_ocr>`、OCR 译文或衍生表格。
- 普通货币金额写 `$`，**禁止**写成 `\$`；表示「约」的裸 `~` 改为 `≈`。
- 不加分隔线、不加国旗 emoji、不在章节标题前加 `---`。

---

## ✅ 校验

普通文章 / Prepared Markdown / 默认乐享模式：

```bash
python3 scripts/bilingual_validate.py source.md "<原文标题>.md" \
  --profile generic --json
```

PDF 富文档严格模式：

```bash
python3 scripts/bilingual_validate.py source.md "<原文标题>.md" \
  --profile pdf-rich --raw-source parsed_raw.md --json
```

按章节校验：

```bash
python3 scripts/bilingual_validate.py source.md "<原文标题>.md" \
  --section "Mechanical Properties" --profile generic
```

- `generic` 始终校验源文段落与本地图片路径 / 顺序；仅当源文存在 TOC 时运行 TOC 专项校验。
- `pdf-rich` 继续运行严格 TOC 和标题结构校验。
- 成功 / 失败退出码分别为 `0` / `1`；`--json` 始终输出含 `status/ok/profile/scope/error` 的 JSON。

---

## 📤 可选发布（只调用公共 uploader）

先按公共 Skill 的定位规则获得 `<uploader-root>`，检查 CLI 契约：

```bash
python3 "<uploader-root>/scripts/lexiang_upload.py" --version   # cli_api 必须为 "1"
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

> 禁止在本 Skill 增加上传脚本、认证逻辑或逐块 MCP 上传代码。两个 Skill 仅通过 `meta.json`、`images/` 和最终 `.md` 文件组合。

---

## 🗂️ 脚本职责

| 脚本 | 职责 |
|---|---|
| `scripts/lexiang_fetch.py` | 仅获取乐享正文与 assets；处理 `[IMAGE]` 与行内 asset，剔除 OCR 元数据 |
| `scripts/pdf_extract.py` | 仅提取 PDF 文字、缩略图与裁剪图片 |
| `scripts/bilingual_validate.py` | 按 `generic` / `pdf-rich` 校验双语产物 |
| `scripts/translate_gemini.py` | 可选 Gemini 翻译，本 Skill 仅此一份 |

---

## 🧩 依赖

- **乐享 fetch**：标准库及现有读取凭证。
- **PDF**：`pymupdf`、`Pillow`、`numpy`。
- **Gemini 备选**：`requests`、`GEMINI_API_KEY`。
- **发布**：独立 Skill `upload-markdown-to-lexiang`，`cli_api=1`。

---

## 📋 交付自检

- [ ] `source.md` 未被修改，是最终校验的唯一原文基准。
- [ ] `meta.json` 标准字段齐全，最终文件使用原文标题命名。
- [ ] 所有源文段落完整保留，没有摘要替代。
- [ ] 所有源文本地图片路径不变、顺序不变、文件存在。
- [ ] 图片块仅保留图片引用，无图片元数据、OCR 文本、OCR 译文或衍生内容。
- [ ] 全文无非必要的 `\$`；普通金额统一使用 `$`。
- [ ] `generic` 对无 TOC 普通文章可通过；有 TOC 时标题保持完整。
- [ ] `pdf-rich` 已完成图表、富元素、TOC 和标题层级专项检查。
- [ ] 校验命令退出码为 `0`；JSON 中 `ok=true`。
- [ ] 上传能力完全来自 `upload-markdown-to-lexiang`。

---

## 📄 License

MIT
