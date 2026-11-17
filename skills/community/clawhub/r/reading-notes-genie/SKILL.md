---
name: reading-notes-genie
description: 閱讀筆記精靈：輸入書名 / 上傳 PDF 或 EPUB，AI 自動生成章節摘要、精華語錄、讀書心得、知識點卡片，並匯出成 Markdown、Anki 卡片、PDF 等多種格式。差異化：結構化輸出而非普通摘要。
---

# 📖 閱讀筆記精靈（Reading Notes Genie）

## 概述

自動分析書籍（PDF / EPUB / 書名），AI 生成：
- **章節摘要** — 每章核心論點與脈絡
- **精華語錄** — 高亮金句、值得背誦的段落
- **讀書心得** — 個人反思與應用建議
- **知識點卡片** — 可獨立複習的知識點（支援 Anki 格式）

**觸發關鍵字：** 讀書筆記、做筆記、章節摘要、書摘、金句、知識卡片、PDF摘要、EPUB摘要、生成Anki、做閱讀總結、讀後感、精華語錄

---

## 輸入方式

| 方式 | 說明 |
|------|------|
| 直接輸入書名 | AI 透過網路查詢書籍資料並生成摘要 |
| 上傳 PDF | 自動解析 PDF 文字 → AI 分析 → 生成筆記 |
| 上傳 EPUB | 解析 EPUB 結構 → AI 分析 → 生成筆記 |

---

## 輸出格式

| 格式 | 說明 |
|------|------|
| Markdown | 結構化筆記，可直接存入 Notion / Obsidian |
| Anki 卡片 | 支援 Cloze / 問答格式，導入 Anki 直接背誦 |
| PDF 報告 | 精美排版的閱讀筆記 PDF，可列印分享 |
| JSON | 結構化數據，方便程式後處理 |

---

## 腳本清單

| 腳本 | 用途 |
|------|------|
| `scripts/epub_parser.py` | EPUB 解析：提取章節結構、段落文字、Metadata |
| `scripts/pdf_extractor.py` | PDF 文字萃取：處理加密、圖片掃描、多欄排版 |
| `scripts/book_summarizer.py` | 核心：LLM 章節摘要 + 語錄萃取（支援 OpenAI / Anthropic / 本地模型） |
| `scripts/knowledge_card.py` | 知識卡片生成：從書籍內容萃取可複習的知識點 |
| `scripts/notes_exporter.py` | 多格式匯出：Markdown / Anki / PDF / JSON |

---

## 使用範例

```bash
# 方式一：輸入書名（AI 網路查詢）
python3 scripts/book_summarizer.py --book "原子習慣" --output ./notes/

# 方式二：分析本地 PDF
python3 scripts/book_summarizer.py --file ./my-book.pdf --output ./notes/

# 方式三：分析 EPUB
python3 scripts/book_summarizer.py --file ./my-book.epub --output ./notes/

# 匯出 Anki 格式
python3 scripts/notes_exporter.py --input ./notes/summary.json --format anki -o cards.apkg

# 匯出 PDF 報告
python3 scripts/notes_exporter.py --input ./notes/summary.json --format pdf -o notes.pdf
```

---

## AI 模型設定

腳本支援三大模型供應商，自動偵測已安裝者：

```bash
# OpenAI（預設）
export OPENAI_API_KEY="sk-..."
# 或
export ANTHROPIC_API_KEY="sk-ant-..."
# 或使用本地模型
export LOCAL_MODEL_URL="http://localhost:11434/api/generate"
```

若無 API Key，腳本會輸出提示並提供**離線純規則版摘要**（依賴關鍵字萃取）。

---

## Anki 卡片格式

支援兩種卡片類型：

**Cloze 填空型：**
```
{{c1::刻意練習}} 是提升技能的核心機制。
→ 自動生成 Cloze 卡片，支援 Anki 間隔重複。
```

**問答型：**
```
Q：什麼是「習慣迴路」？
A：由提示 → 行為 → 獎勵 三部分構成的神經回路。
```

---

## PDF 報告格式

- 書名、作者、閱讀日期
- 章節摘要（圖文並茂）
- 精華語錄（引言樣式）
- 知識點速查表
- 讀後心得引導

---

## 環境依賴

```bash
pip3 install requests epub-lib pdfplumber pypdf anthropic openai
```

或一次性安裝：
```bash
pip3 install -r ~/.qclaw/skills/reading-notes-genie/requirements.txt
```
