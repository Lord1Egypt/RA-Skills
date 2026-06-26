# QR Code Tool Skill

Generate and read QR codes for OpenClaw.

## Features

- ✅ Generate QR from text/URL
- ✅ WiFi QR codes (scan to connect)
- ✅ vCard QR codes (contact sharing)
- ✅ Read/decode QR from images
- ✅ Batch generation

## Requirements

- `qrencode` - For generating QR codes
- `zbar-tools` - For reading QR codes (optional)

### Install Dependencies

**macOS:**
```bash
brew install qrencode zbar
```

**Linux:**
```bash
sudo apt-get install qrencode zbar-tools
```

## Usage

### Generate QR
```bash
bash skills/qr-code-tool-1.0.0/scripts/qr.sh generate "https://example.com"
bash skills/qr-code-tool-1.0.0/scripts/qr.sh generate "Hello World" --output my-qr.png
```

### WiFi QR
```bash
bash skills/qr-code-tool-1.0.0/scripts/qr.sh wifi "MyNetwork" "password123"
```

### Contact QR
```bash
bash skills/qr-code-tool-1.0.0/scripts/qr.sh vcard "John Doe" "+1234567890" "john@example.com"
```

### Read QR
```bash
bash skills/qr-code-tool-1.0.0/scripts/qr.sh read "./qrcode.png"
```

### Batch Generate
```bash
bash skills/qr-code-tool-1.0.0/scripts/qr.sh batch "./urls.txt"
```

## License

MIT
