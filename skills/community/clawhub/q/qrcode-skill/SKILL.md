---
name: qrcode-skill
description: "QR code generation and decoding skill. Use when: generating QR codes from text/URLs, decoding/reading/parsing QR codes from images, creating scannable QR codes, extracting information from QR code images. Calls remote MCP service for QR code operations."
argument-hint: "Describe what QR code operation you need, e.g. 'generate a QR code for https://example.com' or 'decode this QR code image'"
user-invocable: true
disable-model-invocation: false
---

# QR Code Skill

Generate and decode QR codes via the remote MCP service at `https://qrcode.api4claw.com/mcp`.

## Capabilities

| Operation | MCP Tool | Description |
|-----------|----------|-------------|
| Generate QR Code | `generate_qr_code` | Convert text or URL into a QR code PNG image (base64-encoded) |
| Decode QR Code | `decode_qr_code` | Extract text content from a QR code image |

## MCP Server Configuration

This skill requires the following MCP server to be configured:

```json
{
  "mcpServers": {
    "qrcode": {
      "type": "http",
      "url": "https://qrcode.api4claw.com/mcp"
    }
  }
}
```

## Procedure

### Generate a QR Code

1. Confirm the text or URL to encode (max 1000 characters)
2. Optionally confirm desired image size (128–1024 pixels, default 512)
3. Call the `generate_qr_code` MCP tool:
   - `text` (required): The content to encode
   - `size` (optional): Image size in pixels
4. The tool returns a base64-encoded PNG image
5. Present the QR code image to the user using markdown: `![QR Code](data:image/png;base64,<base64_data>)`
6. If the user wants to save it, write the decoded base64 data to a `.png` file

### Decode a QR Code

1. Obtain the QR code image from the user — accept one of:
   - A file path to a PNG image in the workspace
   - A base64-encoded image string
   - An image pasted into the chat
2. If a file path is provided, read it and convert to base64
3. Call the `decode_qr_code` MCP tool:
   - `image_base64` (required): Base64-encoded PNG image data
4. Return the decoded text to the user

## API Reference

See [MCP API Reference](./references/mcp-api.md) for detailed tool schemas and examples.

## Error Handling

- If text exceeds 1000 characters, inform the user and ask them to shorten it
- If the image does not contain a recognizable QR code, report the decoding failure clearly
- If the MCP server is unreachable, inform the user to check network connectivity

## Examples

**Generate:**
> "Generate a QR code for https://github.com"
> "Create a 256px QR code containing my WiFi config: WIFI:T:WPA;S:MyNetwork;P:password123;;"

**Decode:**
> "Decode the QR code in ./assets/ticket.png"
> "What does this QR code say?" (with image attached)
