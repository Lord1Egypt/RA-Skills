# QR Code Generator

Generate QR codes from any text or URL with customizable options.

## Installation

No installation required. Uses Python standard library + certifi for SSL.

```bash
pip install certifi  # Optional but recommended for SSL verification
```

## Usage

### Basic Usage

```bash
# Generate QR code for URL
python3 scripts/qrcode_generator.py "https://example.com"

# Generate QR code for text
python3 scripts/qrcode_generator.py "Hello World"
```

### Advanced Options

```bash
# Custom size
python3 scripts/qrcode_generator.py "https://example.com" --size 500

# Custom margin
python3 scripts/qrcode_generator.py "Hello" --margin 2

# Different format
python3 scripts/qrcode_generator.py "Test" --format gif

# JSON output
python3 scripts/qrcode_generator.py "https://example.com" --json
```

## Examples

| Input | Use Case |
|-------|----------|
| `https://github.com` | Website URL |
| `mailto:hello@example.com` | Email link |
| `tel:+1234567890` | Phone number |
| `WIFI:T:WPA;S:MyNetwork;P:password;;` | WiFi credentials |
| `Hello World` | Plain text |

## API

Uses the free [qrserver.com API](https://api.qrserver.com). No API key required.

## Privacy

⚠️ Input text is sent to a third-party API (api.qrserver.com). Do not use for sensitive information like passwords or private keys.

## License

MIT License
