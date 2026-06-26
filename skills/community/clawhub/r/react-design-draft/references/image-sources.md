# Image Sources (免费图库接入)

Free, commercially-licensed image sources for design draft backgrounds, hero images, and evidence photos.

## Three Built-In Libraries

### Pexels (pexels.com)
- **Strength**: Supports Chinese keyword search, broad coverage of everyday scenes
- **Best for**: General backgrounds, lifestyle, workplace, food, nature, city
- **License**: Free for commercial use, no attribution required
- **Search URL**: `https://www.pexels.com/search/{keyword}/`
- **API**: Free API key available at pexels.com/api
- **Usage**: Default choice for most content types

### Unsplash (unsplash.com)
- **Strength**: Highest photographic quality, artistic and editorial feel
- **Best for**: Portraits, lifestyle, space/architecture, abstract textures, moody atmospheres
- **License**: Free for commercial use (Unsplash License)
- **Search URL**: `https://unsplash.com/s/photos/{keyword}`
- **API**: Free API at unsplash.com/developers
- **Usage**: Preferred when Editorial Magazine mode is active — photo quality matches magazine aesthetic

### Wallhaven (wallhaven.cc)
- **Strength**: Game art, cinematic, wallpaper-grade imagery, sci-fi/fantasy
- **Best for**: Sci-fi, gaming, cinematic, abstract, dark/moody backgrounds
- **License**: Mixed — always check individual image license (CC-type varies)
- **Search URL**: `https://wallhaven.cc/search?q={keyword}&categories=111&purity=100`
- **API**: Free API at wallhaven.cc/help/api
- **Usage**: Best for Swiss mode dark backgrounds, sci-fi/tech content, game-related articles
- **⚠️ Warning**: License varies per image. Only use images marked as free for commercial use.

## Selection Rules

### Mode-Based Priority

| Mode | Primary Source | Secondary | Rationale |
|------|---------------|-----------|-----------|
| **Editorial Magazine** | Unsplash | Pexels | Unsplash's editorial quality matches magazine aesthetic |
| **Swiss International** | Pexels | Wallhaven | Pexels for clean product/data; Wallhaven for dark tech backgrounds |
| **Dark/Tech themes** | Wallhaven | Unsplash | Wallhaven excels at cinematic dark imagery |

### Content Type → Image Type Mapping

| Content Type | Image Role | Source Priority | Search Keywords |
|-------------|-----------|----------------|-----------------|
| Cover/Hero | Atmosphere + title background | Unsplash > Pexels | `{topic} abstract`, `{topic} minimal`, `dark texture` |
| Data chart | No image (CSS/SVG) | N/A | — |
| Quote card | Subtle texture background | Pexels | `paper texture`, `minimal background`, `gradient` |
| Comparison | Evidence photos | Pexels > Unsplash | `{subject} photo`, `{product} closeup` |
| Timeline | Minimal background | Pexels | `timeline bg`, `clean gradient` |
| Flow chart | No image (CSS/SVG) | N/A | — |
| Cases card | Product/person photos | Unsplash > Pexels | `{company} office`, `{person} portrait` |
| Myth-fact | Split-tone background | Pexels | `contrast`, `light dark split` |

### Image Quality Requirements

- **Minimum resolution**: 1600px wide (avoid blurriness on retina)
- **Format**: JPG for photos, PNG for transparent UI elements
- **Total size**: Keep under 5MB per illustration (affects load time)
- **Crop discipline**: Set `object-position` inline for every image based on subject location
- **No watermarks**: Reject any image with visible watermarks

### Search Strategy

1. **Start with English keywords** — all three libraries have better English indexing
2. **Add Chinese keywords** for Pexels (supports Chinese search)
3. **Use abstract terms** for backgrounds: `minimal dark`, `abstract gradient`, `paper texture`
4. **Use specific terms** for evidence photos: `rocket launch`, `satellite orbit`, `factory production line`
5. **Filter by orientation**: `landscape` for covers (21:9, 2.35:1), `portrait` for 3:4 cards, `square` for 1:1

### User Image Priority

**User's own images always take priority over stock libraries.**

When user provides images:
1. Use user's images first
2. Only supplement with stock images when user's images are insufficient
3. Never replace user's images with stock alternatives without asking

When user has no images:
1. Ask once: "需要配图吗？三种走法：A.你自己有照片/截图（推荐）B.我去图库帮你找 C.用纯CSS/SVG无图方案"
2. Accept whatever user picks
3. Do not re-prompt later

### Attribution

- Pexels/Unsplash: No attribution required, but recommended in image caption
- Wallhaven: Check individual license; add attribution when required
- User's images: Credit as "图片来源：用户提供"

## Screenshot Styling (截图美化)

For product reviews, tutorials, and technical content, screenshots are more useful than stock photos. Apply device-frame styling to make raw screenshots look like professional product imagery.

### Device Frame Components

| Frame Type | Use Case | CSS Approach |
|-----------|---------|-------------|
| **macOS window** | Desktop app screenshots | Top bar with traffic lights (●●●), title centered, rounded corners 8px |
| **iOS device** | Mobile app screenshots | Rounded rectangle with notch/dynamic island, home indicator bar |
| **Browser chrome** | Web app screenshots | Tab bar + address bar + bookmark bar, content area below |

### Material Backgrounds (材质背景)

Screenshots should NOT float on white. Place them on a textured background:

| Background | CSS | Best For |
|-----------|-----|----------|
| **格纸** | `background-image: linear-gradient(#e8e5de 1px, transparent 1px), linear-gradient(90deg, #e8e5de 1px, transparent 1px); background-size: 20px 20px;` | Editorial mode, tutorial cards |
| **点阵** | `background-image: radial-gradient(circle, #d4d4d2 1px, transparent 1px); background-size: 16px 16px;` | Swiss mode, tech product |
| **暖白** | `background: #f5f4ed;` | Both modes, minimal style |
| **深色** | `background: #1a1a1e;` | Swiss mode, dark theme pages |

### Shadow & Radius Rules

| Mode | Shadow | Border Radius |
|------|--------|--------------|
| **Editorial** | `0 4px 24px rgba(0,0,0,0.12)` | 8px (window), 16px (device) |
| **Swiss** | `0 2px 12px rgba(0,0,0,0.08)` | 4px (window), 12px (device) |

### Screenshot Priority

1. User-provided screenshots → apply device frame + material background
2. No screenshots available → use stock photos from Pexels/Unsplash
3. Neither available → use pure CSS/SVG layout (no image needed)
