# Step Types and `data` Parameters

All parameters are optional with defaults. When Config `data` and Job request parameters overlap, **the request value takes precedence**.

## `document-parse` — Document Parsing

Converts documents into structured text (HTML/Markdown/Text).

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `model` | string | `"default"` | Parsing model name (e.g., `"document-parse-260128"`) |
| `mode` | string | `"standard"` | `"standard"` or `"enhanced"` |
| `ocr` | string | `"force"` | `"force"` (always OCR) or `"auto"` (only when needed) |
| `lang` | string | null | OCR language code (e.g., `"ko"`, `"en"`) |
| `coordinates` | bool | `true` | Include text element coordinates |
| `output_formats` | string[] | `["html", "text"]` | `"html"`, `"text"`, `"markdown"`, `"pdf"` |
| `chart_recognition` | bool | `true` | Enable chart recognition |
| `merge_multipage_tables` | bool | `false` | Merge tables spanning multiple pages |
| `base64_encoding` | string[] | `["figure"]` | Element types to base64 encode: `table`, `figure`, `chart`, `heading1`, `header`, `footer`, `caption`, `paragraph`, `equation`, `list`, `index`, `footnote` |

```json
{
  "mode": "enhanced",
  "ocr": "auto",
  "coordinates": true,
  "output_formats": ["html", "markdown"],
  "chart_recognition": true,
  "merge_multipage_tables": true
}
```

## `document-classify` — Document Classification

Classifies documents into categories. Results can drive conditional branching via `next_steps`.

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `model` | string | `"default"` | Classification model |
| `confidence` | bool | `true` | Include confidence scores |
| `split` | bool | `false` | Split document by classification result. Each split group is processed independently by subsequent steps |
| `split_criteria` | object[] \| null | null | Split criteria |
| `text.format` | object | — | Classification categories schema. Follows the [OpenAI Structured Outputs format](https://platform.openai.com/docs/guides/structured-outputs) |

**Document Split:**

When `split: true`, the classify step groups pages by their classification result and splits the document accordingly. Each split group is then passed independently to the next steps. This allows attaching **multiple next steps** to a single classify step — each split group follows the branching rules in `next_steps` independently.

For example, a 10-page document classified as pages 1-5 = "Invoice" and pages 6-10 = "Receipt" will produce two separate groups, each routed to the matching next step via conditional branching.

```json
{
  "confidence": true,
  "split": true,
  "text": {
    "format": {
      "type": "json_schema",
      "name": "document_classify",
      "schema": {
        "type": "string",
        "oneOf": [
          {"const": "Invoice", "description": "Commercial invoice with itemized charges and billing information"},
          {"const": "Receipt", "description": "Proof of payment or transaction receipt"},
          {"const": "Contract", "description": "Legal agreement between two or more parties"}
        ]
      }
    }
  }
}
```

**Classification Schema Rules:**

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `schema.type` | string | Yes | Must be `"string"` |
| `schema.oneOf` | array | Yes | Non-empty list of category definitions |
| `schema.oneOf[].const` | string | Yes | Category label. Keep short and consistent |
| `schema.oneOf[].description` | string | Yes | 1-2 sentences clarifying the category. Include decision rules for borderline cases |

Tips:
- Use concrete, non-overlapping label names
- Add brief include/exclude examples in descriptions for ambiguous categories
- Duplicate `const` values are ignored

## `information-extract` — Information Extraction

Extracts structured information from documents based on a JSON Schema.

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `model` | string | `"default"` | Extraction model |
| `mode` | string | `"standard"` | `"standard"`, `"auto"`, `"enhanced"` (vision mode) |
| `confidence` | bool | `true` | Include confidence scores (`high`/`medium`/`low`) |
| `location` | bool | `true` | Include source location (highlight) info |
| `location_granularity` | string | `"all"` | `"all"`, `"element"`, `"word"` |
| `text.format` | object | — | Extraction schema (JSON Schema). Follows the [OpenAI Structured Outputs format](https://platform.openai.com/docs/guides/structured-outputs) |

**Defining a schema:**

Including the schema in step.data means you don't need to send it with every Job request.

```json
{
  "confidence": true,
  "location": true,
  "mode": "enhanced",
  "text": {
    "format": {
      "type": "json_schema",
      "name": "invoice_schema",
      "schema": {
        "type": "object",
        "properties": {
          "vendor_name": { "type": "string" },
          "invoice_date": { "type": "string" },
          "total_amount": { "type": "number" },
          "items": {
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "description": { "type": "string" },
                "quantity": { "type": "integer" },
                "unit_price": { "type": "number" }
              }
            }
          }
        },
        "required": ["vendor_name", "total_amount"]
      }
    }
  }
}
```

- `mode: "enhanced"`: Vision mode that analyzes document images directly. Useful for tables/charts. **50-page limit**.

**Extraction Schema Rules:**

| Level | Allowed Types | Notes |
|-------|--------------|-------|
| First-level properties | `string`, `number`, `integer`, `boolean`, `array` | `object` is **not allowed**. Wrap in `array` of `object` instead |
| Array items | `string`, `number`, `integer`, `boolean`, `object` | `array` is not allowed (no nested arrays) |
| Object properties (inside array) | `string`, `number`, `integer`, `boolean`, `array` | `object` is not allowed (no further nesting) |
| Nested array items (inside object) | `string`, `number`, `integer`, `boolean` | `array` and `object` are not allowed |

Additional rules:
- Property names cannot start with an underscore (`_`)
- Maximum nesting depth is 3 levels: root → array → object → primitive/array

**Correct** — use `array` of `object` for grouped fields:

```json
{
  "type": "object",
  "properties": {
    "vendor_name": { "type": "string" },
    "line_items": {
      "type": "array",
      "items": {
        "type": "object",
        "properties": {
          "description": { "type": "string" },
          "amount": { "type": "number" }
        }
      }
    }
  }
}
```

**Incorrect** — `object` at first level will be rejected:

```json
{
  "type": "object",
  "properties": {
    "vendor": {
      "type": "object",
      "properties": {
        "name": { "type": "string" },
        "address": { "type": "string" }
      }
    }
  }
}
```

To extract grouped fields like vendor info, either flatten them (`vendor_name`, `vendor_address`) or wrap in an array (`vendors: array of object`).

## `instruct` — Free-form Instructions

Send free-form instructions to an LLM for answers or insights. Automatically uses previous Step results as context.

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `model` | string | `"default"` | Generation model |
| `input` | array | — | User question/instruction. If omitted, extracts text from the Job request's input |
| `text.format` | object | — | Response format. Follows the [OpenAI Structured Outputs format](https://platform.openai.com/docs/guides/structured-outputs) |

**Automatic step chaining:**
- `document-parse` → `instruct`: Parsed document text passed as context
- `document-classify` → `instruct`: Classification result passed as context
- `information-extract` → `instruct`: Extraction result passed as context
- `instruct` → `instruct`: Previous instruct result passed as context

Just connect via `next_steps` — chaining works automatically, no extra configuration needed.

```json
{
  "input": [
    {"role": "user", "content": [{"type": "input_text", "text": "Analyze the sentiment of this document"}]}
  ],
  "text": {
    "format": {
      "type": "json_schema",
      "name": "sentiment",
      "schema": {
        "type": "object",
        "properties": {
          "sentiment": {"type": "string", "enum": ["positive", "negative", "neutral"]},
          "reason": {"type": "string"}
        }
      }
    }
  }
}
```
