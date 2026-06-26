---
name: podcast
description: >-
  Two-host podcast video for any URL or free-form topic — 1 minute, 4 acts × ~15s,
  native multi-shot dialogue, optional voice cloning for Host A. Use when the user
  asks to "make a podcast", "podcast about [thing]", "podcast review of [url]",
  "two-host explainer", "interview-style clip", "two people talking on camera",
  "I/me and X talk about Y", or "interview with [persona] about [topic]". Native
  audio is the deliverable; captions are skipped by default because podcast dialogue
  mistranscribes domain terms.
argument-hint: <url-or-topic> [bg_img=] [host_a_img=] [host_b_img=] [voice_a=] [voice_b=] [use_avatar] [aspect_ratio=16:9]
---

# /pika:podcast

4 acts × 15s each = 60s. Host A always LEFT, Host B always RIGHT. Accepts a URL **or** a free-form topic / brief.

## Parameters

| Param | Default | Notes |
|---|---|---|
| `input` | required | URL to review **or** free-form topic / brief (e.g. "I and Elon Musk talk about Mars") |
| `bg_img` | auto-generated | Podcast studio background |
| `host_a_img` | auto-generated | Host A portrait — see Real-person handling below |
| `host_b_img` | auto-generated | Host B portrait — see Real-person handling below |
| `voice_a` | `876341503281471517` | Kling preset or cloned voice ID for Host A |
| `voice_b` | `829837252279803904` | Kling preset or cloned voice ID for Host B |
| `use_avatar` | off | Clone user's identity voice as Host A via `clone_voice` |
| `aspect_ratio` | `16:9` | Output aspect ratio |

## Defaults — fire fast, no mid-flow confirmation

- **Use the param-table defaults silently for voices.** `voice_a` defaults to the Kling preset `876341503281471517` and `voice_b` to `829837252279803904`. Do **not** ask "which voice?" or "should I clone yours?" before firing — only honor explicit overrides (`voice_a=`, `voice_b=`, `use_avatar`).
- **Auto-generate any missing host portraits silently** (Step 1's archetype prompts). Do **not** ask "should I generate a host image?" — just generate.
- **No "type yes to proceed" gates.** Submit → render the 4 acts → return URL. Account credit balance + provider failover are the canonical guardrails. The `--yes` flag is accepted as a no-op for backward compatibility.
- **Topic-mode personas (Step 3)** — when the user names a real public figure, follow Step 4 (Real-person handling) silently: archetype portrait by default, no auto-generated photographic likeness, no question to the user about likeness rights.

## Local images on Claude Desktop

Claude Desktop can't pass inline-pasted images to MCP tools yet (Anthropic-side limitation). If the user pastes a photo inline, or mentions a local file they want as `host_a_img` / `host_b_img`, pause Step 1 and kindly send them this — something like:

> Heads up — pasted images don't reach MCP tools on Claude Desktop yet (Anthropic limitation). Two easy options for your photo:
>
> - **Paste a URL** if it's already hosted (Imgur, S3, your site) — fastest
> - **Attach the image file** so I can upload it before generation.

When a local file arrives, convert it to a public URL with `upload_asset` and use the returned `public_url` as the parameter before Step 1. Already-hosted `https://...` URLs work as-is and skip this entirely.

If the user names a real public figure without attaching anything, do NOT auto-generate their likeness — Step 4 (Real-person handling) uses an archetype portrait instead.

## Steps

### 0. Resolve input (empty-args menu)

Strip flags (`--yes`, `--no-captions`, etc.) and `key=value` parameters from `$ARGUMENTS`. **If what remains is empty or whitespace-only**, print this menu **verbatim** as your full response, then **stop and wait for the user's next message** — do NOT call any tool, do NOT proceed to Step 1, do NOT invent a topic or URL. If the stripped input is non-empty (a URL or any prose), skip this step silently and proceed to Step 1.

> **What would you like a podcast about?** I can take any of:
>
> - **A website URL** (product page, docs site, launch page) — e.g. `https://pika.art`
> - **A GitHub repo** — e.g. `https://github.com/anthropics/claude-code`
> - **A blog post / article URL** — e.g. a recent piece you'd like discussed
> - **A free-form topic or brief** — e.g. *"I and Elon Musk talk about Mars"* or *"two scientists debate AGI"*
>
> Reply with your choice and I'll generate a 1-minute two-host podcast video (4 acts × ~15s).
>
> *Tip: you don't need to type `/pika:podcast` — just say things like "make a podcast about <topic>", "podcast review of <url>", or "I and <persona> talk about <topic>" and I'll fire this skill automatically.*

When the user replies, treat their reply as the resolved input (URL or topic) and proceed to Step 1. Do not re-prompt.

### 1. Generate missing assets (parallel)

Generate only what's not provided. Default archetype prompts:
- `bg_img` — modern podcast studio, two chairs, warm lighting, no people, 16:9
- `host_a_img` — enthusiastic host, studio portrait, left-side framing, 1:1
- `host_b_img` — pragmatic skeptic host, studio portrait, right-side framing, 1:1

If the input mentions specific personas (Step 3), tune the archetype to match the persona vibe — see Real-person handling below.

### 2. Resolve voice IDs (only if `use_avatar` is set)

1. Call `identity_voice_info` → `{ voice_id, platform, sample_url }`
2. If `sample_url` is present: call `clone_voice(voice_url=sample_url, voice_name="host_a_voice")` → set `voice_a` to the returned Kling voice ID

### 3. Parse input mode — URL vs topic

Strip flags (`--yes`, `--no-captions`, etc.) and key=value parameters from `$ARGUMENTS`. Inspect what remains.

**URL mode** — input contains a `https?://` URL:
- Call `capture_website` on the URL.
- Extract: product name, value prop, 2–3 specific features or facts, pricing, one jokeable detail.
- Use these as the script's factual anchors.

**Topic mode** — input is free-form prose (no URL):
- Treat the whole input as the brief. Parse for:
  - **Subject** — what the conversation is about
  - **Hosts** — explicit if mentioned ("I and Elon Musk", "two scientists", "Joe and Sarah"); otherwise use defaults (enthusiastic host + skeptic host)
  - **Angle** — debate / interview / explainer / casual
  - **Concrete facts** — any specific claims, numbers, dates, quotes the user gave
- If no concrete facts are given, use **2–3 clearly framed observations or hypotheses** to anchor jokes and the "wait, actually..." pivot. Do not present invented claims as facts; if factual accuracy matters for the topic, ask for a source or URL.
- If the user says "I and X" or "me and X", Host A = the user (use `use_avatar` flow if not already, or default avatar) and Host B = X.

### 4. Real-person handling (topic mode only)

If the parsed input names a specific real public figure as a host (e.g. "Elon Musk", "Taylor Swift", "Joe Rogan"):

- **Default behavior**: do NOT auto-generate that person's photographic likeness. Generate an **archetype portrait** matching the persona vibe — e.g. "tech-billionaire-energy CEO at a podcast desk" for an Elon-style host, "pop-star aesthetic" for a Taylor-style host. Clearly inspired-by, not impersonation.
- **Override**: if the user explicitly provides `host_a_img=<url>` or `host_b_img=<url>`, use the provided image as-is. The user takes responsibility for likeness rights.
- **Voices**: same logic — default to a generic Kling preset; only use a cloned voice when the user provides one (`voice_a=` / `voice_b=`) or invokes `use_avatar` (which clones the user's own voice for Host A).
- **Script tone**: the dialogue can riff on the named persona's known public positions or vibe (e.g. Mars enthusiasm for Elon-style) — public-record opinions are fair game. Do NOT put specific defamatory, off-character, or fabricated-private-life statements in their mouth.

This guardrail keeps the skill creative ("I want a podcast where I argue with a tech CEO about Mars") without auto-generating deepfakes of named real people.

### 5. Write script

Write 4 acts × 2 lines (HOST_A / HOST_B). Each line ~10–12s of spoken dialogue.

**Required (Matan rules — apply to both URL and topic modes):**
- One specific joke tied to a concrete detail (scraped fact in URL mode; topic-derived claim in topic mode)
- One "wait, actually..." skeptic-flip moment
- At least one mid-sentence interruption
- Natural filler: "okay so", "wait", "right?", "i mean", "honestly"
- Real reactions, not generic praise
- Reference at least one actual feature name, price, claim, or quote
- Natural ending — no forced "bye!"

Acts: Hook → Feature deep-dive → The Turn → Verdict
(In topic mode the analogue: Hook → Substance → The Pivot → Verdict.)

### 6. Generate video acts (subagent, sequential)

Delegate to a subagent with all resolved assets and the script. The subagent runs acts 1→2→3→4 sequentially — do NOT parallelize.

Each act: one `generate_reference_video` call (`kling-v3-omni`, `duration=15`, `sound=true`). Pass `reference_images=[bg_img, host_a_img, host_b_img]` and `voice_ids=[voice_a, voice_b]`. Optional knobs (added by `pika-mcp-server` BACK-339, 2026-05-10): `quality_mode: "pro"` for higher-fidelity kling output (longer wall-clock; reserve for high-stakes renders), and `kling_model` to pin a specific kling family member if you need reproducibility across runs. Three shots:

- Wide 5s: both hosts, no voice token
- MCU-A 5s: `<<<voice_1>>> '<HOST_A line>'`
- MCU-B 5s: `<<<voice_2>>> '<HOST_B line>'`

Emotional beats per act:
- Act 1: A excited, B skeptical
- Act 2: A gesturing/explaining, B questioning
- Act 3: A firm, B surprised and reconsidering
- Act 4: A satisfied, B conceding

After act 4, subagent calls `edit_concat([act1, act2, act3, act4])` and returns the final video URL.

### 7. Output

Return the final video URL and a one-sentence verdict. **Do not call `add_captions`** — Whisper auto-transcription is unreliable on the domain-specific terms typical of podcast dialogue (product names, persona names, technical jargon). Native Kling Omni audio is the deliverable.

---

**Rules:**
- `voice_ids` must be valid Kling voice IDs — never use name-style strings like `Calm_Man`
- Host A always LEFT (`<<<image_2>>>`), Host B always RIGHT (`<<<image_3>>>`) — never swapped

## Load-bearing phrases

These anchors keep the podcast output coherent across URL and topic modes:

| Phrase | Where | Why load-bearing |
|---|---|---|
| `Host A always LEFT, Host B always RIGHT` | Layout and shot prompts | Prevents host identity swapping across the four separate act renders. |
| `4 acts × 15s each` | Overall structure | Keeps the concat predictable and avoids uneven act pacing. |
| `Hook → Feature deep-dive → The Turn → Verdict` | Script structure | Gives the episode a conversational arc instead of four disconnected reactions. |
| `wait, actually...` skeptic-flip moment | Script requirements | Creates the pivot that makes the podcast feel like a real exchange. |
| `Do not call add_captions` | Output rule | Avoids low-quality burned captions on fast two-host dialogue with names and jargon. |

## Engine choice: Kling v3-omni for native two-host dialogue

Use Kling v3-omni for the four acts because it supports native dialogue with two reference hosts and voice tokens in a single shot plan. The tradeoff is that acts run sequentially for consistency and can take longer than pure edit/composite flows. Do not add a separate caption or music layer by default; the value of this skill is the native spoken exchange.

## Runtime expectations

Typical wall-clock is 8-18 minutes:

| Step | Wall clock | Notes |
|---|---:|---|
| Missing asset generation | 30-90s | Skipped for provided background/host refs |
| URL/topic parse + script | 1-3 min | URL mode depends on page fetch quality |
| Four Kling acts | 6-14 min | Runs sequentially to reduce host/voice drift |
| Concat + return | 30-90s | Final URL only; captions skipped by default |

## Examples

URL mode (review a website / repo / blog):

```
/pika:podcast https://pika.art
/pika:podcast https://github.com/anthropics/claude-code
/pika:podcast https://cursor.com use_avatar
```

Topic mode (free-form brief):

```
/pika:podcast Two AI researchers debate whether AGI arrives before 2030
/pika:podcast I and a Mars-obsessed tech CEO talk about colonization timelines
/pika:podcast interview with a seed-stage VC about what kills most startups
/pika:podcast podcast about quantum computing breakthroughs in 2026
```

Mixed (URL inside a topic prompt — agent prefers URL mode if a valid URL is found):

```
/pika:podcast podcast about https://pika.art with skeptical investor energy
```
