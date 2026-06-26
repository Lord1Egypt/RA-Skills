# Travel Map Generator Skill

Generate beautiful, hand-drawn style travel itinerary maps in Studio Ghibli / Hayao Miyazaki aesthetic.

![Ghibli Style Travel Map](assets/example-tokyo-map.png)

## Features

- **Ghibli Watercolor Style**: Creates maps with warm, dreamy watercolor aesthetics
- **Cartoon POI Icons**: Generates cute illustrated icons for each attraction
- **Smart Route Planning**: Automatically optimizes visit order or uses your specified sequence
- **Real Coordinates**: Places icons at accurate geographic positions
- **Overlap Resolution**: Intelligently adjusts icon positions to prevent crowding

## Installation

### Quick Install (Auto-detect)

```bash
./install.sh
```

### Install for Specific Platform

```bash
# Claude Code
./install.sh --platform claude

# Cursor (project-level)
./install.sh --platform cursor

# Cursor (user-level)
./install.sh --platform cursor --user

# GitHub Copilot
./install.sh --platform copilot

# Windsurf
./install.sh --platform windsurf

# All detected platforms
./install.sh --all
```

### Manual Install

```bash
# Clone to your platform's skill directory

# Claude Code
git clone <repo-url> ~/.claude/skills/travel-map-generator-skill

# Cursor
git clone <repo-url> .cursor/rules/travel-map-generator-skill

# GitHub Copilot
git clone <repo-url> .github/skills/travel-map-generator-skill

# Universal (works with most platforms)
git clone <repo-url> ~/.agents/skills/travel-map-generator-skill
```

## Usage

Once installed, invoke the skill with:

```
/travel-map-generator Create a Ghibli-style map of Tokyo
```

Or naturally:

```
Make me a travel map for Paris with the Eiffel Tower and Louvre
Generate a cartoon itinerary map for my Rome trip
Draw a hand-drawn map of Kyoto
```

### Examples

**Basic city map:**
```
/travel-map-generator Create a map of Barcelona
```

**With specific attractions:**
```
/travel-map-generator Make a Tokyo map with Tokyo Tower, Senso-ji Temple, Shibuya Crossing, and Meiji Shrine
```

**With custom visit order:**
```
/travel-map-generator Create a Rome itinerary map - start at Colosseum, then Vatican, then Trevi Fountain
```

## How It Works

The skill follows a 7-phase workflow:

1. **Setup**: Parse user input, extract city and attractions
2. **POI Discovery**: Find top attractions if none specified
3. **Coordinate Collection**: Get lat/lng for each POI
4. **Map Generation**: Create Ghibli-style map background
5. **Icon Generation**: Generate cartoon icons for each POI
6. **Compositing**: Assemble final map with routes and labels
7. **Delivery**: Present the finished map

## Requirements

- Python 3.8+
- Pillow (auto-installed on first use)

## Project Structure

```
travel-map-generator-skill/
├── SKILL.md                    # Main skill definition
├── README.md                   # This file
├── install.sh                  # Cross-platform installer
├── assets/
│   └── ghibli_palette.json     # Color palette for stylization
├── scripts/
│   ├── install_deps.py         # Dependency installer
│   ├── utils.py                # Coordinate math & utilities
│   ├── stylize_map.py          # Map stylization
│   └── composite.py            # Final map assembly
└── references/
    └── coordinate-mapping.md   # Projection math details
```

## Scripts Reference

### install_deps.py
Installs required Python dependencies (Pillow).

```bash
python3 scripts/install_deps.py
```

### stylize_map.py
Transforms a Google Maps screenshot into Ghibli style.

```bash
python3 scripts/stylize_map.py \
  --input map_screenshot.png \
  --output stylized_map.png
```

### composite.py
Assembles the final travel map.

```bash
python3 scripts/composite.py \
  --map stylized_map.png \
  --config config.json \
  --output final_map.png
```

### utils.py
Shared utilities for coordinate projection, viewport calculation, and route optimization.

## Configuration Format

The compositing script expects a JSON config:

```json
{
  "city_name": "Tokyo",
  "viewport": {
    "center_lat": 35.6762,
    "center_lng": 139.6503,
    "zoom": 12,
    "width": 1536,
    "height": 1024
  },
  "pois": [
    {
      "name": "Tokyo Tower",
      "lat": 35.6586,
      "lng": 139.7454,
      "icon_path": "/tmp/travel-map-tokyo/poi_tokyo_tower.png",
      "order": 1
    }
  ]
}
```

## Customization

### Color Palette

Edit `assets/ghibli_palette.json` to customize colors:

```json
{
  "road": "#C4A882",
  "water": "#7EB8C9",
  "vegetation": "#8FB573",
  "building": "#F5E6D0",
  "background": "#FFF8E7"
}
```

### Icon Size

Icon size is automatically calculated based on the number of POIs, but you can modify `compute_icon_size()` in `scripts/utils.py`.

## Troubleshooting

| Issue | Solution |
|-------|----------|
| Pillow not found | Run `pip3 install Pillow` |
| Icons overlapping | The script auto-adjusts, but try reducing POI count |
| Poor map stylization | Use ImageGen for map background instead of screenshot |
| Wrong coordinates | Verify coordinates with Google Maps |

## License

MIT License - See LICENSE file for details.

## Contributing

Contributions welcome! Please ensure:
- Code follows existing style
- All scripts have proper error handling
- New features include documentation updates

## Credits

- Studio Ghibli for the inspiring art style
- Hayao Miyazaki for the aesthetic vision
