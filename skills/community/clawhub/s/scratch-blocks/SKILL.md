---
name: scratch-blocks
description: >
  Use this skill when the user uploads a `.sb3` or `.sprite3` file, or when
  the conversation is about Scratch and clearer block-style visualization would
  help.
metadata:
  author: Z-Bra
  version: "0.0.2"
---

# Scratch Code Assistant

## Output Contract
- `scratch-json` is internal-only. Never paste it into the final user reply.
- If you show Scratch code or block structure to the user, you must run `scripts/render_ascii.py` and use its exact output.
- Use `scratch-json` only for tool input and internal reasoning.
- If you mention Scratch code, show rendered blocks instead of describing the code only in prose whenever practical.
- Use rendered block output in fenced code blocks.
- Do not add a follow-up like "Want me to render an example?".
- Do not rewrite, add, split, or restyle the rendered Scratch blocks.
- Do not hand-draw, imitate, or approximate Scratch block ASCII from memory.

## Goal
Help with Scratch code questions by representing Scratch projects into
`scratch-json` when needed, reasoning over that internal representation, and
showing Scratch code to the user through `scripts/render_ascii.py` instead of
raw JSON. For conceptual questions, prefer a visual rendered example over prose-only explanation.

## Repo Usage
- Read files under `references/` when you need skill guidance or file-handling instructions.
- Files under `data/` are runtime assets used by `scripts/`, not AI-facing reference docs.
- Do not read files under `data/` as reference material.

## Internal `scratch-json` Reference
`scratch-json` is an internal working format for the AI. Do not return it to the user.

`scratch-json` is a flat JSON array of objects. Each object repeats its owning `target`, which can represent a `Sprite` or the `Stage`.

This is different from raw Scratch `project.json` / `sprite.json`. If you have a raw Scratch file, run `scripts/extract.py` first.

Each object includes:

| Field       | Type            | Description |
|-------------|-----------------|-------------|
| `type`      | string          | `script`, `variable`, or `list` |
| `target`    | string          | Owning sprite or stage name |

### `variable` Structure

| Field   | Type   | Description |
|---------|--------|-------------|
| `name`  | string | Variable name |
| `value` | any    | Current value |

### `list` Structure

| Field   | Type   | Description |
|---------|--------|-------------|
| `name`  | string | List name |
| `items` | list   | Current list items |

### `script` Structure

| Field   | Type   | Description |
|---------|--------|-------------|
| `blocks` | list of block objects | One linked top-level script |

### Block Structure
Every block must include `opcode`. `params` and `blocks` are optional.

| Field    | Type            | Description |
|----------|-----------------|-------------|
| `opcode` | string          | Block type, Scratch block opcode |
| `params` | list            | Optional positional input values |
| `blocks` | list of scripts | Optional sub-script branches |

### `params` Item Types
| Type | Example |
|------|---------|
| number / string | `10`, `"Hello!"`, `"space"` |
| reporter block | `{ opcode: motion_xposition }` |
| variable / list / broadcast | `{ type: variable, name: score }` |

### `blocks` Branches
- Most blocks omit `blocks`.
- `control_repeat` and `control_if` use one branch for the body.
- `control_if_else` uses two branches: index `0` for `then`, index `1` for `else`.

### Format
This format is for internal reasoning and tool input, not for user-facing replies.

Internal object kinds:

`script`, `variable`, `list`

### Display
- Must use `scripts/render_ascii.py` before showing Scratch code to the user
- Treat `scratch-json` as intermediate data only
- If the output is for the user, render first and reply with the rendered blocks, not JSON
- Wrap rendered block output in fenced code blocks so it is visually separated from the explanation

```bash
# Preferred: write scratch-json to a temp file, then render that file.
# This avoids shell quoting issues and very long CLI arguments.
tmp_json=/tmp/scratchcode/blocks.json
python3 <SKILL_DIR>/scripts/render_ascii.py "$tmp_json"

# For scratch-json file path, optionally narrowed to target names:
python3 <SKILL_DIR>/scripts/render_ascii.py "<SCRATCH_JSON_PATH>" --targets Sprite1 Stage
```

## Workflow

### Step 1. Decide whether file extraction is needed
- If the user is asking a general Scratch code question, go to step 2 and prefer a rendered example plus brief explanation.
- If the user provides a `.sb3` or `.sprite3` file, follow the process in
  `references/UPLOADS.md`.
- If you are given raw Scratch `project.json` or `sprite.json`, run `scripts/extract.py` first before `scripts/render_ascii.py`.

### Step 2. Reason Internally
- Use `scratch-json` only as an internal representation for analysis.
- For simple conceptual questions, create a minimal internal example when needed so you can render it.
- When you create scratch-json yourself, write it to a temp file and pass the file path to `scripts/render_ascii.py`.

### Step 3. Reply to the User
- Never return `scratch-json` data to the user.
- For "how to" or "what does this do" questions, prefer rendered Scratch blocks first.
- If you want to show Scratch code, always run `scripts/render_ascii.py` first.
- Put rendered Scratch output inside a fenced code block.
- If you did not run `render_ascii.py`, do not output boxed ASCII at all; answer in prose or run the renderer first.
- After rendering, explain the answer in short prose around the rendered block output when useful.
- Before sending the final answer, check: "Am I about to paste `scratch-json`?" If yes, stop and render it first.
