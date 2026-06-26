# @Stickers Bot — Step-by-Step Guide

## Static Sticker Pack

1. Open Telegram → search `@Stickers`
2. Send `/newpack`
3. Send a name for the pack (e.g. "Saints of LA")
4. Send the sticker PNG **as a Document** (not as a photo — Telegram compresses photos to JPEG, destroying transparency)
   - Mobile: tap 📎 → File → select PNG
   - Desktop: drag-and-drop OR use "Send as file" option
5. Send an emoji to associate with the sticker (e.g. 🔥)
6. Repeat steps 4–5 for each additional sticker
7. Send `/publish` when done
8. Bot gives you the pack link: `t.me/addstickers/<packname>`

**Cannot mix static and animated stickers in the same pack.**

---

## Animated / Video Sticker Pack (WebM)

1. Open Telegram → search `@Stickers`
2. Send `/newvideo` (this creates a video sticker pack — different from `/newpack`)
3. Send a name for the pack
4. Send the `.webm` file **as a Document**
5. When prompted, confirm "video stickers"
6. Send an emoji
7. Repeat for more stickers
8. Send `/publish`

---

## TGS (Lottie) Format — DO NOT ATTEMPT with raster art

TGS is Lottie vector animation, max 64KB compressed. It **cannot** embed raster PNG images (they're too large even after compression). TGS requires original layered vector artwork from After Effects or Illustrator.

**For NFT art / raster images → use WebM video stickers.** That's the right format.

---

## Telegram Requirements Summary

| Type | Format | Size | Resolution | Max Duration | Max File |
|------|--------|------|------------|-------------|---------|
| Static | PNG | transparent bg | 512×512 | — | 512 KB |
| Animated | WebM VP9 | transparent bg (yuva420p) | 512×512 | 3 seconds | 256 KB |

---

## Troubleshooting

- **Bot rejects the file** → check size limits; re-encode with lower bitrate (`-b:v 200k`)
- **Transparency missing** → confirm `-pix_fmt yuva420p` in ffmpeg command
- **Sticker looks blurry** → ensure source PNG is 512×512 before encoding
- **"Send as file" option missing** → on mobile, long-press the attach icon
