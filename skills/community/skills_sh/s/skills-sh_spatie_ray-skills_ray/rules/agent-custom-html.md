---
name: agent-custom-html
description: How to send custom HTML to Ray for agent output
metadata:
  tags: agent, html, payload, custom
---

## Agent Custom HTML Payload

The agent custom HTML payload displays fully formatted HTML content in Ray. It provides richer rendering than the standard HTML payload, with full CSS support.

### When to Use

Use the agent custom HTML payload when you want to:

- Display LLM/agent output as a fully formatted HTML page
- Show rich content with CSS styling
- Create iterative updates to a log entry (carousel feature)
- Render complex layouts that benefit from full HTML/CSS support

As an agent ALWAYS prefer `agent-custom-html` type above [rules/html.md](rules/html.md).

### Payload Structure

```json
{
  "type": "ai_custom_html",
  "content": {
    "html": "<h1>Hello World</h1><p>Your HTML content here</p>",
    "label": "Agent Response",
    "iterationOf": "123e4567-e89b-12d3-a456-426614174000"
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

| Field         | Type   | Required | Description                                                                                                                                                                    |
| ------------- | ------ | -------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| `html`        | string | Yes      | Valid HTML content. JavaScript is not allowed, but all CSS is supported. ALWAYS make sure to wrap the HTML content in `<html>` and `<body>` tags. And styles in `<head>` tags. |
| `label`       | string | No       | Label for the log entry (e.g., "Claude Response").                                                                                                                             |
| `iterationOf` | string | No       | UUID of an existing log entry to append this HTML as a new iteration (creates a carousel).                                                                                     |

### Iteration Carousel

You can create iterative updates to a log entry by using the `iterationOf` field. This creates a carousel in Ray that allows users to navigate between different iterations.

**Important:** When using iterations, you must:

1. Generate and **remember the UUID** from the first request
2. Use that same UUID in the `iterationOf` field of subsequent requests

### HTTP API Examples

#### Basic HTML

```bash
curl -X POST http://localhost:23517/ \
  -H "Content-Type: application/json" \
  -d '{"uuid":"'$(uuidgen)'","payloads":[{"type":"ai_custom_html","content":{"html":"<html><body><h1>Hello World</h1><p>This is <strong>styled</strong> content.</p></body></html>","label":"Agent Response"},"origin":{"function_name":"code-agent","file":"code-agent","line_number":1,"hostname":"'$(hostname)'"}}],"meta":{}}'
```

#### Styled HTML with CSS

```bash
curl -X POST http://localhost:23517/ \
  -H "Content-Type: application/json" \
  -d '{"uuid":"'$(uuidgen)'","payloads":[{"type":"ai_custom_html","content":{"html":"<html><head><style>.card { padding: 20px; border-radius: 8px; background: #f5f5f5; } .title { color: #333; font-size: 24px; } .content { color: #666; }</style></head><body><div class=\"card\"><h1 class=\"title\">Status Report</h1><p class=\"content\">All systems operational.</p></div></body><html>","label":"Claude Response"},"origin":{"function_name":"code-agent","file":"code-agent","line_number":1,"hostname":"'$(hostname)'"}}],"meta":{}}'
```

#### Table Layout

```bash
curl -X POST http://localhost:23517/ \
  -H "Content-Type: application/json" \
  -d '{"uuid":"'$(uuidgen)'","payloads":[{"type":"ai_custom_html","content":{"html":"<html><head><style>table { width: 100%; border-collapse: collapse; } th, td { padding: 8px; border: 1px solid #ddd; text-align: left; } th { background: #f0f0f0; }</style><head><body><table><tr><th>Name</th><th>Status</th></tr><tr><td>Task 1</td><td style=\"color: green;\">Complete</td></tr><tr><td>Task 2</td><td style=\"color: orange;\">In Progress</td></tr></table></body></html>","label":"Task Status"},"origin":{"function_name":"code-agent","file":"code-agent","line_number":1,"hostname":"'$(hostname)'"}}],"meta":{}}'
```

#### Iterative Updates (Carousel)

To create a carousel of iterations, first send the initial HTML and **store the UUID**:

```bash
# Step 1: Generate and store the UUID for the first iteration
FIRST_UUID=$(uuidgen)
echo "Remember this UUID for iterations: $FIRST_UUID"

curl -X POST http://localhost:23517/ \
  -H "Content-Type: application/json" \
  -d '{"uuid":"'$FIRST_UUID'","payloads":[{"type":"ai_custom_html","content":{"html":"<h1>Step 1</h1><p>Processing started...</p>","label":"Progress"},"origin":{"function_name":"code-agent","file":"code-agent","line_number":1,"hostname":"'$(hostname)'"}}],"meta":{}}'
```

Then add subsequent iterations by referencing the original UUID in `iterationOf`:

```bash
# Step 2: Add iteration using the SAME UUID from step 1
curl -X POST http://localhost:23517/ \
  -H "Content-Type: application/json" \
  -d '{"uuid":"'$(uuidgen)'","payloads":[{"type":"ai_custom_html","content":{"html":"<h1>Step 2</h1><p>Processing complete!</p>","label":"Progress","iterationOf":"'$FIRST_UUID'"},"origin":{"function_name":"code-agent","file":"code-agent","line_number":1,"hostname":"'$(hostname)'"}}],"meta":{}}'
```

**Note:** The `uuid` field in the request body is for the new log entry. The `iterationOf` field must contain the UUID from the **first** iteration to link them together in a carousel.

### MCP Tool

When using the Ray MCP server, you can also use the `send_custom_html_output` tool which provides additional features like iteration carousel.

**Tool name:** `send_custom_html_output`

| Parameter       | Type   | Required | Description                                             |
| --------------- | ------ | -------- | ------------------------------------------------------- |
| `html`          | string | Yes      | Valid HTML content.                                     |
| `projectName`   | string | Yes      | The Ray project name.                                   |
| `llmName`       | string | No       | Name of the LLM for labeling.                           |
| `hostname`      | string | No       | The hostname.                                           |
| `appendToLogId` | string | No       | Append as iteration to existing log (creates carousel). |

### Features

- **Full CSS Support**: Use inline styles or `<style>` tags for custom styling
- **Secure Sandbox**: HTML is rendered in a secure sandbox (no JavaScript)
- **Iteration Carousel**: Update logs in place using `iterationOf` (HTTP API) or `appendToLogId` (MCP)
