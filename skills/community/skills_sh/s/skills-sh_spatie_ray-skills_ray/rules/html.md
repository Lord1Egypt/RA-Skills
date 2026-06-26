---
name: html
description: How to send HTML to Ray
metadata:
  tags: html, payload
---

## HTML Payload

The HTML payload displays raw HTML content in Ray without escaping.

### When to Use

Use the HTML payload when you want to:

- Display formatted HTML content
- Show styled text with HTML tags
- Render custom HTML structures

### Payload Structure

```json
{
  "type": "custom",
  "content": {
    "content": "<h1>Hello</h1><p>This is <strong>HTML</strong></p>",
    "label": "HTML"
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

- `content`: Raw HTML content (no escaping applied)
- `label`: Always `"HTML"`

### Examples

#### Simple HTML

```bash
curl -X POST http://localhost:23517/ \
  -H "Content-Type: application/json" \
  -d '{"uuid":"'$(uuidgen)'","payloads":[{"type":"custom","content":{"content":"<h1>Hello World</h1>","label":"HTML"},"origin":{"function_name":"code-agent","file":"code-agent","line_number":1,"hostname":"'$(hostname)'"}}],"meta":{}}'
```

#### Formatted content

```bash
curl -X POST http://localhost:23517/ \
  -H "Content-Type: application/json" \
  -d '{"uuid":"'$(uuidgen)'","payloads":[{"type":"custom","content":{"content":"<p>Status: <strong style=\"color: green;\">Success</strong></p><ul><li>Item 1</li><li>Item 2</li></ul>","label":"HTML"},"origin":{"function_name":"code-agent","file":"code-agent","line_number":1,"hostname":"'$(hostname)'"}}],"meta":{}}'
```

#### Code block

```bash
curl -X POST http://localhost:23517/ \
  -H "Content-Type: application/json" \
  -d '{"uuid":"'$(uuidgen)'","payloads":[{"type":"custom","content":{"content":"<pre><code>function hello() {\n  console.log(\"Hello\");\n}</code></pre>","label":"HTML"},"origin":{"function_name":"code-agent","file":"code-agent","line_number":1,"hostname":"'$(hostname)'"}}],"meta":{}}'
```
