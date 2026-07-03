# 导出 Word / PDF（`siluzan-seo export`）

将 **Markdown**、**纯文本** 或 **SEO JSON 上线包** 转为 Word（`.docx`）或 PDF（`.pdf`），供客户审阅、归档或线下传阅。JSON 导出会保留 Blog 包中的元数据、正文、对比表与中文附录等结构。

## 何时使用

| 用户意图 | 是否用 export |
|----------|----------------|
| 已有 `output.json` / Blog 包 JSON，要 Word 或 PDF | ✅ |
| 已有 `.md` 说明稿或纯文本 `.txt` | ✅ |
| 仍在生成或修改 JSON schema | ❌ 先生成并校验 JSON，再 export |
| 要直接灌入 CMS / 建站 | ❌ 用 JSON 原文，不经过 export |

Agent：**在用户明确要求 Word/PDF/文档版** 或交付审阅稿时再执行；不要默认每篇 SEO 文章都导出。

---

## 命令语法

```bash
siluzan-seo export -f <输入文件> -t <格式> [-o <输出路径>]
```

| 参数 | 必填 | 说明 |
|------|------|------|
| `-f, --file` | 是 | 输入文件：`.json` / `.md` / `.markdown` / `.txt` |
| `-t, --format` | 是 | `docx` / `word` / `doc` → Word；`pdf` → PDF |
| `-o, --output` | 否 | 输出路径；省略时与输入同目录、同名换扩展名 |

### 示例

```bash
# Blog SEO JSON → Word
siluzan-seo export -f ./blog-output.json -t docx

# 同上 → PDF，指定输出名
siluzan-seo export -f ./blog-output.json -t pdf -o ./deliverables/article.pdf

# Markdown 冒烟稿 → Word
siluzan-seo export -f ./draft.md -t docx
```

---

## 输入格式

### 1. SEO JSON（Blog / 外链）

**Blog**（含 `article_en`）：导出 H1、SEO Metadata、英文正文、对比表（若有）、SEO 审计块（若有）、中文总结、完整中文翻译。

**外链**（含 `article_content`、无 `article_en`）：元数据 + 正文 + 中文总结。

正文为 **纯文本**（与 `schemas/output.json` 一致），非 Markdown。小节标题由「短行 + 空行」启发式识别；FAQ 的 `Q:` / `A:`（及中文 `问：` / `答：`）**各占独立段落**。

### 2. Markdown（`.md`）

支持 `#` / `##` 标题、空行分段、`Q:` / `A:`、`问：` / `答：`。适合说明稿或已从别处转好的 MD。

### 3. 纯文本（`.txt`）

与 JSON 内 `article_en` 相同规则（小节标题、FAQ 分段）。

---

## 输出特性

### Word（docx）

- `title` → **Heading 1**（保留 Word 大纲与目录锚点）
- 正文小节 → **Heading 2**
- 章节分隔（如 English Article、中文总结）→ 带底边框的区块标题
- Q/A 独立段落；段间距在样式层定义，避免标题与正文之间多余空行

### PDF

- 嵌入系统中文字体（Windows 优先黑体/雅黑；无字体时缓存下载 Noto Sans SC 至 `~/.siluzan/fonts/`）
- 书签大纲：`title` / `section` / `heading2`
- 命名锚点（`destination`）便于 PDF 阅读器内跳转

可选环境变量：

| 变量 | 说明 |
|------|------|
| `SILUZAN_PDF_FONT` | 指定 PDF 正文字体文件路径（`.ttf` / `.otf`） |
| `SILUZAN_PDF_FONT_BOLD` | 粗体字体路径（默认同 regular） |

---

## 分页说明（JSON 导出）

仅在 **JSON 完整包** 中插入分页：

| 位置 | 条件 |
|------|------|
| 对比表前 | 存在 `comparison_tables` |
| SEO 审计前 | 存在 `seo_audit` 等审计相关字段 |
| 中文附录前 | 存在 `chinese_summary` 或 `article_zh`（总结与翻译在同一附录内，中间不再硬分页） |

短测试 JSON 通常 1～2 页；含对比表与审计的完整 Blog 包页数更多，属预期行为。

---

## Agent 操作要点

1. 确认 CLI 已安装：`siluzan-seo --version`（未安装见 [setup.md](setup.md) 一键安装）
2. 确认输入 JSON 已通过 `schemas/output.json` 校验
3. 执行 `siluzan-seo export -f ... -t docx|pdf`
4. 将生成的文件路径回报用户

**不要**用 export 替代 JSON 交付；export 是 JSON 的 **可读副本**，不是建站数据源。
