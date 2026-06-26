---
name: url-toolkit
description: URL encoding, decoding, parameter parsing, and URL manipulation toolkit for developers.
metadata: { "openclaw": { "emoji": "🔗", "requires": { "bins": ["python3"] } } }
---

# URL Toolkit

A comprehensive URL manipulation tool for developers.

## Features

- **Encode** - Encode URL (percent encoding)
- **Decode** - Decode URL
- **Parse** - Parse URL into components (scheme, host, path, query, etc.)
- **Query Parse** - Parse query string into key-value pairs
- **Query Build** - Build query string from key-value pairs

## Usage

```bash
python3 skills/url-toolkit/scripts/url_toolkit.py <action> [options]
```

## Actions

| Action | Description |
|--------|-------------|
| `encode` | URL encode a string |
| `decode` | URL decode a string |
| `parse` | Parse URL into components |
| `query-parse` | Parse query string to JSON |
| `query-build` | Build query string from JSON |

## Options

| Option | Type | Default | Description |
|--------|------|---------|-------------|
| `--input` | string | - | Input string or URL |
| `--full` | bool | false | Full encoding (all chars) vs safe encoding |

## Examples

```bash
# URL encode
python3 skills/url-toolkit/scripts/url_toolkit.py encode --input "hello world"
# Output: {"success": true, "result": "hello%20world"}

# URL decode
python3 skills/url-toolkit/scripts/url_toolkit.py decode --input "hello%20world"
# Output: {"success": true, "result": "hello world"}

# Parse URL
python3 skills/url-toolkit/scripts/url_toolkit.py parse --input "https://example.com:8080/path?q=test&id=123#section"
# Output: {"success": true, "result": {"scheme": "https", "host": "example.com", ...}}

# Parse query string
python3 skills/url-toolkit/scripts/url_toolkit.py query-parse --input "q=test&id=123&name=hello+world"
# Output: {"success": true, "result": {"q": "test", "id": "123", "name": "hello world"}}

# Build query string
python3 skills/url-toolkit/scripts/url_toolkit.py query-build --input '{"q":"test","id":123,"name":"hello world"}'
# Output: {"success": true, "result": "q=test&id=123&name=hello%20world"}
```

## Use Cases

1. **API development** - Encode/decode URL parameters
2. **Web scraping** - Parse URLs and extract components
3. **Debugging** - Inspect query parameters
4. **URL building** - Construct URLs from components
5. **Data processing** - Clean and normalize URLs

## Current Status

Ready for testing.
