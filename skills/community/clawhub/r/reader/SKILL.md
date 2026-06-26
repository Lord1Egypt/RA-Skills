---
name: reader
description: Local-first reading and distillation engine for documents and pasted text. Use whenever the user wants to read, summarize, extract key points, compare documents, understand a report, pull action items, or turn long text into a clear brief. Works locally with plain text, markdown, HTML, JSON, and other text-like files. No external sync or credentials.
---

# Reader: Read less. Understand more.

## Core Philosophy
1. Distill before overwhelming.
2. Prefer clarity over verbosity.
3. Extract decisions, actions, and questions — not just summaries.
4. Keep reading local, transparent, and low-friction.

## Runtime Requirements
- Python 3 must be available as `python3`
- No external packages required

## Storage
All data is stored locally only under:
- `~/.openclaw/workspace/memory/reader/history.json`

No external sync. No cloud storage. No third-party APIs.

## Use Cases
- Summarize a document or pasted text
- Extract key points, action items, and open questions
- Compare two drafts or reports
- Turn long text into a concise reading brief
- Help the user understand dense writing faster

## Key Workflows
- **Read**: `read_text.py --file path/to/file`
- **Summarize**: `summarize.py --file path/to/file --style executive`
- **Brief**: `extract_brief.py --file path/to/file`
- **Compare**: `compare_texts.py --file_a old.txt --file_b new.txt`

## Scripts
| Script | Purpose |
|---|---|
| `init_storage.py` | Initialize local storage |
| `read_text.py` | Normalize and read local text-like files |
| `summarize.py` | Generate concise summaries |
| `extract_brief.py` | Extract summary, key points, actions, and questions |
| `compare_texts.py` | Compare two documents |
