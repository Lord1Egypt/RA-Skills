---
name: ragflow-workbench
description: "RAGFlow Workbench — end-to-end RAG platform on Windows: Docker install check, admin bootstrap and API key generation, default model setup (Embedding/Chat/Rerank), knowledge base CRUD, document upload-parse lifecycle, retrieval/search, chat creation. Triggers when the user mentions: RAGFlow installation or deployment, setting up a local RAG instance on Windows, creating a knowledge base, configuring models for RAG, managing documents in datasets, searching across knowledge bases."
---

# RAGFlow Workbench

**Prerequisites**: This skill requires `uv` (Python package manager) and `docker` (container runtime).

Prefer using scripts from `scripts/`. Use `--json` by default to ensure structured output for automation.
User-facing output follows `references/output-format.md`.

---

## Smart Execution Flow

Determine the RAGFlow environment readiness from the `.env` file to avoid redundant checks:

```
┌─ Check if .env contains a valid RAGFLOW_API_KEY?
│
├─ ✅ Yes (connection established)
│    Skip environment checks, use API directly
│    bootstrap_admin.py / configure_default_models.py do not need re-execution
│    Start from API workflows: datasets.py / upload.py / search.py etc.
│
├─ ❌ No (first-time use)
│    ⚠️ Note: The following steps involve environment detection and privileged operations;
│       you MUST confirm with the user before executing.
│
│    1. Ask the user for their intent (present these options; add more as context allows):
│       a. "Have you not yet downloaded and installed RAGFlow locally? Would you like me to help you download and install it?"
│       b. "Do you already have a local RAGFlow instance running? Please provide the address and login credentials, or an existing API Key — I will test the connection automatically and let you know the result."
│
│    2. Execute based on user response:
│       ┌─ User chooses fresh install (a)
│       │   Guide user to download Docker Desktop → deploy RAGFlow → wait for readiness
│       │   Then continue with check → bootstrap → configure workflow
│       │
│       ├─ User provides existing instance info (b1)
│       │   1. Test connection with provided address/credentials
│       │   2. Success → write to .env, skip env checks in future sessions
│       │   3. Failure → report specific error, guide troubleshooting
│       │
│       ├─ User provides existing API Key (b2)
│       │   1. Test key validity
│       │   2. Valid → write to .env, skip all bootstrap steps
│       │
│       └─ Other cases → handle flexibly based on actual user response
│
│    3. Automated execution after confirmation (choose as appropriate):
│       - check_windows_install.py --json    Environment check (after fresh install)
│       - bootstrap_admin.py --json          Bootstrap + API Key
│       - configure_default_models.py --json Configure default models
│       → .env now contains RAGFLOW_API_KEY; future sessions skip env checks
│
└─ 🚀 Enter API Workflow
```

**How it works**: After `bootstrap_admin.py` succeeds, it writes `RAGFLOW_API_URL` and `RAGFLOW_API_KEY` to `.env`. As long as these values exist and are non-empty, the environment is considered validated and `check_windows_install.py` and other setup scripts will not be re-run.

---

## Use Cases

- First-time RAGFlow setup on Windows, ready out of the box
- Auto-create admin user and obtain API Key
- Configure default Embedding / Chat / Rerank models
- Create knowledge bases, upload files, trigger parsing, check parse status
- Search knowledge bases, manage datasets/documents, create chat sessions

## Full Lifecycle Workflow

```
check_windows_install.py  →  bootstrap_admin.py  →  configure_default_models.py
                                                          ↓
                          datasets.py / upload.py / parse.py / parse_status.py
                                                          ↓
                          search.py / create_chat.py
```

### Quick Start

```bash
uv venv
.\.venv\Scripts\Activate.ps1
copy .env.example .env

uv run python scripts/check_windows_install.py --json
uv run python scripts/bootstrap_admin.py --json
uv run python scripts/configure_default_models.py --json
```

### Knowledge Base & Document Management

```bash
uv run python scripts/datasets.py create "Sample Knowledge Base" --json
uv run python scripts/upload.py DATASET_ID /path/to/file.pdf --json
uv run python scripts/parse.py DATASET_ID DOC_ID --json
uv run python scripts/parse_status.py DATASET_ID --json
```

### Search & Chat

```bash
uv run python scripts/search.py "query text" DATASET_ID --json
uv run python scripts/create_chat.py "Chat Name" --dataset-ids DATASET_ID --llm-id qwen2-7b-instruct --json
```

## Full Command Reference

See [`references/command-reference.md`](references/command-reference.md) for all commands and parameters, including:
- `datasets.py` list / info / create / delete
- `upload.py` list / delete + file upload
- `parse.py` / `parse_status.py` / `stop_parse_documents.py`
- `search.py` full retrieval parameters
- `update_dataset.py` / `update_document.py`
- `list_models.py` / `create_chat.py`

## Execution Constraints

- **Delete operations** must first list candidates and obtain explicit user confirmation
- Only delete using explicit `dataset_id` / `document_id`
- Upload does not automatically trigger parsing; only run `parse.py` when the user requests it
- `parse.py` only initiates tasks; progress must be checked via `parse_status.py`
- If `parse_status.py` returns a `progress_msg`, echo it verbatim; when status is `FAIL`, treat it as the primary error and guide the user to [`references/troubleshooting.md`](references/troubleshooting.md)
- `bootstrap_admin.py` and `configure_default_models.py` require Docker containers accessible via `docker exec`

## Output Rules

- Follow `references/output-format.md`
- Use tables for 3+ structured data items
- Preserve `api_error`, `error`, `message` and similar fields as-is
- Do not fabricate progress percentages, failure reasons, or model configuration results


