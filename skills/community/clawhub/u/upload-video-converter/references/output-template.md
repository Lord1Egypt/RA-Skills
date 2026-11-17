# Conversion Delivery Template

Deliver every conversion job in this structure.

## 1. Job overview

- Source: filename, codec/container, resolution, fps (CFR/VFR), bit depth, duration, size
- Destination(s) and their hard requirements
- Priority: quality / size / speed

## 2. Per-destination results

### Destination X

| Field | Required | Delivered |
|---|---|---|
| Container | | |
| Video codec / profile | | |
| Resolution | | |
| Frame rate | | |
| Pixel format / color | | |
| Audio | | |
| Duration | | |
| File size | | |

- **Path used:** passthrough / remux / re-encode (and why)
- **Quality tradeoffs:** what was sacrificed, where visible
- **Command:** exact command or settings used

## 3. Verification

- Output probed: yes/no, key values
- Spot-play check: start / middle / end (sync, artifacts)
- Test upload result if performed

## 4. Blocked items

- Files that need editing first (duration caps → cutter skill)
- Aspect-ratio work needed (→ resizer skill)
- Specs that couldn't be met and why

## 5. One-line delivery note

Example: "3 outputs from one ProRes master: 58MB marketplace 1080p (CRF 20), Meta ad blocked pending 30s cut, 3.1MB email loop; commands attached."
