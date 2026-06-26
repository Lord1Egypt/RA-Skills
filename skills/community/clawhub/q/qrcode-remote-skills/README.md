English | [中文](README.zh-cn.md)

# QR Code Remote Skills

An agent skill for generating and decoding QR codes.

Built on the [CaoLiao QR Code API](https://cli.im/open-api/qrcode-api/quick-start.html) and local libraries. No API key required.

This skill generates static QR codes only (not CaoLiao dynamic codes).

## Security

- **Privacy**: QR code images uploaded to the server for decoding are temporary files that are automatically deleted after a period of time. No long-term storage of your images.
- **Transparency**: All third-party libraries used (zxingcpp, Pillow, qrcode, CaoLiao API, etc.) are public and open-source. You can audit the dependencies yourself.
- **Local-first**: Decoding is performed locally by default. Remote API is only used when local decoding fails, minimizing data transmission.

## Features

| Feature | Description |
|---------|-------------|
| Generate QR code | Encode text/URL into a QR code, return link with preview |
| Generate & save locally | Download QR code image to a specified path |
| Decode QR code | Read QR code content from an image URL or local file |
| Batch generate (URL) | Generate QR code URL list from Excel/CSV/TXT |
| Batch generate (image) | Generate QR code images locally from Excel/CSV/TXT |
| Batch decode | Batch decode QR codes from Excel/CSV/TXT, write results back |

## Installation

### Via skills CLI (Recommended)

```bash
npx skills add caoliao/qrcode-remote-skills
```

```bash
# Global install (available across projects)
npx skills add caoliao/qrcode-remote-skills -g

# Install for a specific agent
npx skills add caoliao/qrcode-remote-skills -a cursor
npx skills add caoliao/qrcode-remote-skills -a claude-code
```

### Manual Installation

Clone this repository into your agent's skills directory:

```bash
git clone https://github.com/caoliao/qrcode-remote-skills
```

### Install Dependencies (pick one)

The agent will auto-detect your environment and install dependencies on first use. You can also install manually:

**Python**

```bash
cd qrcode-remote-skills
pip install -r requirements.txt
```

Dependencies: `zxingcpp`, `Pillow`, `openpyxl`, `qrcode`

**Node.js (when Python is unavailable)**

```bash
cd qrcode-remote-skills
npm install
```

Dependencies: `qrcode`, `jsqr`, `jimp`, `xlsx`, `archiver`

> Both script sets are functionally identical. The agent auto-detects the available runtime.

### Verify Installation

After installation, simply ask your agent "Generate a QR code for me" to trigger this skill.

## Examples

### Generate a QR Code

> **You:** Generate a QR code for https://cli.im

> **AI:** QR code generated:
>
> ![QR Code](https://api.2dcode.biz/v1/create-qr-code?data=https%3A%2F%2Fcli.im&size=400x400)
>
> **QR Code URL:** `https://api.2dcode.biz/v1/create-qr-code?data=https%3A%2F%2Fcli.im&size=400x400`

---

### Generate & Save Locally

> **You:** Generate a QR code and save it to the desktop, content is Hello World, SVG format

> **AI:** *(runs script to download image)*
>
> QR code generated and saved locally:
>
> **QR Code URL:** `https://api.2dcode.biz/v1/create-qr-code?data=Hello%20World&size=400x400&format=svg`
> **Local file:** `C:\Users\xxx\Desktop\qrcode.svg`

---

### Decode a QR Code (URL)

> **You:** Decode this QR code https://example.com/qr.png

> **AI:** *(runs decode script)*
>
> QR code decoded (via zxing):
> - Content: https://cli.im

---

### Decode a QR Code (Image)

> **You:** Decode this QR code *(paste/drag an image)*

> **AI:** *(gets image path, runs decode script)*
>
> QR code decoded (via zxing):
> - Content: https://example.com

---

### Batch Generate (URL Links)

> **You:** I have a data.xlsx, batch generate QR codes

> **AI:** Would you like QR code URL links or image files saved locally?

> **You:** Links are fine

> **AI:** *(runs script)*
>
> Batch generation complete: 50 QR code links saved to `D:\output\urls.txt`

---

### Batch Generate (Images)

> **You:** Batch generate QR code images from the link column in products.csv, zip them up

> **AI:** *(runs script)*
>
> Batch generation complete (via local): 200 total, 200 succeeded, 0 failed
> Output directory: `D:\output\qrcodes`
> ZIP file: `D:\output\qrcodes.zip`

---

### Batch Decode

> **You:** Batch decode QR code images in images.xlsx

> **AI:** Detected the following columns. Which column contains the QR code image URLs?
>
> | Index | Column Name |
> |-------|-------------|
> | 0 | Product Name |
> | 1 | Image Link |
> | 2 | Notes |

> **You:** Column 1

> **AI:** *(runs script)*
>
> Batch decode complete: 50 total, 48 succeeded, 2 failed
> Results written to: `D:\data\images.xlsx` (new "Decode Result" column added)

## Project Structure

```
qrcode-remote-skills/
├── README.md                   # Chinese documentation
├── README.en.md                # English documentation (this file)
├── SKILL.md                    # Agent skill instructions
├── reference.md                # CaoLiao API reference
├── requirements.txt            # Python dependencies
├── package.json                # Node.js dependencies
└── scripts/
    ├── generate.py / .js       # Single QR code generation & save
    ├── batch_generate.py / .js # Batch generation (URL links / images)
    ├── decode.py / .js         # Single decode (local-first + API fallback)
    └── batch_decode.py / .js   # Batch decode (write-back / TXT output)
```

## Technical Details

- **Dual runtime**: All scripts are available in both Python and Node.js with identical parameters and output formats
- **Generation**: Constructs CaoLiao API URLs directly by default (zero latency); downloads images when saving locally; batch image generation uses local libraries (Python: `qrcode` / Node: `qrcode`)
- **Decoding**: Prefers local library decoding (Python: `zxingcpp` / Node: `jsQR` + `jimp`), falls back to CaoLiao API on failure
- **Batch operations**: Supports Excel (.xlsx), CSV, TXT input; auto-detects data columns, prompts user when ambiguous
- **CaoLiao API**: Free, no authentication required. [Official docs](https://cli.im/open-api/qrcode-api/quick-start.html)
