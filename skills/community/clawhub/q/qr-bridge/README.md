# qr-bridge

**Decode the QR. Trace the gate. Explain why it breaks.**

An entry-point reconnaissance skill for AI coding agents. Goes beyond simple QR scanning — traces redirect chains, detects WeChat/WeCom/login gates, and explains *why* a link doesn't work.

## Why This Exists

AI agents can see QR codes in images but can't decode them. When they do get a URL, short links, platform gates, and login walls block the path. qr-bridge solves the full chain:

```
Image → QR Decode → URL → Redirect Trace → Gate Detection → Diagnosis
```

Born from a real scenario: trying to register for a Beijing AI meetup from a poster image, only to hit a WeChat-gated form that no amount of `curl` could open.

## Features

| Command | What It Does |
|---------|-------------|
| **Decode** | Extract QR codes from images using macOS CoreImage (zero dependencies, ~10ms) |
| **Trace** | Follow redirect chains from short URLs, output every hop |
| **Inspect** | Detect WeChat, WeCom, Taobao, Douyin, Xiaohongshu, and login gates |
| **Diagnose** | Explain WHY a link fails and suggest actionable next steps |
| **Generate** | Create QR codes from text/URLs |

## Quick Start

### As a Claude Code Skill
```bash
# Copy to your skills directory
cp -r . ~/.claude/skills/qr-bridge/

# Compile the Swift decoder
bash scripts/setup.sh
```

Then use naturally: *"Scan the QR code in this image"* or *"Where does this short link go?"*

### Standalone CLI
```bash
# Compile
swiftc scripts/qr-decode.swift -o scripts/qr-decode -O

# Decode
./scripts/qr-decode /path/to/image.png
```

Output:
```json
{
  "ok": true,
  "count": 1,
  "results": [
    {
      "message": "https://example.com",
      "symbology": "QRCode",
      "bounds": { "x": 40, "y": 40, "width": 290, "height": 290 }
    }
  ]
}
```

## Technical Details

- **Primary decoder**: macOS CoreImage (`CIDetectorTypeQRCode`) — native, zero external dependencies
- **Fallback**: pyzbar (if CoreImage unavailable)
- **QR generation**: Python `qrcode` library
- **Gate detection**: Pattern matching on domains, response headers, and page content
- **Redirect tracing**: `curl -sIL` with full hop logging

### Supported Gate Types

| Gate | Detection | What It Needs |
|------|-----------|---------------|
| WeChat | `weixin.qq.com` domains, MicroMessenger UA check | Open in WeChat app |
| WeCom | `work.weixin.qq.com`, enterprise auth | Must be org member |
| Taobao | `tb.cn`, `tbopen://` deep links | Open in Taobao app |
| Douyin | `douyin.com`, `snssdk://` | Open in Douyin app |
| Xiaohongshu | `xhslink.com` | Open in XHS app |
| Login Wall | 401/403, `/login` redirect | Sign in first |

## Requirements

- macOS (for CoreImage decoder)
- Python 3 + `qrcode[pil]` (for QR generation)
- Optional: `pyzbar` + `zbar` (fallback decoder)

## Origin Story

This skill was built during a collaboration between Claude Code and OpenClaw (觉), where we discovered that:
1. AI vision models can *see* QR codes but can't *decode* them
2. The real challenge isn't decoding — it's navigating the gates behind the code
3. macOS CoreImage can decode QR codes natively, no third-party libraries needed

The insight came from OpenClaw using CoreImage while Claude Code was stuck trying to install Python libraries. Different tools, same team.

## License

MIT

中文文档: [README_CN.md](README_CN.md)
