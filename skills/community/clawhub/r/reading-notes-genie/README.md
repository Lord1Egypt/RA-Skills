# 📚 Reading Notes Genie — 閱讀筆記精靈

> 輸入書名 / 上傳 PDF 或 EPUB，AI 自動生成結構化閱讀筆記，精華語錄、知識點卡片、支援 Markdown / Anki / PDF 多格式匯出。

[![Python 3.9+](https://img.shields.io/badge/Python-3.9+-blue.svg)](https://python.org)

---

## ✨ 功能特色

| 功能 | 說明 |
|------|------|
| 📄 PDF 解析 | 文字萃取、表格萃取、OCR 掃描件、書籤導航 |
| 📚 EPUB 解析 | 章節結構、Metadata、封面萃取 |
| 🤖 AI 摘要 | OpenAI / Anthropic / 本地模型（Ollama）自動偵測 |
| 💬 章節摘要 | 每章核心論點 + 3-5 個要點 + 精華語錄 |
| 🃏 知識卡片 | 自動萃取可複習的知識點，支援 Cloze / 問答格式 |
| 📤 多格式匯出 | Markdown · JSON · Anki (.apkg) · PDF |

---

## 🚀 快速開始

### 安裝依賴

```bash
pip3 install -r requirements.txt
```

### 基本用法

```bash
# 方式一：輸入書名（AI 網路查詢，無需本地檔案）
python3 scripts/book_summarizer.py \
  --book "原子習慣" \
  --output ./notes/

# 方式二：分析本地 PDF
python3 scripts/book_summarizer.py \
  --file ./my-book.pdf \
  --output ./notes/

# 方式三：分析 EPUB
python3 scripts/book_summarizer.py \
  --file ./my-book.epub \
  --output ./notes/
```

### AI 模型設定

```bash
# OpenAI（推薦）
export OPENAI_API_KEY="sk-..."

# Anthropic Claude
export ANTHROPIC_API_KEY="sk-ant-..."

# 本地模型（Ollama）
export LOCAL_MODEL_URL="http://localhost:11434/api/generate"
export LOCAL_MODEL="llama3"
```

> 無 API Key 時，會自動使用離線關鍵字萃取模式（仍可解析 PDF/EPUB 內容）。

---

## 📤 匯出格式

### 1. Markdown（可直接存入 Obsidian / Notion）

```bash
python3 scripts/notes_exporter.py \
  --input ./notes/原子習慣.json \
  --format markdown \
  --output ./output/
# → output/原子習慣.md
```

### 2. Anki 卡片（間隔重複背誦）

```bash
# 文字格式（通用）
python3 scripts/notes_exporter.py \
  --input ./notes/原子習慣.json \
  --format anki \
  --output ./output/
# → output/原子習慣_anki.txt
# 在 Anki → 檔案 → 匯入 → 選擇上傳的 .txt

# 真正 .apkg（需要 pip install genanki）
python3 scripts/notes_exporter.py \
  --input ./notes/原子習慣.json \
  --format apkg \
  --output ./output/
# → output/原子習慣.apkg（雙擊直接匯入 Anki）
```

### 3. PDF 報告（精美排版，可列印）

```bash
python3 scripts/notes_exporter.py \
  --input ./notes/原子習慣.json \
  --format pdf \
  --output ./output/
# → output/原子習慣.pdf
```

### 4. 僅生成知識卡片

```bash
python3 scripts/knowledge_card.py \
  ./notes/原子習慣.json \
  --format all \
  --output ./cards/
```

---

## 📁 腳本架構

```
scripts/
├── epub_parser.py         # EPUB 解析（Metadata + 章節 + 封面）
├── pdf_extractor.py       # PDF 萃取（文字 + OCR + 表格 + 書籤）
├── book_summarizer.py     # AI 摘要核心（章節摘要 + 語錄萃取）
├── knowledge_card.py      # 知識卡生成（Cloze + 問答 + Markdown）
└── notes_exporter.py      # 多格式匯出（MD / Anki / PDF / JSON）
```

---

## 🔧 環境需求

- Python 3.9+
- 推薦 API：金鑰（OpenAI / Anthropic）
- 可選：`tesseract` + `poppler`（PDF OCR）、`genanki`（.apkg 格式）

---

## 📄 License

MIT
