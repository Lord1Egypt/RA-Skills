---
name: qr-bridge
description: Decode QR codes, trace redirects, inspect gated destinations, and explain what the link actually needs
author: Vicky-v7
version: 1.0.0
allowed-tools: Bash, Read, Write, Glob, Grep, WebFetch, WebSearch
tags: qr, redirect, reconnaissance, macos, coreimage
---

# QR Bridge

**Entry point reconnaissance tool.** Decode QR codes, trace redirect chains, inspect gated destinations, and explain what the link actually needs.

## When to Use This Skill

Activate when the user asks to:
- Decode / scan / read a QR code from an image
- Trace where a short URL redirects to
- Check if a link requires WeChat / WeCom / login / app
- Diagnose why a link "doesn't work"
- Generate a QR code from text or URL

## Setup (First Run Only)

Before first use, compile the Swift decoder binary:

```bash
bash ~/.claude/skills/qr-bridge/scripts/setup.sh
```

If setup was already run, the binary exists at `~/.claude/skills/qr-bridge/scripts/qr-decode`. Skip setup if it exists.

## Commands

### 1. DECODE - Extract QR code content from an image

**Step 1: Check if binary exists**
```bash
ls ~/.claude/skills/qr-bridge/scripts/qr-decode 2>/dev/null && echo "COMPILED" || echo "NEED_SETUP"
```

If NEED_SETUP, run:
```bash
swiftc ~/.claude/skills/qr-bridge/scripts/qr-decode.swift -o ~/.claude/skills/qr-bridge/scripts/qr-decode -O
```

**Step 2: Run decoder (compiled binary - fast)**
```bash
~/.claude/skills/qr-bridge/scripts/qr-decode "/path/to/image.png"
```

**Step 3: If compiled binary fails, use interpreted mode (slower but always works)**
```bash
swift ~/.claude/skills/qr-bridge/scripts/qr-decode.swift "/path/to/image.png"
```

**Step 4: If CoreImage fails, try pyzbar fallback**
```python
python3 -c "
from pyzbar.pyzbar import decode
from PIL import Image
import json, sys
img = Image.open(sys.argv[1])
results = decode(img)
out = [{'message': r.data.decode(), 'symbology': r.type} for r in results]
print(json.dumps({'ok': bool(out), 'count': len(out), 'results': out}, indent=2))
" "/path/to/image.png"
```

**Output format (JSON):**
```json
{
  "ok": true,
  "count": 1,
  "results": [
    {
      "message": "https://example.com/path",
      "symbology": "QRCode",
      "bounds": { "x": 0, "y": 0, "width": 200, "height": 200 }
    }
  ],
  "file": "/path/to/image.png",
  "error": null
}
```

### 2. TRACE - Follow redirect chains

After decoding a URL from a QR code (or given a URL directly), trace the full redirect chain:

```bash
curl -sIL -o /dev/null -w '%{url_effective}\n' --max-redirs 15 --connect-timeout 10 "URL_HERE" 2>&1
```

For the **full chain with each hop**, use:
```bash
curl -sIL --max-redirs 15 --connect-timeout 10 -w '\n--- FINAL: %{url_effective} (HTTP %{http_code}) ---\n' "URL_HERE" 2>&1
```

Parse the `Location:` headers from the output to build the chain:
```
1. https://short.link/abc        → 302
2. https://tracking.example.com  → 301
3. https://final-destination.com → 200
```

### 3. INSPECT - Detect gated destinations

After tracing, inspect the final URL for access gates. Check for these patterns:

**WeChat/WeCom Gates (common in Chinese QR codes):**
- Domain contains: `weixin.qq.com`, `work.weixin.qq.com`, `mp.weixin.qq.com`, `open.weixin.qq.com`
- Redirect to `open.weixin.qq.com/connect/oauth2/authorize`
- Response contains: `请在微信客户端打开`, `请在企业微信客户端打开`
- Response header `logicret: -2` = article not found / deleted / unpublished
- User-Agent gating: returns different content for WeChat UA vs browser UA
- WeChat mini-program links: `weixin://dl/business/?appid=` — cannot be opened outside WeChat

**App-Gated Links:**
- Taobao: `tb.cn`, `m.tb.cn` — returns 200 with JS redirect to Taobao app. Look for `tbopen://` scheme or `s_status: STATUS_NORMAL` header
- Douyin: `v.douyin.com` — 302 redirect to `www.douyin.com`, then 404 for invalid links. Valid links redirect to `www.douyin.com/video/`
- Xiaohongshu: `xhslink.com` — 307 → `www.xiaohongshu.com`. Look for `snssdk://` or `xhsdiscover://` deep-link schemes
- Alipay: `ur.alipay.com` — redirects to `alipays://` scheme
- Response contains deep-link schemes: `weixin://`, `alipays://`, `tbopen://`, `snssdk://`, `xhsdiscover://`
- Meta refresh or JavaScript redirect to app store

**Login Walls:**
- HTTP 401 or 403 status
- Redirect to `/login`, `/signin`, `/oauth/authorize`
- Response contains login form elements

**Content Validity Check (run AFTER gate detection):**
- WeChat: header `logicret` value — `-2` means content invalid/deleted
- Douyin: final destination is 404 = video removed or link expired
- Taobao: response body contains `对不起` or `宝贝不存在` = product delisted

**Detection commands:**
```bash
# Step 1: Check response headers for platform signals
curl -sI --max-redirs 10 --connect-timeout 10 "URL_HERE" 2>&1

# Step 2: Check with browser-like UA
curl -sL --max-redirs 10 --connect-timeout 10 \
  -H "User-Agent: Mozilla/5.0 (iPhone; CPU iPhone OS 17_0 like Mac OS X) AppleWebKit/605.1.15" \
  "URL_HERE" | head -c 5000

# Step 3: Check with WeChat UA (reveals WeChat-gated content)
curl -sL --max-redirs 10 --connect-timeout 10 \
  -H "User-Agent: Mozilla/5.0 (iPhone; CPU iPhone OS 17_0 like Mac OS X) AppleWebKit/605.1.15 MicroMessenger/8.0.0" \
  "URL_HERE" | head -c 5000

# Step 4: Compare — if Step 2 and Step 3 return different content, the link is UA-gated
```

**Header signals to check:**
- `logicret: -2` → WeChat article invalid
- `s_status: STATUS_NORMAL` → Taobao link active
- `Location:` containing app deep-link schemes → app-gated redirect

### 4. DIAGNOSE - Explain and suggest next steps

Based on decode + trace + inspect results, provide a structured diagnosis:

**Output format:**
```
## QR Bridge Diagnosis

**Source:** [image filename]
**Decoded:** [raw content from QR]
**Type:** [URL | Text | vCard | WiFi | other]

### Redirect Chain
1. [url] → [status]
2. [url] → [status]
3. [url] → [final status]

### Access Gate
- **Gate type:** [WeChat | WeCom | Login | App-only | None]
- **Why it fails:** [explanation in plain language]
- **What it needs:** [specific requirement]

### Next Steps
- [actionable suggestion 1]
- [actionable suggestion 2]
```

**Common diagnoses to provide:**

| Gate Type | Why It Fails | What It Needs |
|-----------|-------------|---------------|
| WeChat | Link requires WeChat's built-in browser | Open in WeChat app > scan QR |
| WeChat (invalid) | `logicret: -2` — article deleted/unpublished | Request a valid article link |
| WeCom | Enterprise WeChat only | Must be a WeCom member of that org |
| Taobao | JS redirect to Taobao app | Open link in Taobao/淘宝 app |
| Douyin | 302→douyin.com, content requires app | Open in Douyin/抖音 app |
| Xiaohongshu | 307→xiaohongshu.com, app deep-link | Open in 小红书 app |
| Alipay | `alipays://` scheme redirect | Open in Alipay/支付宝 app |
| Mini Program | `weixin://dl/business/` scheme | Open in WeChat > scan QR to launch mini-program |
| Login Wall | Requires authentication | Sign in at [domain] first |
| App-Only | Deep link to native app | Install [app name] and scan in-app |
| Expired | Short link no longer resolves | Link has expired, request a new one |
| Geo-blocked | Returns different content by region | May need VPN to [region] |

### 5. GENERATE - Create QR codes from text/URLs

```bash
python3 -c "
import qrcode, sys, os
data = sys.argv[1]
out = sys.argv[2] if len(sys.argv) > 2 else os.path.expanduser('~/Desktop/qr-output.png')
qr = qrcode.QRCode(version=None, error_correction=qrcode.constants.ERROR_CORRECT_H, box_size=10, border=4)
qr.add_data(data)
qr.make(fit=True)
img = qr.make_image(fill_color='black', back_color='white')
img.save(out)
print(f'QR code saved to: {out}')
print(f'Content: {data}')
print(f'Size: {img.size[0]}x{img.size[1]}px')
" "CONTENT_HERE" "/output/path.png"
```

If qrcode is not installed:
```bash
pip3 install "qrcode[pil]"
```

## Full Workflow

When the user provides a QR code image, run the **full pipeline automatically**:

1. **DECODE** the image
2. If the decoded content is a URL:
   a. **TRACE** the redirect chain
   b. **INSPECT** the final destination for gates
   c. **DIAGNOSE** with full report
3. If the decoded content is NOT a URL (plain text, WiFi config, vCard, etc.):
   a. Present the content with type identification
   b. Skip trace/inspect

Always present results in the structured diagnosis format above.

## Error Handling

**Image cannot be read:**
- Verify the file exists and path is correct
- Check format (PNG, JPEG, HEIC, TIFF supported)
- Suggest converting if format is unusual: `sips -s format png input.webp --out converted.png`

**No QR code detected:**
- Image may be too low resolution
- QR code may be partially obscured
- Suggest: crop to QR region, improve contrast, try a screenshot instead of photo
- Try pyzbar fallback (different algorithm may succeed)

**Redirect fails (timeout/DNS):**
- Short link service may be down
- Link may have expired
- Try again with longer timeout: `--connect-timeout 30`

**Cannot determine gate type:**
- Fetch page content and look for clues in HTML/JS
- Check response headers for `X-Powered-By`, `Server`, custom headers
- Report what IS known and suggest manual inspection

## Notes

- This skill is macOS-native. CoreImage is the primary decoder (zero external dependencies).
- The Swift binary is compiled once and reused for speed (~10ms vs ~2s interpreted).
- For batch processing, loop the binary over multiple files.
- All output is designed to be actionable: never just say "it failed" -- explain WHY and WHAT TO DO.
