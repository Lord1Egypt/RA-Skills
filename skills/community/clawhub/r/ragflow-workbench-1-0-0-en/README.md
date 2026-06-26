# RAGFlow Workbench

## Overview

**ragflow-workbench** is an end-to-end RAGFlow automation skill pack for Windows. It covers the full lifecycle from zero-setup RAGFlow deployment to daily knowledge base management — installation checks, admin initialization, model configuration, knowledge base CRUD, document upload/parsing/retrieval, and chat creation — all through one-click command-line scripts.

No need to manually interact with the RAGFlow web UI or memorize complex API calls; ready out of the box.

---

## Feature List

### 1. Environment Preparation & Installation Check
| Feature | Description |
|---------|-------------|
| Docker readiness check | Verify Docker CLI availability and version |
| Container running check | Confirm RAGFlow container is running |
| API reachability | Test RAGFlow API (port 9380) connectivity |
| Web UI reachability | Test RAGFlow Web UI (port 9222) accessibility |
| One-click health report | Aggregate all four status checks with actionable recommendations |

### 2. Admin Bootstrap & API Key Generation
| Feature | Description |
|---------|-------------|
| Admin registration | Auto-encrypt password via container and register admin account |
| Auto-login & JWT | Obtain auth token for subsequent operations |
| API Key create/reuse | Auto-create named API token (reuse if exists) |
| .env auto-configuration | Write API URL, API Key, container name to env file |

### 3. Default Model Configuration
| Feature | Description |
|---------|-------------|
| Embedding model config | Add and set vector embedding model (default bge-m3) |
| Chat model config | Add and set chat model (default qwen2-7b-instruct) |
| Rerank model config | Add and set reranking model (default bge-reranker-v2-m3) |
| OpenAI-compatible gateway | Supports any `host.docker.internal` or other local model service URL |
| Tunable parameters | Supports max_tokens, API Key, model name, etc. |

### 4. Knowledge Base (Dataset) Management
| Feature | Description |
|---------|-------------|
| List knowledge bases | List all knowledge bases (ID, name, chunk count, creation time, etc.) |
| Knowledge base details | View full configuration of a single knowledge base |
| Create knowledge base | Specify name/description/embedding model/chunk method/permissions/language |
| Delete knowledge base | **Safety: requires explicit user confirmation** |
| Update knowledge base | Modify name/description/embedding model/chunk method/permissions/parser config |
| Default knowledge base | Auto-record recently created KB ID as quick-operation target |

### 5. Document Upload & Management
| Feature | Description |
|---------|-------------|
| Upload files | Upload PDF and other files to a knowledge base (auto-detect MIME type) |
| Document list | Paginated list of all documents in a knowledge base (name/status/chunks/tokens) |
| Delete documents | Batch delete by document IDs |
| Update documents | Modify document name/chunk method/parser config/metadata/enabled status |

### 6. Document Parse Lifecycle
| Feature | Description |
|---------|-------------|
| Start parsing | Launch async parse task for specified documents, return immediately |
| Stop parsing | Cancel ongoing parse tasks |
| Parse status | View summary of all document parse statuses (UNSTART/RUNNING/DONE/FAIL/CANCEL) |
| Filter by document | Check progress for specific document IDs |
| Progress messages | Echo server-side progress messages verbatim; FAIL shows specific error reason |
| Auto-troubleshoot guidance | On FAIL, automatically guide user to troubleshooting guide |

### 7. Knowledge Retrieval
| Feature | Description |
|---------|-------------|
| Semantic search | Query by text, return matching chunks with similarity scores |
| Multi-dataset search | Query across multiple knowledge bases at once |
| Multi-document filter | Restrict search scope to specific documents |
| Hybrid search | Vector similarity + keyword weight tuning |
| Knowledge graph enhancement | Optionally enable KG retrieval |
| Fine-grained parameters | Top-k, similarity threshold, pagination, rerank model all configurable |
| Retrieval test mode | Directly call underlying retrieval_test API |

### 8. Chat Creation
| Feature | Description |
|---------|-------------|
| Create chat | Bind knowledge base + chat model + rerank model |
| Custom prompts | Supports system prompt, empty-retrieval reply, etc. |

### 9. Model Listing
| Feature | Description |
|---------|-------------|
| List models | Group all available models by type or vendor |
| Model details | View model ID/name/type/vendor/tokens used/status/API URL |

### 10. Troubleshooting
| Feature | Description |
|---------|-------------|
| Chunk too large detection | Identify Embedding API physical limit errors and suggest fixes |
| Configuration tuning guide | Reduce `chunk_token_num` to 50%-60% of API limit |

---

## Workflow

```
1. Environment check    →  scripts/check_windows_install.py
2. Admin bootstrap      →  scripts/bootstrap_admin.py
3. Model configuration  →  scripts/configure_default_models.py
4. Create knowledge base →  scripts/datasets.py create
5. Upload documents     →  scripts/upload.py
6. Start parsing        →  scripts/parse.py
7. Check status         →  scripts/parse_status.py
8. Search knowledge     →  scripts/search.py
9. Create chat          →  scripts/create_chat.py
```

Every step supports `--json` for structured output, making it easy to integrate into automated workflows.

---

## Dependencies

- **Python** >= 3.10 (uv recommended for environment management)
- **Docker** (to run RAGFlow container)
- **RAGFlow** deployed and running via Docker


