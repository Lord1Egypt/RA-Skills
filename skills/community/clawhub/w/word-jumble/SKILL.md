---
name: word-jumble
description: Generate a Word Jumble puzzle — scrambled words with circled letters that spell out a final idiom, plus a cartoon illustration hint and a printable puzzle image. Use when asked to generate a word jumble, create a daily puzzle, or schedule a jumble. Output is a puzzle JSON file, a cartoon image, and a printable 900×900px screenshot — posting/scheduling is the caller's responsibility. Note: uses the platform image_generate tool to create cartoon illustrations, which sends prompts to an external image generation API (whichever provider is configured).
---

# Word Jumble

Generates a complete Word Jumble puzzle: 4 scrambled words → circled letters → final idiom answer, with a cartoon hint image and a printable rendered screenshot.

**This skill does not post anywhere.** Posting is the caller's responsibility.

## Output

All output goes into an `output/` directory (create if needed, default: `~/.openclaw/workspace/word-jumbles/`):

- `output/YYYY-MM-DD-puzzle.json` — raw puzzle data
- `output/images/YYYY-MM-DD-cartoon.jpg` — tall cartoon hint image (9:16)
- `output/images/YYYY-MM-DD-printable.png` — rendered 1200×900 printable screenshot

## Puzzle Format

```typescript
type Puzzle = {
  scrambles: {
    scrambled: string[];      // shuffled letters
    unscrambled: string[];    // correct word, letter by letter
    circled: number[];        // 1-indexed positions in unscrambled
    clue_letters: string[];   // letters at those positions (must match)
    clue: string;             // wordplay clue, no answer giveaway
  }[];
  final_puzzle: {
    scrambled: string[];      // circled letters shuffled (spaces for word breaks)
    clue: string;             // clue for the idiom, no answer giveaway
    solution: string[];       // answer letters + spaces
    imageUrl: string;         // relative path to cartoon image
  };
}
```

## Validation Invariants (must all pass)

1. `sorted(scrambled) === sorted(unscrambled)` for every word
2. `clue_letters[i] === unscrambled[circled[i] - 1]` for all i (1-indexed)
3. `sorted(all clue_letters) === sorted(solution letters excluding spaces)`

**Always validate in code before proceeding.** Use `scripts/validate_puzzle.py`:

```bash
python3 scripts/validate_puzzle.py output/YYYY-MM-DD-puzzle.json
```

## Step-by-Step Process

### 1. Generate the puzzle JSON

Prompt the LLM (yourself) with this structure:

> Make a Word Jumble puzzle whose final answer is a common idiom. Use 4 words (8–10 letters each). Each word has 2–3 circled letters. Verify every circled position extracts the right letter. Verify circled letters anagram to the final answer. Format as JSON matching the Puzzle type.

Then **validate the output in code** using `validate_puzzle.py`. Regenerate if invalid — do not proceed with a broken puzzle.

### 2. Generate the cartoon image

Use `image_generate` with a 9:16 aspect ratio. The image must:
- Illustrate the idiom **literally and visually** (e.g. "bite the dust" → cowboy falling face-first)
- Be black and white, hand-drawn newspaper comic style
- Contain **no text, no labels, no words** that could give away the answer
- Be a strong visual hint — funny and evocative

Save to `output/images/YYYY-MM-DD-cartoon.jpg`.

### 3. Render the printable

Bake the puzzle JSON and cartoon path into `assets/puzzle-template.html`:
- Replace `__PUZZLE_JSON__` with the JSON string
- Replace `__CARTOON_IMAGE__` with the cartoon filename (relative, same directory when served)

Serve the HTML locally (localhost only):
```bash
cd <tmpdir containing html + cartoon> && python3 -m http.server 7891 --bind 127.0.0.1
```

Open `http://localhost:7891/puzzle.html` in the browser tool, resize viewport to **900×900**, screenshot (`fullPage: false`), save to `output/images/YYYY-MM-DD-printable.png`. (Layout is fluid — the body fills 100% width, so the viewport width controls the final puzzle width.)

Kill the server after screenshotting.

### 4. Return results

Hand back:
- Path to the printable PNG
- Path to the cartoon image
- The puzzle JSON (or path to it)

Do not post anywhere — the caller decides what to do with the output.

## Notes

- Pick fresh idioms each run — avoid repeating recent answers
- Clues should be clever wordplay, never a synonym of the answer
- The cartoon image should be funny and slightly absurdist — it's the soul of the puzzle
- If `image_generate` is unavailable, skip the cartoon and note it in output

## Security

- The local HTTP server binds to `127.0.0.1` only — not accessible from the network
- The answer key is printed in plain text, upside-down, in small print at the bottom of the page. This is intentional — it's a puzzle, not a secret. The answer being technically present in the DOM is fine: it's visually hidden by rotation, and the four scrambled clue words are not shown anywhere, so there's still plenty of solving to do.
- Image generation sends prompts to an external API — callers should be aware of this
