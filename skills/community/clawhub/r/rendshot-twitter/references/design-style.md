# Twitter/X Visual Design Guide

## Design for Dark Mode

~80% of Twitter users use dark mode. Design accordingly:
- **Default dark background**: `#15202B` (Twitter dim) or `#000000` (lights out)
- **Avoid pure white backgrounds**: Jarring in dark mode feeds. Use off-white `#F7F9F9` if light is needed
- **High contrast text**: White `#E7E9EA` or near-white on dark backgrounds
- **Test both modes**: Preview your image on both dark and light backgrounds

## Style Categories

### 1. Tech / Developer — Best for: Product launches, dev content
- Dark background with code accent colors
- Monospace font for tech keywords
- Terminal/editor aesthetic
- Colors: Dark `#0D1117` + Green `#3FB950` + Blue `#58A6FF`

### 2. Business / Startup — Best for: Announcements, metrics
- Clean, professional, data-forward
- Company brand colors + navy/white
- Metric cards, stat callouts
- Colors: Navy `#1A2332` + White `#FFFFFF` + Accent from brand

### 3. Creator / Personal Brand — Best for: Threads, hot takes
- Bold, opinionated design
- Strong typography (one big statement)
- Minimal elements, maximum impact
- Colors: High contrast, 2 colors max

### 4. Data / Research — Best for: Charts, studies, insights
- Clean chart aesthetics
- Labeled data with source citation
- Muted palette with one highlight color
- Colors: Light gray `#F0F2F5` + Blue `#4A90D9` + Highlight `#FF6B6B`

### 5. Meme / Humor — Best for: Virality, brand personality
- Bold text, simple layout
- Pop culture references
- Bright colors or high-contrast B&W
- Colors: Whatever fits the joke

## Typography Rules

### Post Image (1200x675)
- **Title**: 48-72px, bold, max 6-8 words
- **Subtitle**: 28-36px, lighter weight
- **Text must read at ~400px width** (Twitter mobile preview)
- Font: Bold sans-serif (Inter, DM Sans, SF Pro, Geist)

### Link Card (1200x628)
- **Title**: 36-48px (smaller than post image — card has extra text below)
- **Site name**: 16-20px, subtle brand anchor
- Card appears with additional title + description from og:tags, so image text should complement, not duplicate

### Thread Header
- Include "Thread 🧵" or "1/N" indicator
- Title should hook (question, bold claim, number)
- Same typography as post image

## Layout Patterns

### Announcement / Launch
```
┌─────────────────────────┐
│  [Logo]    [Tag/Badge]  │
│                         │
│    HEADLINE TEXT         │
│    Supporting line       │
│                         │
│    [Visual / Screenshot] │
│                         │
└─────────────────────────┘
```

### Data / Stat
```
┌─────────────────────────┐
│                         │
│       BIG NUMBER        │
│       Context line      │
│                         │
│   ─── Chart/Graph ───   │
│                         │
│   Source: @handle        │
└─────────────────────────┘
```

### Thread Header
```
┌─────────────────────────┐
│  🧵 Thread              │
│                         │
│  HOOK TITLE             │
│  (compelling question)  │
│                         │
│          [1/12]         │
└─────────────────────────┘
```

## Design Anti-Patterns

1. **Text wall**: Too many words — nobody reads paragraphs in a tweet image
2. **Light backgrounds**: Look jarring in dark mode feeds
3. **Tiny text**: Must be readable at mobile preview size (~400px)
4. **Busy backgrounds**: Compete with text for attention
5. **Stock photo aesthetic**: Feels corporate and inauthentic on Twitter
6. **Too many colors**: 2-3 max. Twitter is a fast-scroll environment
