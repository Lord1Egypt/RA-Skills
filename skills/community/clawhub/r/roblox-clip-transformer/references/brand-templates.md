# Brand Templates

Template specifications for game logos, watermarks, call-to-actions, and title cards.

## Title Cards

### Opening Title Card

For game trailers and promotional clips.

```
┌─────────────────────────┐
│                         │
│      [GAME LOGO]        │
│                         │
│    [GAME TITLE]         │
│    [TAGLINE]            │
│                         │
│   ⚡ ROBLOX ⚡          │
│                         │
└─────────────────────────┘
```

**Specifications:**
- Duration: 2-3 seconds
- Animation: Fade in + slight zoom
- Font: Bold, sans-serif (32-48pt for title)
- Background: Game screenshot (blurred) or solid color
- Logo: PNG with transparency, centered

**FFmpeg Command:**
```bash
ffmpeg -loop 1 -i title_image.png -c:v libx264 -t 3 -pix_fmt yuv420p title_card.mp4
```

### End Card Template

```
┌─────────────────────────┐
│                         │
│   [GAME LOGO]           │
│                         │
│   PLAY NOW!            │
│   🔗 [GAME LINK]        │
│                         │
│   @CreatorName         │
│   👍 Like & Subscribe  │
│                         │
└─────────────────────────┘
```

**Specifications:**
- Duration: 3-5 seconds
- CTA: Large, prominent
- Link: Use game URL or shortened link
- Social: Creator handles

---

## Watermarks & Overlays

### Corner Watermark (Logo)

**Position Options:**
- Top-left: game logo thumbnail
- Top-right: creator logo
- Bottom-right: platform link

**Size:** 150x150px (scale 10-15% of video width)

**FFmpeg Overlay:**
```bash
ffmpeg -i video.mp4 -i logo.png \
  -filter_complex "overlay=W-w-20:H-h-20" \
  output.mp4
```

**Positions:**
- Top-left: `overlay=20:20`
- Top-right: `overlay=W-w-20:20`
- Bottom-left: `overlay=20:H-h-20`
- Bottom-right: `overlay=W-w-20:H-h-20`

### Animated Watermark

Pulse animation for attention:
```bash
ffmpeg -i video.mp4 -i logo.png \
  -filter_complex "overlay=W-w-20:H-h-20:enable='between(t,0,2)+between(t,58,60)'" \
  output.mp4
```

---

## Call-to-Action (CTA) Overlays

### Text CTAs

**Font Recommendations:**
- Family: Montserrat, Roboto, or Open Sans
- Weight: Bold
- Size: 36-48pt (main), 24-32pt (secondary)
- Color: White with dark outline/shadow

**FFmpeg Drawtext:**
```bash
ffmpeg -i video.mp4 -vf \
  "drawtext=text='PLAY NOW':fontfile=/path/to/font.ttf:fontsize=48:fontcolor=white:x=(w-text_w)/2:y=h*0.85:shadowcolor=black:shadowx=2:shadowy=2" \
  output.mp4
```

### Button CTAs

Graphical button overlay:
- Background: Rounded rectangle (brand color)
- Text: White, centered
- Size: 300x80px
- Position: Bottom center

---

## Game Link Overlays

For showing the game URL:

```
🎮 Play: roblox.com/games/[GAME_ID]
```

**Styles:**
- Minimal: Text below logo
- Card: Box with background
- Animated: Typewriter effect

**Typewriter Animation:**
```bash
ffmpeg -i video.mp4 -vf \
  "drawtext=textfile=game_link.txt:fontfile=/path/to/font.ttf:fontsize=32:fontcolor=white:x=(w-text_w)/2:y=h*0.9:enable='gt(t,30)'" \
  output.mp4
```

---

## Lower Thirds

For creator information or game details:

```
┌────────────────────────┐
│ [Avatar] Creator Name   │
│          @Handle       │
└────────────────────────┘
```

**Specifications:**
- Background: Semi-transparent dark (rgba(0,0,0,0.7))
- Position: Bottom-left
- Animation: Slide in from left
- Duration: Show 3-5 seconds

**FFmpeg Template:**
```bash
ffmpeg -i video.mp4 -i lower_third.png \
  -filter_complex "[0:v][1:v]overlay=0:H-h-100:enable='between(t,5,10)'" \
  output.mp4
```

---

## Progress Bar

Visual progress indicator for longer clips:

```
[████████░░░░░░░░░░] 40%
```

**FFmpeg Drawbox:**
```bash
ffmpeg -i video.mp4 -vf \
  "drawbox=x=0:y=h-10:w=iw*0.4:h=10:color=white:t=fill" \
  output.mp4
```

For dynamic (requires complex filter):
```bash
ffmpeg -i video.mp4 -vf \
  "drawbox=x=0:y=h-10:w='iw*t/60':h=10:color=white:t=fill" \
  output.mp4
```

---

## Roblox Brand Guidelines

### Official Roblox Elements

When using Roblox branding:

**Logo Usage:**
- Use official Roblox logo from press kit
- Minimum size: 80px height
- Clear space: Equal to logo height
- Never stretch or distort

**Colors:**
- Red: #E2231A (primary)
- Black: #000000
- White: #FFFFFF

**Typography:**
- Headlines: Gibson Bold
- Body: Gibson Regular

### Game-Specific Branding

**Best Practices:**
1. Use game icon/thumbnail as logo
2. Match game's color palette
3. Include game name prominently
4. Add Roblox attribution (small, bottom)

---

## Template Files

Create these asset files in `assets/`:

```
assets/
├── fonts/
│   ├── Gibson-Bold.ttf
│   ├── Gibson-Regular.ttf
│   └── Montserrat-Bold.ttf
├── overlays/
│   ├── lower_third.png      # Transparent PNG, bottom-left info card
│   ├── cta_button.png       # Rounded rectangle with gradient
│   └── progress_bar.png     # Progress indicator template
├── music/
│   ├── upbeat_120bpm.mp3    # Royalty-free background
│   ├── chill_90bpm.mp3     # Calm background
│   └── epic_140bpm.mp3     # Action/trailer music
└── brand/
    ├── roblox_logo.png      # Official Roblox logo
    └── game_logo_template.png  # Placeholder for game logo
```

---

## Quick Start Template

```bash
# Create title card
ffmpeg -loop 1 -i assets/brand/game_logo.png -c:v libx264 -t 3 title.mp4

# Create end card  
ffmpeg -loop 1 -i assets/brand/end_card.png -c:v libx264 -t 5 end.mp4

# Combine: Title + Gameplay + End
ffmpeg -i title.mp4 -i gameplay.mp4 -i end.mp4 \
  -filter_complex "[0:v][1:v][2:v]concat=n=3:v=1:a=0" \
  output.mp4

# Add watermark
ffmpeg -i output.mp4 -i assets/overlays/watermark.png \
  -filter_complex "overlay=W-w-20:H-h-20" \
  final.mp4
```

---

## Design Tips

1. **Keep it simple** - Don't overload with overlays
2. **Be consistent** - Use same fonts/colors across videos
3. **Leave space** - Account for platform UI (buttons, usernames)
4. **Test on mobile** - View on actual phone before publishing
5. **Match game aesthetic** - Use game's colors and style