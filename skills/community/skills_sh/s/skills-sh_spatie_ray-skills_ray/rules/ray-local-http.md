---
name: ray-local-http
description: How does the Ray local HTTP server work
metadata:
  tags: http, log, payload
---

## Ray Local HTTP Server

Ray runs a local HTTP server that accepts payloads for display in the Ray desktop application.

**Documentation**: https://myray.app/docs/developing-ray-libraries/payload

### Endpoint

```
POST http://localhost:23517/
```

IMPORTANT: If the endpoint is not working, the user might have changed their default port in the settings of Ray. In that case, ask them to provide the correct port.

### Headers

```
Content-Type: application/json
Accept: application/json
```

### Request Structure

```json
{
  "uuid": "<unique-id>",
  "payloads": [
    {
      "type": "<payload-type>",
      "content": { /* payload-specific content */ },
      "origin": {
        "function_name": "<function-name>",
        "file": "<file-path>",
        "line_number": <number>,
        "hostname": "<hostname>"
      }
    }
  ],
  "meta": {}
}
```

### Fields

All sections are **mandatory** when creating payloads.

#### uuid

A valid UUIDv4 value. This identifier is important for future modifications to the payload, such as changing its color after transmission. Use `$(uuidgen)` in bash to generate one.

#### payloads

An array containing the actual data being sent. Each payload has:

- `type`: The payload type (e.g., `log`, `custom`, `table`, `json_string`)
- `content`: Payload-specific content object for display in Ray
- `origin`: Source information object

#### origin

Captures where the ray() call originated. Ray uses this information to enable file linking functionality within the desktop app.

- `function_name`: The calling function (ALWAYS use `"code-agent"` for agent calls)
- `file`: The source file path or identifier (ALWAYS USE `"code-agent"` for agent calls)
- `line_number`: Line number in the source (ALWAYS use `1` as default)
- `hostname`: The hostname (ALWAYS call the `hostname` command to get the name of the machine)

#### meta

Metadata about the integration library. Can contain language version and Ray package version details. For Claude agent use, can be empty `{}`.

### Supported Payload Types

- `log` - General value logging (see [log.md](log.md))
- `table` - Key-value table display (see [table.md](table.md))
- `json_string` - JSON structure display (see [json.md](json.md))
- `custom` with label `"Text"` - Plain text with preserved whitespace (see [text.md](text.md))
- `custom` with label `"HTML"` - Raw HTML content (see [html.md](html.md))
- `custom` with label `"XML"` - Formatted XML content (see [xml.md](xml.md))
- `carbon` - Date/time display (see [carbon.md](carbon.md))
- `custom` with custom label - Arbitrary content (see [custom.md](custom.md))
- `custom` with empty label - Decoded JSON (see [decoded-json.md](decoded-json.md))
- `custom` with filename label - File contents (see [file-contents.md](file-contents.md))

### Supported Action Types

Actions control Ray's behavior rather than displaying data. They all use empty content arrays `[]`.

- `confetti` - Trigger confetti animation (see [action-confetti.md](action-confetti.md))
- `hide_app` - Hide Ray window (see [action-hide-app.md](action-hide-app.md))
- `show_app` - Show Ray window (see [action-show-app.md](action-show-app.md))
- `clear_all` - Clear all logs (see [action-clear-all.md](action-clear-all.md))

### Basic curl Template

```bash
curl -X POST http://localhost:23517/ \
  -H "Content-Type: application/json" \
  -d '{"uuid":"'$(uuidgen)'","payloads":[{"type":"TYPE","content":{...},"origin":{"function_name":"code-agent","file":"code-agent","line_number":1,"hostname":"my-computer"}}],"meta":{}}'
```
