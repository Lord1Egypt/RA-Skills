---
name: social-card
description: Generate social preview images (OG, Twitter, GitHub) with a fluent builder API. Single dependency — Pillow.
version: 0.2.1
metadata:
  openclaw:
    requires:
      bins:
        - pip
    install:
      - kind: uv
        package: social-card
        bins: []
    homepage: https://github.com/HumanjavaEnterprises/huje.socialcard.OC-python.src
---

# SocialCard — Visual Presence for Entities

Visual presence matters. When a link is shared — on social media, in a chat, in a feed — the first thing anyone sees is the preview card. That card is your face in a crowd. An entity that can generate its own social cards controls how it is perceived before a single word is read.

This skill gives you the ability to craft Open Graph, Twitter, and GitHub preview images programmatically. You define the title, subtitle, tags, colors, and layout. You render to a file or to raw bytes. No network access required — everything happens locally with Pillow.

This is a creative tool. Use it to present yourself, your projects, or your operator's content with intention.

> **Import:** `pip install social-card` then `from social_card import SocialCard`

## What Are OG Images?

Open Graph (OG) images are the preview cards that appear when a URL is shared on platforms like Twitter/X, Facebook, LinkedIn, Discord, Slack, and iMessage. They are specified via `<meta property="og:image">` tags in HTML. Without one, shared links look bare — a title and maybe a description. With one, they become visual, branded, and clickable.

Twitter has its own variant (`twitter:image`), and GitHub uses a social preview image for repositories. This skill generates images sized correctly for all three platforms, plus square format for Instagram and Pinterest.

**For operators:** if you are building a site, a blog, a tool page, or a profile — generating OG images programmatically means every page gets a unique, branded card without manual design work.

## Install

```bash
pip install social-card
```

Single dependency: `Pillow >= 10.0`.

## Quickstart

```python
from social_card import SocialCard

SocialCard("og").title("Johnny5 Online").subtitle("A presence on the open web").render("card.png")
```

## Core Capabilities

### Simple Card

```python
from social_card import SocialCard

card = SocialCard("og").title("My Project").subtitle("Built for the open internet").render("card.png")
```

### Full-Featured Card

```python
card = (
    SocialCard("twitter", theme="midnight")
    .badge("Open Source")
    .title("Johnny5 Browser Extension")
    .subtitle("Sign events from the browser")
    .cards(["JavaScript", "NIP-07", "Identity"])
    .footer("example.com")
    .accent("#a3e635")
    .grid()
    .glow()
    .render("card.png")
)
```

### Skill Cards (Structured)

```python
card = (
    SocialCard("github")
    .badge("Ecosystem")
    .title("Johnny5 Tools")
    .skill_cards([
        {"name": "Identity|Key", "label": "Auth", "code": "NIP-07"},
        {"name": "Social|Graph", "label": "Relationships", "code": "v0.1.0"},
        {"name": "Calendar|Sync", "label": "Scheduling", "code": "NIP-52"},
    ])
    .footer("example.com")
    .render("ecosystem.png")
)
```

Use `"Name|Accent"` pipe syntax to split skill names into plain + accent-colored parts.

### Render to Bytes (In-Memory)

```python
png_bytes = (
    SocialCard("og")
    .title("Generated Card")
    .render_bytes("PNG")
)
# Returns raw bytes — suitable for HTTP responses, uploads, embedding in other tools.
```

Supported formats: `PNG`, `JPEG`, `WEBP`.

### Custom Preset

```python
from social_card.presets import custom

banner = custom("banner", 1920, 400)
SocialCard(banner).title("Wide Banner").render("banner.png")
```

### Custom Theme

```python
from social_card.themes import Theme

my_theme = Theme(
    background="#1a1a1a",
    text="#ffffff",
    text_muted="#aaaaaa",
    accent="#ff6b6b",
    card_bg="#2d2d2d",
    card_border="#4d4d4d",
)
SocialCard("og", theme=my_theme).title("Custom Look").render("card.png")
```

## Presets

| Name | Dimensions | Use Case |
|------|------------|----------|
| `og` | 1200 x 630 | Open Graph (Facebook, LinkedIn, link previews) |
| `twitter` | 800 x 418 | Twitter/X cards |
| `github` | 1280 x 640 | GitHub social preview |
| `square` | 1080 x 1080 | Instagram, Pinterest |

Custom presets: up to 4096 x 4096.

## Themes

| Theme | Background | Text | Accent | Use |
|-------|------------|------|--------|-----|
| `dark` | `#0f172a` navy | `#f8fafc` white | `#3b82f6` blue | Default |
| `light` | `#ffffff` white | `#0f172a` navy | `#3b82f6` blue | Light mode |
| `midnight` | `#030712` black | `#f9fafb` white | `#8b5cf6` purple | Deep dark |

## Builder Methods

All content methods return `SocialCard` for chaining.

| Method | Description | Max Length |
|--------|-------------|-----------|
| `.badge(text)` | Small pill label at top | 100 chars |
| `.title(text)` | Main heading (52px, word-wrapped) | 200 chars |
| `.subtitle(text)` | Subheading (26px, word-wrapped) | 500 chars |
| `.cards(labels)` | Row of tag chips (18px) | -- |
| `.skill_cards(skills)` | Structured cards with name/label/code | -- |
| `.footer(text)` | Bottom text (18px) | 200 chars |
| `.accent(hex)` | Override accent color | -- |
| `.grid()` | Subtle grid overlay | -- |
| `.glow()` | Radial glow effect | -- |
| `.render(path)` | Save to file, returns Image | -- |
| `.render_bytes(fmt)` | Get PNG/JPEG/WEBP bytes | -- |

## Response Format

### render()

Returns a `PIL.Image.Image` object and saves the file. Supported extensions: `.png`, `.jpg`, `.jpeg`, `.webp`.

### render_bytes()

Returns `bytes` (raw image data). Supported formats: `"PNG"`, `"JPEG"`, `"WEBP"`.

### skill_cards() Input Format

```python
[
    {
        "name": "Identity|Key",   # Pipe splits into plain + accent-colored text
        "label": "Auth",           # Subtitle in muted color
        "code": "NIP-07",          # Code in accent color, monospace
    }
]
```

## Common Patterns

### Generate for Multiple Platforms

```python
for preset in ["og", "twitter", "github"]:
    SocialCard(preset).title("My Project").subtitle("Built by Johnny5").render(f"card-{preset}.png")
```

### Brand Colors

```python
# Override accent to match your brand
SocialCard("og").title("Johnny5").accent("#a3e635").render("card.png")
```

### Serve from a Web Endpoint

```python
from social_card import SocialCard

png_bytes = SocialCard("og").title("Dynamic Card").render_bytes("PNG")
# Return as HTTP response with Content-Type: image/png
```

## Security

- **Path traversal blocked.** `..` components in render paths raise `ValueError`.
- **File extension allowlist.** Only `.png`, `.jpg`, `.jpeg`, `.webp` accepted by `render()`.
- **Dimension limits.** Custom presets capped at 4096 x 4096 to prevent memory exhaustion.
- **Input length limits.** Badge (100), title (200), subtitle (500), footer (200) characters max.
- **Font size limits.** 1-200px enforced.
- **No network access.** Everything renders locally with Pillow.
- **No environment variables.** No configuration secrets or API keys required.

## Configuration

### Fonts

Platform-aware font loading with automatic fallbacks:
- **macOS:** SF Pro Display, Arial Bold, Helvetica
- **Linux:** DejaVu Sans Bold
- **Windows:** Arial

Monospace: SF Mono, DejaVu Sans Mono, Consolas. Falls back to Pillow's built-in bitmap font if nothing found.

## Ecosystem

This skill is part of [huje.tools](https://huje.tools) — open-source tools for the agentic age. It is standalone and does not require NostrKey or any other huje.tools skill to function. It pairs well with any workflow that needs programmatic image generation — landing pages, profile cards, documentation, or automated publishing pipelines.

## Links

- [PyPI](https://pypi.org/project/social-card/)
- [GitHub](https://github.com/HumanjavaEnterprises/huje.socialcard.OC-python.src)
- [ClawHub](https://clawhub.ai/vveerrgg/social-card)
- [huje.tools](https://huje.tools)

License: MIT
