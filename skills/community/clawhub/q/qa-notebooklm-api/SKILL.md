---
name: qa_notebooklm_api
description: >
  Use NotebookLM CLI to manage notebooks, add sources (text/URLs), ask questions,
  summarize, and generate learning materials (slides, quizzes, flashcards, etc.).
  Activate when user mentions creating a NotebookLM notebook, adding sources,
  asking questions about notebook content, summarizing, or generating study
  materials like slides, quizzes, or flashcards.
  Requires: `notebooklm` CLI installed and authenticated.
  Install: `pip install notebooklm` or see https://github.com/tiangong-ai/notebooklm-cli
---

# NotebookLM Skill

Manage NotebookLM notebooks via the `notebooklm` CLI.

## Setup

```bash
# Install notebooklm CLI
pip install notebooklm

# Authenticate (opens browser)
notebooklm login
```

## Core Actions

### List all notebooks
```bash
notebooklm list
```

### Create a new notebook
```bash
notebooklm create "Notebook Title"
```
Returns the notebook ID (e.g. `9e2f71b6-373e-432f-9ed0-e6a017cfdcac`).

### Add a URL or text source to a notebook
```bash
# Set notebook as current context
notebooklm use <notebook_id>

# Add URL source
notebooklm source add "https://example.com/article"

# Add multiple sources (wait for each)
notebooklm source add "https://url1.com"
notebooklm source wait <source_id>
```

### Ask a question (chat with notebook)
```bash
# Ask in current notebook (set with notebooklm use <id>)
notebooklm ask "What are the main topics?"
notebooklm ask "Summarize this content in Chinese"
notebooklm ask "Generate 5 quiz questions" --json

# Start new conversation
notebooklm ask "Summarize" --new
```

### Get notebook summary
```bash
notebooklm summary
```

### Generate learning materials
```bash
notebooklm generate slide-deck "create a presentation about X"
notebooklm generate quiz "create a 10-question quiz"
notebooklm generate flashcards "make flashcards for key terms"
notebooklm generate infographic "visual summary"
notebooklm generate report "detailed report"
```

### Poll artifact status and download
```bash
# Poll (after generate, check if ready)
notebooklm artifact poll <artifact_id>

# List artifacts
notebooklm artifact list

# Download slide deck as PPTX/PDF
notebooklm download slide-deck --artifact <id> --format pptx
notebooklm download slide-deck --artifact <id> --format pdf

# Download as PDF
notebooklm download slide-deck

# Download quiz/flashcards
notebooklm download quiz
notebooklm download flashcards
```

## Intent → Action Mapping

| User says | Action |
|---|---|
| "列出我的 notebook" / "list notebooks" | `notebooklm list` |
| "新建 notebook 叫 X" | `notebooklm create "X"` |
| "在 notebook 里加入这个链接" | `notebooklm use <id> && notebooklm source add <url>` |
| "导入这段文字到 notebook" | `notebooklm use <id> && notebooklm source add "<text>"` |
| "总结这个 notebook" | `notebooklm use <id> && notebooklm summary` |
| "问我这个 notebook X 问题" | `notebooklm use <id> && notebooklm ask "X"` |
| "生成 PPT" / "生成幻灯片" | `notebooklm use <id> && notebooklm generate slide-deck` then poll & download |
| "生成测验" / "生成 quiz" | `notebooklm use <id> && notebooklm generate quiz` |
| "生成闪卡" | `notebooklm use <id> && notebooklm generate flashcards` |
| "下载生成的 PPT" | `notebooklm download slide-deck --format pptx` |

## Workflow: Create notebook + add sources + generate PPT

```bash
# 1. Create
notebooklm create "English Grammar Notes"

# 2. Set as current
notebooklm use <new_id>

# 3. Add sources
notebooklm source add "https://example.com/grammar-guide"
# wait for ready
notebooklm source wait <source_id>

# 4. Generate slide deck
notebooklm generate slide-deck "Create educational slides about modal verbs"

# 5. Poll until done (takes 2-5 min)
notebooklm artifact poll <artifact_id>

# 6. Download
notebooklm download slide-deck --artifact <artifact_id> --format pptx
```

## Notes

- Artifact generation takes 2-10 minutes — poll periodically with `notebooklm artifact poll <id>`
- Use `--json` flag with `ask` for machine-readable responses
- Use `notebooklm status` to check current notebook context
- Use `notebooklm source list` to see all sources in a notebook
- Artifact types available: slide-deck, quiz, flashcards, infographic, report, audio, video, mind-map, data-table
