# Roblox Clip Transformer Assets

This directory contains reusable assets for video transformation.

## Directory Structure

```
assets/
├── music/           # Royalty-free background tracks
├── fonts/           # Typography for overlays
├── overlays/        # PNG templates (lower thirds, CTAs, watermarks)
└── brand/           # Brand assets (logos, colors)
```

## Adding Assets

### Music (`music/`)

Add royalty-free background music for videos:

- `upbeat_120bpm.mp3` - Fast-paced, energetic track
- `chill_90bpm.mp3` - Calm, background music
- `epic_140bpm.mp3` - Action/trailer style music
- `dramatic_100bpm.mp3` - Tension, suspense tracks

**Recommendations:**
- Use royalty-free sources (YouTube Audio Library, Free Music Archive)
- Match BPM to video style
- Keep tracks under 60 seconds for easy looping
- Prefer tracks with clear beat structure

### Fonts (`fonts/`)

Add fonts for text overlays:

- `Montserrat-Bold.ttf` - Headlines and titles
- `Montserrat-Regular.ttf` - Body text
- `Roboto-Bold.ttf` - Alternative headline font

**Recommendations:**
- Use web-safe fonts for compatibility
- Bold weights for readability on small screens
- Ensure commercial use license

### Overlays (`overlays/`)

Add PNG templates with transparency:

- `lower_third.png` - Info card for creator/game details
- `cta_button.png` - Call-to-action button background
- `watermark.png` - Small logo for corner
- `progress_bar.png` - Video progress indicator
- `end_card.png` - End screen template

**Specifications:**
- Use PNG with alpha channel
- Resolution: 1080x1920 for vertical overlays
- Keep file sizes under 500KB each

### Brand (`brand/`)

Add brand-specific assets:

- `game_logo.png` - Game thumbnail/icon (transparent PNG)
- `creator_logo.png` - Creator watermark
- `roblox_logo.png` - Official Roblox branding

**Roblox Guidelines:**
- Use official Roblox press kit for logos
- Minimum clear space: equal to logo height
- Never distort or modify official logos

## Default Assets

The skill includes placeholder paths. Add your own assets to:

1. Download royalty-free music to `assets/music/`
2. Add your game logo to `assets/brand/game_logo.png`
3. Create custom overlays in `assets/overlays/`

## Using Custom Assets

```bash
# Specify custom logo
roblox-transform input.mp4 -o output.mp4 -p tiktok --logo assets/brand/game_logo.png

# Use custom music
roblox-transform input.mp4 -o output.mp4 -p shorts --music assets/music/upbeat_120bpm.mp3
```

## Legal Notes

- Ensure all assets are properly licensed
- Use royalty-free music to avoid copyright issues
- Follow Roblox brand guidelines for official logos
- Credit sources when required