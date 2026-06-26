# Command Reference

## Environment Initialization

```bash
uv venv
.\.venv\Scripts\Activate.ps1
copy .env.example .env
```

## Installation Check & Bootstrap

```bash
uv run python scripts/check_windows_install.py --json
uv run python scripts/bootstrap_admin.py --json
uv run python scripts/configure_default_models.py --json
```

Optional parameters for `configure_default_models.py`:

```bash
uv run python scripts/configure_default_models.py ^
  --embedding-model bge-m3 ^
  --chat-model qwen2-7b-instruct ^
  --rerank-model bge-reranker-v2-m3 ^
  --api-base http://host.docker.internal:8080/v1 ^
  --json
```

## Dataset Management (`datasets.py`)

```bash
# List all knowledge bases
uv run python scripts/datasets.py list --json

# View single knowledge base details (use default or specified ID)
uv run python scripts/datasets.py info DATASET_ID --json

# Create a knowledge base
uv run python scripts/datasets.py create "Name" --description "Description" --json

# Delete knowledge base (requires user confirmation)
uv run python scripts/datasets.py delete --ids id1,id2 --json
```

## Document Upload & Management (`upload.py`)

```bash
# Upload file to knowledge base
uv run python scripts/upload.py DATASET_ID /path/to/file.pdf --json

# List documents in knowledge base
uv run python scripts/upload.py list DATASET_ID --json

# Delete documents
uv run python scripts/upload.py delete DATASET_ID --ids doc1,doc2 --json
```

## Document Parsing

```bash
# Start parsing
uv run python scripts/parse.py DATASET_ID DOC_ID1 [DOC_ID2 ...] --json

# Check parse status
uv run python scripts/parse_status.py DATASET_ID --json

# Stop parsing and view current status snapshot
uv run python scripts/stop_parse_documents.py DATASET_ID DOC_ID1 [DOC_ID2 ...] --json

# Filter status by document ID
uv run python scripts/parse_status.py DATASET_ID --doc-ids DOC_ID1,DOC_ID2 --json
```

## Update Operations

```bash
# Update knowledge base
uv run python scripts/update_dataset.py DATASET_ID --name "New Name" --description "New Description" --json

# Update parser_config (chunk_token_num, etc.)
uv run python scripts/update_dataset.py DATASET_ID --parser-config "@_parser_config.json" --json

# Update document
uv run python scripts/update_document.py DATASET_ID DOC_ID --name "New Document Name" --json

# Enable/disable document
uv run python scripts/update_document.py DATASET_ID DOC_ID --enabled 1 --json
```

## Search

```bash
# Basic search
uv run python scripts/search.py "query text" --json
uv run python scripts/search.py "query text" DATASET_ID --json

# Specify multiple datasets and documents
uv run python scripts/search.py --dataset-ids ID1,ID2 --doc-ids DOC1,DOC2 "query text" --json

# Retrieval test mode
uv run python scripts/search.py --retrieval-test --kb-id DATASET_ID "query text" --json

# Advanced parameters
uv run python scripts/search.py "query text" --top-k 10 --threshold 0.3 --keyword --json
```

## Models & Chat

```bash
# List available models
uv run python scripts/list_models.py --json

# Create chat (bind knowledge base and model)
uv run python scripts/create_chat.py "KB Q&A" --dataset-ids DATASET_ID --llm-id qwen2-7b-instruct --rerank-id bge-reranker-v2-m3 --json
```
