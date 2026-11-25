---
name: Screenshot to Code
description: Turn one UI screenshot into a React + Tailwind component that uses the project's design tokens, with a demo page and NOTES.md listing what could not be seen. Use when asked to rebuild a UI from an image, screenshot or mockup.
---

# Screenshot to Code (manual edition)

One screenshot -> one React + Tailwind component, in the project's tokens, with a demo
page and honest notes. Never a whole page, never invented copy.

This edition is the workflow and the checks. The paid edition adds seven tested scripts
that build the prompts, validate the model's JSON, write the files and enforce the
constraints automatically.

## Ask first (one round)

1. Path to the screenshot (required).
2. Design tokens: a `tokens.css` or `tailwind.config.*` (optional). If none, say
   "no tokens - neutral defaults" and continue.
3. Component name (optional; the vision pass suggests one).

Do not start without the screenshot path.

## Flow

Create `.tmp/` for intermediate files.

### 1. Vision pass - exactly one call

Send the image itself (attached, not just a path) to a vision model with this request:

- One component, not a page: a card, dialog, header, nav or form.
- Return **one JSON object**, nothing else, with:
  - `component`: a PascalCase name
  - `regions`: the visible blocks in order, each with a short label
  - `text`: every visible string, verbatim (`?` stays `?`)
  - `tokens`: which supplied tokens each color/space/font maps to, when obvious
  - `breakpoints`: only those actually visible or stated
  - `unknowns`: what the image cannot tell you (hover states, exact spacing, hidden
    text, focus styles, animation)
- No code in this reply. The spec is the source of truth for the next step.

If the JSON is malformed you may retry **once** with the parse error appended. The vision
budget is 3 calls per screenshot; beyond that, stop and ask for a clearer image.

### 2. Confirm the spec

Show the user a short summary: component name, regions, number of strings, unknowns. Do
not spend the code call until the spec makes sense.

### 3. Code pass - text only

Send the spec (and the token list) to a cheap coding model with these constraints:

- One React + TypeScript component, one default export.
- Tailwind classes; when tokens exist, use `var(--color-*)` or token classes, never the
  token's hex value.
- Copy the spec's strings verbatim. No invented copy, no lorem ipsum.
- No external images, web fonts or icon packages. Inline SVG for icons.
- No breakpoints unless the spec has them.
- Also return the demo page and the notes (see below).

Save the result as:

```
output/<Name>.tsx        the component
output/<Name>.demo.tsx   a demo that renders it with representative props
output/NOTES.md          the spec's unknowns, plus anything you noticed
```

The model's saved files are not the source of truth until they pass the checks below.

### 4. Checks (must pass)

Inspect the generated files and fix, do not excuse:

- exactly one component and one default export
- no `http://` or `https://` asset URLs; no `<img src="http...">`, no font/icon imports
- no hardcoded hex for colors that exist as tokens
- every visible string comes from the spec
- `NOTES.md` exists and lists the unknowns
- unused tokens are noted, not used to pad the code

### 5. Render proof

- Existing Vite/Next project: copy the two files in and run its build/typecheck.
- Otherwise scaffold a throwaway Vite + React + Tailwind sandbox and build it.
- If you cannot run a build, say so instead of claiming it renders.

## Hard rules

- **One component per screenshot.** Cards, dialogs, headers. Not a page, not a flow.
- **No invented text.** Use the spec's strings verbatim; `?` stays `?`.
- **No external images, fonts or icon packages.** Inline SVG is fine.
- **Tokens are law.** Use `var(--color-*)` / token classes; never the token's hex.
- **No breakpoints** unless the spec mentions them.
- **NOTES.md keeps the unknowns.** Add your own if you know more.
- Never claim pixel fidelity. This edition has no visual diff.

## Done when

- The checks above pass (or every failure is listed and explained).
- The demo renders in a sandbox or the user's app (or you state that you could not run one).
- `output/` contains `<Name>.tsx`, `<Name>.demo.tsx`, `NOTES.md`.
- Your summary states how many vision calls were used (normally 1) and what is unknown.
