# Knowledge Base API Reference

Knowledge Base connects your data (documents, FAQs, APIs, raw text) to agents so answers are factual and brand-aligned. Two retrieval modes:
- **Agentic mode** (default) — LLM decides when to search each KB based on the query
- **RAG mode** — Every user query is searched against the KB

## Create a Knowledge Base

`POST /v1/ext/kb`

```bash
curl --request POST \
  --url https://api.trugen.ai/v1/ext/kb \
  --header 'Content-Type: multipart/form-data' \
  --header 'x-api-key: <api-key>' \
  --form 'name=HR Policy' \
  --form 'description=This knowledge base contains HR and compensation related information.' \
  --form 'input=@./hr-policy.pdf' \
  --form 'text=As of 2025, we have increased personal leaves to 15 per year.'
```

**Supported input formats:**
- File upload: `.pdf`, `.docx`, `.txt`, `.html`
- Raw text via `text` form field
- Website URL (scraped and indexed)

**Response:**
```json
{ "id": "5273e435-3cbb-4a11-9ea9-2c150ba19009", "message": "Knowledge Base created successfully" }
```

## Attach KB to Agent

Pass the KB `id` and `name` in the `knowledge_base` array when creating or updating an agent:
```json
"knowledge_base": [
  { "id": "5273e435-3cbb-4a11-9ea9-2c150ba19009", "name": "HR Policy" }
]
```

> You can attach **multiple** knowledge bases to a single agent.

## Agentic Mode — Naming Tip

In agentic mode, the LLM uses the KB `name` and `description` to decide which KB to query. Use descriptive names:
```
Name: Get-HR-Policies
Description: Use this whenever the user is asking any question about HR policies.
```

## Get Knowledge Base by ID

`GET /v1/ext/kb/{id}`

```bash
curl --request GET \
  --url https://api.trugen.ai/v1/ext/kb/{id} \
  --header 'x-api-key: <api-key>'
```

**Response:** Returns `knowledge_base` object (id, name, description, no_of_rec, created_at, updated_at) plus a `documents` array with each document's id, name, preview_url, and type.

## List All Knowledge Bases

`GET /v1/ext/kbs`

```bash
curl --request GET \
  --url https://api.trugen.ai/v1/ext/kbs \
  --header 'x-api-key: <api-key>'
```

## Update Knowledge Base

`PUT /v1/ext/kb/{id}`

```bash
curl --request PUT \
  --url https://api.trugen.ai/v1/ext/kb/{id} \
  --header 'Content-Type: application/json' \
  --header 'x-api-key: <api-key>' \
  --data '{
    "name": "Revised HR Policies",
    "description": "Revised HR and Compensation policy.",
    "is_active": true
  }'
```

**Response:** `{ "id": "...", "message": "Knowledge Base updated successfully" }`

## Add More Documents to an Existing KB

`POST /v1/ext/kb/{id}/doc`

```bash
curl --request POST \
  --url https://api.trugen.ai/v1/ext/kb/{id}/doc \
  --header 'Content-Type: multipart/form-data' \
  --header 'x-api-key: <api-key>' \
  --form 'text=New policy text or https://yoursite.com/page' \
  --form 'input=@new-document.pdf'
```

**Response:** `{ "added": 1, "message": "Content added successfully to existing Knowledge Base" }`

## Delete a Document from a KB

`DELETE /v1/ext/kb/doc/{document_id}`

```bash
curl --request DELETE \
  --url https://api.trugen.ai/v1/ext/kb/doc/{document_id} \
  --header 'x-api-key: <api-key>'
```

**Response:** `{ "id": "...", "message": "Document deleted successfully" }`

## Delete a Knowledge Base

`DELETE /v1/ext/kb/{id}`

```bash
curl --request DELETE \
  --url https://api.trugen.ai/v1/ext/kb/{id} \
  --header 'x-api-key: <api-key>'
```
