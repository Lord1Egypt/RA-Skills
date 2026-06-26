---
name: x5-protocol
description: >
  Send X5 protocol API requests from the terminal. Use this skill whenever the user
  wants to test, call, or send X5 API requests; parse .x5 files; generate X5 cURL
  commands; or debug X5 service endpoints. Also trigger on mentions of X5 protocol,
  .x5 files, X5-Method headers, X5 signature/encoding, or when the user provides
  appid/appkey and wants to call an API.
---

# X5 Protocol Skill

Send X5 protocol requests directly from the terminal using `scripts/x5_client.py`.

## Quick Start

```bash
# Send request from .x5 file
python3 ~/.claude/skills/x5-protocol/scripts/x5_client.py --file request.x5 --json

# Inline request
python3 ~/.claude/skills/x5-protocol/scripts/x5_client.py \
  --appid my_app --appkey my_key \
  --url http://localhost:8080/x5/api \
  --method createUser \
  --body '{"name":"test"}' \
  --json
```

## X5 Protocol Specification

### Signature Calculation

```
sign = md5(appid + JSON.stringify(body) + appkey).toUpperCase()
```

The body is serialized as compact JSON (no spaces), then concatenated with appid and appkey, MD5-hashed, and uppercased.

### Request Encoding Steps

1. Build the X5 envelope:

```json
{
  "header": {
    "appid": "app_id",
    "sign": "MD5_SIGNATURE_UPPERCASE",
    "method": "X5_Method_Name"
  },
  "body": "{\"key\":\"value\"}"
}
```

2. JSON-serialize the envelope (compact, no spaces)
3. Base64-encode the JSON string
4. Send as POST with `Content-Type: application/x-www-form-urlencoded`
5. Body: `data=<url_encoded_base64>`

### Response Format

X5 responses use the same envelope structure:

```json
{
  "header": {
    "code": 0,
    "message": "success"
  },
  "body": { ... }
}
```

Success: HTTP 2xx AND X5 code 0 or 200.

## .x5 File Format

```x5
### Request Description
@name = RequestName
@appid = my_app_id
@appkey = my_app_key
@url = http://localhost:8080/x5/api/endpoint

POST @url
X5-Method: methodName
X-Custom-Header: custom-value

{
  "key": "value"
}
```

**Directives**:

| Directive | Description |
|-----------|-------------|
| `@name` | Request name (for multi-request files) |
| `@appid` | Application ID |
| `@appkey` | Application secret key |
| `@url` | Request URL (referenced by `POST @url`) |
| `X5-Method:` | X5 API method name (overwrites HTTP method) |

**Key parsing rules**:
- `###` separates multiple requests in one file
- `#` lines are comments
- `POST @url` sets URL via `@url` directive reference
- `X5-Method:` overwrites the method from the `POST` line
- Any `Header-Name: value` line becomes a custom HTTP header
- JSON body starts with `{` or `[`

**Multiple requests per file**:

```x5
### Create Resource
@name = createResource
@appid = my_app
@appkey = my_key
@url = http://localhost:8080/x5/resource/create

POST @url
X5-Method: createResource
{"name": "test"}

### Query Resource
@name = queryResource
@appid = my_app
@appkey = my_key
@url = http://localhost:8080/x5/resource/query

POST @url
X5-Method: queryResource
{"resourceId": "123"}
```

## CLI Reference

```
python3 x5_client.py [OPTIONS]

Options:
  --file FILE           Path to .x5 file
  --request-name NAME   Specific request name (for multi-request files)
  --list                List all requests in .x5 file (no send)
  --appid APPID         App ID (inline or override)
  --appkey APPKEY       App Key (inline or override)
  --url URL             Target URL (inline or override)
  --method METHOD       X5 method name (inline or override)
  --body BODY           JSON body string
  --body-file FILE      JSON body file path
  --header KEY=VALUE    Custom HTTP header (repeatable)
  --curl                Generate cURL command (no send)
  --dry-run             Show encoded request (no send)
  --json                Output in JSON format
  --timeout MS          Timeout in ms (default: 30000)
```

## Usage Patterns

### Pattern 1: Send from .x5 file

```bash
python3 ~/.claude/skills/x5-protocol/scripts/x5_client.py --file /path/to/request.x5 --json
```

For multi-request files, use `--request-name`:
```bash
python3 ~/.claude/skills/x5-protocol/scripts/x5_client.py --file /path/to/api.x5 --request-name createUser --json
```

### Pattern 2: Inline request

Use when the user describes a request conversationally or provides parameters directly:

```bash
python3 ~/.claude/skills/x5-protocol/scripts/x5_client.py \
  --appid VALUE --appkey VALUE --url VALUE --method VALUE \
  --body '{"key":"value"}' --json
```

### Pattern 3: Generate cURL

```bash
python3 ~/.claude/skills/x5-protocol/scripts/x5_client.py --file request.x5 --curl
```

### Pattern 4: List requests in file

```bash
python3 ~/.claude/skills/x5-protocol/scripts/x5_client.py --file request.x5 --list
```

### Pattern 5: Debug / inspect encoded request

```bash
python3 ~/.claude/skills/x5-protocol/scripts/x5_client.py --file request.x5 --dry-run --json
```

Shows signature, Base64 payload, and full envelope without sending.

## Important Notes

- Always use `--json` for programmatic consumption — parse the JSON output to present results to the user
- When a .x5 file has multiple requests and the user doesn't specify which one, list them and ask
- CLI params (`--appid`, `--appkey`, etc.) override values from the .x5 file
- The script uses Python stdlib only (zero dependencies)
- Exit code 0 = success, 1 = error, 2 = argument error
- On error with `--json`, output is `{"success": false, "error": "message"}`
