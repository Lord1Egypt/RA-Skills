---
name: web-data-convertor
description: "Web Data Convertor: Convert between web formats: JSON↔CSV, JSON↔XML, JSON↔YAML, Markdown↔HTML, query strings, Unix timestamps↔dates with timezone support. Use when an agent needs web data convertor, json to csv conversion, csv to json conversion, tabular data transformation, spreadsheet data export, convert csv to json, csv text, convert date to unix through AgentPMT-hosted remote tool calls. Discovery terms: web data convertor, json to csv conversion, csv to json conversion."
version: 1.0.0
homepage: https://www.agentpmt.com/marketplace/web-data-convertor
compatibility: "Agent instructions for AgentPMT-hosted remote tool calls. Follow this skill body for supported account, wallet, and setup routes. No local command runtime is declared."
metadata: {"author":"agentpmt","openclaw":{"homepage":"https://www.agentpmt.com/marketplace/web-data-convertor"}}
---
# Web Data Convertor

## Freshness
Last updated: `2026-06-23`.

If the current date is more than 7 days after the last updated date, reinstall this skill from skills.sh or ClawHub before relying on endpoints, schemas, setup steps, or examples.

## What This Tool Does
Web Data Converter is a format transformation utility that converts data between common web and application formats used in APIs, configuration files, and content management. It handles bidirectional conversion between JSON and CSV for tabular data interchange, preserving headers and automatically detecting numeric values during CSV parsing. XML to JSON conversion maintains attributes and nested structures, while JSON to XML produces well-formed markup suitable for legacy system integration. Configuration file workflows benefit from YAML to JSON and JSON to YAML transformations, enabling seamless translation between human-readable configs and programmatic data structures. Content creators can convert Markdown to HTML with support for tables, fenced code blocks, and extended syntax, or reverse the process by converting HTML back to clean Markdown for documentation and editing. URL query string parsing extracts parameters into structured JSON objects with automatic handling of multi-value parameters. Time conversion functions translate between Unix timestamps and human-readable date formats with full timezone support across all standard timezones, outputting both ISO 8601 and readable formats. All conversions include validation and clear error messages for malformed input.

## Product Instructions
### Web Data Convertor

Convert between common web data formats including JSON, CSV, XML, YAML, HTML, Markdown, query strings, and Unix timestamps.

#### Actions

##### convert-unix-to-date

Convert a Unix timestamp to a human-readable date string.

**Required fields:**
- `action`: `"convert-unix-to-date"`
- `timestamp` (integer): Unix timestamp in seconds since epoch

**Optional fields:**
- `timezone` (string): IANA timezone name. Default: `"UTC"`. Examples: `"America/New_York"`, `"Europe/London"`, `"Asia/Tokyo"`

**Returns:** ISO format date, readable date string, and timezone used.

**Example:**
```json
{
  "action": "convert-unix-to-date",
  "timestamp": 1700000000,
  "timezone": "America/New_York"
}
```

---

##### convert-date-to-unix

Convert a date string to a Unix timestamp.

**Required fields:**
- `action`: `"convert-date-to-unix"`
- `date_string` (string): Date string to convert

**Optional fields:**
- `format` (string): Python strftime format string for parsing. If omitted, common formats are tried automatically.

**Supported auto-detected formats:** `YYYY-MM-DD HH:MM:SS`, `YYYY-MM-DD`, `YYYY/MM/DD HH:MM:SS`, `YYYY/MM/DD`, `DD-MM-YYYY HH:MM:SS`, `DD-MM-YYYY`, `DD/MM/YYYY HH:MM:SS`, `DD/MM/YYYY`

**Example:**
```json
{
  "action": "convert-date-to-unix",
  "date_string": "2024-11-14 22:13:20"
}
```

**Example with custom format:**
```json
{
  "action": "convert-date-to-unix",
  "date_string": "14-Nov-2024 10:30 PM",
  "format": "%d-%b-%Y %I:%M %p"
}
```

---

##### convert-json-to-csv

Convert a JSON object or array of objects to CSV format.

**Required fields:**
- `action`: `"convert-json-to-csv"`
- `json_text` (string): Valid JSON string (object or array of objects)

**Notes:** A single object is treated as a one-row CSV. All unique keys across objects become CSV column headers, sorted alphabetically.

**Example:**
```json
{
  "action": "convert-json-to-csv",
  "json_text": "[{\"name\":\"Alice\",\"age\":30},{\"name\":\"Bob\",\"age\":25}]"
}
```

---

##### convert-csv-to-json

Convert CSV text to a JSON array of objects.

**Required fields:**
- `action`: `"convert-csv-to-json"`
- `csv_text` (string): CSV string with a header row

**Notes:** The first row is used as field names. Numeric values are automatically converted to numbers.

**Example:**
```json
{
  "action": "convert-csv-to-json",
  "csv_text": "name,age,city\nAlice,30,NYC\nBob,25,LA"
}
```

---

##### convert-xml-to-json

Convert an XML string to JSON.

**Required fields:**
- `action`: `"convert-xml-to-json"`
- `xml_text` (string): Valid XML string

**Notes:** XML attributes are stored under `@attributes`. Text content is stored under `#text`. Repeated child elements with the same tag become arrays.

**Example:**
```json
{
  "action": "convert-xml-to-json",
  "xml_text": "<users><user id=\"1\"><name>Alice</name></user><user id=\"2\"><name>Bob</name></user></users>"
}
```

---

##### convert-json-to-xml

Convert a JSON string to XML format.

**Required fields:**
- `action`: `"convert-json-to-xml"`
- `json_text` (string): Valid JSON string

**Notes:** If the JSON has a single top-level key, that key becomes the root element. Otherwise, a `<root>` element wraps the content. Use `@attributes` and `#text` keys to control XML attributes and text content.

**Example:**
```json
{
  "action": "convert-json-to-xml",
  "json_text": "{\"book\":{\"@attributes\":{\"id\":\"1\"},\"title\":\"Example\",\"author\":\"Jane\"}}"
}
```

---

##### convert-markdown-to-html

Convert Markdown text to HTML.

**Required fields:**
- `action`: `"convert-markdown-to-html"`
- `markdown_text` (string): Markdown content to convert

**Notes:** Supports standard Markdown, code blocks, tables, and fenced code blocks.

**Example:**
```json
{
  "action": "convert-markdown-to-html",
  "markdown_text": "# Hello World\n\nThis is **bold** and this is *italic*.\n\n- Item 1\n- Item 2"
}
```

---

##### convert-html-to-markdown

Convert HTML to Markdown format.

**Required fields:**
- `action`: `"convert-html-to-markdown"`
- `html_text` (string): HTML content to convert

**Notes:** Links are preserved. Line wrapping is disabled for clean output.

**Example:**
```json
{
  "action": "convert-html-to-markdown",
  "html_text": "<h1>Title</h1><p>A paragraph with <a href=\"https://example.com\">a link</a>.</p>"
}
```

---

##### convert-yaml-to-json

Convert a YAML string to JSON.

**Required fields:**
- `action`: `"convert-yaml-to-json"`
- `yaml_text` (string): Valid YAML string

**Example:**
```json
{
  "action": "convert-yaml-to-json",
  "yaml_text": "name: Alice\nage: 30\nhobbies:\n  - reading\n  - hiking"
}
```

---

##### convert-json-to-yaml

Convert a JSON string to YAML format.

**Required fields:**
- `action`: `"convert-json-to-yaml"`
- `json_text` (string): Valid JSON string

**Example:**
```json
{
  "action": "convert-json-to-yaml",
  "json_text": "{\"name\":\"Alice\",\"age\":30,\"hobbies\":[\"reading\",\"hiking\"]}"
}
```

---

##### convert-query-string-to-json

Parse a URL query string into a JSON object.

**Required fields:**
- `action`: `"convert-query-string-to-json"`
- `query_string` (string): URL query string (leading `?` is optional)

**Notes:** Parameters with a single value return a string. Parameters appearing multiple times return an array of values.

**Example:**
```json
{
  "action": "convert-query-string-to-json",
  "query_string": "?name=Alice&city=NYC&tag=a&tag=b"
}
```

---

#### Common Workflows

1. **API response reformatting:** Convert JSON API responses to CSV for spreadsheet import using `convert-json-to-csv`.
2. **Configuration migration:** Convert YAML config files to JSON or vice versa using `convert-yaml-to-json` / `convert-json-to-yaml`.
3. **Content publishing:** Convert Markdown drafts to HTML for web publishing using `convert-markdown-to-html`.
4. **Legacy system integration:** Convert between XML and JSON when bridging old and new systems using `convert-xml-to-json` / `convert-json-to-xml`.
5. **URL parameter extraction:** Parse query strings from URLs into structured JSON using `convert-query-string-to-json`.
6. **Timestamp handling:** Convert between Unix timestamps and readable dates for logging or scheduling using `convert-unix-to-date` / `convert-date-to-unix`.

#### Important Notes

- All input data is passed as strings in the respective text parameters (`json_text`, `csv_text`, `xml_text`, etc.).
- CSV input must include a header row for `convert-csv-to-json`.
- XML-to-JSON and JSON-to-XML conversions use `@attributes` for XML attributes and `#text` for text content.
- Timezone values must use IANA format (e.g., `"America/Chicago"`, not `"CST"`).
- JSON inputs must be valid JSON strings; malformed input returns an error.

## When To Use
- Use this skill for `Web Data Convertor` on AgentPMT.
- Use it when an agent needs this specific tool's behavior, schema, inputs, outputs, and invocation shape.
- Search and activation keywords: web data convertor, json to csv conversion, csv to json conversion, tabular data transformation, spreadsheet data export, convert csv to json, csv text, convert date to unix.
- Supported action names: `convert-csv-to-json`, `convert-date-to-unix`, `convert-html-to-markdown`, `convert-json-to-csv`, `convert-json-to-xml`, `convert-json-to-yaml`, `convert-markdown-to-html`, `convert-query-string-to-json`, `convert-unix-to-date`, `convert-xml-to-json`, `convert-yaml-to-json`.

## Use Cases
- JSON to CSV conversion
- CSV to JSON conversion
- tabular data transformation
- spreadsheet data export
- API response to CSV
- XML to JSON conversion
- JSON to XML conversion
- legacy system integration
- SOAP to REST translation
- configuration file conversion
- YAML to JSON conversion
- JSON to YAML conversion
- Kubernetes config conversion
- Docker Compose conversion
- infrastructure as code conversion
- Markdown to HTML conversion

## Categories And Industries
No categories or industry tags are published for this tool.

## Actions And Schema
Complete generated action schema: `./schema.md`.
Supported action count: `11`.
x402 availability: not enabled for this product.

- `convert-csv-to-json` (action slug: `convert-csv-to-json`): Convert CSV text (with header row) to a JSON array of objects. Numeric values are automatically converted. Price: `5` credits. Parameters: `csv_text`.
- `convert-date-to-unix` (action slug: `convert-date-to-unix`): Convert a date string to a Unix timestamp. Auto-detects common formats or use a custom format string. Price: `5` credits. Parameters: `date_format`, `date_string`.
- `convert-html-to-markdown` (action slug: `convert-html-to-markdown`): Convert HTML to clean Markdown format. Links are preserved, line wrapping is disabled. Price: `5` credits. Parameters: `html_text`.
- `convert-json-to-csv` (action slug: `convert-json-to-csv`): Convert a JSON object or array of objects to CSV format. All unique keys across objects become sorted column headers. Price: `5` credits. Parameters: `json_text`.
- `convert-json-to-xml` (action slug: `convert-json-to-xml`): Convert a JSON string to XML format. Single top-level key becomes root element; otherwise a root element wraps content. Use @attributes and #text keys for XML attributes and text. Price: `5` credits. Parameters: `json_text`.
- `convert-json-to-yaml` (action slug: `convert-json-to-yaml`): Convert a JSON string to YAML format with human-readable output. Price: `5` credits. Parameters: `json_text`.
- `convert-markdown-to-html` (action slug: `convert-markdown-to-html`): Convert Markdown text to HTML. Supports standard markdown, code blocks, tables, and fenced code. Price: `5` credits. Parameters: `markdown_text`.
- `convert-query-string-to-json` (action slug: `convert-query-string-to-json`): Parse a URL query string into a JSON object. Single-value params become strings, multi-value params become arrays. Leading '?' is optional. Price: `5` credits. Parameters: `query_string`.
- `convert-unix-to-date` (action slug: `convert-unix-to-date`): Convert a Unix timestamp to a human-readable date string with ISO format, readable format, and timezone info. Price: `5` credits. Parameters: `timestamp`, `timezone`.
- `convert-xml-to-json` (action slug: `convert-xml-to-json`): Convert an XML string to JSON. Attributes stored under @attributes, text content under #text. Repeated same-tag elements become arrays. Price: `5` credits. Parameters: `xml_text`.
- `convert-yaml-to-json` (action slug: `convert-yaml-to-json`): Convert a YAML string to JSON format. Price: `5` credits. Parameters: `yaml_text`.

## Live Schema And Examples
Use the compact schema above for ordinary calls. Before a new production integration, or whenever parameters, enum values, nested objects, outputs, or examples are unclear, fetch live details first.

- Exact schema: call `agentpmt-tool-search-and-execution` with `action: "get_schema"`, and `tool_id: "web-data-convertor"`.
- Detailed examples: call `agentpmt-tool-search-and-execution` with `action: "get_instructions"` and `tool_id: "web-data-convertor"`, or call this product with `action: "get_instructions"` when the product tool is already selected.
- Treat returned live schema and instructions as more specific than this generated summary.

MCP schema lookup through the main AgentPMT MCP server:

```json
{
  "method": "tools/call",
  "params": {
    "name": "AgentPMT-Tool-Search-and-Execution",
    "arguments": {
      "action": "get_schema",
      "tool_id": "web-data-convertor"
    }
  }
}
```

For live examples, keep the same MCP tool and use these arguments:

```json
{
  "action": "get_instructions",
  "tool_id": "web-data-convertor"
}
```

Authenticated AgentPMT REST schema lookup body:

```json
{
  "name": "agentpmt-tool-search-and-execution",
  "parameters": {
    "action": "get_schema",
    "tool_id": "web-data-convertor"
  }
}
```

Authenticated AgentPMT REST live examples body:

```json
{
  "name": "agentpmt-tool-search-and-execution",
  "parameters": {
    "action": "get_instructions",
    "tool_id": "web-data-convertor"
  }
}
```

## Call This Tool
Product slug: `web-data-convertor`

Marketplace page: https://www.agentpmt.com/marketplace/web-data-convertor

- AgentPMT account route: first use `../agentpmt-account-mcp-rest-api-setup` to connect the main MCP server or REST API for an Agent Group where this tool is enabled.
- x402 route: not enabled for this product.
- AgentPMT overview: use `../what-is-agentpmt` for marketplace, Agent Group, workflow, MCP, REST, and payment concepts.

If those setup skills are not installed beside this product skill, use the downloads below.

Core AgentPMT setup skills:
- What AgentPMT is: ../what-is-agentpmt
  - ClawHub page: https://clawhub.ai/agentpmt/what-is-agentpmt
  - OpenClaw install: `openclaw skills install what-is-agentpmt`
  - skills.sh install: `npx skills add AgentPMT/agent-skills --skill what-is-agentpmt`
- AgentPMT account MCP/REST setup: ../agentpmt-account-mcp-rest-api-setup
  - ClawHub page: https://clawhub.ai/agentpmt/agentpmt-account-mcp-rest-api-setup
  - OpenClaw install: `openclaw skills install agentpmt-account-mcp-rest-api-setup`
  - skills.sh install: `npx skills add AgentPMT/agent-skills --skill agentpmt-account-mcp-rest-api-setup`

skills.sh install script:

```bash
npx skills add AgentPMT/agent-skills --skill what-is-agentpmt
npx skills add AgentPMT/agent-skills --skill agentpmt-account-mcp-rest-api-setup
```

MCP call shape after the main AgentPMT MCP server is connected:

```json
{
  "method": "tools/call",
  "params": {
    "name": "Web-Data-Convertor",
    "arguments": {
      "action": "convert-csv-to-json",
      "csv_text": "example csv text"
    }
  }
}
```

Use the exact tool name returned by `tools/list`; the name above is the expected readable form.

Authenticated AgentPMT REST call body:

```json
{
  "name": "web-data-convertor",
  "parameters": {
    "action": "convert-csv-to-json",
    "csv_text": "example csv text"
  }
}
```

Use the setup skill for the account connection details before making REST calls.

## Response Handling
- Treat the returned JSON as the source of truth for this tool call.
- If the response includes warnings or correction targets, apply them before retrying.
- If the response includes a `passed` or success-style boolean, use it as the workflow gate.
- If validation fails or the response shape is unclear, call `get_schema` or `get_instructions` before retrying.
- If `convert-csv-to-json` fails, preserve the request parameters and retry only after fixing schema, auth, or payment errors.

## Security
- Do not place account secrets, wallet private keys, mnemonics, signatures, or payment headers in prompts or logs.
- Keep tool inputs scoped to the minimum content needed for the task.
- Use the setup skills for credential handling; this product skill only defines product-specific behavior.

## AgentPMT Reference
- What AgentPMT is: ../what-is-agentpmt (ClawHub: `what-is-agentpmt`, page: https://clawhub.ai/agentpmt/what-is-agentpmt; skills.sh: `npx skills add AgentPMT/agent-skills --skill what-is-agentpmt`)
- AgentPMT account MCP/REST setup: ../agentpmt-account-mcp-rest-api-setup (ClawHub: `agentpmt-account-mcp-rest-api-setup`, page: https://clawhub.ai/agentpmt/agentpmt-account-mcp-rest-api-setup; skills.sh: `npx skills add AgentPMT/agent-skills --skill agentpmt-account-mcp-rest-api-setup`)
- Marketplace product: https://www.agentpmt.com/marketplace/web-data-convertor
- AgentPMT main MCP server: https://api.agentpmt.com/mcp/
- AgentPMT REST invoke endpoint: https://api.agentpmt.com/products/purchase
