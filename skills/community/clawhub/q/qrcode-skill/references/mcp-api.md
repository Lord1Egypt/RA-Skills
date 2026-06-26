# MCP API Reference

## Server Endpoint

```text
URL: https://qrcode.api4claw.com/mcp
Protocol: MCP (Model Context Protocol) over HTTP
Protocol Version: 2024-11-05
```

## Tools

### generate_qr_code

Generate a QR code PNG image from text. Returns base64-encoded PNG.

**Input Schema:**

| Parameter | Type   | Required | Description                                          |
|-----------|--------|----------|------------------------------------------------------|
| `text`    | string | Yes      | Text to encode into QR code (max 1000 characters)    |
| `size`    | number | No       | Image size in pixels, range [128, 1024], default 512 |

**Request Example:**

```json
{
  "jsonrpc": "2.0",
  "id": 1,
  "method": "tools/call",
  "params": {
    "name": "generate_qr_code",
    "arguments": {
      "text": "https://github.com",
      "size": 512
    }
  }
}
```

**Response:**

Returns a base64-encoded PNG image string.

---

### decode_qr_code

Decode a QR code from a base64-encoded PNG image. Returns the decoded text.

**Input Schema:**

| Parameter      | Type   | Required | Description                                        |
|----------------|--------|----------|----------------------------------------------------|
| `image_base64` | string | Yes      | Base64-encoded PNG image data containing a QR code |

**Request Example:**

```json
{
  "jsonrpc": "2.0",
  "id": 2,
  "method": "tools/call",
  "params": {
    "name": "decode_qr_code",
    "arguments": {
      "image_base64": "iVBORw0KGgoAAAANSUhEUg..."
    }
  }
}
```

**Response:**

Returns the decoded text string from the QR code.
