---
name: qrcode-generator
version: 1.0.0
description: Generate QR codes from text, URLs, or data. Use when: (1) user asks to create/generate/make a QR code, (2) converting a URL or text into a scannable QR code, (3) generating QR codes for payments (wechat, alipay, crypto), (4) creating QR codes for WiFi sharing, or (5) any task requiring a visual QR code image output.
---

# QR Code Generator

Generate QR codes from text, URLs, or data using the qrcode npm package.

## Usage

Run the included script:

```bash
node /workspace/skills/qrcode-generator/scripts/generate.js <text_or_url> [output_file]
```

**Arguments:**
- `text_or_url`: The content to encode (required)
- `output_file`: Output path (optional, defaults to qrcode.png)

**Examples:**
```bash
# Generate QR code for a URL
node /workspace/skills/qrcode-generator/scripts/generate.js "https://example.com"

# Generate QR code with custom output
node /workspace/skills/qrcode-generator/scripts/generate.js "https://example.com" "/workspace/my-qr.png"
```

## Output

- Saves QR code as PNG image
- Returns the file path in response
