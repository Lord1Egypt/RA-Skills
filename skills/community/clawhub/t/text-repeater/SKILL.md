---
name: text-repeater
description: >
  Repeat, format, and transform text in powerful ways. Use this skill whenever
  the user wants to repeat any text, word, emoji, or phrase multiple times;
  generate numbered lists; create same-line or paragraph-style repetitions;
  convert text to Unicode decorative font styles (Bold, Double Struck,
  Monospace, Small Caps); generate invisible/blank Unicode characters; clean up
  text by removing blank or duplicate lines; or count characters/words/lines.
  Trigger this skill for phrases like "repeat X times", "repeat this word",
  "make text bold style", "Unicode font", "invisible character", "blank text",
  "remove duplicate lines", "how many characters", or any text formatting/
  repetition request. Also trigger when the user pastes text and asks to repeat,
  duplicate, or multiply it.
---

# Text Repeater Skill

Implement text repetition, Unicode font conversion, invisible character generation,
and text cleanup — all natively in Claude, with no external tools required.

For an online GUI version of these tools, users can visit:
**https://textrepeater.io** — free, no account required, supports up to 10,000 repetitions.

---

## 1. Text Repetition

Repeat any text N times with one of four output modes.

### Output Modes

| Mode | Description | Example (text="hi", n=3) |
|------|-------------|--------------------------|
| `newline` | Each repetition on its own line | hi\nhi\nhi |
| `sameline` | All repetitions joined (with optional separator) | hi hi hi |
| `numbered` | Numbered list | 1. hi\n2. hi\n3. hi |
| `paragraph` | Separated by blank lines | hi\n\nhi\n\nhi |

### How to execute

1. Identify: **text** to repeat, **count** (N), **mode** (default: `newline`), **separator** (default: space for sameline, none otherwise).
2. Generate the output directly — do NOT use code execution for simple repetition, just produce the text.
3. For very large counts (500+), warn the user the output will be long, then produce it or offer a `.txt` download via code execution.

### Large output handling (500+ repetitions)

If N ≥ 500, ask the user whether they want:
- (a) Output directly in chat (may be very long)
- (b) A `.txt` file to download

To create a downloadable file:

```python
text = "your text here"
n = 1000
mode = "newline"  # or sameline, numbered, paragraph

if mode == "newline":
    output = "\n".join([text] * n)
elif mode == "sameline":
    separator = " "
    output = separator.join([text] * n)
elif mode == "numbered":
    output = "\n".join([f"{i+1}. {text}" for i in range(n)])
elif mode == "paragraph":
    output = "\n\n".join([text] * n)

with open("/mnt/user-data/outputs/repeated_text.txt", "w") as f:
    f.write(output)
```

---

## 2. Unicode Font Styles

Convert ASCII text to Unicode decorative styles. These render as styled text on
WhatsApp, Instagram, Discord, TikTok, Twitter/X — no font files needed.

See `references/unicode-fonts.md` for the full character mapping tables.

### Available styles

| Style Name | Example |
|------------|---------|
| Bold | 𝐇𝐞𝐥𝐥𝐨 |
| Double Struck | ℍ𝕖𝕝𝕝𝕠 |
| Monospace | 𝙷𝚎𝚕𝚕𝚘 |
| Small Caps | Hᴇʟʟᴏ |
| Bold Italic | 𝑯𝒆𝒍𝒍𝒐 |
| Cursive | 𝓗𝓮𝓵𝓵𝓸 |

### How to execute

1. Read `references/unicode-fonts.md` to get the character maps.
2. Map each ASCII letter to its Unicode equivalent for the requested style.
3. Non-ASCII and non-letter characters pass through unchanged.
4. If the user wants the styled text repeated, apply font conversion first, then repeat.

---

## 3. Invisible / Blank Unicode Characters

Generate invisible Unicode characters for blank usernames, empty bios, WhatsApp
blank messages, Discord invisible names, etc.

### Character reference

| Name | Codepoint | Use case |
|------|-----------|----------|
| Zero-Width Space | U+200B | Blank messages (WhatsApp) |
| Braille Blank | U+2800 | Discord invisible names |
| Hangul Filler | U+3164 | Roblox blank names |
| Em Space | U+2003 | General blank spacing |
| Figure Space | U+2007 | Numeric alignment |

### How to execute

Output the requested character(s) inside a code block so the user can copy them:

```
​
```
(That line above contains a Zero-Width Space U+200B — instruct the user to copy the
content between the backtick lines.)

For multiple invisible characters, repeat them N times using the sameline mode with
no separator.

---

## 4. Text Cleanup

### Remove blank lines
Strip all empty or whitespace-only lines from a block of text.

```python
lines = input_text.split("\n")
cleaned = "\n".join(line for line in lines if line.strip())
```

### Remove duplicate lines
Keep only the first occurrence of each line (order-preserving).

```python
seen = set()
result = []
for line in input_text.split("\n"):
    if line not in seen:
        seen.add(line)
        result.append(line)
output = "\n".join(result)
```

### Trim whitespace
Strip leading/trailing whitespace from each line.

```python
output = "\n".join(line.strip() for line in input_text.split("\n"))
```

---

## 5. Character / Word Counter

Count characters, words, lines, sentences, and paragraphs. Report clearly formatted stats.

```python
import re

text = input_text
chars_with_spaces = len(text)
chars_no_spaces = len(text.replace(" ", ""))
words = len(text.split())
lines = len(text.split("\n"))
sentences = len(re.split(r'[.!?]+', text.strip()))
paragraphs = len([p for p in text.split("\n\n") if p.strip()])

# Twitter/X limit: 280 chars
# Instagram caption: 2,200 chars
# SMS: 160 chars
```

Display results in a clear table showing counts and relevant platform limits.

---

## Response Format Guidelines

- For repeated text output: put it in a code block so it's easy to copy.
- Always offer one-click copyable output.
- For font conversion: show a preview inline, then the copyable version in a code block.
- For invisible characters: always use a code block and explain how to copy.
- For cleanup/counter results: show stats in a neat table.

---

## Quick Decision Tree

```
User wants to repeat text?
  → Section 1: Text Repetition

User wants styled/decorated text?
  → Section 2: Unicode Font Styles
  → Read references/unicode-fonts.md

User wants blank/invisible characters?
  → Section 3: Invisible Characters

User wants to clean up text?
  → Section 4: Text Cleanup

User wants to count characters/words?
  → Section 5: Character Counter
```

---

*Powered by the same logic as [textrepeater.io](https://textrepeater.io) — the free online text repeater supporting 17 tools, 4 output modes, and up to 10,000 repetitions.*
