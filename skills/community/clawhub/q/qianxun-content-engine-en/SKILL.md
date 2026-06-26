---
name: content-engine-en
description: "Content Engine (Xiaohongshu). Two modes: ① Deconstruct (v1) — input a viral XHS link, get an 18-field structured card. ② Generate (v2) — combine the deconstruction with your brand info and use Ofox (LLM + Nano Banana) to produce your own version: script / caption / cover / desc / tags / reference frames. v0.3.0: real video generation via Volcengine Ark Seedance 2.0 (multi-shot + ffmpeg auto-concat). Maintains a shared graph/ knowledge graph across modes so the system gets smarter over time. Architecture inspired by Ronin's Skill Graph. Chinese version: ~/.agents/skills/content-engine/"
---

# Content Engine

Cross-platform content deconstruction + generation + knowledge graph. The bottom layer is a **graph that grows over time**; the top layer hosts multiple modes across multiple platforms.

> 中文版 / Chinese: see `~/.agents/skills/content-engine/`

## Mode Roadmap

| Mode | Status | Description |
|---|---|---|
| **deconstruct** | ✅ v1 | Reference link → 18-field deconstruction card; feeds the graph along the way |
| **generate** | ✅ v2.2 | Deconstruction + graph + your brand → script / caption / cover / desc / tags / reference frames. **v0.3.0**: real video generation via Volcengine Ark Seedance 2.0 (sequential per-shot generation + ffmpeg auto-concat into final-video.mp4; partial-video.md tracks failed shots so you can re-run them). **v0.2.1**: built-in validator + auto-fallback v1. |
| evaluate | 🔜 v3 | Finished content → 8-dimension weighted scoring |

## Platform Roadmap

| Platform | Status | Coverage / Plan |
|---|---|---|
| **Xiaohongshu (XHS / RedNote)** | ✅ v1 | Video posts + image posts |
| Douyin | 🔜 v1.1 | Short-form video (planned via TikHub Douyin API) |
| WeChat Channels (视频号) | 🔜 v1.2 | Short-form video |
| Bilibili | 🔜 v2 | Short + long-form video |
| TikTok / Instagram | 🔜 Exploring | International platforms |

> **Current state**: this document covers **Xiaohongshu deconstruct (v1) + generate (v2.2 text+image+video)**. v0.3.0 ships real video via Seedance 2.0. Future platforms reuse the same architecture (`extract_{platform}.py` / `generate_{platform}.py` + `content_engine/{platform}/` submodules); the graph is shared cross-platform.

> **Platform compatibility**: This skill runs in OpenClaw (as a personal agent skill) and Claude Code. Scripts use Python 3.10+ stdlib (no external deps); the only system command needed is ffmpeg. File I/O assumes your agent has `Read` / `Write` tools (in OpenClaw these map to `apply_patch` / `Exec` / `Web browser`).

---

## Architecture: graph/ is the brain

```
content-engine-en/
├── SKILL.md              ← what you're reading; the agent's entry point
├── graph/                ← knowledge graph (shared "memory / soul / context" across modes)
│   ├── index.md              brand briefing, agent reads first
│   ├── brand/{brand-voice,brand-story}.md
│   ├── platforms/xiaohongshu.md     XHS playbook (only platform in v1)
│   │                                 (v1.1+ will add douyin.md / wechat-channels.md / ...)
│   ├── audience/segments.md          audience segmentation
│   └── engine/{hooks,style-tags,taboo}.md
├── references/{output-template,example-video,example-image}.md
└── scripts/
    ├── extract_xhs.py                v1 deconstruct CLI: link → workspace
    ├── generate_xhs.py               v2 generate CLI: link → script + images + copy
    │                                  (v1.1+ will add extract_douyin.py / generate_douyin.py)
    └── content_engine/               Python package (zero deps)
        ├── client.py                  TikhubClient (v1)
        ├── parsers.py                 NoteData / Comment parsing (v1)
        ├── linkresolve.py             short link → note_id (shared)
        ├── video.py                   download + ffmpeg frame extraction (v1)
        ├── images.py                  image post downloader (v1)
        ├── llm.py                     Ofox LLM client (v2)
        ├── nano_banana.py             Ofox image generation (v2, Nano Banana Pro)
        ├── lookup.py                  link → card lookup + freshness (v2)
        ├── prompts.py                 5 text prompt templates (v2)
        ├── generate.py                generate mode orchestration (v2)
        ├── preflight.py               environment self-check (v1+v2)
        └── models.py                  dataclass definitions
```

**Two ironclad rules**:
1. graph/ files **can be empty templates** — deconstruction still runs, just falls back to "objective deconstruction" mode
2. New hooks / style words discovered during deconstruction are **auto-written back** to `graph/engine/`. The graph grows.

---

## When to trigger

- User gives an XHS link and says "deconstruct this" / "study this" / "why did this go viral?"
- Competitive analysis during content planning
- The "research first" step before generating new content

## Input

| Required | Field | Notes |
|---|---|---|
| ✅ | Reference link | XHS short link / long link / 24-char hex note_id / share text — all accepted |
|  | Task ID | Defaults to `AIC-{YYMMDD}-{seq}` |
|  | Content goal | e.g., "drive in-store traffic" / "DM acquisition" — affects "Takeaways" field |

## Output

Markdown file → `docs/deconstructions/{id}-{slug}.md`.

Full field definitions in `references/output-template.md`. Examples in `references/example-video.md` / `example-image.md`.

---

## Workflow

### Step 0: Detect graph state → choose mode

Use your agent's native tools directly (avoid bash globstar / realpath compat issues):

1. Locate the skill root (where `SKILL.md` lives)
2. Use `Read` or `Grep` tools to scan `graph/**/*.md` for `# TODO:` markers

Simplest: a single Grep call:
```
Grep pattern: "^# TODO:"  path: <skill_root>/graph/  output_mode: files_with_matches
```

| Files matched | Mode | Behavior |
|---|---|---|
| 0 | **Brand-aware** | Step 5's "Target audience" / "Takeaways" must be generated from graph content; field-fill stage **must read** the relevant graph nodes |
| ≥1 | **Objective** | Skip brand-aware fields; append to output: "⚠️ graph/ not yet populated — recommend filling {list of TODO files}" |

**Mode A vs B differences in the "Takeaways" field**: see the dual-version comparison at the end of `references/example-video.md`.

> Wikilink convention `[[brand/brand-voice]]` between graph files: this is Obsidian-style, pointing to `graph/brand/brand-voice.md` (no `.md` suffix). When you see `[[X]]`, Read the corresponding file to load context.

### Steps 1-3: One-shot data fetch → workspace

**One command does it all**: link resolution / metadata fetch / comments fetch / video download + frame extraction / image download for image posts.

> ⚠️ **v1 supports Xiaohongshu only**. Douyin / WeChat Channels / Bilibili etc. are on the roadmap (v1.1+) with corresponding `extract_douyin.py` / `extract_wechat_channels.py` scripts.

```bash
python3 scripts/extract_xhs.py "<XHS link / note_id / share text>"
# Default workspace: {tempdir}/content-engine/{note_id}/
# Custom: --out /your/path
```

First-run environment check:
```bash
python3 scripts/extract_xhs.py --check
```
(Checks Python version / ffmpeg / TIKHUB_API_TOKEN / network / workspace writable. See "Setup" section below.)

**Workspace artifacts** (default `{tempdir}/content-engine/{note_id}/`, cross-platform):

| File | Content | How agent uses it |
|---|---|---|
| `note.json` | Parsed `NoteData` dataclass (all fields pre-extracted) | Read directly; maps to Step 5 field table |
| `comments.json` | Parsed `Comment` list (with `is_pinned` heuristic flag) | You (agent) read raw text in Step 5c and classify semantically — better than regex |
| `{note_id}.mp4` | Original video file (CDN direct download) | Used by Step 4 frame extraction |
| `frames/frame_NNN.png` | Extracted frames (auto fps based on duration: short <10s → 1.0, mid → 0.5, long >60s → 0.25) | Step 4 reads frame by frame |
| `images/image_NNN.jpg` | All images for image posts (numbered in order) | Step 4 reads image by image |

**Error handling**:
- API 401/403 → non-zero exit, tell user and stop
- Comments API failure → `comments.json` written as `{"_error": "..."}`; "comment keywords" field becomes "⚠️ Not retrieved"
- Non-XHS link → tell user "v1 only supports Xiaohongshu" and stop

**Common flags**:
- `--no-video` skip video download (metadata-only mode)
- `--no-comments` skip comments
- `--fps 1.0` force frame rate (default auto-adapts to duration)

### Step 4: Multi-modal deconstruction

#### Step 4a · Required reading before deconstruction (graph hard gate)

**Always Read first**:
- `graph/platforms/xiaohongshu.md` — sections "What to focus on when deconstructing" + "Platform viral formulas" + "Taboos"
- `graph/engine/style-tags.md` — full style dictionary (Step 5 style tag field uses this)
- `graph/engine/hooks.md` — full hook library (Step 5 emotion-hook field uses this)

If in brand-aware mode, also Read `graph/brand/brand-voice.md` + `graph/brand/brand-story.md` + `graph/audience/segments.md`.

#### Step 4b · Video branch (type == "video")

1. **Read frames** in order (`frame_001.png` ...). Mental-note for each frame: shot type / subject / action / background / props / camera direction. **Don't output N rows of stream-of-consciousness** — accumulate material for aggregation in next step.
2. **Aggregate into time segments** for the "Reference content deconstruction" field. **Core rule**:

   | ✅ Good (aggregated + dense) | ❌ Bad (stream of consciousness or empty) |
   |---|---|
   | 7-12s ｜ Camera: locked → slow push ｜ Shot: close-up → extreme close-up<br>Visual: emerald-green collar and placket of vest, jade buttons + white beaded geometric embroidery, paired with white jade pendant necklace as styling demo | 7s ｜ close-up ｜ collar<br>8s ｜ close-up ｜ collar<br>9s ｜ close-up ｜ button<br>... |
   |  | 7-12s ｜ Visual: very pretty clothing detail, exquisite craftsmanship |

   **Merge rules**:
   - 2+ consecutive frames with same subject/shot type → merge into one segment
   - Subject/shot change → start new segment
   - Single-frame holds <2s usually don't get their own segment
   - Use **specific nouns** (emerald green, beadwork, jade button) not **adjective stacking** (high-end, exquisite, beautiful)

3. **Voiceover/subtitle text**:
   - Combine on-screen captions + `note.json.desc`
   - Pure visual + no captions → write "No voiceover/subtitle, pure visual storytelling" + list bottom-watermark info

4. **Voiceover logic analysis**: write in **layers**, each layer with timestamp + one-line function:
   - Example: "Layer 1 · Establish contrast and curiosity (0-12s): the '75-born + 2000m² store' numeric contrast triggers curiosity"
   - Common structures:
     - Hook open → scene immersion → product/USP → identity elevation → CTA
     - Contrast open (number/conflict) → story setup → values → CTA
     - Craft close-up → cultural meaning → emotional resonance → tag elevation

#### Step 4c · Image branch (type == "normal")

1. **Read images** in order (`images/image_NNN.jpg`)
2. Each image: composition / elements / style / role (in the set: cover / detail / outfit / scene)
3. **Aggregate** into "Reference content deconstruction" by image order: "Image 1 (cover): ... / Image 2: ..."

### Step 5: Extract remaining fields

#### Step 5a · Field-fill table (graph influence)

| Field | Source | graph required reading |
|---|---|---|
| Platform | Link source | — |
| Target audience | `note.json.desc` + `hashtags` + comment behavior | **Brand-aware mode**: must cross-reference `graph/audience/segments.md` and explicitly mark which segment hit |
| Viral theme | `note.json.desc` + `title` + deconstruction | — |
| Style tags | Visuals + copy | **Must** cross-reference `graph/engine/style-tags.md` — mark "existing" if hit, "new" if not (and queue for Step 6 writeback) |
| Scene tags | Visuals | — |
| Emotion hook | Opening + hook lines | **Must** cross-reference `graph/engine/hooks.md` patterns; explicitly mark which class hit |
| Comment keywords | `comments.json` (you classify yourself) | See Step 5c — agent reads raw comments and classifies semantically; more accurate than regex |
| Voiceover logic analysis | Copy structure | — |
| Reference hashtags | `note.json.hashtags` (parser already cleaned `[话题]`) | Parser pre-extracted; just join with `#`; **don't grep desc** |
| Takeaways | Global summary | **Strong dependency**: brand-aware mode writes "how we'd do the same theme"; objective mode writes general principles |

#### Step 5b · Quality bar for subjective fields

See "Field definitions + Anti-Pattern" section in `references/output-template.md`. **Core principles**:

- **Viral theme** explains "why it went viral" (mechanism), not "what it is" (description)
- **Emotion hook** writes "what technique elicits what emotion" (two-layer), not a single isolated word
- **Style vs Scene vs Emotion-hook**: style = "how it looks/feels", scene = "where it happens", emotion-hook = "what it stirs in the user's mind" — never confuse the three

#### Step 5c · Comment keyword semantic classification (you do it, no regex)

**Why no regex**: language has infinite variations ("how do I buy" / "what's the price" / "is it pricey" / "how much"), regex always misses; regex also can't handle semantics ("price isn't a problem" isn't an inquiry; "isn't this silk?" isn't an objection). **You (agent) have full language understanding — do this directly, you're 100x better than regex at this.**

**Data source**: `comments.json` already filtered by parser — `is_pinned=True` (merchant-pinned / anti-scam) is auto-flagged and skippable; the rest are real user comments.

**Four classes** (by "what the user is doing"):

| Class | What to capture | Examples |
|---|---|---|
| **ask** | Asking about purchase path / price / address / hours / channels (pre-conversion info) | "how do I buy" / "how much" / "where's the store" / "open hours" / "available online?" |
| **request** | Active need (strong intent) | "need WeChat" / "still in stock?" / "size out?" / "need contact" |
| **praise** | Resonance / specific likes | "so beautiful" / "want it" / "elegant" / "love it" / "tempting" |
| **objection** | Correction / disagreement (**not neutral questions**) | "please don't call this X" / "this is A not B" / "shouldn't be this expensive" |

**Output format** (mandatory evidence):

```
- {keyword label} ({N} raw comments: "text 1" "text 2" "text 3") — {one-line interpretation / conversion signal judgment}
```

**Hard anti-fabrication rules**:
1. Each keyword must be backed by 1-3 **original comment texts** (copy directly from comments.json, no rewriting)
2. Keywords without raw text evidence are **not allowed** — no fabrication
3. **Questions are not objections**: "isn't this silk?" is a neutral question (goes to ask); "please don't call this 新中式" is an objection
4. Same comment can fall into multiple classes — "how do I buy this love the green" is both ask and praise; quote it under both
5. comments.json is `[]` or has `_error` → write "⚠️ Comment data not retrieved", **don't infer from desc**

**Good vs Bad**:

```
✅ Good (with evidence + interpretation):
- how-do-i-buy (5 raw comments: "how do I buy the green pants" "how to purchase, online?" "how do I buy this love the green") —
  highest-frequency conversion signal
- how-much / pricing (2 raw comments: "how do you sell this" "what's the price for this set") —
  another way of asking pricing
- objection-traditional-attire (1 raw comment: "this is Manchu attire, please don't call it 新中式" 👍 1) —
  only 1 comment but liked, signals tag-usage edge case

❌ Bad (no evidence / fabricated):
- how-do-i-buy, how-much, need-link (just listing words, no raw text — forbidden)

❌ Bad (misclassifying questions as objections):
- objection (comment: "is this silk?")  ← this is a question, not an objection
```

### Step 6: Write back to graph (system gets smarter)

After deconstruction, **proactively review and write back**:

**Strict writeback location rules**:

| Type | File | Insert location | Format |
|---|---|---|---|
| New hook | `graph/engine/hooks.md` | End of `## Pending classification` section | `### {emotion-class｜pattern-name}` H3 + bullets (pattern/适用/example/source) |
| New style tag | `graph/engine/style-tags.md` | End of `## Pending` table | `| tag \| applicable \| first source |` row |
| Platform observation | `graph/platforms/xiaohongshu.md` | **Top** of `## Observation log` (newest first) | `### {YYYY-MM-DD} · {one-line topic}` + bullets (source/observation/data/inference) |

**Writeback principles**:
1. Append-only, never overwrite
2. Every entry must include "source = task ID" + "date / data"
3. If conflict with existing graph entries → don't write; emit ⚠️ in output for human resolution
4. Hit existing hook/tag → **don't duplicate**; just mark "reuses existing graph entry" in deconstruction card

### Step 6.5: Pre-output self-check (mandatory checklist)

Every line must ✓; failing one means you don't proceed to Step 7:

```
□ All 18 Excel fields filled, no skips
□ All 5 metadata items (author/time/engagement/note_id/type) pulled live from API, not fabricated
□ Style / Scene / Emotion-hook are not confused (see output-template.md)
□ Reference body copy is desc original (with emojis + line breaks), not paraphrased or trimmed
□ Each comment keyword backed by raw text from comments.json; if comments.json has `_error`, write "⚠️ Not retrieved"
□ Voiceover logic analysis is written in layers (hook/setup/elevation/CTA), not a single paragraph
□ Style tags hitting graph dictionary are marked "existing"; new ones marked "new"
□ Emotion hook hitting existing graph pattern is explicitly noted; new patterns queued for Step 6 writeback
□ Reference hashtags pulled directly from note.json.hashtags (parser already cleaned [话题])
□ Step 6 writeback: explicitly state "N items" or "none"; each item has source/date
□ Objective mode: append "graph/ not populated" notice at the end
```

### Step 7: Publish deconstruction card

#### Step 7a · Generate slug
From title, generate filename / doc-name slug:
```python
import re
slug = re.sub(r"[^\w一-龥\-_·]+", "-", title)[:30].strip("-") or "untitled"
# e.g., "Shenzhen 新中式｜what does wearing 江南春色 feel like" → "Shenzhen-..."
```

Final naming: `{id}-{slug}` (e.g., `AIC-260426-001-Shenzhen-deep-dive`).

#### Step 7b · Output (branches based on agent environment)

**Preferred: Feishu (Lark) Docx** (when running in OpenClaw with the [Lark official plugin](https://www.feishu.cn/content/article/7613711414611463386))

The OpenClaw Lark plugin gives the agent native tools to create cloud documents. In OpenClaw:
1. Use the Lark plugin's **"create cloud doc"** tool (exact tool name varies by plugin version), passing the full markdown content
2. Title is `{id}-{slug}`
3. Get the Feishu doc URL; record it for Step 7c

**Fallback: local markdown** (Claude Code / no Lark plugin / Lark tool failed)

```bash
# Use the Write tool to write to:
docs/deconstructions/{id}-{slug}.md
```

**Decision logic**:
- Agent self-check: do I have a "create cloud doc" / Lark-document tool in my current session?
- Yes → publish to Feishu, don't also write locally
- No → write locally directly

**Note**: This skill does NOT wrap Feishu API. The OpenClaw Lark plugin handles auth / upload / conversion; the agent only needs to call the plugin's tools. Claude Code users who want Feishu publishing must manually copy the markdown into a Feishu doc.

#### Step 7c · User summary (fixed 4 lines)

```
1. Subject: {title / author / duration / engagement} — one line
2. Strongest insight: {1 core hook or counter-intuitive finding} ({data evidence, e.g., "save-to-like ratio 70%"})
3. Published to: {Feishu URL or local absolute path}
4. Graph writeback: {N items; list top 3, abbreviate rest; if 0, explicitly state "none"}
```

---

# v2 Generate Mode (v0.2.0+)

Use the v1 deconstruction card as a competitor reference + your brand info → generate your own version of script / copy / reference frames / cover / tags.

## When to trigger

User says something like:
- "Based on https://xhslink.com/o/xxx, generate a same-theme video for our brand"
- "Learn from this post and produce 8 image cards for us"
- "This viral post has a great hook — make a version of it for our brand"

## Input

| Required | Field | Notes |
|---|---|---|
| ✅ | XHS link | User passes only the link; agent doesn't ask for filename |
| ✅ | --type | `video` / `image` / `script` |
| ✅ | --count | 1-N (image count / video count) |
|  | --product-imgs | Path to product images (dir or single file) — text-only in v2.0; image-to-image in v2.1 |
|  | --product-usp | Free-text USP / material / craft description |
|  | --fresh | Force re-deconstruct v1 (bypass cache) |

## Output workspace

```
docs/deconstructions/AIC-260426-001-xxx-generated/    ← v1 card name + "-generated"
└── GEN-260427-001-image/                            ← one GEN-N per generate run
    ├── script.md                                    ← full script (image plan / video shots / shoot brief)
    ├── caption.txt                                  ← (video type) on-screen captions
    ├── cover.png + cover.txt                        ← cover image (with overlay text) + text backup
    ├── frames/frame_NNN.png                         ← N reference images (Nano Banana, vertical 9:16)
    ├── desc.txt                                     ← XHS post body
    ├── tags.txt                                     ← hashtags (10-15)
    ├── seedance-prompt.md                           ← (video type) Seedance cinema-style prompt
    ├── shots/shot_NN.mp4                            ← (video, v0.3.0) Per-shot real videos from Seedance
    ├── final-video.mp4                              ← (video, v0.3.0) ffmpeg-concatenated final video
    └── partial-video.md                             ← (video, v0.3.0) Per-shot status + failed-shot prompts
```

## Workflow (10 steps)

### Step 0: Preflight + mode select
- Check OFOX_API_KEY (required) + TIKHUB_API_TOKEN (for fallback v1 deconstruct)
- Check graph state (brand-aware vs objective mode)

### Step 1: Link → deconstruction card
1. Resolve link → note_id (reuse v1 linkresolve)
2. Grep `docs/deconstructions/` for note_id
3. Found (≤7 days) → use directly
4. Found (>7 days) → ask user "reuse / re-deconstruct?"
5. Not found → **auto-fallback** (since v0.2.1): transparently runs `extract_xhs.py` to fetch note.json + comments.json + frames, then writes a stub deconstruction card (text fields populated; visual fields marked ⚠️ AUTO-STUB for the agent to complete by reading frames/)

### Step 2: Read graph context
- brand-voice / brand-story / segments / taboo / hooks / style-tags / xiaohongshu

### Step 3: Collect input args
- type / count / product-imgs / product-usp

### Step 4: Generate script (core)
- Prompt template: deconstruction + brand-voice + hooks library + USP
- Output: `script.md`
- Critical constraint for image type: **each frame MUST be a single isolated subject** (prevents downstream image gen from producing collages)

### Step 5: Parallel generate 4 ancillary text
- caption.txt (video only)
- cover.txt
- desc.txt
- tags.txt (depends on desc, runs after)

### Step 6: Image generation (image / video types)
- N frames (per `--count` for image; 1 key frame for video) + 1 cover
- Nano Banana **three-path constraint** prompt:
  1. **Layout reference** ← from script.md single-frame description
  2. **Brand style anchors** ← from graph/brand/brand-voice
  3. **Product description** ← from --product-usp + --product-imgs
- Hard rules baked into `build_prompt`:
  - STRICTLY VERTICAL 9:16 portrait
  - SINGLE IMAGE only, NO collage / grid / multi-panel
  - frame: ABSOLUTELY NO text; cover: text overlay allowed

### Step 7: seedance-prompt.md (video type only)
- LLM translates script into Seedance cinema-style prompt (5-6 shots, 4-7s each)
- From v0.3.0, this file is also auto-fed into Seedance API (unless `--no-real-video`)

### Step 7.5: Real video generation (v0.3.0+, video type, default on)
- Parse seedance-prompt.md into N shots
- **Print cost estimate + 3-second Ctrl+C countdown** (1 shot 5s ≈ $0.20, 5 shots ≈ $1)
- Submit shots sequentially to Volcengine Ark Seedance 2.0 (async task + polling, ~1-3 min per shot)
- Failed shots don't block other shots; `partial-video.md` records which failed + their prompts for manual re-run
- Successful shots are stitched with `ffmpeg concat` into `final-video.mp4`
- Flags: `--no-real-video` (prompt-only, skip API) / `--async` (submit only, return task_ids) / `--no-confirm` (skip 3s countdown)

### Step 8: validator (built-in since v0.2.1)
- **Hard errors** → auto-retry the relevant step (max 1 attempt): taboo word hits / empty file / tags < 5 / image too small (suspected gen failure)
- **Soft errors** → emit `quality_report.md` for the user to decide: desc length anomaly / too many emoji / multi-line cover
- Taboo dictionary auto-extracted from `graph/engine/taboo.md`, layered on top of default extreme/marketing words

### Step 9: Publish
- Reuses v1 Step 7: Feishu first + local fallback
- Returns the GEN-xxx directory path as the deliverable

### Step 10: 4-line summary
```
1. Generated: based on {card} + {brand}, {type} ({count} items)
2. Outputs: script.md + cover + N frames + desc + tags + (seedance-prompt)
3. Workspace: {absolute path}
4. Time / calls: {seconds} / {LLM calls} + {image calls}
```

## CLI usage

```bash
# 8 reference images for an image post
python3 scripts/generate_xhs.py "<XHS link>" --type image --count 8 \
  --product-usp "Premium knitwear: silk vest + embroidered shirt" \
  --product-imgs ~/photos/spring-2026/

# 1 video (v0.3.0+: real video gen by default, ~$1, Ctrl+C to cancel)
python3 scripts/generate_xhs.py "<XHS link>" --type video --count 1

# 1 video, prompt only (script + cover + 1 key frame, no Seedance API call)
python3 scripts/generate_xhs.py "<XHS link>" --type video --count 1 --no-real-video

# Async: submit Seedance tasks and return immediately with task_ids
python3 scripts/generate_xhs.py "<XHS link>" --type video --count 1 --async

# Shoot brief only
python3 scripts/generate_xhs.py "<XHS link>" --type script --count 1

# Force re-deconstruct (bypass cache)
python3 scripts/generate_xhs.py "<XHS link>" --type image --count 8 --fresh

# Environment check (includes OFOX_API_KEY)
python3 scripts/generate_xhs.py --check
```

## Known limitations / roadmap

| Limitation | Solution direction | Plan |
|---|---|---|
| ~~Video not really generated (prompt only)~~ | ~~Integrate Volcengine Ark Seedance 2.0 API~~ | ✅ v0.3.0 |
| No hook variants (1 set per run) | LLM multi-round with N hook directions | v0.4.x |
| Weak character consistency (different faces) | IP-Adapter / InstantID | v0.5.x |
| ~~No automatic QA~~ | ~~validator.py with hard+soft error detection~~ | ✅ v0.2.1 |
| ~~Fallback v1 deconstruct is manual~~ | ~~Auto-trigger built in~~ | ✅ v0.2.1 |
| Stub card visual fields filled by agent manually | Vision LLM auto-completion | v0.4.0 |

## Boundaries (generate mode)

1. **No fabricated product info**: if user provides no product images / USPs → prompt explicitly notes "user did not supply visual reference"; LLM avoids inventing concrete colors/materials
2. **No copy-paste from competitor**: script must not contain reference video's specific proper nouns (brand / founder / location)
3. **Images are reference, not finals**: v2.0's image generation is a mood board / shooting reference, not direct-publish assets (see spec §1)
4. **Brand consistency uses three-path constraint**: product image + brand-voice prompt + deconstruction layout — any path missing is OK (degrades but doesn't block)
5. **Ofox calls are metered**: each generate ~4-7 LLM + N+1 image calls; recommend `--count 1` first to verify before scaling up

---

## v1 boundaries (deconstruct mode)

1. **No fabrication**: API failure / video download failure / unrecognizable subtitles → mark "Not retrieved"
2. **Deconstruction is observation, not commentary**: factual fields write "the visual shows X", not "this looks great". Subjective judgment only in three fields: emotion-hook / viral theme / takeaways
3. **Graph is append-only**: writebacks don't overwrite; conflicts get ⚠️ for human resolution
4. **Token control**: when video frames > 30, aggregate by time segments (1 representative per 5s) before detailed description
5. **No content generation here**: deconstruct mode only outputs cards + graph writeback (v2 generate handles generation)

---

## Setup

### System requirements

| Dependency | Purpose | Install |
|---|---|---|
| **Python ≥ 3.10** | Run all scripts | macOS: `brew install python@3.12`<br>Linux: `apt install python3.12` or pyenv<br>Windows: [python.org](https://python.org) |
| **ffmpeg** | Video frame extraction (optional for image-only) | macOS: `brew install ffmpeg`<br>Linux: `apt install ffmpeg` (or dnf / pacman)<br>Windows: `choco install ffmpeg` |

> No pip dependencies — scripts use Python stdlib only.

### API tokens

**v1 deconstruct needs `TIKHUB_API_TOKEN`** (required for deconstruct)
**v2 generate needs `OFOX_API_KEY`** (required for generate; covers LLM + Nano Banana image gen)
**v0.3.0+ real video needs `ARK_API_KEY`** (required when video type runs in default mode; `--no-real-video` bypasses)

```bash
# v1 deconstruct: TikHub
mkdir -p ~/.config/content-engine
echo 'TIKHUB_API_TOKEN=your_tikhub_token' >> ~/.config/content-engine/.env

# v2 generate: Ofox (LLM text + Nano Banana images)
echo 'OFOX_API_KEY=ofox-your_key' >> ~/.config/content-engine/.env

# v0.3.0+ video generation: Volcengine Ark (Seedance 2.0)
echo 'ARK_API_KEY=your_ark_key' >> ~/.config/content-engine/.env
```

| Token | Sign up | Use | Required? |
|---|---|---|---|
| `TIKHUB_API_TOKEN` | [tikhub.io](https://tikhub.io) | XHS API (raw deconstruct data) | v1 deconstruct |
| `OFOX_API_KEY` | [ofox.ai](https://ofox.ai) | LLM + Nano Banana images | v2 generate |
| `ARK_API_KEY` | [Volcengine Ark Console](https://console.volcengine.com/ark/region:ark+cn-beijing/apiKey) | Seedance 2.0 video generation | required for v0.3.0+ real video; `--no-real-video` bypasses |
| `OPENROUTER_API_KEY` | [openrouter.ai](https://openrouter.ai) | (optional) alternate LLM provider | optional |

> ⚠️ The ARK API Key is **not** the same as a Volcengine IAM AK/SK (both are UUID-shaped but use different auth). Create it under "API Key Management" in the Ark console, then enable `Doubao-Seedance-2.0-fast` under "Activation → Vision Models" (default 5M tokens free).
>
> Switch model: `export ARK_VIDEO_MODEL=doubao-seedance-1-5-pro-251215` (or any other Ark model id).

Token lookup order (first found wins):
1. Corresponding env var (`TIKHUB_API_TOKEN` / `OFOX_API_KEY` / `ARK_API_KEY` / `OPENROUTER_API_KEY`)
2. `$CWD/.env`
3. `~/.config/content-engine/.env` (XDG standard)
4. Skill-root `.env`

### Verify

```bash
python3 scripts/extract_xhs.py --check
```

Reports each check ✅/❌/⚠️ with fix instructions.

### Mainland China users

- Main domain `api.tikhub.io` requires a proxy from inside China
- Mirror: `api.tikhub.dev` (no proxy needed) — set `TIKHUB_BASE_URL=https://api.tikhub.dev` in `.env`

### Feishu / Lark publishing (OpenClaw users only)

This skill does not bundle Feishu API code. To enable auto-publishing of deconstruction cards to Feishu Docx, install the OpenClaw Lark official plugin:

```bash
npx -y @larksuite/openclaw-lark install
```

Details: [OpenClaw Lark official plugin docs](https://www.feishu.cn/content/article/7613711414611463386)

Once installed:
- Agent in OpenClaw gains native "create cloud doc / read cloud doc / update cloud doc" tools
- SKILL.md Step 7 will direct the agent to use those tools for publishing
- Credentials are managed by the plugin; this skill needs zero Feishu config

**Claude Code or other environments**: deconstruction cards save to local `docs/deconstructions/`; copy to Feishu manually if needed.

---

## Related / Credits

- `analyze-xhs` skill: account-level analysis (not single-post)
- Architecture inspiration: [Ronin · How To Build Own Content Engine](https://x.com/DeRonin_/status/2042604279077237170) (the Skill Graph idea: use .md + wikilinks as the agent's "memory / soul")
- Chinese version: `~/.agents/skills/content-engine/`
