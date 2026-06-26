---
name: qr-code-tool
description: QR code generation and reading. Use when user says "generate QR code", "create QR", "read QR code", or wants to work with QR codes.
---

# QR Code Tool

Generate and read QR codes quickly.

## Commands

### Generate QR Code
When user says: "generate QR code for X", "create QR for URL Y"
```bash
bash skills/qr-code-tool-1.0.0/scripts/qr.sh generate "<text/url>" [--output filename.png]
```

### Generate WiFi QR
When user says: "create WiFi QR code"
```bash
bash skills/qr-code-tool-1.0.0/scripts/qr.sh wifi "<ssid>" "<password>" [--encryption WPA]
```

### Generate vCard QR
When user says: "create contact QR"
```bash
bash skills/qr-code-tool-1.0.0/scripts/qr.sh vcard "<name>" "<phone>" "<email>"
```

### Read QR Code
When user says: "read this QR code", "decode QR"
```bash
bash skills/qr-code-tool-1.0.0/scripts/qr.sh read "<image-path>"
```

### Batch Generate
When user says: "generate QR codes for list"
```bash
bash skills/qr-code-tool-1.0.0/scripts/qr.sh batch "<input-file.txt>" [--output-dir ./qrcodes]
```

## Examples

```bash
# Generate QR for URL
bash skills/qr-code-tool-1.0.0/scripts/qr.sh generate "https://example.com"

# Generate WiFi QR
bash skills/qr-code-tool-1.0.0/scripts/qr.sh wifi "MyNetwork" "password123"

# Generate contact QR
bash skills/qr-code-tool-1.0.0/scripts/qr.sh vcard "John Doe" "+1234567890" "john@example.com"

# Read QR from image
bash skills/qr-code-tool-1.0.0/scripts/qr.sh read "./qrcode.png"

# Batch generate from file
bash skills/qr-code-tool-1.0.0/scripts/qr.sh batch "./urls.txt" --output-dir ./qrcodes
```

## Output

QR codes are saved to:
- Default: `workspace/qrcodes/`
- Custom: `--output` parameter

## Response Format

When generating:
```
✅ QR Code Generated
   Content: https://example.com
   File: ./qrcodes/qr_20260310_103045.png
   Size: 300x300
```

When reading:
```
📱 QR Code Content:
https://example.com/page?id=123
```
