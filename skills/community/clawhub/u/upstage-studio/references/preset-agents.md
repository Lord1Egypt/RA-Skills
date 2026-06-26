# Preset Agents

Preset agents are built-in, globally available agents with predefined workflows. Unlike custom agents (`agt_xxx`), they are referenced by simple name strings and require no agent/config setup.

> **Cross-skill note**: For standalone schema generation outside of an Agent workflow, see the dedicated `upstage-schema-generation` skill. For standalone document classification, see `upstage-document-classification`. The preset agents below let you pipeline these as steps within a larger Agent workflow.

## Available Preset Agents

| Model Name | Pipeline | Description |
|------------|----------|-------------|
| `schema-generate` | DP → Schema Generate | Auto-generate extraction JSON schema from document |
| `class-generate` | DP → Class Generate | Auto-generate classification categories from document |
| `schema-update` | DP → Schema Update | Refine extraction schema based on extraction results |

## Usage

Use preset agents by passing the model name directly to `POST /v2/responses`. No agent/config creation needed.

Preset agent Configs are immutable. To customize the output, pass `text` at request level — this is the only way to provide schemas or instructions to preset agents.

```json
{
  "model": "schema-generate",
  "input": [
    {
      "role": "user",
      "content": [
        { "type": "input_file", "file_id": "file_xxx" }
      ]
    }
  ],
  "text": {
    "format": {
      "type": "json_schema",
      "name": "invoice",
      "schema": {"type": "object", "properties": {"vendor": {"type": "string"}, "amount": {"type": "number"}}}
    }
  },
  "background": true,
  "include": ["all"]
}
```

## Response

When `include: ["all"]`, output contains one message per step:

```json
{
  "id": "job_xxx",
  "object": "response",
  "status": "completed",
  "model": "schema-generate",
  "output": [
    {
      "type": "message",
      "role": "assistant",
      "model": "Document Parse",
      "content": [{ "type": "output_text", "text": "..." }]
    },
    {
      "type": "message",
      "role": "assistant",
      "model": "Schema Generate",
      "content": [{ "type": "output_text", "text": "..." }]
    }
  ]
}
```

---

## schema-generate

Auto-generates an information-extraction JSON schema by analyzing the document content.

**Pipeline:** Document Parse → Schema Generate

**Step `data` parameters:**

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `model` | string | `"default"` | Generation model name |
| `input` | array | — | Guidance for schema generation. Same format as `instruct` step |

**Example with guidance:**

```json
{
  "model": "schema-generate",
  "input": [
    {
      "role": "user",
      "content": [
        { "type": "input_file", "file_id": "file_xxx" },
        { "type": "input_text", "text": "Extract contract parties, duration, and amount" }
      ]
    }
  ]
}
```

Without `input_text`, the agent analyzes the document and generates a schema based on its content.

---

## class-generate

Auto-generates document classification categories by analyzing the document content.

**Pipeline:** Document Parse → Class Generate

**Step `data` parameters:**

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `model` | string | `"default"` | Generation model name |

**Example:**

```json
{
  "model": "class-generate",
  "input": [
    {
      "role": "user",
      "content": [
        { "type": "input_file", "file_id": "file_xxx" }
      ]
    }
  ]
}
```

---

## schema-update

Refines an existing extraction schema based on extraction results and user corrections. Typically used after `information-extract` to iteratively improve the schema.

**Pipeline:** Document Parse → Schema Update

**Step `data` parameters:**

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `model` | string | `"default"` | Updater model name |
| `use_aso_updater` | bool | `false` | Use ASO (Auto Schema Optimizer) updater |

**Aggregation pattern:** Unlike other steps that run per-document, schema-update aggregates multiple document results into a single execution.

**Example:**

```json
{
  "model": "schema-update",
  "input": [
    {
      "role": "user",
      "content": [
        { "type": "input_file", "file_id": "file_xxx" }
      ]
    }
  ]
}
```

---

## Differences from Custom Agents

| Aspect | Custom Agents | Preset Agents |
|--------|---------------|---------------|
| Model ID | `agt_xxx` (user-created) | Simple name (e.g., `"schema-generate"`) |
| Setup required | Create Agent → Config → Steps | None — use directly |
| Visibility | `private`, `readonly`, `public` | `public` (global) |
| Config | User-defined, mutable | Predefined, immutable |
| Step customization | Full control over step `data` | Default parameters only (override via request `text` field) |
