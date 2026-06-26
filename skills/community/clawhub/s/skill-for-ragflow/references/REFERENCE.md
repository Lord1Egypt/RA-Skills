# Output Format Reference

Style guide for consistent RAGFlow skill responses.
Apply this reference to all user-facing output for this skill.

Use this reference only for the final user-facing response. The bundled CLI may still emit raw JSON for automation, especially with `--json`; summarize that raw output into these formats instead of reproducing it verbatim unless the user explicitly asks for the exact payload.

## Format Decision Matrix

| Information Type | Format | Use Case |
|------------------|--------|----------|
| Multiple items (3+) with attributes | Table | Datasets list, search results, model list |
| Sequential steps | Numbered List | Upload workflow, procedures |
| Features/options | Bullet List | Capability overview, model features |
| Structured data | JSON Code Block | API responses, DSL definitions |
| Document content | Quote Block | Retrieved chunks |
| Single object properties | Definition List | Dataset details, model details |
| Status | Status marker + text | Parsing tables use `UNSTART` / `RUNNING` / `CANCEL` / `DONE` / `FAIL`; generic success can use `OK` |

## Common Formats

### Tables (3+ items)
```markdown
| Dataset | Docs | Chunks | Status |
|---------|------|--------|--------|
| delete  | 4    | 53     | OK     |
```
- Abbreviate long IDs: `abc123...`
- Use consistent status labels: `UNSTART`, `RUNNING`, `CANCEL`, `DONE`, `FAIL` for parsing; `OK` for generic success; `WARN` for warnings

### Bullet Lists
```markdown
- Upload documents to dataset
- Start parsing to generate chunks
```
- Start with verbs for actions
- Keep nesting shallow

### Numbered Lists
```markdown
1. Create dataset
2. Upload files
3. Start parsing
```
- Use for sequential procedures

### Status Labels
| Label | Meaning |
|-------|---------|
| `UNSTART` | Not started |
| `RUNNING` | In progress |
| `CANCEL` | Cancelled |
| `DONE` | Finished successfully |
| `FAIL` | Failed / Unavailable |
| `OK` | Success / Available |
| `WARN` | Warning |
| `EMPTY` | Empty |

## Response Templates

**List operations:**
```markdown
**Datasets** (3 total)

| Name | ID | Status | Chunks |
|------|-----|--------|--------|
| docs | abc... | OK | 152 |
```

**Search results:**
```markdown
**Results** (2 found)

| # | Source | Similarity | Content |
|---|--------|------------|---------|
| 1 | doc.pdf | 85% | excerpt... |
```

**Object details:**
```markdown
**Dataset Details**

**ID:** `1ce917df20e411f191a984ba59bc54d9`
**Name:** delete
**Chunks:** 53
```

**Model list:**
```markdown
**Available Models** (12 in 3 groups)

| Group | Model | Type | Factory |
|-------|-------|------|---------|
| chat | gpt-4 | chat | OpenAI |
| chat | gpt-3.5 | chat | OpenAI |
| embedding | text-embedding-3 | embedding | OpenAI |
```

**Parsing status:**
```markdown
**Parsing Status**

| Document | Status | Chunks |
|----------|--------|--------|
| report.pdf | DONE | 45 |
| notes.md | RUNNING | - |
| data.xlsx | FAIL | 0 |
```

**Chat/Agent conversation:**
```markdown
**Response**

> The answer to your question...

**Sources:** 3 chunks from 2 documents
- doc1.pdf (similarity: 0.85)
- doc2.md (similarity: 0.72)
```

**Embedded website access:**
```markdown
**Embedded Chat**

**Chat:** `chat_abc123...`
**Mode:** fullscreen iframe
**Session:** `sess_abc123...`
**Answer:** OK

The iframe URL was generated successfully. Do not print the full `token`, `beta`, iframe `src`, or HTML with `auth=` unless the user explicitly asks for the secret value.
```

When reporting embedded-site results:

- Prefer describing the target (`chat` or `agent`), mode (`fullscreen` or `widget`), locale, session ID, and whether a token was reused or created.
- Redact secrets by default. If the user needs the value, show only the minimum required field and say that it is sensitive.
- If the CLI returned raw JSON containing `token`, `beta`, `src`, or `html`, summarize it instead of pasting it verbatim into the user-facing response.
- Prefer reporting operational state first: generated embed code, fetched metadata, created or reused session, or received answer.

**Chunk operations:**
```markdown
**Chunks** (15 total)

| ID | Content Preview | Keywords |
|----|-----------------|----------|
| abc... | First 50 chars... | term1, term2 |
```

**Session operations:**
```markdown
**Sessions** (3 total)

| ID | Name | Messages | Created |
|----|------|----------|---------|
| ses_abc... | Q&A Session | 12 | 2024-01-15 |
```

**Single resource details:**
```markdown
**Document Details**

**ID:** `doc_abc123...`
**Name:** report.pdf
**Status:** DONE
**Chunks:** 45
**Created:** 2024-01-15
```


**Tags list:**
```markdown
**Document Tags** (4 total)

- internal-only
- q2-report
- approved
- draft
```

**Connectors list:**
```markdown
**Connectors** (2 total)

| Provider | Name | Status | Type |
|----------|------|--------|------|
| GitHub   | Main Repo | OK | source |
| Notion   | Wiki | FAIL | source |
```

**RAPTOR status:**
```markdown
**RAPTOR Processing**

| Document | Level | Chunks | Status |
|----------|-------|--------|--------|
| manual.pdf | 1 | 45 | DONE |
| manual.pdf | 2 | 12 | RUNNING |
| manual.pdf | 3 | 0 | UNSTART |
```

## Error Response Format

**API errors:**
```markdown
**Error**

**Code:** `123`
**Message:** Dataset not found
```

**Connection errors:**
```markdown
**Connection Failed**

Cannot connect to RAGFlow server at `http://xxx/xx`
Check the RAGFLOW_URL environment variable and server availability
```

**Validation errors:**
```markdown
**Validation Error**

Missing required parameter: `--dataset`
Run with `--help` for usage information
```

**Tags list:**
```markdown
**Document Tags** (4 total)

- internal-only
- q2-report
- approved
- draft
```

**Connectors list:**
```markdown
**Connectors** (2 total)

| Provider | Name | Status | Type |
|----------|------|--------|------|
| GitHub   | Main Repo | OK | source |
| Notion   | Wiki | FAIL | source |
```

**RAPTOR status:**
```markdown
**RAPTOR Processing**

| Document | Level | Chunks | Status |
|----------|-------|--------|--------|
| manual.pdf | 1 | 45 | DONE |
| manual.pdf | 2 | 12 | RUNNING |
| manual.pdf | 3 | 0 | UNSTART |
```
