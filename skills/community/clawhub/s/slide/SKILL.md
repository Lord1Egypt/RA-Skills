---
name: slide
version: "1.0.0"
description: "Create and manage presentation slides using JSONL storage. Use when building slide decks, applying themes, or exporting to HTML presentations."
author: BytesAgain
homepage: https://bytesagain.com
source: https://github.com/bytesagain/ai-skills
tags: [slide, presentation, deck, html, export]
---

# Slide — Presentation Slide Builder

Create, edit, and manage presentation slide decks stored in a local JSONL backend. Supports themes, templates, speaker notes, reordering, outlining, and HTML export.

## Prerequisites

- Python 3.8+
- `bash` shell
- No external dependencies required

## Data Storage

All slide data is stored in `~/.slide/data.jsonl`. Each line is a JSON object representing either a deck or an individual slide. The tool auto-creates the directory and file on first use.

## Commands

| Command   | Description                                              | Usage                                                       |
|-----------|----------------------------------------------------------|-------------------------------------------------------------|
| create    | Create a new slide deck with a title                     | `create TITLE [--author AUTHOR] [--description DESC]`       |
| add       | Add a new slide to an existing deck                      | `add DECK_ID --title TITLE [--content TEXT] [--layout TYPE]`|
| edit      | Edit a slide's title, content, or layout                 | `edit SLIDE_ID [--title T] [--content C] [--layout L]`      |
| reorder   | Move a slide to a new position within its deck           | `reorder SLIDE_ID --position N`                             |
| theme     | Apply or view a theme for a deck                         | `theme DECK_ID [--set THEME_NAME] [--list]`                 |
| outline   | Show a text outline of all slides in a deck              | `outline DECK_ID`                                           |
| export    | Export a deck to HTML or JSON                            | `export DECK_ID [--format html\|json] [--output FILE]`      |
| preview   | Generate a quick text preview of a slide                 | `preview SLIDE_ID`                                          |
| list      | List all decks or slides within a deck                   | `list [--deck DECK_ID] [--limit N]`                         |
| template  | List built-in templates or apply one to a new deck       | `template [--apply NAME] [--list]`                          |
| notes     | Add or view speaker notes for a slide                    | `notes SLIDE_ID [--set TEXT]`                               |
| help      | Show usage information                                   | `help`                                                      |
| version   | Show version number                                      | `version`                                                   |

## Examples

```bash
# Create a new deck
bash scripts/script.sh create "Quarterly Review" --author "Kelly"

# Add a title slide
bash scripts/script.sh add deck_abc --title "Welcome" --content "Q1 2026 Results" --layout title

# Edit slide content
bash scripts/script.sh edit slide_xyz --content "Updated revenue figures"

# Reorder a slide to position 3
bash scripts/script.sh reorder slide_xyz --position 3

# Apply a theme
bash scripts/script.sh theme deck_abc --set dark

# Show outline
bash scripts/script.sh outline deck_abc

# Add speaker notes
bash scripts/script.sh notes slide_xyz --set "Mention customer growth"

# Export deck to HTML
bash scripts/script.sh export deck_abc --format html --output presentation.html

# List available templates
bash scripts/script.sh template --list
```

## Output Format

All commands output structured JSON to stdout. The `export --format html` command outputs a self-contained HTML file with embedded CSS and JavaScript for presentation mode.

## Slide Layouts

Built-in layout types: `title`, `content`, `two-column`, `image`, `blank`, `section-header`.

## Themes

Built-in themes: `default`, `dark`, `light`, `corporate`, `creative`, `minimal`.

## Templates

Built-in templates: `blank`, `pitch-deck`, `quarterly-review`, `project-proposal`, `workshop`.

## Notes

- Deck IDs are prefixed with `deck_` and slide IDs with `slide_`.
- Slides maintain an `order` field for sequencing within a deck.
- The HTML export includes keyboard navigation (arrow keys) and fullscreen mode.

---

Powered by BytesAgain | bytesagain.com | hello@bytesagain.com
