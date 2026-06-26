---
name: token-image
description: >
  Generate themed social/marketing image React components using design tokens.
  Produces TSX files that render to PNG.
  Use when the user asks to generate images, banners, cards, or social assets — e.g.
  "Build 4 blog banners for my React series", "Make a set of og-images", or
  "Generate 3 Twitter cards: Hooks, Context, Suspense".
---

# token-image

Generate a series of social/marketing image React components in the same theme.

## Vocabulary

| Term | What it is | Scope |
|------|-----------|-------|
| **Viewport** | Shared outer frame component. Safe-area padding, content alignment, root container, optional branding. Written once, reused by every image in the set. | Per set |
| **Stylesheet** | Shared CSS file. Starts from default-styles.css, adds preset-specific overrides. Styles all typography, cards, grids, and layout via token CSS vars. Written once, imported by every image. | Per set |
| **Brief** | Per-image content instructions written by the orchestrator. Includes exact text strings, layout description, creative direction, metadata. Writers implement the brief — they do not make content decisions. | Per image |
| **Layout** | Content arrangement description inside the Viewport. Written by the orchestrator per image (e.g., "split — title left, 2x2 cards right"). The shared agent creates CSS classes to support all layouts in the set. | Per image |

## Supporting Files

| File | Purpose | When to use |
|------|---------|-------------|
| `scripts/init.sh` | Bootstrap workspace (tokens, deps, `--preset <name>` or `--tokens <path>` required) | After intake: if `.token-image/` workspace missing |
| `assets/<preset>/tokens.json` | Token set for the chosen design system | Selected during intake; copied to `.token-image/tokens/` by init.sh |
| `assets/<preset>/design-guide.md` | Design principles and stylesheet overrides for the chosen token set | Read during intake after preset selection; injected into agent prompts |
| `.token-image/src/token.active.json` | Project's active token file | Read in full during intake; passed to every agent |
| `references/default-styles.css` | Base stylesheet with typography, card, grid, and layout styles | Read by shared-files agent in Phase 2 Step 2 |
| `references/viewports.md` | Viewport examples (2-3 variants) | Read by shared-files agent in Phase 2 Step 2 |
| `references/components.md` | Component snippets (Card, Grid, decoration patterns) | Read by Writer agents in Phase 2 Step 3 |
| `prompts/shared.md` | Shared files agent prompt (Viewport + Stylesheet) | Read by agent in Phase 2 Step 2 |
| `prompts/writer.md` | Writer agent prompt | Read by Writer agents in Phase 2 Step 3 |
| `prompts/reviewer.md` | Reviewer agent prompt | Read by Reviewer agents in Phase 2 Step 3 |

---

## Phase 0: Pre-flight

Announce: "I'm using the token-image skill."

Check for `.token-image/` workspace directory in the project root.
- If present: note that workspace exists. Read `.token-image/src/token.active.json` for reference.
- If missing: note that workspace needs initialization. Do NOT run init.sh yet — wait until Phase 1 when the user picks a preset.

Ensure Playwright browsers are installed:

```bash
npx playwright install chromium
```

This is idempotent — if already installed, it's a no-op.

---

## Phase 1: Intake

Before generating anything, ask the user these questions. Skip any that were already answered in the initial prompt.

1. **Theme** — Which token set should I use?
    - Available presets: {list all subdirectories in `<skill_base_dir>/assets/`}
    - Or paste a path to your own `tokens.json` (with optional `design-guide.md` alongside it). This will be passed as `--tokens <path>` to init.sh.

2. **Images** — What should each image be about, and how many?
   (e.g. "4 banners: Hooks, Context, Suspense, Server Components")

3. **Format** — Which image format?
   - `twitter-card` 1200×600
   - `instagram-square` 1080×1080
   - `og-image` 1200×630
   - `custom` — User specify width and height

4. **Layout** — Describe the layout for each image.
     What goes where? (e.g., "title top-left, 2x2 card grid on right",
     "full-canvas hero with oversized title", "numbered steps down the left side")
     You can describe one layout for all images or a different one per image.
     If you're not sure, say "auto" and I'll pick based on content.

5. **Branding** — What should be consistent across all images?
     (e.g., "logo bottom-right", "series label 'REACT SERIES · PART N' in footer",
     "no branding", "subtle watermark center-bottom")
     This becomes part of the shared Viewport that wraps every image.
     If none, say "none" and I'll keep the viewport clean.

Wait for the user's answers before proceeding. If the user says "auto" or leaves something blank, make a reasonable choice and state it.

After the user selects a preset or provides a custom token file:
- If workspace is missing, run init.sh:
  ```bash
  # For a built-in preset:
  bash <skill_base_dir>/scripts/init.sh --preset <chosen_preset>
  # For a custom token file:
  bash <skill_base_dir>/scripts/init.sh --tokens <path/to/tokens.json>
  ```
- If workspace exists but uses a different preset, copy the chosen preset's tokens to active:
  ```bash
  cp .token-image/tokens/<chosen_preset>/tokens.json .token-image/src/token.active.json
  ```
- For a built-in preset: read `<skill_base_dir>/assets/<preset>/tokens.json` into context as `{token_json}` and `<skill_base_dir>/assets/<preset>/design-guide.md` into context as `{design_guide}`
- For a custom token file: read the custom `tokens.json` and optionally `design-guide.md` if it exists alongside it

Once you have all answers, confirm the plan:
```
Got it. Here's what I'll generate:
- Format: {format} ({width}×{height})
- Theme: {token_file}
- Branding: {user's branding spec from Q5}
- Images:
  1. {title 1} — {subtitle 1}
    - Layout: {layout description 1}
  2. {title 2} — {subtitle 2}
    - Layout: {layout description 2}
  ...

I'll plan content, create shared Viewport + Stylesheet, then one component per image.
Proceed?
```

Only proceed after the user confirms.

---

## Phase 2: Generate

### Step 1: Content Planning

Do NOT delegate this step. The orchestrator (you) writes a content brief for every image in the set.

Based on the user's intake answers, produce two things:

**A. Shared element inventory** — decide what's shared across the whole set, informed by the user's branding answer (Q5):
- Viewport variant needed (hero for one image, standard for the rest)
- Branding and metadata placement from user's Q5 answer (logo position, series label, watermark, etc.)
- Any special alignment or spacing requirements
- Write this as a short list the shared-files agent will use.

**B. Per-image brief** — for each image, describe what goes inside the Viewport. Include:
- Exact text strings (title, subtitle, body, metadata)
- Layout description (what goes where)
- **Creative direction** — a specific aesthetic target for this image (position, scale, density, tension). This is what makes images feel distinct rather than generic.

Example output for a 4-image set:

```
SHARED:
- Viewport: hero variant (Image 1), standard variant centered (Images 2-4)
- Stylesheet: Nothing preset, no overrides needed
- Metadata format: "REACT SERIES · PART N" for all images, bottom
- No branding

  Image 1 — hero, full canvas:
    Layout: hero — oversized display title pushed to bottom-right, tagline below
    Creative direction: "Poster-style, 70% whitespace above, oversized display text, bottom-right anchored"

  Image 2 — split, text left + decoration right:
    Layout: split — title and body left panel, dot-grid background pattern right panel
    Title: "useState". Subtitle: "Managing local component state".
    Body: short paragraph about useState and when to reach for it.

  Image 3 — split, swapped:
    Layout: split — dot-grid background pattern left panel, title and body right panel
    Title: "useEffect". Subtitle: "Handling side effects in function components".

  Image 4 — title above grid:
    Layout: title spanning full width, 2×2 card grid below
    Title: "Hook Patterns". Cards:
    - STATE: "Manage local state with useState"
    - EFFECT: "Handle side effects with useEffect"
    - CONTEXT: "Share data across the component tree"
    - CUSTOM: "Build reusable logic abstractions"
```

**Consistency rules (enforced by the orchestrator when writing briefs):**

- **Title style:** All titles in the set should have the same character — same approximate length, same tone. Don't mix single-word titles with long phrases.
- **Layout variety:** Avoid repeating the same layout for every image. Aim for at least 2 different layout patterns in a set of 3+ images.
- **Layout descriptions:** Be specific about what goes where. "Split with cards" is better than "split". "Title above, 2x2 grid below" is better than "grid".
- **Content density:** If content for an image is too dense, flag it and suggest adding another image to the set.
- **No empty panels:** If a split layout would leave one side mostly empty, consider a different layout or move content to fill it.
- **No random decoration:** Do not instruct Writers to add standalone decorative elements (dots, shapes, circles) unless the creative direction explicitly calls for them. Background patterns are acceptable.

### Step 2: Generate shared files (Viewport + Stylesheet)

Dispatch one agent to create the Viewport component and the complete stylesheet. This agent is the **layout architect** — it reads the full content plan and creates CSS classes for every layout the images need.

Tell the agent:
- The format dimensions (width, height, name) and the full content plan (from Step 1, including layout descriptions for every image)
- To read `<skill_base_dir>/prompts/shared.md` for full instructions
- To read `.token-image/src/token.active.json` for tokens
- To read `<skill_base_dir>/references/viewports.md` for viewport examples
- To read `<skill_base_dir>/references/default-styles.css` for the base stylesheet
- To read `<skill_base_dir>/references/components.md` for layout pattern reference (CSS + TSX pairs)
- To read `<skill_base_dir>/assets/<preset>/design-guide.md` for the design guide
- The preset name

The agent writes directly to `.token-image/src/viewport.tsx` and `.token-image/src/styles.css`.

The stylesheet must include an "available classes" comment block listing all layout CSS classes, so writers know what's available.

Do NOT run the Reviewer on shared files — they are structural, not design-heavy.

### Step 3: Dispatch per-image agents

This step runs in rounds. Each round: all Writers in parallel → batch render → all Reviewers in parallel. Max 3 rounds per image.

**Round N:**

1. **Dispatch Writer agents** for all images in parallel using the Agent tool.

   Tell each Writer agent:
   - The content brief for this specific image (from Step 1), the format spec (width, height, name), the **layout description** (from the brief's `Layout:` field), the creative direction, and the file index
   - To read `<skill_base_dir>/prompts/writer.md` for full instructions
   - To read `.token-image/src/token.active.json` for tokens
   - To read `.token-image/src/viewport.tsx` for the Viewport component
   - To read `.token-image/src/styles.css` for available CSS classes (the "available classes" comment block at the top lists all layout classes)
   - To read `<skill_base_dir>/references/components.md` for component patterns
   - To read `<skill_base_dir>/assets/<preset>/design-guide.md` for the design guide
   - The preset name

   The Writer writes the component directly to `.token-image/src/<format>-<index>.tsx`.

2. **Batch render all components.** After all Writers complete, run:

   ```bash
   cd .token-image && npm run render
   ```

   This renders every `.tsx` → `.png` in one pass (single Playwright session). The PNGs are saved to `.token-image/src/<format>-<index>.png`.

3. **Dispatch Reviewer agents** for all images in parallel using the Agent tool.

   Tell each Reviewer agent:
   - The content brief for this image
   - To read `<skill_base_dir>/prompts/reviewer.md` for full instructions
   - To read `.token-image/src/viewport.tsx` for the Viewport component
   - To read `.token-image/src/styles.css` for the shared stylesheet
   - To read `.token-image/src/token.active.json` for tokens
   - To read `.token-image/src/<format>-<index>.tsx` for the component to review
   - To read `.token-image/src/<format>-<index>.png` for the rendered image (already rendered by the orchestrator — reviewer does NOT run render)
   - The Reviewer uses multi-modal capabilities to check both code compliance AND visual quality

4. **Collect results.** For any image that didn't PASS, carry it into the next round (updated Writer + re-render that component + Reviewer again). Images that PASS are done.

   For re-renders of individual components in subsequent rounds:
   ```bash
   cd .token-image && npm run render -- <format>-<index>
   ```

Run max 3 rounds total. After 3 rounds, accept whatever state the remaining images are in.

---

## Phase 3: Output

Save files to `.token-image/src/`:

| File | Purpose |
|------|---------|
| `viewport.tsx` | Shared Viewport component |
| `styles.css` | Shared stylesheet (default + preset overrides) |
| `<format>-<index>.tsx` | Per-image components |

Create the `.token-image/src/` directory if it doesn't exist.

After all images are written and reviewed, summarize:
- How many components were generated
- Any images that hit the 3-round limit with remaining issues (and what they are)
- All PNGs have been rendered to `.token-image/src/`
- Reminder: run `cd .token-image && npm run render [component]` to re-render if needed

Then automatically launch the visual editor:

```bash
cd .token-image && npm run editor
```

This opens the editor in the user's browser so they can visually inspect and tweak tokens immediately.

---

## Phase 4: Next Steps

After generating all components, tell the user:

"Done. The visual editor should be open in your browser. Useful commands:
  npm run render                     # re-render all .tsx → .png
  npm run render -- square-1         # render one by name
  npm run render:2x -- square-1      # render one at 2x dimensions
  npm run editor                     # re-launch visual token editor (if closed)"


## IMPORTANT

- Never skip the Reviewer step
- Never output partial results — wait for all parallel agents to complete
- Always plan content first (Step 1), then generate shared files (Step 2), then dispatch Writers (Step 3)
- Content decisions belong to the orchestrator — Writers implement, not interpret
- Creative direction is mandatory in every brief — this is what prevents generic output
