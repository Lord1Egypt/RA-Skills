# QR Code Configuration

## Setting File

QR code preference is stored in `qrcode_setting.txt` in the output directory.

**Location priority**:
1. Project directory: `./wechat-post/{topic-slug}/qrcode_setting.txt`
2. Skill user dir: `$HOME/.jeffli-skills/jeffli-wechat-post/qrcode_setting.txt`
3. Global default: `$HOME/.jeffli-skills/qrcode_setting.txt`

## Schema

```yaml
qrcode_enabled: true | false
qrcode_path: /path/to/qr/image.png   # absolute or relative path
qrcode_position: bottom-right         # future: bottom-left, center
qrcode_size_ratio: 0.12              # % of image width, default 12%
```

## Setting Persistence

When user answers Q4 (是否需要二维码), save to all three locations:
- Project-specific: `./wechat-post/{topic-slug}/qrcode_setting.txt`
- User default: `$HOME/.jeffli-skills/jeffli-wechat-post/qrcode_setting.txt`

**Read priority on next run**:
1. Check project-specific setting
2. Fall back to user default
3. Fall back to global default
4. Default to `qrcode_enabled: false`

## QR Code Image Requirements

| Property | Value |
|----------|-------|
| Format | PNG (transparent background preferred) |
| Minimum size | 300×300 px |
| Recommended size | 500×500 px |
| Margin | At least 10% white space around QR |

## Composite Script

After generating the main image, composite QR code:

```bash
python3 ${SKILL_DIR}/scripts/composite-qr.py <main_image> <qr_image> <output_path>
```

**composite-qr.py logic**:
1. Open main image, get dimensions
2. Calculate QR position (bottom-right, 12% of width, with 5% margin)
3. Paste QR image with white border (3% of QR width)
4. Save to output path
