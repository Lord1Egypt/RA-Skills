# uuid-generator

Generate UUIDs in various formats. Supports UUID v1, v4, v5, and custom patterns.

## Features

- **UUID v4** (default): Cryptographically random UUIDs
- **UUID v1**: Time-based UUIDs with timestamp and MAC address
- **UUID v5**: Namespace-based deterministic UUIDs (SHA-1)
- **Bulk generate**: Generate multiple UUIDs at once
- **Format options**: Standard, uppercase, no-dashes, URL-safe

## Usage

```
uuid
uuid v4
uuid v4 --count 10
uuid v1
uuid v5 ns:url "https://example.com"
uuid --format no-dashes
uuid --format uppercase
```

## Parameters

- `version`: UUID version to generate (v1/v4/v5, default: v4)
- `count`: Number of UUIDs to generate (default: 1)
- `namespace`: (v5 only) Namespace: url, dns, oid, x500, or custom
- `name`: (v5 only) Name within the namespace
- `format`: Output format: standard/uppercase/nodashes/urlsafe

## ⚠️ Disclaimer

This tool is provided "as is" for informational purposes only. Data accuracy is not guaranteed. Not financial, legal, or professional advice. Always verify critical information from official sources.

本工具仅供信息参考，不保证数据完全准确，不构成任何金融/法律/专业建议。请以官方来源为准。
