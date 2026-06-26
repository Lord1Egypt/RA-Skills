---
name: timeline-chart
description: "Professional timeline chart generator with Chinese/number support and dynamic layout"
---

# Timeline Chart Generator

Professional timeline chart generator for project milestones, historical events, and process flows.

## Features

- Auto-parse timeline event data
- Smart layout for time nodes and event cards
- Full Chinese, number, and punctuation support
- Dynamic card height to avoid text overflow
- Professional business-style design
- Color-coded node types

## Use Cases

- Project timeline display
- Historical event timeline
- Process evolution diagram
- Milestone showcase
- Decision flow chart

## Quick Start

```python
from template import create_timeline

events = [
    ('2024-01-01', 'Project Started', 'Start', None),
    ('2024-06-01', 'Milestone 1', 'M1', 'Team: 5 people'),
    ('2024-12-01', 'Project Completed', 'End', 'Success rate: 95%'),
]

create_timeline(events, 'output.png', 'Project Timeline')
```

## Technical Details

### Font Requirements

Install Chinese fonts:
```bash
apt-get install -y fonts-noto-cjk
fc-cache -fv
```

### Recommended Fonts

- **Noto Serif CJK SC**: Songti style, for formal business
- **Noto Sans CJK SC**: Heiti style, for modern tech
- **WenQuanYi Zen Hei**: Open-source Chinese font

### Color Scheme

- Primary Blue: `#1E40AF`
- Secondary Blue: `#3B82F6`
- Light Blue: `#DBEAFE`
- Success Green: `#059669`
- Warning Orange: `#D97706`

## Files

- `SKILL.md`: This documentation
- `template.py`: Complete code template
- `skill.json`: Skill metadata

## Requirements

- Python 3.7+
- Pillow >= 8.0.0
- fonts-noto-cjk

## License

MIT-0

## Author

制图创作引领大师 (Image Creation Master)

## Version History

### 1.0.0 (2026-05-06)
- First release
- Chinese and number display support
- Dynamic layout system
- Complete code template
