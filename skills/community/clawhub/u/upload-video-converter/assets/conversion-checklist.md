# Conversion — Pre-Delivery Checklist

Fix any failed item before delivering.

## A. Source understanding (6)

- [ ] Source probed: codec, container, resolution, fps, pix_fmt, duration, size
- [ ] VFR detected and handled (forced CFR if re-encoding)
- [ ] HDR/10-bit detected and conversion path chosen
- [ ] Audio codec/channels/sample rate noted
- [ ] Source is the master, not an already-compressed output (no generation loss)
- [ ] Duration vs destination caps checked (over-length flagged for cutting, not truncated)

## B. Path correctness (5)

- [ ] Passthrough/remux considered before re-encode
- [ ] No upscaling anywhere
- [ ] Resolution dropped only after bitrate targeting was insufficient
- [ ] Frame rate kept at source unless destination requires otherwise
- [ ] Separate outputs per destination (no one-size-fits-all file)

## C. Encode quality (6)

- [ ] H.264 High profile + yuv420p + AAC for upload targets (or destination-specific codec)
- [ ] CRF used when headroom exists; two-pass when cap is tight
- [ ] Video bitrate above the quality floor for its resolution
- [ ] Audio bitrate appropriate (128k speech / 160-192k music)
- [ ] `-movflags +faststart` on web-bound MP4s
- [ ] Preset slow/medium (never ultrafast for delivery)

## D. Verification (6)

- [ ] Output probed and matches destination spec table
- [ ] File size under cap with margin (≥3%)
- [ ] Spot-played at start / middle / end
- [ ] A/V sync checked at the end of the file
- [ ] No color shift vs source (HDR handled)
- [ ] Test upload done when the destination allows drafts

## E. Delivery (5)

- [ ] Per-destination spec table filled (required vs delivered)
- [ ] Path and tradeoffs stated
- [ ] Exact command/settings included
- [ ] Blocked items routed (cutter / resizer) instead of silently handled
- [ ] One-line delivery note present

## Red lines (any hit = do not deliver)

- Output was re-encoded from an already-compressed prior output
- Upscaled video
- VFR source re-encoded without CFR and not checked for drift
- No probe of the output file
