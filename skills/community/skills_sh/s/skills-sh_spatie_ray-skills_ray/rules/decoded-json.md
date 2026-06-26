---
name: decoded-json
description: How to send decoded JSON to Ray
metadata:
  tags: json, decoded, payload
---

## Decoded JSON Payload

The decoded JSON payload displays parsed JSON as a structured view. Unlike the JSON string payload, the content is the actual decoded JSON object/array, not a string.

### When to Use

Use the decoded JSON payload when you want to:

- Display JSON that's already parsed/decoded
- Show structured data without string escaping
- Present object/array data directly

### Payload Structure

```json
{
  "type": "custom",
  "content": {
    "content": {"key": "value", "nested": {"a": 1}},
    "label": ""
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

- `content`: The decoded JSON value (object, array, or primitive) - NOT a string
- `label`: Always empty string `""`

### Important Note

The key difference from `json_string` payload:
- `json_string`: `"content": {"value": "{\"key\": \"value\"}"}` - value is a JSON string
- `decoded_json`: `"content": {"content": {"key": "value"}, "label": ""}` - content is the actual object

### Examples

#### Simple object

```bash
curl -X POST http://localhost:23517/ \
  -H "Content-Type: application/json" \
  -d '{"uuid":"'$(uuidgen)'","payloads":[{"type":"custom","content":{"content":{"name":"Claude","active":true},"label":""},"origin":{"function_name":"code-agent","file":"code-agent","line_number":1,"hostname":"'$(hostname)'"}}],"meta":{}}'
```

#### Nested structure

```bash
curl -X POST http://localhost:23517/ \
  -H "Content-Type: application/json" \
  -d '{"uuid":"'$(uuidgen)'","payloads":[{"type":"custom","content":{"content":{"user":{"id":1,"name":"John"},"roles":["admin","user"]},"label":""},"origin":{"function_name":"code-agent","file":"code-agent","line_number":1,"hostname":"'$(hostname)'"}}],"meta":{}}'
```

#### Array data

```bash
curl -X POST http://localhost:23517/ \
  -H "Content-Type: application/json" \
  -d '{"uuid":"'$(uuidgen)'","payloads":[{"type":"custom","content":{"content":[{"id":1,"name":"Item 1"},{"id":2,"name":"Item 2"}],"label":""},"origin":{"function_name":"code-agent","file":"code-agent","line_number":1,"hostname":"'$(hostname)'"}}],"meta":{}}'
```
