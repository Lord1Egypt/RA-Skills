---
slug: qrcode-tool
name: QR Code Generator
description: "Generate QR codes from URLs or text. Export as PNG with customizable size. No API key required."
keywords: qrcode, qr, barcode, generator, url, text
version: "1.0.0"
author: Qiance
language: en
---

# QR Code Generator

Generate QR codes from any text or URL. Supports customization and exports as PNG format.

## Features

- Generate QR codes from any text/URL
- Custom size (default 300px)
- Custom margin
- Export as PNG format
- No API key required

## Usage

```bash
# Generate QR code for URL
python3 scripts/qrcode_generator.py "https://example.com"

# Generate QR code for text
python3 scripts/qrcode_generator.py "Hello World"

# Custom size
python3 scripts/qrcode_generator.py "https://example.com" --size 500
```

## Examples

```
Generate QR code for: https://github.com
Generate QR code for: Contact me at hello@example.com
Generate QR code for: WIFI:T:WPA;S:MyNetwork;P:password;;
```

## Technical Details

- Uses qrserver.com public API
- SSL certificate verification enabled (certifi)
- No sensitive data transmission

## Dependencies

- Python 3.7+
- certifi (SSL certificates)

## Privacy Note

Input text is sent to api.qrserver.com (third-party service). Not recommended for sensitive information.

---

## 中文说明

输入URL或文本，生成PNG二维码。

- 自定义尺寸（默认300px）
- 无需API Key
- 使用qrserver.com公开API
