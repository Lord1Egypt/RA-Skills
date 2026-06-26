# QR Code Decode Skill

QR code detection and decoding skill for AI agents. Upload an image (URL or base64), get structured results — decoded content, format, content type, position, and confidence.

**Service URL:** `https://data.cli.im/x-deepscan/vision`

## Quick Start

```bash
curl -s -X POST https://data.cli.im/x-deepscan/vision/detect \
  -H "Content-Type: application/json" \
  -d '{"url": "https://example.com/qrcode.jpg"}'
```

## API

### POST /detect

Unified JSON endpoint. Supports URL, base64, batch, and mixed input:

```bash
# Single URL
curl -s -X POST https://data.cli.im/x-deepscan/vision/detect \
  -H "Content-Type: application/json" \
  -d '{"url": "https://example.com/photo.jpg"}'

# Single base64
curl -s -X POST https://data.cli.im/x-deepscan/vision/detect \
  -H "Content-Type: application/json" \
  -d "{\"image\": \"$(base64 -i photo.jpg)\"}"

# Batch URLs
curl -s -X POST https://data.cli.im/x-deepscan/vision/detect \
  -H "Content-Type: application/json" \
  -d '{"urls": ["https://example.com/1.jpg", "https://example.com/2.jpg"]}'
```

Response:

```json
{
  "count": 1,
  "codes": [
    {
      "content": "https://example.com",
      "format": "QR Code",
      "content_type": "url",
      "bbox": {"x1": 211.8, "y1": 211.3, "x2": 425.8, "y2": 424.7},
      "confidence": 0.93
    }
  ]
}
```

### POST /detect/upload

File upload (alternative):

```bash
curl -X POST https://data.cli.im/x-deepscan/vision/detect/upload -F "file=@photo.jpg"
```

## Agent SKILL

See `SKILL.md` for AI agent integration documentation. Compatible with Claude Code, Cursor, and other agent tools.

## Rate Limits

| Tier | Limit |
|------|-------|
| Free | 20 requests/min, 200 requests/day (per IP) |

## Terms of Use

- This service provides free QR code detection and decoding capabilities.
- Usage that violates any applicable laws or regulations is prohibited.
- Malicious attacks, stress testing, or abuse of the service is prohibited.
- We reserve the right to restrict access in cases of abuse.
- No guarantee of 100% availability. We are not liable for losses caused by service interruptions.

## Contact

- **Email:** support@nears.cn
- **Website:** [cli.im](https://cli.im)
- **WeChat:** Scan to join our group

  <img src="https://gstatic.clewm.net/caoliao-resource/260401/453165_1bb24385.png" width="200" alt="WeChat Group">

For suggestions, bug reports, or partnership inquiries, feel free to reach out.
