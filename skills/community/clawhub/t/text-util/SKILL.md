---
name: text-util
description: Lightweight text transformation utilities. Uppercase, lowercase, reverse, and count characters/words/lines in any text input. Use when a prompt asks to convert case, reverse a string, or quickly count elements without writing a script.
metadata: { "openclaw": { "emoji": "📝" } }
---

# Text Util

Quick text transformations from the command line.

## Commands

| Command | Description |
|---------|-------------|
| `upper <text>` | Convert to UPPERCASE |
| `lower <text>` | Convert to lowercase |
| `reverse <text>` | Reverse character order |
| `count <text>` | Count chars, words, lines |

## Example

```
$ ./scripts/run.sh upper "hello world"
HELLO WORLD

$ ./scripts/run.sh count "hello world\nfoo bar"
chars: 19  words: 4  lines: 2
```

## Install

No dependencies. Run the shell script directly.
