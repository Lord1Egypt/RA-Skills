# End-to-End Examples

## Basic: Parse → Extract

```bash
# 1. Upload file
curl -X POST https://api.upstage.ai/v2/files \
  -H "Authorization: Bearer $UPSTAGE_API_KEY" \
  -F "file=@invoice.pdf" \
  -F "purpose=user_data"
# → {"id": "file_xxx", ...}

# 2. Create Agent
curl -X POST https://api.upstage.ai/v2/agents \
  -H "Authorization: Bearer $UPSTAGE_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"name": "invoice-processor", "visibility": "private"}'
# → {"id": "agt_xxx", ...}

# 3. Create Config
curl -X POST https://api.upstage.ai/v2/agents/agt_xxx/configs \
  -H "Authorization: Bearer $UPSTAGE_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "parse-extract",
    "steps": [
      {"name": "parse", "type": "document-parse", "data": {"ocr": "auto"}, "is_first": true, "next_steps": [{"step_name": "extract"}]},
      {"name": "extract", "type": "information-extract", "data": {"confidence": true}, "next_steps": []}
    ]
  }'

# 4. Run Job
curl -X POST https://api.upstage.ai/v2/responses \
  -H "Authorization: Bearer $UPSTAGE_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "model": "agt_xxx",
    "input": [{"role": "user", "content": [
      {"type": "input_file", "file_id": "file_xxx"}
    ]}],
    "text": {
      "format": {
        "type": "json_schema",
        "name": "invoice",
        "schema": {"type": "object", "properties": {"vendor": {"type": "string"}, "amount": {"type": "number"}}}
      }
    }
  }'
# → {"id": "job_xxx", "status": "in_progress", ...}

# 5. Poll for results
curl https://api.upstage.ai/v2/responses/job_xxx \
  -H "Authorization: Bearer $UPSTAGE_API_KEY"

# 6. List results
curl "https://api.upstage.ai/v2/agents/agt_xxx/jobs?include[]=output:extract" \
  -H "Authorization: Bearer $UPSTAGE_API_KEY"
```

## Conditional Branching: Parse → Classify → Branch → Extract

```bash
curl -X POST https://api.upstage.ai/v2/agents/agt_xxx/configs \
  -H "Authorization: Bearer $UPSTAGE_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "classify-branch",
    "steps": [
      {"name": "parse", "type": "document-parse", "data": {}, "is_first": true, "next_steps": [{"step_name": "classify"}]},
      {"name": "classify", "type": "document-classify", "data": {}, "next_steps": [
        {"step_name": "extract-invoice", "condition": {"field": "document_type", "operator": "==", "value": "Invoice"}},
        {"step_name": "extract-default"}
      ]},
      {"name": "extract-invoice", "type": "information-extract", "data": {"mode": "enhanced", "confidence": true}, "next_steps": []},
      {"name": "extract-default", "type": "information-extract", "data": {}, "next_steps": []}
    ]
  }'
```

## Split + Conditional Branching: Parse → Classify (split) → Branch → Extract

```bash
curl -X POST https://api.upstage.ai/v2/agents/agt_xxx/configs \
  -H "Authorization: Bearer $UPSTAGE_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "split-classify-extract",
    "steps": [
      {"name": "parse", "type": "document-parse", "data": {}, "is_first": true, "next_steps": [{"step_name": "classify"}]},
      {"name": "classify", "type": "document-classify", "data": {
        "split": true,
        "text": {"format": {"type": "json_schema", "name": "doc_type", "schema": {"type": "string", "oneOf": [
          {"const": "Invoice"}, {"const": "Receipt"}, {"const": "Other"}
        ]}}}
      }, "next_steps": [
        {"step_name": "extract-invoice", "condition": {"field": "document_type", "operator": "==", "value": "Invoice"}},
        {"step_name": "extract-receipt", "condition": {"field": "document_type", "operator": "==", "value": "Receipt"}},
        {"step_name": "extract-default"}
      ]},
      {"name": "extract-invoice", "type": "information-extract", "data": {"mode": "enhanced"}, "next_steps": []},
      {"name": "extract-receipt", "type": "information-extract", "data": {}, "next_steps": []},
      {"name": "extract-default", "type": "information-extract", "data": {}, "next_steps": []}
    ]
  }'
```

Each page group split by classification is independently routed to its matching extract step.

## Chained Workflow: Parse → Extract → Instruct

```bash
curl -X POST https://api.upstage.ai/v2/agents/agt_xxx/configs \
  -H "Authorization: Bearer $UPSTAGE_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "extract-then-analyze",
    "steps": [
      {"name": "parse", "type": "document-parse", "data": {}, "is_first": true, "next_steps": [{"step_name": "extract"}]},
      {"name": "extract", "type": "information-extract", "data": {"confidence": true}, "next_steps": [{"step_name": "analyze"}]},
      {"name": "analyze", "type": "instruct", "data": {
        "input": [{"role": "user", "content": [{"type": "input_text", "text": "Summarize the key findings from the extraction results"}]}]
      }, "next_steps": []}
    ]
  }'
```

## Clone an Agent

```bash
# Full clone with Jobs
curl -X POST https://api.upstage.ai/v2/agents \
  -H "Authorization: Bearer $UPSTAGE_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"name": "cloned", "clone": {"agent_id": "agt_src", "with_jobs": true}}'

# Clone specific Config + source only
curl -X POST https://api.upstage.ai/v2/agents \
  -H "Authorization: Bearer $UPSTAGE_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"name": "filtered-clone", "clone": {"agent_id": "agt_src", "with_jobs": true, "config_id": "cfg_xxx", "source": "studio"}}'
```

## Publish Agent To Library

```bash
# 1. Patch library metadata
curl -X PATCH https://api.upstage.ai/v2/agents/agt_xxx \
  -H "Authorization: Bearer $UPSTAGE_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "description": "Extracts invoice key fields",
    "category": "finance",
    "language": "en",
    "supported_doc_types": ["invoice", "receipt"]
  }'

# 2. Publish a specific config
curl -X PUT https://api.upstage.ai/v2/agents/agt_xxx/visibility \
  -H "Authorization: Bearer $UPSTAGE_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "visibility": "public",
    "published_config_id": "cfg_xxx"
  }'

# 3. Upload a thumbnail
curl -X POST https://api.upstage.ai/v2/agents/agt_xxx/thumbnail \
  -H "Authorization: Bearer $UPSTAGE_API_KEY" \
  -F "file=@thumbnail.png"

# 4. Browse public library agents
curl "https://api.upstage.ai/v2/agents/library?category=finance&language=en&order=desc" \
  -H "Authorization: Bearer $UPSTAGE_API_KEY"
```

## Like / Unlike Agent

```bash
# Like
curl -X POST https://api.upstage.ai/v2/agents/agt_xxx/likes \
  -H "Authorization: Bearer $UPSTAGE_API_KEY"

# Unlike
curl -X DELETE https://api.upstage.ai/v2/agents/agt_xxx/likes \
  -H "Authorization: Bearer $UPSTAGE_API_KEY"
```
