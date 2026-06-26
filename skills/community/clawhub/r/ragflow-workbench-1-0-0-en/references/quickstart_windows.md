# Windows Quick Start Guide

## 0. Initialize uv Environment

```bash
uv venv
.\.venv\Scripts\Activate.ps1
```

## 1. Installation Check

Ensure Docker Desktop is running and the RAGFlow container is active.

```bash
uv run python scripts/check_windows_install.py
```

If the check fails, resolve container or port issues before proceeding.

## 2. Initialize Admin & API Key

The script will automatically:

- Encrypt the password using `crypt` inside the container
- Register an admin account (skips if already exists)
- Log in and generate an API Token
- Write `RAGFLOW_API_URL` / `RAGFLOW_API_KEY` to `.env`

```bash
uv run python scripts/bootstrap_admin.py --json
```

## 3. Configure Default Models

This script adds and sets the default models (Embedding/Chat/Rerank):

```bash
uv run python scripts/configure_default_models.py --json
```

To specify model names or a local model gateway URL:

```bash
uv run python scripts/configure_default_models.py ^
  --embedding-model bge-m3 ^
  --chat-model qwen2-7b-instruct ^
  --rerank-model bge-reranker-v2-m3 ^
  --api-base http://host.docker.internal:8080/v1 ^
  --json
```

## 4. Create Knowledge Base & Upload

```bash
uv run python scripts/datasets.py create "Getting Started KB" --json
uv run python scripts/upload.py DATASET_ID C:\path\to\file.pdf --json
uv run python scripts/parse.py DATASET_ID DOC_ID --json
uv run python scripts/parse_status.py DATASET_ID --json
```

## 5. Create Chat & Search

Create a chat session (bind knowledge base and models):

```bash
uv run python scripts/create_chat.py "Getting Started Chat" ^
  --dataset-ids DATASET_ID ^
  --llm-id qwen2-7b-instruct ^
  --rerank-id bge-reranker-v2-m3 ^
  --json
```

Test search:

```bash
uv run python scripts/search.py "summarize knowledge base" DATASET_ID --json
```
