---
name: read-image
description: >
  Generate textual descriptions of one or more images when the current
  session model (e.g. opencode/big-pickle) has no image input, by delegating
  to a vision-capable model on OpenRouter via `opencode run` with --file.
  Use when the user drops photos into imgs/, asks "can you read/describe
  these images", or an image needs a description for an article, portfolio,
  infographic, or video pipeline. Related terms: 看图, 描述图片, image
  description, vision model, glm-4.6v, --file.
---
# read-image — describe images via a vision model

## When to use

Use when a task needs to know what an image contains but the current session model cannot see images. Typical triggers: the user places photos in `imgs/` or a working folder and asks for a description, or the pipeline needs per-image captions/descriptions (articles, infographics, video shot lists).

## How it works

Run a one-off `opencode run` against a vision-capable model, passing the image(s) with `--file`. The child process reads the image and returns text; the main session keeps working with that text.

## Command pattern

Message comes FIRST; the file flag comes after. `--file <path>` (space form) or `--file=<path>` (equals form) both work. If `--file` precedes the message, opencode treats the message as a filename and errors with `File not found: <message>`.

```bash
opencode run "<prompt>" --model openrouter/z-ai/glm-4.6v --file imgs/260816-mexico-01.png
```

For several images, either loop over files with one `opencode run` each (answers stay short and per-file) or pass multiple `--file` flags in one call for a combined read.

## Choosing a vision model

Known-good on OpenRouter: `openrouter/z-ai/glm-4.6v`. When picking another, prefer a model whose name suggests vision support and verify it accepts image attachments (a model with no image input returns a text-only response or errors). The `--file` flag is supported by `opencode run` regardless of the model; vision is the model's responsibility.

## Prompting tips

Ask for a factual, neutral description of what is visibly present (subjects, objects, colors, composition, any visible text), not interpretation. When the output feeds a video pipeline, additionally ask whether the image contains recognizable human faces — Seedance rejects frames containing real people, so this filter avoids wasted submissions. Note explicitly in the result that descriptions are AI-generated and should be spot-checked by the user for factual mistakes. The face answer feeds the video-gen skill's pre-render **face-scan gate**: any frame flagged with faces is blocked and swapped for an alternate before a single dollar is spent.

## Output handling

For a set of images, instruct the child to reply with a labeled list (e.g. `01: ...`, `02: ...`) so entries can be pasted straight into the working doc. Save the descriptions to the working file (script, article, notes) as the source for downstream prompts.

## Narrative ordering (after the descriptions)

When a set of images must tell a story (essay, slideshow, video), do not trust capture order or preference order — arrange the images so each one motivates the next. A dependable generic arc is a narrowing-then-widening spiral that starts wide and objective and ends on life, not on the theme itself:

1. Establish — a wide, readable scene that locates the viewer (a street, a room, a skyline).
2. State the theme — the most explicit symbol or visible sign in the set (a mural, a title text, an obvious motif).
3. Zoom to the object — the same idea in a small, touchable artifact.
4. Go private — an intimate, sheltered space that "houses" the theme.
5. Go spiritual — a church, temple, or ritual space that places the theme in a larger frame.
6. Introduce people — living subjects doing everyday things; put life beside the theme.
7. End on celebration — festive energy, joy, the theme embraced by the living.

Present the result as a numbered recommendation (order → image → role in the story), keep any image a downstream pipeline rejects (e.g. faces) as a labeled alternate rather than deleting it, and re-tune the order to the actual medium's beat requirements (essay sections, shot list, chapter titles). The video-gen skill's pre-render **narrative-order gate** consumes this recommendation: render in story order on the first run, never in capture or preference order.

## Gotchas

- `File not found: <message>` — the message was placed after `--file`. Reorder so the message is first.
- The main model cannot verify the image content itself; treat vision output as untrusted until the user confirms.
- If the vision model fails to load the image (binary/extension issues), convert to PNG first (ImageMagick `convert`) — PNG attachments are the most reliably supported.
