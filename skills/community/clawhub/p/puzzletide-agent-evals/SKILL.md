---
name: puzzletide-agent-evals
description: "Use this skill when the user wants verifiable reasoning tasks to benchmark or test an LLM or agent — reproducible puzzle task sets (sudoku, word search) with objective, by-construction grading. No answer key to trust: answers are verified against the rules and the grid."
version: 0.1.1
author: Caravaca Labs
homepage: https://github.com/Caravaca-Labs/puzzletide-cli/blob/main/docs/agent-skills.md#puzzletide-agent-evals
metadata:
  openclaw:
    tags: ["evals", "benchmarks", "testing", "puzzles", "puzzletide", "cli"]
    requires:
      anyBins: ["ptide", "puzzletide"]
    install:
      - kind: node
        package: puzzletide
        bins: ["ptide", "puzzletide"]
  hermes:
    tags: ["evals", "benchmarks", "testing", "puzzles", "puzzletide", "cli"]
    category: software-dev
    requires_toolsets: ["terminal"]
---

# PuzzleTide Agent Evals

Generate reproducible, objectively gradable puzzle tasks for testing models
and agents with the local PuzzleTide CLI.

Why puzzles: they are verifiable by construction. A sudoku answer either
satisfies the rules and preserves the givens or it doesn't; a word search
answer either spells the word along a straight line in the grid or it
doesn't. Grading needs no LLM judge and no trusted answer key.

Prefer the local CLI. Check availability in this order:

```bash
ptide --version
puzzletide --version
npx puzzletide --version
```

If none of those work, ask the user before installing (`npm install -g puzzletide`).

## Generate a task set

```bash
ptide eval generate --type sudoku --n 20 --difficulty hard --seed 1 --out tasks.json
ptide eval generate --type wordsearch --n 10 --difficulty medium --seed 1 --out tasks.json
```

The tuple (type, difficulty, n, seed) fully determines the task set, so it
names a reproducible benchmark — same command, same tasks, on any machine.

Each task has `id`, `instructions`, and the puzzle payload:
- sudoku: `puzzle` (81 chars, `.` = empty). Expected answer: completed 81-char string.
- wordsearch: `grid` (array of row strings) and `words`. Expected answer: JSON array
  of `{word, startRow, startCol, endRow, endCol}` (0-indexed).

## Run the subject model

Send each task's `instructions` + payload to the model under test and collect
answers as a JSON array of `{id, answer}`.

## Grade

```bash
ptide eval check --tasks tasks.json --answers answers.json --json
```

Returns per-task pass/fail with reasons and a summary score. Grading is
deterministic and local.

## Links

- Source and docs: [GitHub](https://github.com/Caravaca-Labs/puzzletide-cli) · [npm](https://www.npmjs.com/package/puzzletide) · [CLI reference](https://github.com/Caravaca-Labs/puzzletide-cli/blob/main/docs/cli.md)
- From the makers of [puzzletide.com](https://puzzletide.com) — free [word search](https://puzzletide.com/word-search), [crossword](https://puzzletide.com/crossword), and [sudoku](https://puzzletide.com/sudoku) puzzles

## Safety

- Everything runs locally; no account, API key, or network access.
- Do not install packages without asking the user first.
