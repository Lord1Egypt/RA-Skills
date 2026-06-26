# Visual Note Card Generator

A custom skill for [Claude Code](https://docs.anthropic.com/en/docs/claude-code) and [OpenClaw](https://openclaw.ai/) that generates professional Chinese visual note cards (视觉笔记卡片/信息图) as single-page HTML infographics.

![Claude Code Skill](https://img.shields.io/badge/Claude_Code-Skill-blue)
![OpenClaw Compatible](https://img.shields.io/badge/OpenClaw-Compatible-purple)
![License](https://img.shields.io/badge/License-MIT-green)

## Overview

This skill turns any topic, article, or concept into a beautifully structured visual note card — a poster-style infographic optimized for social media sharing or printing. All output is a single self-contained HTML file with no external dependencies (except Google Fonts and html2canvas CDN).

### Features

- **Single HTML output** — no build tools, no frameworks, fully self-contained
- **Bilingual support** — Chinese body text with English display titles
- **Built-in export** — floating action button with PNG/JPEG export at multiple resolutions (1×, 1.5×, 2×)
- **Structured layout** — editorial knowledge card aesthetic with framework grid, dark/light panels, and highlight bar
- **Customizable palette** — default teal/orange theme with support for user-requested color schemes

### Example Output

![Demo](demo.png)

The card follows a fixed layout structure:

```
┌──────────────────────────────────────────┐
│ TOPIC LABEL              SOURCE LABEL    │  ← Top Bar
├────────────────────┬─────────────────────┤
│ English Title      │ Thesis statement    │  ← Title Area
│ 中文标题            │ with key insight    │
├─────┬─────┬─────┬──┴──────────────────────┤
│  M  │  P  │  D  │  G  │                  │  ← Framework Row (4 cards)
├─────┴─────┴─────┴─────┴──────────────────┤
│ ⚡ Dark Panel      │ ★ Light Panel        │  ← Two-Column Content
│ (narrative/story)  │ (numbered insights)  │
├──────────────────────────────────────────┤
│ Formula = M × P × D × G    Closing note  │  ← Highlight Bar
├──────────────────────────────────────────┤
│ FRAMEWORK LABEL              BRAND NAME   │  ← Footer
└──────────────────────────────────────────┘
```

## Installation

### Prerequisites

- [Claude Code](https://docs.anthropic.com/en/docs/claude-code) or [OpenClaw](https://openclaw.ai/) installed and configured

### Install

Clone this repository into your skills directory:

**Claude Code:**

```bash
git clone https://github.com/beilunyang/visual-note-card-skills.git ~/.claude/skills/visual-note-card
```

**OpenClaw:**

```bash
git clone https://github.com/beilunyang/visual-note-card-skills.git ~/.openclaw/skills/visual-note-card
```

Both tools will automatically detect the skill and use it when you ask for visual notes or knowledge cards.

### Uninstall

**Claude Code:**

```bash
rm -rf ~/.claude/skills/visual-note-card
```

**OpenClaw:**

```bash
rm -rf ~/.openclaw/skills/visual-note-card
```

## Usage

Simply ask Claude Code or OpenClaw to create a visual note card:

```
# Chinese prompts
帮我做一张关于 RAG 架构的视觉笔记
把这篇文章做成信息图
生成一张知识卡片，主题是微服务

# English prompts
Create a visual note about product-market fit
Make a knowledge card summarizing this article
```

### What triggers this skill

The skill activates when you mention:
- 视觉笔记 / 知识卡片 / 信息图 / 一页纸总结
- visual note / knowledge card / infographic / one-pager summary
- Any request to summarize content into a structured visual card format

## Project Structure

```
.
├── SKILL.md              # Skill definition and design system specification
├── assets/
│   └── template.html     # Canonical HTML/CSS reference template
├── LICENSE
├── CONTRIBUTING.md
└── README.md
```

## Customization

### Color Palette

The default palette uses CSS variables defined in the template:

| Variable | Default | Usage |
|----------|---------|-------|
| `--primary` | `#1a7a6d` (teal) | Headers, badges, accents |
| `--accent` | `#e8713a` (orange) | Emphasis, secondary badges |
| `--bg` | `#f0ebe4` (warm gray) | Page background |
| `--black` | `#1a1a1a` | Dark panel, primary text |

You can request alternate color schemes when generating cards. The skill will maintain the same structural contrast ratios with your chosen colors.

### Typography

- **English display**: Playfair Display (serif)
- **Chinese body**: Noto Sans SC
- **Monospace/labels**: JetBrains Mono

All fonts are loaded via Google Fonts CDN.

## Contributing

Contributions are welcome! Please read [CONTRIBUTING.md](CONTRIBUTING.md) for details.

## License

This project is licensed under the MIT License — see the [LICENSE](LICENSE) file for details.
