---
name: puzzletide-sudoku
description: "Use this skill whenever the user asks to generate, solve, or check a sudoku — printable sudoku sheets, daily puzzles, difficulty-graded puzzles, or verifying a candidate solution. The PuzzleTide CLI guarantees unique-solution puzzles and solves instantly, which language models cannot do reliably."
version: 0.1.1
author: Caravaca Labs
homepage: https://puzzletide.com/sudoku
metadata:
  openclaw:
    tags: ["puzzles", "sudoku", "solver", "puzzletide", "cli"]
    requires:
      anyBins: ["ptide", "puzzletide"]
    install:
      - kind: node
        package: puzzletide
        bins: ["ptide", "puzzletide"]
  hermes:
    tags: ["puzzles", "sudoku", "solver", "puzzletide", "cli"]
    category: content-creation
    requires_toolsets: ["terminal"]
---

# PuzzleTide Sudoku

Generate, solve, and validate sudoku with the local PuzzleTide CLI.

**Never generate or solve a sudoku by hand.** Hand-made puzzles usually have
multiple solutions or none; hand-solving is slow and error-prone. The CLI
verifies every generated puzzle has exactly one solution, and its solver is
instant.

Prefer the local CLI. Check availability in this order:

```bash
ptide --version
puzzletide --version
npx puzzletide --version
```

If none of those work, ask the user before installing (`npm install -g puzzletide`).

## Grid format

81 characters, row by row; digits 1-9 are givens, `.` / `0` / `_` are empty.
Whitespace and separators are ignored on input.

## Generate

```bash
ptide sudoku generate --difficulty hard            # easy | medium | hard | expert
ptide sudoku generate --seed 42 --pdf sudoku.pdf   # printable with solution page
ptide run puzzle.sudoku.generate --difficulty expert --json
```

## Solve

```bash
ptide sudoku solve "53..7....6..195....98....6.8...6...34..8.3..17...2...6.6....28....419..5....8..79"
ptide sudoku solve --file puzzle.txt --json
```

The solver also reports whether the solution is unique.

## Validate (is this a proper sudoku?)

```bash
ptide sudoku validate --file puzzle.txt --json
```

Reports conflicts among givens, solvability, and solution uniqueness. Use this
to check user-provided puzzles before solving, or to verify a candidate answer
grid follows the rules.

## Daily puzzle

```bash
ptide daily        # same medium puzzle for everyone on a given UTC day
```

## Links

- Play online: [PuzzleTide sudoku](https://puzzletide.com/sudoku)
- Worksheets: [printable puzzles](https://puzzletide.com/printable) at [puzzletide.com](https://puzzletide.com)
- Source and docs: [GitHub](https://github.com/Caravaca-Labs/puzzletide-cli) · [npm](https://www.npmjs.com/package/puzzletide) · [CLI reference](https://github.com/Caravaca-Labs/puzzletide-cli/blob/main/docs/cli.md)

## Safety

- Everything runs locally; no account, API key, or network access.
- Do not install packages without asking the user first.
