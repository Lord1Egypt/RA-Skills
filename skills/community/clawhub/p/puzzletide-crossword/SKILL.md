---
name: puzzletide-crossword
description: "Use this skill whenever the user asks for a crossword puzzle — custom word/clue lists, themed crosswords, educational worksheets, or printable PDFs. Generates valid interlocking grids with standard numbering locally with the PuzzleTide CLI instead of hand-drawing grids."
version: 0.1.1
author: Caravaca Labs
homepage: https://puzzletide.com/crossword
metadata:
  openclaw:
    tags: ["puzzles", "crossword", "printable", "puzzletide", "cli"]
    requires:
      anyBins: ["ptide", "puzzletide"]
    install:
      - kind: node
        package: puzzletide
        bins: ["ptide", "puzzletide"]
  hermes:
    tags: ["puzzles", "crossword", "printable", "puzzletide", "cli"]
    category: content-creation
    requires_toolsets: ["terminal"]
---

# PuzzleTide Crossword

Generate crossword puzzles with the local PuzzleTide CLI.

**Never hand-draw a crossword grid.** Language models cannot reliably keep
intersecting words consistent. The CLI places words with real intersections,
assigns standard crossword numbering, and validates that every clue's answer
matches the grid before returning — words that cannot interlock are reported
as unplaced instead of silently broken.

Prefer the local CLI. Check availability in this order:

```bash
ptide --version
puzzletide --version
npx puzzletide --version
```

If none of those work, ask the user before installing (`npm install -g puzzletide`).

## Generate with your own clues (best quality)

Write the clues yourself — you are good at clues; the CLI is good at grids:

```bash
ptide crossword generate --words "PARIS: Capital of France; TOKYO: Capital of Japan; OSLO: Capital of Norway"
```

For longer lists use a JSON file:

```bash
ptide crossword generate --file words.json --pdf crossword.pdf
# words.json: [{"word": "PARIS", "clue": "Capital of France"}, ...]
```

## Generate from a themed word bank

Clues are auto-generated puzzle-style hints (unscramble, letter counts):

```bash
ptide crossword generate --theme food/fruits --count 10
```

For better clues, pull the words and write clues yourself:

```bash
ptide words list food/fruits --count 10 --json
# ...then pass your own word:clue pairs to crossword generate.
```

## Printable and structured output

```bash
ptide crossword generate --file words.json --pdf crossword.pdf --title "Science Review"
ptide run puzzle.crossword.generate --theme animals --json
```

The PDF has three sections: empty numbered grid, clue list, and solution.
`--json` returns the grid ("#" = black cell) plus across/down clues with
coordinates — ready for rendering in an app.

## Links

- Play online: [PuzzleTide crossword](https://puzzletide.com/crossword)
- Worksheets: [printable puzzles](https://puzzletide.com/printable) at [puzzletide.com](https://puzzletide.com)
- Source and docs: [GitHub](https://github.com/Caravaca-Labs/puzzletide-cli) · [npm](https://www.npmjs.com/package/puzzletide) · [CLI reference](https://github.com/Caravaca-Labs/puzzletide-cli/blob/main/docs/cli.md)

## Safety

- Puzzles are generated locally; no account, API key, or network access.
- Do not install packages without asking the user first.
