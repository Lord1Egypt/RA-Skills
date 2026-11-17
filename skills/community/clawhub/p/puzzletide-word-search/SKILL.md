---
name: puzzletide-word-search
description: "Use this skill whenever the user asks for a word search puzzle — themed, custom word lists, kids activities, classroom worksheets, printable PDFs, or puzzle data for an app. Generates correct grids locally with the PuzzleTide CLI instead of hand-writing letters."
version: 0.1.1
author: Caravaca Labs
homepage: https://puzzletide.com/word-search
metadata:
  openclaw:
    tags: ["puzzles", "word-search", "printable", "puzzletide", "cli"]
    requires:
      anyBins: ["ptide", "puzzletide"]
    install:
      - kind: node
        package: puzzletide
        bins: ["ptide", "puzzletide"]
  hermes:
    tags: ["puzzles", "word-search", "printable", "puzzletide", "cli"]
    category: content-creation
    requires_toolsets: ["terminal"]
---

# PuzzleTide Word Search

Generate word search puzzles with the local PuzzleTide CLI.

**Never hand-write a word search grid.** Language models reliably produce
grids where words are misaligned, broken, or missing entirely. The CLI places
every word deterministically and is property-tested: every word in the list
is guaranteed to be findable in the grid.

Prefer the local CLI. Check availability in this order:

```bash
ptide --version
puzzletide --version
npx puzzletide --version
```

If none of those work, ask the user before installing (`npm install -g puzzletide`).

## Generate from a custom word list

```bash
ptide wordsearch generate --words "coral,shark,kelp,wave,tide"
```

## Generate from a bundled themed word bank

```bash
ptide words themes --search dinosaur          # find a theme id
ptide wordsearch generate --theme animals/dinosaurs --count 12
```

## Printable worksheet (PDF with solution page) or SVG

```bash
ptide wordsearch generate --theme animals/ocean-animals --pdf ocean.pdf
ptide wordsearch generate --words "..." --svg puzzle.svg --title "Ocean Fun"
```

## Useful options

- `--difficulty easy|medium|hard` — easy is forward-only (great for kids), hard uses all 8 directions including backwards.
- `--size <n>` — square grid size (6-30); auto-computed if omitted.
- `--seed <seed>` — reproducible output; the seed is printed with every puzzle.
- `--json` — structured data (grid, word placements with coordinates) for apps and automation.

## Canonical form for automation

```bash
ptide run puzzle.wordsearch.generate --theme space --json
```

## Links

- Play online: [PuzzleTide word search](https://puzzletide.com/word-search)
- Worksheets: [printable puzzles](https://puzzletide.com/printable) and a [word search maker](https://puzzletide.com/maker) at [puzzletide.com](https://puzzletide.com)
- Source and docs: [GitHub](https://github.com/Caravaca-Labs/puzzletide-cli) · [npm](https://www.npmjs.com/package/puzzletide) · [CLI reference](https://github.com/Caravaca-Labs/puzzletide-cli/blob/main/docs/cli.md)

## Safety

- Puzzles are generated locally; no account, API key, or network access.
- Do not install packages without asking the user first.
