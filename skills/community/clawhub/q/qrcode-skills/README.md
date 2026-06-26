English | [中文](README.zh-cn.md)

# QR Code Skills

An agent skill for generating and decoding QR codes.

**Fully local** — no remote API or API key required.

**Declaration:**
- **All dependencies are open-source**: Every dependency (Python: zxingcpp, Pillow, openpyxl, qrcode; Node.js: qrcode, qr-scanner-wechat, sharp, xlsx, archiver) is a publicly available open-source project. Source code and licenses can be found on PyPI / npm.
- **All operations run locally**: Generation and decoding are performed entirely on the user's machine. No remote API calls, no data uploads. The only exception is when decoding a remote image URL; the image is downloaded locally first, then decoded.

For QR code generation URLs (preview without saving files) or better decoding accuracy, use [qrcode-remote-skills](https://github.com/caoliao/qrcode-remote-skills): `npx skills add caoliao/qrcode-remote-skills`.

## Features

| Feature | Description |
|---------|-------------|
| Generate QR code | Encode text/URL into a QR code image, saved locally |
| Decode QR code | Read QR code content from a local image or image URL |
| Batch generate | Generate QR code images locally from Excel/CSV/TXT |
| Batch decode | Batch decode QR codes from Excel/CSV/TXT, write results back |

## Installation

### Via skills CLI (Recommended)

```bash
npx skills add caoliao/qrcode-skills
```

```bash
# Global install (available across projects)
npx skills add caoliao/qrcode-skills -g

# Install for a specific agent
npx skills add caoliao/qrcode-skills -a cursor
npx skills add caoliao/qrcode-skills -a claude-code
```

### Manual Installation

Clone this repository into your agent's skills directory:

```bash
git clone https://github.com/caoliao/qrcode-skills
```

### Install Dependencies (pick one)

The agent will auto-detect your environment and install dependencies on first use. You can also install manually:

**Python**

```bash
cd qrcode-skills
pip install -r requirements.txt
```

Dependencies: `zxingcpp`, `Pillow`, `openpyxl`, `qrcode`

**Node.js (when Python is unavailable)**

```bash
cd qrcode-skills
npm install
```

Dependencies: `qrcode`, `qr-scanner-wechat`, `sharp`, `xlsx`, `archiver`

> Both script sets are functionally identical. The agent auto-detects the available runtime.

### Verify Installation

After installation, simply ask your agent "Generate a QR code for me" to trigger this skill.

## Examples

### Generate a QR Code

> **You:** Generate a QR code for https://example.com

> **AI:** *(runs local generation script)*
>
> QR code generated and saved locally:
>
> **Local file:** `D:\workspace\qrcode.png`

---

### Generate & Save to Specific Path

> **You:** Generate a QR code and save it to the desktop, content is Hello World, SVG format

> **AI:** *(runs local generation script)*
>
> QR code generated and saved locally:
>
> **Local file:** `C:\Users\xxx\Desktop\qrcode.svg`

---

### Decode a QR Code (Local File)

> **You:** Decode this QR code *(paste/drag an image)*

> **AI:** *(gets image path, runs decode script)*
>
> QR code decoded (via zxing):
> - Content: https://example.com

---

### Decode a QR Code (URL)

> **You:** Decode this QR code https://example.com/qr.png

> **AI:** *(downloads image locally, runs decode script)*
>
> QR code decoded (via zxing):
> - Content: https://cli.im

---

### Batch Generate

> **You:** Batch generate QR code images from the link column in products.csv, zip them up

> **AI:** *(runs script)*
>
> Batch generation complete: 200 total, 200 succeeded, 0 failed
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
qrcode-skills/
├── README.md                   # English documentation (this file)
├── README.zh-cn.md             # Chinese documentation
├── SKILL.md                    # Agent skill instructions
├── requirements.txt            # Python dependencies
├── package.json                # Node.js dependencies
└── scripts/
    ├── generate.py / .js       # Single QR code generation & save
    ├── batch_generate.py / .js # Batch generation (images)
    ├── decode.py / .js         # Single decode (fully local)
    └── batch_decode.py / .js   # Batch decode (fully local)
```

## Technical Details

- **Dual runtime**: All scripts are available in both Python and Node.js with identical parameters and output formats
- **Generation**: Uses local libraries (Python: `qrcode` / Node: `qrcode`) to generate QR code images directly
- **Decoding**: Uses local libraries (Python: `zxingcpp` / Node: `qr-scanner-wechat`) for decoding, no remote dependency
- **Batch operations**: Supports Excel (.xlsx), CSV, TXT input; auto-detects data columns, prompts user when ambiguous
- **Fully offline**: All generation and decoding operations run locally with no network required (unless decoding input is a remote image URL)
- **Open-source only**: All dependencies are open-source libraries; no proprietary or closed-source components
