
# Slice Skill

Turn an article, note, paper, or rough topic into a vertical 1080×1920 card video — narrated, paginated to TTS rhythm, with 13 visual themes covering 抖音 / 小红书 / 知乎 / X / 公众号 / 飞书 / TikTok / LinkedIn / 雪球 / 微博 / 即刻 / B 站 / 播客.

> **Renamed from `paper-slide` → `slice`.** The product is now called **Slice** (`voxflow.studio/apps/slice`); the legacy slug is no longer registered. `paper-slide` survives only as one of the 13 theme ids.

## Pick the Route

| Context | Route | Notes |
|---|---|---|
| User wants the deck JSON (no render) — fast, scriptable, pipeable | **CLI**: `voxflow slice <article.md> --theme <id>` | Hits `/api/paper-slide/slice` directly (200 quota). Returns the canonical 5–8 card deck JSON validated by the same backend the web app uses, all 13 themes accepted. No mp4 — pipe `--json` into custom tools, the local Remotion composition (contributors), or paste into the web app for rendering. |
| User is iterating on a deck — multi-round edits to copy/structure before committing to a render | **CLI**: `voxflow slice stage <deck.json>` | Boots a localhost preview page (no quota cost) that hot-reloads on every save of the deck JSON. Useful loop: `voxflow slice ... -o deck.json` → `voxflow slice stage deck.json` → tweak prompt → re-run slice → preview updates instantly. See **Stage Route** below. |
| User wants a finished mp4 + cover (default consumer flow) | **Web app**: `https://voxflow.studio/apps/slice` | The only place that runs the **exact** 6 Slice themes end-to-end. Free tier ships 9:16 mp4 + multi-aspect cover (9:16/3:4/1:1). |
| User wants a similar-looking video offline via CLI but the deck-only `voxflow slice` isn't enough | `voxflow present` or `voxflow picstory --style sketchnote` | **Approximation only.** Different visual schemes; cannot output Slice's `editorial-mag` / `notion-card` / `brutalist` / `glass-dark` themes. See **CLI Approximation** below. |
| Local checkout has `video-present/src/compositions/PaperSlide` (VoxFlow contributors only) | Local Remotion experiment script | See **Local Remotion Route**. Note: experiment script only exercises the original `paper-slide` composition; other 12 themes render via cloud worker only. |
| User only wants strategy or copy | Produce the deck JSON via `voxflow slice` (or by hand following the schema); tell them which renderer to use. | The deck schema is renderer-agnostic; same JSON renders in any theme. |
| User asks to open-source / package | Keep private APIs, tokens, generated audio, MP4 outputs out of the skill package. | |

## Workflow

1. **Pick a theme that matches the platform.** Read `references/themes.md` once — it lists all 13 themes, their visual signature, and which platform / content type each one fits. Don't default to `paper-slide` for everything.
2. **Pick a scenario.** Concrete use case beats generic filler: paper digest, product update, meeting closeout, career advice, founder lesson, market commentary, incident review.
3. **Write a tight deck.** 4-6 cards: one title + 3-5 body. One idea per body card. Captions short enough to fit one line.
4. **Choose visuals from controlled keywords.** Don't search the web or generate random images at render time — pick a canonical `figureKeyword`; the renderer maps it to a local hand-drawn scene / pose / icon. (See `references/deck-schema.md`.)
5. **Render via the chosen route.** Web app for exact themes; CLI for approximation; local script for contributors.
6. **Verify the artifact.** Check duration, dimensions (1080×1920), and at least one title frame + one body frame before reporting done.
7. **Report paths.** Absolute paths to MP4 / posters / props.

Read `references/deck-schema.md` when writing deck JSON, picking keywords, or debugging layout. Read `references/example-decks.md` for seed decks. Read `references/themes.md` when picking a theme or explaining theme tradeoffs.

## Web App Route (default — works for everyone)

```
https://voxflow.studio/apps/slice
```

Workflow:

1. Paste the article / note into the hero composer.
2. AI slices it into 5–8 cards.
3. Pick a theme (13 options — see `references/themes.md`) + a voice (6 production voices: 男主播 / 霸总男声 / 闲聊男声 / 小美 / 小心 / 小徐).
4. Render → 1080×1920 mp4 + multi-aspect cover (9:16 / 3:4 / 1:1).

Tell the user this is the **only** route that produces the exact Slice render for all 13 themes — they're private Remotion compositions, not shipped with the CLI.

## CLI Deck Route (`voxflow slice`)

For users who want the structured deck JSON without the render — fast (one round-trip, 200 quota), pipeable, theme-aware. Hits the same `/api/paper-slide/slice` backend the web app uses, so the deck shape is canonical.

```bash
voxflow slice article.md                                  # default theme: paper-slide
voxflow slice article.md --theme editorial-mag -o deck.json
voxflow slice --text "long article ..." --theme bold-poster --json | jq .deck
```

When to use this route:

- The user wants to inspect / iterate on the AI's slicing quality before committing to a render.
- The user wants to paste the deck into the web app's "import deck" flow to render with a different theme.
- The user is a contributor with the private `video-present/src/compositions/PaperSlide` Remotion composition and wants to render the deck locally — `voxflow slice ... --json -o props.json` then feed `props.json` into the experiment script.
- The user is building automation that needs structured output (e.g. publishing knowledge cards as text on Twitter / 即刻 from `deck.cards[*].caption + narration`).

Limits:

- No mp4. The cloud renderer that produces the 1080×1920 video lives in the web app.
- No TTS. Pair `voxflow slice` with `voxflow narrate` if you want per-card audio without rendering.

## Stage Route — `voxflow slice stage` (iteration preview)

For the human-in-the-loop iteration phase **before** committing to a cloud render. Stage spins up a localhost HTTP server with hot reload — every save of the deck JSON updates the page instantly. No quota cost, no network round-trip.

```bash
voxflow slice deck.md -o deck.json     # 1. produce a deck (200 quota)
voxflow slice stage deck.json          # 2. open localhost preview (free)
                                       # 3. edit deck.json by hand or re-run slice
                                       # 4. preview hot-reloads on save
```

Want a no-quota, no-login starter? Use the bundled sample directly:

```bash
voxflow slice stage examples/11-slice-stage/sample-deck.json
```

Flags:

```
voxflow slice stage <deck.json> [--port <n>] [--theme <id>] [--no-open]
  --port      Default 5180. Auto-skips +1 up to 5189 on conflict.
  --theme     Lock the preview to one theme (must be one of the 13 valid ids).
  --no-open   Don't auto-launch the browser (CI / SSH / agent environments).
```

When to use Stage:

- The user is in a multi-round editing loop — copy tweaks, card re-ordering, theme A/B — and reopening the mp4 each iteration is expensive friction.
- The user wants to publish single cards (PNG) or carousels (ZIP) for image-first platforms (小红书 / X / 微博 / 公众号 头图) — Phase 1.4+ adds these export buttons.
- AI-driven loops where the agent regenerates `deck.json` and the human reviews via browser — the page updates without the agent having to re-print paths.

What Stage is NOT:

- Not a full Remotion preview yet. MVP shows deck structure (cards + JSON); cloud-rendered theme thumbnails arrive in Phase 1.3 via `renderStill`.
- Not a publish flow. To get the finished mp4, still use the web app or contributor Remotion route.
- Not a substitute for the full render — themes are server-side compositions; Stage previews the **deck**, not the final video frames.

### Edit-with-AI loop (the actual iteration workflow)

Stage doesn't try to be Cursor — it's a **visual feedback closer** that hands prompts to whatever AI tool the user already has open (Claude Code, Cursor, ChatGPT, anything). Two affordances cover the whole edit loop:

| Intent | UX | Output |
|---|---|---|
| Whole-card rewrite ("regen this card, keep the rest") | Hover the card → corner button **Edit with AI** | Modal with a prompt: file path + `cards[N]` JSON snippet + `<your instruction>` slot |
| Local phrase rewrite ("just this phrase is off") | Select text inside a card → floating **Edit selection with AI** button appears | Modal with a prompt: file path + the exact selected substring quoted + full card JSON for context |

The user types the instruction (e.g. "shorten to 12 chars, more visceral"), clicks **Copy prompt**, pastes into their AI. The AI uses its native file-edit tools (Claude Code's Edit, Cursor's Apply, etc.) to rewrite the file. Stage's SSE watcher hot-reloads the preview within ~150 ms. Loop until satisfied.

Why this design and not an embedded chat / MCP server: see [#3330](https://github.com/VoxFlowStudio/FlowStudio/issues/3330) for the full design rationale (universal copy-paste vs. Claude Code-only MCP, cost vs. coverage tradeoff, future MCP upgrade path conditional on usage telemetry).

## CLI Approximation Route (full mp4 fallback)

If the user **must** have an mp4 from the CLI alone (no web app, no contributor Remotion access), fall back to `voxflow present` or `voxflow picstory` — they cover the same article-to-video shape but with their own visual schemes, not the exact 13 Slice themes.

```bash
voxflow present --text "paste article or summary" --style editorial --output slice-approx.mp4
voxflow picstory --topic "topic" --style sketchnote --scenes 4 --output slice-sketch.mp4
```

Closest CLI scheme per Slice theme:

| Slice theme | Closest CLI route |
|---|---|
| paper-slide | `voxflow picstory --style sketchnote` |
| editorial-mag | `voxflow present --style editorial` |
| bold-poster | `voxflow present --style brutalist` (closest weight) |
| notion-card | `voxflow present --style minimal` |
| brutalist | `voxflow present --style brutalist` |
| glass-dark | `voxflow present --style noir` or `--style aurora` |
| editorial-stencil | `voxflow present --style editorial` (no letterbox / dual-tone equivalent) |
| broadsheet | `voxflow present --style editorial` (no FT salmon palette) |
| blueprint | `voxflow picstory --style chalkboard` (closest grid/diagram feel) |
| daisy-pastel | `voxflow picstory --style sketchnote` (no pastel illustration equivalent) |
| showa-catalog | `voxflow picstory --style vintage_newspaper` (no city-pop equivalent) |
| photo-feature | `voxflow picstory --style photo` (photo-feature needs imageUrl per card — see deck-schema) |
| atmospheric | `voxflow present --style noir` |

Always tell the user: "This is a Slice-adjacent draft. The exact 13-theme renderer lives on `voxflow.studio/apps/slice`."

## Local Remotion Route (contributors only)

**Skip if `video-present/src/compositions/PaperSlide` is not in your checkout** — it's private code; npm / skills users don't have it.

From the contributor checkout root:

```bash
cd video-present
node scripts/paper-slide-experiments.mjs
```

Render a subset:

```bash
cd video-present
PAPER_SLIDE_EXPERIMENT_FILTER=research-reading node scripts/paper-slide-experiments.mjs
```

Verify outputs:

```bash
ffprobe -v error -select_streams v:0 \
  -show_entries stream=width,height,duration \
  -of default=nw=1 out/paper-slide-experiments/research-reading.mp4

ffmpeg -y -hide_banner -loglevel error -ss 9 \
  -i out/paper-slide-experiments/research-reading.mp4 \
  -frames:v 1 -q:v 2 out/paper-slide-experiments/research-reading-body.jpg
```

Expected: `1080×1920`, 20-35 seconds, no black flashes, no caption overflow, figure not clipped.

## Deck Writing Rules (apply across all 13 themes)

- **Title card**: hook, contrast, or promise. Avoid abstract labels like "Introduction".
- **Body card**: one idea only. Caption usually under 16 Chinese chars or 7 English words.
- **Narration**: conversational, 25-60 Chinese chars per body card.
- **Scene keywords** (prefer when they fit): `problem-framing`, `evidence-board`, `customer-pain`, `timeline-review`, `owner-deadline`, `risk-guardrail`, `cashflow-ledger`, `team-alignment`, `before-after`, `learning-loop`, `decision-fork`, `growth-system`.
- **Figure / icon keywords** (visual accents): `thinking`, `running`, `climbing`, `stuck`, `celebrating`, `briefcase`, `users`, `target`, `clock`, `flame`, `lightbulb`, `chart-bar`.
- **Vary adjacent visuals.** Don't use `thinking` on every card.
- **Theme is independent of deck content** — the same deck JSON renders in any of the 13 themes; pick the theme based on platform / mood, not content. Exception: `photo-feature` and `atmospheric` use each card's `imageUrl` as a backdrop and degrade to an SVG stub when missing — see `references/deck-schema.md`.
