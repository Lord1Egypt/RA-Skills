---
name: upstage-builder
description: "Build pipelines, agents, RAG flows, and full web services by combining Upstage Solar models, embeddings, and document APIs. Use when building, scaffolding, or deploying anything with Upstage — '솔라로 RAG 만들어줘', 'Upstage 웹앱 만들어줘', 'Upstage로 에이전트 짜줘', 'build a RAG with Solar', 'create an Upstage-based app'. Covers Solar Pro3/Pro2/Mini, embeddings, OCR, document parse, information extraction, classification, schema generation, and Agent API. For single-API one-shot calls (just OCR, just classify), prefer the dedicated upstage-<api> skill instead."
---

# upstage-builder — Upstage API and Webapp Delivery Skill

You are an expert at generating code that uses the **Upstage API** (`api.upstage.ai`). When the user asks you to build features or services using Upstage/Solar models, follow this guide.

For full webapp requests, do not stop at code generation. Treat project location, environment variables, deployment method, and shareable URL delivery as part of the task.

## Webapp Setup Rules

When the user asks for a full web service/app built with Upstage, follow this startup flow:

1. If deployment system and project root are not already known, ask once:
   - Which deployment system should be used?
   - Which project root should be used?
2. If defaults are already configured, use them.
3. For this installation, default to:
   - project root: `/data/.openclaw/workspace/projects`
   - deployment provider: `vercel`
   - visibility mode: `password-protected`
4. Prefer password-protected or private delivery over public delivery unless the user explicitly asks for public access.
5. Create one folder per app under the configured project root.
6. Return these at the end whenever possible:
   - project path
   - stack used
   - required environment variables
   - deployment method
   - visibility mode
   - external deployment URL, or the exact next step if deployment could not be completed
   - site password if password-protected mode was used

Read `references/webapp-workflow.md` for the full project/deployment workflow.

## Quick Start

Upstage APIs are **OpenAI SDK compatible**. Just change `base_url`:

```python
from openai import OpenAI
import os

client = OpenAI(
    api_key=os.environ["UPSTAGE_API_KEY"],
    base_url="https://api.upstage.ai/v1"
)

response = client.chat.completions.create(
    model="solar-pro3",
    messages=[{"role": "user", "content": "Hello!"}]
)
print(response.choices[0].message.content)
```

**API Key**: Always use `os.environ["UPSTAGE_API_KEY"]`. Never hardcode keys. Users get their key from [console.upstage.ai](https://console.upstage.ai).

---

## Output Files

When generated code writes intermediate result files (extracted JSON, parsed markdown, embeddings cache, etc.):

- **Default**: `<system-temp>/<input-stem>.<suffix>.<ext>` (e.g., `/tmp/receipt.ocr.json`, `/tmp/report.parsed.md`). Use `tempfile.gettempdir()` for cross-platform code.
- **Override**: if the user specifies an output path, use it.
- **Always print the resolved absolute path** so the user can locate the file.

This rule does NOT apply to webapp scaffolding (project root, `.env`, `DEPLOY.md`) — those follow the configured project root in **Webapp Setup Rules** above.

Per-API suffix convention (matches the dedicated specialty skills):

| API | Suffix | Common ext |
|-----|--------|-----------|
| OCR | `.ocr` | `.json` |
| Document Parse | `.parsed` | `.md`, `.html` |
| Document Classification | `.classified` | `.json` |
| Information Extraction | `.extracted` | `.json` |
| Schema Generation | `.schema` | `.json` |
| Agent (Studio) | `.agent` (or `.<step-name>` per step) | `.json` |
| Solar (delegated) | `.solar` (with timestamp prefix) | `.md`, `.txt` |

---

## Model Catalog

### Chat Models

| Model | Description | Context | Best For |
|-------|-------------|---------|----------|
| `solar-pro3` | Flagship (102B MoE, 12B active) | 128K | Complex reasoning, function calling, structured output |
| `solar-pro2` | Previous gen flagship (31B) | 65K | General tasks, good balance |
| `solar-mini` | Lightweight, fast (10.7B) | 32K | Cost-sensitive, simple tasks |
| `syn-pro` | Synthetic data optimized | - | Data generation (no function calling) |

### Embedding Models

| Model | Description | Dimensions |
|-------|-------------|------------|
| `embedding-query` | For search queries/questions | 4096 |
| `embedding-passage` | For documents/passages to search | 4096 |

### Document Models

| Model | Description |
|-------|-------------|
| `ocr` | Text extraction with word-level coordinates |
| `document-parse` | Convert docs to HTML/Markdown with layout detection |
| `document-classify` | Classify documents into user-defined categories |
| `information-extract` | Extract structured data with custom JSON schema |
| `schema-generate` | Auto-generate extraction schemas from sample docs |
| `receipt-extraction` | Prebuilt: extract from receipts |

---

## Model Selection Guide

| Your Need | Use This Model |
|-----------|---------------|
| Complex reasoning, coding | `solar-pro3` with `reasoning_effort: "high"` |
| Fast simple responses | `solar-mini` |
| Cost-sensitive production | `solar-mini` |
| Synthetic data generation | `syn-pro` |
| Function calling / tool use | `solar-pro3` (parallel tool calls supported) |
| Structured JSON output | `solar-pro3`, `solar-pro2`, or `solar-mini` |
| Semantic search (queries) | `embedding-query` |
| Semantic search (documents) | `embedding-passage` |
| PDF/image → text | `ocr` |
| PDF/image → markdown/HTML | `document-parse` |
| Extract fields from docs | `information-extract` |
| Classify document types | `document-classify` |

---

## API Categories

### 1. Chat Completions
**Endpoint**: `POST /v1/chat/completions`
- Standard chat, streaming, function calling, structured output, reasoning, prompt caching
- OpenAI SDK compatible (just change base_url)
- **Details**: Read `references/chat-completions.md`

### 2. Embeddings
**Endpoint**: `POST /v1/embeddings`
- Dual-model: `embedding-query` for queries, `embedding-passage` for documents
- 4096-dimensional normalized vectors (dot product = cosine similarity)
- Max 100 texts per batch, 4000 tokens per text
- **Details**: Read `references/embeddings.md`

### 3. Document Processing (OCR + Parse + Split)
**Endpoints**: `POST /v1/document-digitization`, `POST /v1/document-digitization/async`
- OCR: word-level text extraction with bounding boxes
- Parse: converts PDF/images to structured HTML/Markdown, chart recognition, equation LaTeX
- Sync (≤100 pages) and Async (≤1000 pages) modes
- Split: via Classification API with `split=true`
- **Details**: Read `references/document-processing.md`

### 4. Information Extraction
**Endpoints**: `POST /v1/information-extraction`, `POST /v1/information-extraction/async`
- Custom schema-based extraction from documents
- Schema Generation: auto-generate schemas from sample docs
- Prebuilt models: receipt, air waybill, bill of lading, commercial invoice, KR export declaration
- OpenAI SDK compatible (base_url changes to `/v1/information-extraction`)
- **Details**: Read `references/information-extraction.md`

### 5. Document Classification
**Endpoint**: `POST /v1/document-classification`
- Classify into user-defined categories with confidence scores
- Document split feature (`split=true`) for multi-doc PDFs
- OpenAI SDK compatible (base_url changes to `/v1/document-classification`)
- **Details**: Read `references/document-classification.md`

### 6. Agent API (Studio Workflows)
**Base URL**: `https://api.upstage.ai/v2` (v2, not v1)
- Multi-step workflows configured in Upstage Studio
- File upload → Agent job → Poll for results
- OpenAI Responses API compatible
- **Details**: Read `references/agent-api.md`

### 7. Common Patterns & Error Handling
- Error codes, rate limits, retry strategies, SDK setup
- RAG pipeline, document routing, batch processing patterns
- **Details**: Read `references/common-patterns.md`

---

## Code Generation Guidelines

When generating Upstage API code, follow these rules:

1. **Always use OpenAI SDK** unless the API requires multipart/form-data (OCR, Document Parse, Prebuilt IE)
2. **API key from environment**: `os.environ["UPSTAGE_API_KEY"]` — never hardcode
3. **base_url varies by API**:
   - Chat & Embeddings: `https://api.upstage.ai/v1`
   - Document Classification: `https://api.upstage.ai/v1/document-classification`
   - Information Extraction: `https://api.upstage.ai/v1/information-extraction`
   - Agent API: `https://api.upstage.ai/v2`
4. **Use model aliases** (e.g., `solar-pro3`), not version-specific names
5. **Default to `solar-pro3`** for complex tasks, `solar-mini` for simple/cost-sensitive
6. **For document APIs using multipart/form-data**, use `requests` library directly
7. **For RAG pipelines**: use `embedding-passage` for indexing, `embedding-query` for search
8. **Include error handling**: catch `openai.RateLimitError` with exponential backoff

### Key Differences from OpenAI

- Reasoning uses `reasoning_effort` param (not separate reasoning model)
- Embeddings use dual-model approach (query vs passage) — not a single model
- Document APIs are unique to Upstage (OCR, Parse, IE, Classification)
- Structured outputs require `strict: true` and `additionalProperties: false`
- IE schemas: first-level properties must be string/integer/number/array (no objects at top level)

---

## Examples

- Basic chat: See `examples/chat-example.py`
- RAG pipeline: See `examples/rag-example.py`
- Document processing: See `examples/document-example.py <path/to/document.pdf>`
- Smoke test: Install `requirements.txt`, then run `python scripts/smoke_test.py` to verify chat, embeddings, and optional design registry access
- Reference refresh: Run `python scripts/refresh_references.py` to pull the latest API reference snapshots into `references/`
- Webapp project init: Run `python scripts/init_webapp_project.py <project-slug>` to create a standard app folder with `README.md`, `.env.example`, and `DEPLOY.md`

---

## Reference Files

When you need detailed API parameters, response formats, or advanced features, read the appropriate reference file. These files are generated snapshots; refresh them with `python scripts/refresh_references.py` when you want the latest upstream docs.

| File | Content |
|------|---------|
| `references/chat-completions.md` | Full Chat API: params, function calling, structured output, streaming, reasoning, prompt caching |
| `references/embeddings.md` | Embeddings API: query/passage models, batch processing, similarity |
| `references/document-processing.md` | OCR, Document Parse (sync/async), Document Split |
| `references/information-extraction.md` | IE (sync/async), Schema Generation, Prebuilt IE |
| `references/document-classification.md` | Classification API with confidence scores |
| `references/agent-api.md` | Agent API v2: Studio workflows, file upload, jobs |
| `references/common-patterns.md` | Error handling, rate limits, auth, RAG/routing/batch patterns |
| `references/webapp-workflow.md` | Project-root, deployment-provider, and delivery workflow for full webapp tasks |

---

## Source URLs

Original sources for reference files. Running `python scripts/refresh_references.py` fetches the latest content from these URLs and updates the `references/` files.

| Source | URL | Auth | Updates |
|--------|-----|------|---------|
| Upstage API Docs | `https://console.upstage.ai/api/docs/for-agents/raw` | None | references/chat-completions.md ~ common-patterns.md (7 files) |
