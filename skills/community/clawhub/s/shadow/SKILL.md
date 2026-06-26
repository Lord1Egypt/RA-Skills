---
name: shadow
version: "1.0.0"
description: "Generate and preview CSS shadow effects using CLI tools. Use when you need box-shadow, text-shadow, drop-shadow, layered shadows, presets, animations,"
author: BytesAgain
homepage: https://bytesagain.com
source: https://github.com/bytesagain/ai-skills
tags:
  - css
  - shadow
  - design
  - frontend
  - generator
---

# Shadow — CSS Shadow Effect Generator

A powerful CLI tool for generating, previewing, and managing CSS shadow effects. Supports box-shadow, text-shadow, drop-shadow, inset shadows, multi-layer effects, presets, random generation, animation keyframes, and export to CSS/JSON.

## Prerequisites

- Python 3.8+
- Bash shell

## Data Storage

All saved shadow presets and configurations are persisted in `~/.shadow/data.jsonl`. Each line is a JSON object representing a shadow definition with its parameters.

## Commands

Run all commands via the script at `scripts/script.sh`.

### `box`
Generate a CSS box-shadow value.
```bash
bash scripts/script.sh box [--x 0] [--y 4] [--blur 8] [--spread 0] [--color "rgba(0,0,0,0.2)"] [--name my-shadow] [--save]
```

### `text`
Generate a CSS text-shadow value.
```bash
bash scripts/script.sh text [--x 1] [--y 1] [--blur 2] [--color "#333"] [--name heading-shadow] [--save]
```

### `drop`
Generate a CSS drop-shadow filter value.
```bash
bash scripts/script.sh drop [--x 0] [--y 4] [--blur 8] [--color "rgba(0,0,0,0.3)"] [--name drop1] [--save]
```

### `inset`
Generate an inset box-shadow value.
```bash
bash scripts/script.sh inset [--x 0] [--y 2] [--blur 4] [--spread 0] [--color "rgba(0,0,0,0.1)"] [--name inner] [--save]
```

### `layer`
Combine multiple shadows into a layered effect.
```bash
bash scripts/script.sh layer <shadow_name1> <shadow_name2> [shadow_name3...] [--name layered] [--save]
```

### `preset`
List or apply built-in shadow presets (material, neumorphism, flat, elevated, etc.).
```bash
bash scripts/script.sh preset [list|apply] [--name material-1] [--save]
```

### `random`
Generate a random shadow effect with optional constraints.
```bash
bash scripts/script.sh random [--type box|text|drop] [--layers 1-3] [--save] [--name random1]
```

### `animate`
Generate CSS animation keyframes for shadow transitions.
```bash
bash scripts/script.sh animate <shadow_name_from> <shadow_name_to> [--duration 0.3s] [--name hover-effect]
```

### `export`
Export saved shadows to CSS, JSON, or SCSS format.
```bash
bash scripts/script.sh export [--format css|json|scss] [--name specific-shadow] [--all]
```

### `preview`
Preview a shadow as ASCII art or generate an HTML preview file.
```bash
bash scripts/script.sh preview <shadow_name> [--html] [--output preview.html]
```

### `help`
Show usage information and available commands.
```bash
bash scripts/script.sh help
```

### `version`
Show the current version of the shadow tool.
```bash
bash scripts/script.sh version
```

## Workflow Example

```bash
# Generate a box shadow
bash scripts/script.sh box --x 0 --y 4 --blur 12 --color "rgba(0,0,0,0.15)" --name card --save

# Generate an inset shadow
bash scripts/script.sh inset --x 0 --y 2 --blur 4 --color "rgba(0,0,0,0.08)" --name inner --save

# Layer them
bash scripts/script.sh layer card inner --name card-combo --save

# Preview
bash scripts/script.sh preview card-combo --html --output card-preview.html

# Export all as CSS
bash scripts/script.sh export --format css --all
```

## Built-in Presets

- **material-1** through **material-5**: Google Material Design elevation shadows
- **neumorphism**: Soft UI neumorphic effect
- **flat**: Minimal flat shadow
- **elevated**: Strong elevation effect
- **glow**: Colored glow effect

## Notes

- All shadows are saved locally for reuse and composition.
- Export supports CSS custom properties format for design systems.
- Animation keyframes work with any saved shadow pair.

---

Powered by BytesAgain | bytesagain.com | hello@bytesagain.com
