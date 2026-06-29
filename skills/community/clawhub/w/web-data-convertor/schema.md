# Web Data Convertor Schema

This generated reference belongs to the adjacent `SKILL.md`. Use it for exact action names, action slugs, parameter summaries, sample parameters, and generated JSON parameter schemas.

Product slug: `web-data-convertor`

x402 availability: not enabled for this product.

## `convert-csv-to-json`

Action slug: `convert-csv-to-json`

Price: `5` credits

Convert CSV text (with header row) to a JSON array of objects. Numeric values are automatically converted.

Parameters:

| Parameter | Type | Required | Description |
|---|---|---|---|
| `csv_text` | `string` | yes | CSV string with a header row. |

Sample parameters:

```json
{
  "csv_text": "example csv text"
}
```

Generated JSON parameter schema:

```json
{
  "csv_text": {
    "description": "CSV string with a header row.",
    "required": true,
    "type": "string"
  }
}
```

## `convert-date-to-unix`

Action slug: `convert-date-to-unix`

Price: `5` credits

Convert a date string to a Unix timestamp. Auto-detects common formats or use a custom format string.

Parameters:

| Parameter | Type | Required | Description |
|---|---|---|---|
| `date_format` | `string` | no | Python strftime format string for parsing. If omitted, common formats are tried automatically. |
| `date_string` | `string` | yes | Date string to convert (e.g., '2024-11-14 22:13:20', '2024-11-14'). |

Sample parameters:

```json
{
  "date_format": "example date format",
  "date_string": "example date string"
}
```

Generated JSON parameter schema:

```json
{
  "date_format": {
    "description": "Python strftime format string for parsing. If omitted, common formats are tried automatically.",
    "required": false,
    "type": "string"
  },
  "date_string": {
    "description": "Date string to convert (e.g., '2024-11-14 22:13:20', '2024-11-14').",
    "required": true,
    "type": "string"
  }
}
```

## `convert-html-to-markdown`

Action slug: `convert-html-to-markdown`

Price: `5` credits

Convert HTML to clean Markdown format. Links are preserved, line wrapping is disabled.

Parameters:

| Parameter | Type | Required | Description |
|---|---|---|---|
| `html_text` | `string` | yes | HTML content to convert. |

Sample parameters:

```json
{
  "html_text": "example html text"
}
```

Generated JSON parameter schema:

```json
{
  "html_text": {
    "description": "HTML content to convert.",
    "required": true,
    "type": "string"
  }
}
```

## `convert-json-to-csv`

Action slug: `convert-json-to-csv`

Price: `5` credits

Convert a JSON object or array of objects to CSV format. All unique keys across objects become sorted column headers.

Parameters:

| Parameter | Type | Required | Description |
|---|---|---|---|
| `json_text` | `string` | yes | Valid JSON string (object or array of objects). |

Sample parameters:

```json
{
  "json_text": "example json text"
}
```

Generated JSON parameter schema:

```json
{
  "json_text": {
    "description": "Valid JSON string (object or array of objects).",
    "required": true,
    "type": "string"
  }
}
```

## `convert-json-to-xml`

Action slug: `convert-json-to-xml`

Price: `5` credits

Convert a JSON string to XML format. Single top-level key becomes root element; otherwise a root element wraps content. Use @attributes and #text keys for XML attributes and text.

Parameters:

| Parameter | Type | Required | Description |
|---|---|---|---|
| `json_text` | `string` | yes | Valid JSON string. |

Sample parameters:

```json
{
  "json_text": "example json text"
}
```

Generated JSON parameter schema:

```json
{
  "json_text": {
    "description": "Valid JSON string.",
    "required": true,
    "type": "string"
  }
}
```

## `convert-json-to-yaml`

Action slug: `convert-json-to-yaml`

Price: `5` credits

Convert a JSON string to YAML format with human-readable output.

Parameters:

| Parameter | Type | Required | Description |
|---|---|---|---|
| `json_text` | `string` | yes | Valid JSON string. |

Sample parameters:

```json
{
  "json_text": "example json text"
}
```

Generated JSON parameter schema:

```json
{
  "json_text": {
    "description": "Valid JSON string.",
    "required": true,
    "type": "string"
  }
}
```

## `convert-markdown-to-html`

Action slug: `convert-markdown-to-html`

Price: `5` credits

Convert Markdown text to HTML. Supports standard markdown, code blocks, tables, and fenced code.

Parameters:

| Parameter | Type | Required | Description |
|---|---|---|---|
| `markdown_text` | `string` | yes | Markdown content to convert. |

Sample parameters:

```json
{
  "markdown_text": "example markdown text"
}
```

Generated JSON parameter schema:

```json
{
  "markdown_text": {
    "description": "Markdown content to convert.",
    "required": true,
    "type": "string"
  }
}
```

## `convert-query-string-to-json`

Action slug: `convert-query-string-to-json`

Price: `5` credits

Parse a URL query string into a JSON object. Single-value params become strings, multi-value params become arrays. Leading '?' is optional.

Parameters:

| Parameter | Type | Required | Description |
|---|---|---|---|
| `query_string` | `string` | yes | URL query string (e.g., 'key1=value1&key2=value2'). |

Sample parameters:

```json
{
  "query_string": "example search query"
}
```

Generated JSON parameter schema:

```json
{
  "query_string": {
    "description": "URL query string (e.g., 'key1=value1&key2=value2').",
    "required": true,
    "type": "string"
  }
}
```

## `convert-unix-to-date`

Action slug: `convert-unix-to-date`

Price: `5` credits

Convert a Unix timestamp to a human-readable date string with ISO format, readable format, and timezone info.

Parameters:

| Parameter | Type | Required | Description |
|---|---|---|---|
| `timestamp` | `integer` | yes | Unix timestamp in seconds since epoch. |
| `timezone` | `string` | no | IANA timezone name (e.g., 'America/New_York', 'UTC', 'Europe/London'). Default: 'UTC'. |

Sample parameters:

```json
{
  "timestamp": 1,
  "timezone": "UTC"
}
```

Generated JSON parameter schema:

```json
{
  "timestamp": {
    "description": "Unix timestamp in seconds since epoch.",
    "required": true,
    "type": "integer"
  },
  "timezone": {
    "default": "UTC",
    "description": "IANA timezone name (e.g., 'America/New_York', 'UTC', 'Europe/London'). Default: 'UTC'.",
    "required": false,
    "type": "string"
  }
}
```

## `convert-xml-to-json`

Action slug: `convert-xml-to-json`

Price: `5` credits

Convert an XML string to JSON. Attributes stored under @attributes, text content under #text. Repeated same-tag elements become arrays.

Parameters:

| Parameter | Type | Required | Description |
|---|---|---|---|
| `xml_text` | `string` | yes | Valid XML string. |

Sample parameters:

```json
{
  "xml_text": "example xml text"
}
```

Generated JSON parameter schema:

```json
{
  "xml_text": {
    "description": "Valid XML string.",
    "required": true,
    "type": "string"
  }
}
```

## `convert-yaml-to-json`

Action slug: `convert-yaml-to-json`

Price: `5` credits

Convert a YAML string to JSON format.

Parameters:

| Parameter | Type | Required | Description |
|---|---|---|---|
| `yaml_text` | `string` | yes | Valid YAML string. |

Sample parameters:

```json
{
  "yaml_text": "example yaml text"
}
```

Generated JSON parameter schema:

```json
{
  "yaml_text": {
    "description": "Valid YAML string.",
    "required": true,
    "type": "string"
  }
}
```
