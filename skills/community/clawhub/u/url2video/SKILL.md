---
name: website-to-video
description: Convert any website into a promotional video using Remotion + React. Use when the user wants to generate a video from a website URL, create a promo video, make a brand video from a site, or asks for "website to video", "宣传视频", "promo video from URL", or mentions creating videos from websites. This skill handles scraping, content extraction, Remotion animation setup, TTS narration, free BGM, and VPS-optimized rendering.
---

# Website to Video Generator

Turn any website into a 60-second promotional video with animations, Chinese narration, subtitles, and free BGM.

## When to Use

- User provides a website URL and wants a video
- Creating brand/promotional videos from web content
- Need tech-style animated videos with narration
- Any request mentioning "网站生成视频", "promo video", "宣传视频", " Remotion video from URL"

## Workflow

### Step 1: Scrape Website Content

```bash
# Extract website content
python3 /root/.openclaw/workspace/scripts/smart_search.py "site:example.com" --max-results 5
```

Or use `web_fetch` tool to get the homepage content. Extract:
- Brand name
- Tagline / slogan
- Core services/products (3-5 items)
- Key statistics (users, projects, languages, etc.)
- Target audience
- CTA (call to action)

### Step 2: Extract Brand Colors

```bash
curl -sL https://example.com | grep -oE '(#[0-9a-fA-F]{3,8}|rgb\([^)]+\))' | sort | uniq -c | sort -rn | head -10
```

Identify:
- **Primary color**: Most frequent hex (CTA buttons, highlights)
- **Background color**: Dark theme usually `#1a1a2e` or `#0a0a0f`
- **Secondary/Accent**: Second most frequent
- **Text colors**: White `#fff` or light gray

### Step 3: Create Remotion Project

```bash
mkdir -p remotion-{brand}-promo/{src,audio,out}
cd remotion-{brand}-promo
npm init -y
npm install remotion @remotion/cli react react-dom
npm install -D typescript @types/react
```

Create files:
- `src/index.tsx` - Composition registration
- `src/{Brand}Promo.tsx` - Main video component
- `remotion.config.ts` - Config
- `audio/narration.txt` - Script for TTS

### Step 4: Write Narration Script

Create `audio/narration.txt` with 5 segments (12s each = 60s total):

```
Segment 1: [Brand] introduction + tagline
Segment 2: Vision / core value proposition  
Segment 3: Key services/products (3 items)
Segment 4: Trust signals / statistics
Segment 5: CTA + website URL
```

### Step 5: Generate TTS Audio

Use `tts` tool to generate Chinese narration for each segment. Then concatenate:

```bash
# If multiple TTS files
ffmpeg -i "concat:audio/part1.mp3|audio/part2.mp3|audio/part3.mp3|audio/part4.mp3|audio/part5.mp3" -acodec copy audio/narration.mp3
```

### Step 6: Download Free BGM

Get free tech-style background music from Pixabay:

```bash
cd audio
curl -L -o bgm.mp3 "https://cdn.pixabay.com/download/audio/2022/05/27/audio_1808fbf07a.mp3?filename=electronic-future-beats-117998.mp3" -H "User-Agent: Mozilla/5.0"
```

Volume: 0.15 (very subtle, don't overpower narration)

### Step 7: Build React Animation Component

Follow these **design rules**:

#### A. Safe Area Layout
```typescript
const SAFE_AREA = {
  subtitleHeight: 60,
  subtitleBottom: 8,
};
```
- Core content: `paddingBottom: 80` (stays above subtitle zone)
- Subtitle: `bottom: 8`, font-size `22px`
- Never let content overlap subtitle area

#### B. Subtitle Component
```typescript
const Subtitle = ({ text, active }: { text: string; active: boolean }) => {
  const frame = useCurrentFrame();
  const opacity = active
    ? interpolate(frame, [0, 8], [0, 1], { extrapolateLeft: 'clamp', extrapolateRight: 'clamp' })
    : interpolate(frame, [0, 8], [1, 0], { extrapolateLeft: 'clamp', extrapolateRight: 'clamp' });

  return (
    <div style={{
      position: 'absolute',
      bottom: 8,
      left: 0,
      right: 0,
      textAlign: 'center',
      opacity,
      zIndex: 100,
    }}>
      <div style={{
        display: 'inline-block',
        padding: '6px 20px',
        background: 'rgba(0,0,0,0.75)',
        backdropFilter: 'blur(8px)',
        borderRadius: 8,
        border: `1px solid ${COLORS.primary}25`,
      }}>
        <span style={{ fontSize: 22, color: COLORS.text }}>{text}</span>
      </div>
    </div>
  );
};
```

#### C. Use SVG Vector Icons (NOT emoji)

Create SVG icon components inline:
```typescript
const IconRocket = ({ size = 40, color = COLORS.primary }) => (
  <svg width={size} height={size} viewBox="0 0 24 24" fill="none" stroke={color} strokeWidth="2">
    <path d="M4.5 16.5c-1.5 1.26-2 5-2 5s3.74-.5 5-2c.71-.84.7-2.13-.09-2.91a2.18 2.18 0 0 0-2.91-.09z" />
    <path d="m12 15-3-3a22 22 0 0 1 2-3.95A12.88 12.88 0 0 1 22 2c0 2.72-.78 7.5-6 11a22.35 22.35 0 0 1-4 2z" />
  </svg>
);
```

**Required icons**: Eye, Rocket, Book, Target, Wrench, Palette, Monitor, Globe, Arrow

#### D. Decorative Shapes

Add rotating geometric decorations:
```typescript
const DecoShapes = () => {
  const frame = useCurrentFrame();
  return (
    <>
      <div style={{ position: 'absolute', top: '8%', left: '5%', opacity: 0.15, transform: `rotate(${frame * 0.3}deg)` }}>
        <svg width="60" height="60"><polygon points="30,5 55,17.5 55,42.5 30,55 5,42.5 5,17.5" fill="none" stroke={COLORS.primary} strokeWidth="1.5" /></svg>
      </div>
    </>
  );
};
```

#### E. Lightning Number Animation

Numbers must complete within 0.5 seconds (12 frames @ 24fps):
```typescript
const studentCount = Math.floor(interpolate(frame, [0, 12], [0, 1200], { extrapolateRight: 'clamp' }));
```

#### F. 5-Scene Structure

| Scene | Time | Content |
|-------|------|---------|
| 1 | 0-12s | Logo + brand + tagline |
| 2 | 12-24s | Vision (before → after comparison) |
| 3 | 24-36s | 3 core services with icons |
| 4 | 36-48s | Stats with lightning numbers + tags |
| 5 | 48-60s | CTA button + website URL |

Each scene: `durationInFrames={288}` (12s @ 24fps)
Total: `1440` frames = 60s

### Step 8: VPS-Optimized Rendering

**CRITICAL**: VPS has limited RAM. Use these settings:

```typescript
// src/index.tsx
<Composition
  id="promo"
  component={Promo}
  durationInFrames={1440}
  fps={24}
  width={854}
  height={480}
/>
```

Render command:
```bash
npx remotion render src/index.tsx promo out/video.mp4 --overwrite --concurrency=1
```

**Why these settings:**
- 854×480: Low-res but clear enough for mobile/social media
- 24fps: Smooth enough, saves 20% frames vs 30fps
- concurrency=1: Prevents OOM kills
- **Higher resolutions WILL fail** (1280×720 @ 30fps = SIGKILL at ~80%)

### Step 9: Generate Screenshots for Review

Before full render, generate keyframe screenshots:
```bash
npx remotion still src/index.tsx promo stills/scene1.png --frame=144
npx remotion still src/index.tsx promo stills/scene2.png --frame=432
npx remotion still src/index.tsx promo stills/scene3.png --frame=720
npx remotion still src/index.tsx promo stills/scene4.png --frame=1008
npx remotion still src/index.tsx promo stills/scene5.png --frame=1296
```

Send to user for approval before final render.

## Color Palette Template

```typescript
const COLORS = {
  background: '#1a1a2e',    // Extract from website or use dark
  primary: '#ff6b35',        // Website main CTA color
  secondary: '#2ec4b6',      // Accent color
  accent: '#ff6b35',
  text: '#ffffff',
  textMuted: '#999999',
  darkCard: 'rgba(255,255,255,0.06)',
};
```

## Key Constraints

1. **VPS Resource Limits**: 854×480 @ 24fps is the safe maximum
2. **Subtitle Safe Zone**: Bottom 12% of frame reserved for subtitles
3. **SVG Icons Only**: No emoji — use inline SVG components
4. **Brand Colors**: Extract from website, don't guess
5. **Free BGM**: Always use royalty-free music (Pixabay)
6. **Chinese Narration**: TTS for all segments, synchronized with subtitles
7. **5-Scene Structure**: Don't deviate — 12s × 5 = 60s

## Output

- `out/video.mp4` - Final video (~6MB for 60s)
- `stills/` - 5 keyframe screenshots for review
- Full Remotion project for future edits

## Troubleshooting

| Problem | Cause | Fix |
|---------|-------|-----|
| SIGKILL during render | OOM (memory) | Lower resolution/fps, use concurrency=1 |
| "setup-cache.js" error | Chrome headless issue | Re-run, or delete `node_modules/.cache` |
| Subtitle overlaps content | Content too low | Add `paddingBottom: 80` to content container |
| Emoji render as boxes | System font missing | Use inline SVG icons instead |
| BGM too loud | Volume too high | Set Audio volume={0.15} |
| TTS audio cut off | Duration mismatch | Extend segment or trim TTS |
