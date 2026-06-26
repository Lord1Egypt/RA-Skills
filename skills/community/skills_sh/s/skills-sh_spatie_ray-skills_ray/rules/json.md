---
name: json
description: How to send JSON to Ray
metadata:
  tags: json, payload
---

## JSON String Payload

The JSON string payload displays structured JSON data with syntax highlighting and collapsible sections.

### When to Use

Use the JSON string payload when you want to:

- Display complex nested data structures
- Show API responses
- Present configuration objects
- Debug JSON data

### Payload Structure

```json
{
  "type": "json_string",
  "content": {
    "value": "{\"serialized\": \"json\"}"
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

- `value`: A JSON string (the JSON must be serialized/escaped as a string value)

### Examples

#### Simple object

```bash
curl -X POST http://localhost:23517/ \
  -H "Content-Type: application/json" \
  -d '{"uuid":"'$(uuidgen)'","payloads":[{"type":"json_string","content":{"value":"{\"name\":\"Claude\",\"active\":true}"},"origin":{"function_name":"code-agent","file":"code-agent","line_number":1,"hostname":"my-computer"}}],"meta":{}}'
```

#### Nested structure

```bash
curl -X POST http://localhost:23517/ \
  -H "Content-Type: application/json" \
  -d '{"uuid":"'$(uuidgen)'","payloads":[{"type":"json_string","content":{"value":"{\"user\":{\"id\":1,\"name\":\"John\"},\"permissions\":[\"read\",\"write\"]}"},"origin":{"function_name":"code-agent","file":"code-agent","line_number":1,"hostname":"my-computer"}}],"meta":{}}'
```

#### API response

```bash
curl -X POST http://localhost:23517/ \
  -H "Content-Type: application/json" \
  -d '{"uuid":"'$(uuidgen)'","payloads":[{"type":"json_string","content":{"value":"{\"status\":200,\"data\":{\"items\":[{\"id\":1,\"name\":\"Item 1\"},{\"id\":2,\"name\":\"Item 2\"}],\"total\":2}}"},"origin":{"function_name":"code-agent","file":"code-agent","line_number":1,"hostname":"my-computer"}}],"meta":{}}'
```

### Building JSON Strings

When constructing the payload, the inner JSON must be properly escaped:

```bash
# The value field contains a JSON string, so quotes must be escaped
# Original: {"key": "value"}
# Escaped:  {\"key\": \"value\"}
```
