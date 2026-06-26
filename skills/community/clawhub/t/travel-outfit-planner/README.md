# Capsule Wardrobe Generator

Generate travel capsule-wardrobe plans with outfit formulas, packing lists, layering strategy, and a visual lookbook HTML.

## Features

- **Capsule wardrobe planning**: Minimize items, maximize outfits across multi-destination trips
- **Daily outfit calendar**: Day-by-day outfit formulas with weather tips
- **Color coordination**: Cohesive palette with mix-and-match formulas
- **Visual lookbook**: Auto-generated HTML with scene photos (via Pexels API), color swatches, and Xiaohongshu search links
- **Packing checklist**: Deduplicated list with luggage strategy
- **Travel reminders**: Etiquette, safety, weather, and shopping tips

## Installation

```bash
clawhub install <username>/travel-outfit-planner
```

Or manually copy the skill folder to `~/.claude/skills/travel-outfit-planner/`.

## Requirements

- **Python 3.8+** (for the lookbook HTML generator script)
- **Pexels API Key** (optional, free at [pexels.com](https://www.pexels.com/api/)) — enables real scene photos in the lookbook

## Usage

Ask your AI assistant about trip outfits:

- "我下周去日本7天，帮我规划穿搭"
- "京都+大阪5天旅行，女生，日系清新风格，怎么带衣服"
- "欧洲三国15天，情侣出行，跨气候穿搭方案"

The skill outputs:
1. A complete Markdown wardrobe plan (outfit formulas, packing list, daily calendar, travel tips)
2. An HTML visual lookbook (`wardrobe-lookbook.html`) with color swatches, scene photos, and search links

## File Structure

```
travel-outfit-planner/
├── SKILL.md                          # Skill definition (frontmatter + instructions)
├── README.md                         # This file
├── scripts/
│   └── fetch_lookbook_images.py      # Lookbook HTML generator (Python, stdlib only)
└── references/
    └── lookbook-guide.md             # JSON schema and module reference for the lookbook
```

## License

MIT-0 (MIT No Attribution)
