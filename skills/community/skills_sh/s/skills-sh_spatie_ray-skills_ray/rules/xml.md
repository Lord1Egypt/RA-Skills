---
name: xml
description: How to send XML to Ray
metadata:
  tags: xml, payload
---

## XML Payload

The XML payload displays formatted XML content with proper indentation and encoding.

### When to Use

Use the XML payload when you want to:

- Display XML documents
- Show API responses in XML format
- Debug XML configuration files

### Payload Structure

```json
{
  "type": "custom",
  "content": {
    "content": "&lt;root&gt;<br>&nbsp;&nbsp;&lt;child&gt;value&lt;/child&gt;<br>&lt;/root&gt;",
    "label": "XML"
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

- `content`: The XML content, formatted and encoded
- `label`: Always `"XML"`

### Formatting Rules

Before sending, the XML must be formatted:

1. Pretty-print/indent the XML structure
2. HTML-encode all entities (`<` becomes `&lt;`, `>` becomes `&gt;`, etc.)
3. Replace newlines with `<br>`
4. Replace spaces with `&nbsp;`

### Examples

#### Simple XML

```bash
curl -X POST http://localhost:23517/ \
  -H "Content-Type: application/json" \
  -d '{"uuid":"'$(uuidgen)'","payloads":[{"type":"custom","content":{"content":"&lt;root&gt;&lt;item&gt;value&lt;/item&gt;&lt;/root&gt;","label":"XML"},"origin":{"function_name":"code-agent","file":"code-agent","line_number":1,"hostname":"'$(hostname)'"}}],"meta":{}}'
```

#### Nested XML with indentation

```bash
curl -X POST http://localhost:23517/ \
  -H "Content-Type: application/json" \
  -d '{"uuid":"'$(uuidgen)'","payloads":[{"type":"custom","content":{"content":"&lt;one&gt;<br>&nbsp;&nbsp;&lt;two&gt;<br>&nbsp;&nbsp;&nbsp;&nbsp;&lt;three&gt;3&lt;/three&gt;<br>&nbsp;&nbsp;&lt;/two&gt;<br>&lt;/one&gt;","label":"XML"},"origin":{"function_name":"code-agent","file":"code-agent","line_number":1,"hostname":"'$(hostname)'"}}],"meta":{}}'
```

#### XML with attributes

```bash
curl -X POST http://localhost:23517/ \
  -H "Content-Type: application/json" \
  -d '{"uuid":"'$(uuidgen)'","payloads":[{"type":"custom","content":{"content":"&lt;users&gt;<br>&nbsp;&nbsp;&lt;user&nbsp;id=&quot;1&quot;&nbsp;active=&quot;true&quot;&gt;<br>&nbsp;&nbsp;&nbsp;&nbsp;&lt;name&gt;John&lt;/name&gt;<br>&nbsp;&nbsp;&lt;/user&gt;<br>&lt;/users&gt;","label":"XML"},"origin":{"function_name":"code-agent","file":"code-agent","line_number":1,"hostname":"'$(hostname)'"}}],"meta":{}}'
```
