---
name: table
description: How to send a table to Ray
metadata:
  tags: table, payload
---

## Table Payload

The table payload displays key-value pairs in a structured table format.

### When to Use

Use the table payload when you want to:

- Display structured data with named fields
- Show configuration or settings
- Present results with labels

### Payload Structure

```json
{
  "type": "table",
  "content": {
    "values": {
      "key1": "value1",
      "key2": "value2"
    },
    "label": "Table"
  },
  "origin": {
    "function_name": "code-agent",
    "file": "code-agent",
    "line_number": 1,
    "hostname": "my-computer"
  }
}
```

### Content Fields

- `values`: Object with key-value pairs to display
- `label`: Display label for the table (e.g., `"Table"`, `"Results"`, `"Config"`)

### Examples

#### Simple table

```bash
curl -X POST http://localhost:23517/ \
  -H "Content-Type: application/json" \
  -d '{"uuid":"'$(uuidgen)'","payloads":[{"type":"table","content":{"values":{"name":"Claude","version":"1.0"},"label":"Info"},"origin":{"function_name":"code-agent","file":"code-agent","line_number":1,"hostname":"my-computer"}}],"meta":{}}'
```

#### Results table

```bash
curl -X POST http://localhost:23517/ \
  -H "Content-Type: application/json" \
  -d '{"uuid":"'$(uuidgen)'","payloads":[{"type":"table","content":{"values":{"status":"success","items_processed":42,"errors":0},"label":"Results"},"origin":{"function_name":"code-agent","file":"code-agent","line_number":1,"hostname":"my-computer"}}],"meta":{}}'
```

#### Configuration display

```bash
curl -X POST http://localhost:23517/ \
  -H "Content-Type: application/json" \
  -d '{"uuid":"'$(uuidgen)'","payloads":[{"type":"table","content":{"values":{"environment":"development","debug":true,"port":3000,"host":"localhost"},"label":"Config"},"origin":{"function_name":"code-agent","file":"code-agent","line_number":1,"hostname":"my-computer"}}],"meta":{}}'
```
