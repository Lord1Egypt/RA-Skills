# Phase 4 Reference — Content Writing Guidelines

## TOC

- §1 Pre-Write Gate (pre-writing checklist)
- §2 XHS Content Format Hard Requirements
- §3 Writing Framework
- §4 De-AI Checklist
- §5 Topic Tag Strategy
- §6 Image Copy (Text-to-Image)
- §7 HTML Preview Template
- §8 User Approval Flow

---

## §1 Pre-Write Gate

All 5 items below must be confirmed ready before writing begins; if any is missing, pause and prompt the user to provide it:

1. ✅ `key_quote` extracted from Phase 1 deep (verbatim from original post)
2. ✅ `pain_description` confirmed (1–2 sentences on user pain point)
3. ✅ `tools_tried` confirmed (solutions the user already attempted)
4. ✅ Product info read from `session_state.json` (product name, install command, link)
5. ✅ `style_fingerprint.json` read (Phase 2 style fingerprint)

---

## §2 XHS Content Format Hard Requirements

| Item | Requirement | Notes |
|------|-------------|-------|
| Title | **≤ 20 characters** | Must use native setter when writing; exceeding the limit won't error but publish will fail |
| Body | ≤ 1000 characters | Beyond this, users' scroll intent drops |
| Paragraphs | 30–60 chars/paragraph | Blank line between paragraphs, mobile-friendly |
| Topic tags | 3–5 `#tags` | Must be existing platform topics |
| CTA | Required at end | Comment prompt / save reminder / follow prompt — one or combined |
| External links | **Prohibited** | Body containing http/www links triggers throttling |
| Contact info | **Prohibited** | WeChat ID / phone number / email all trigger risk control |

---

## §3 Writing Framework (Pain → Struggle → Discovery → Proof → Invitation)

**Title** (≤ 20 characters):
- Pain-point type: `😱 <pain scenario>? <solution preview>`, e.g.: `😱 <core pain>? This fixes it`
- How-to type: `<number> methods | <scenario description>`, e.g.: `3 methods to solve <pain keyword>`
- Story type: `<scenario> + <turning point result>`, e.g.: `Using {product.name}, <core benefit>`

**Body structure** (expand in order, none may be skipped):

```
[Opening — Pain resonance] (40–80 chars)
Simulate or directly quote user pain point, create "this is exactly me" immersion.
Quote key_quote (with quotes or > format).

[Struggle — Attempts and failures] (60–100 chars)
Describe the tools_tried solutions the user (or author) already tried, explain why they fell short.
Be specific, not vague.

[Discovery — The turning point] (50–80 chars)
Naturally introduce {product.name}, use one or two sentences to explain its core differentiator.
Do not pile up feature lists — only say the one point that solves the pain above.

[Proof — Concrete evidence] (80–150 chars)
Give verifiable specifics: install/usage method, core usage, or result numbers.
If session_state.json install_cmd is non-empty, quote that command:
  {product.install_cmd}
If product has no install command (SaaS/App), replace with concrete operation steps or screenshot description.
Core usage examples (pick 1–2 specific operations based on product info from session_state.json).

[Invitation — Closing CTA] (20–40 chars)
Use style_fingerprint.cta to choose:
  Question type: How do you usually solve <pain>? Chat in comments 👇
  Save type: Save this first, you'll definitely need it 🔖
  Combined: Save this post, let me know your needs in comments 👇🔖
```

---

## §4 De-AI Checklist

After writing, check each item against the body; rewrite anything that fails:

- [ ] No AI high-frequency phrases like "in conclusion" / "to summarize" / "in-depth analysis"
- [ ] No three or more consecutive paragraphs with the same sentence structure
- [ ] No identity-cliché openings like "As a developer" / "As a programmer"
- [ ] No meaningless praise like "this tool is powerful and high-performing"
- [ ] Body has at least one specific number or command (can't be all abstract description)
- [ ] Title and opening emoji count ≤ 2 (XHS prefers 1–2, too many looks spammy)
- [ ] Full text contains no URLs (external links trigger throttling)
- [ ] Competitor comparisons contain no unverifiable specific numbers or performance claims; only mention publicly known limitations, no fabricated data

---

## §5 Topic Tag Strategy

Tag combination principle (3–5 tags):

```
#<high-traffic generic word>   # high-traffic topic related to product positioning
#<specific scene word>         # directly related to the pain point of this post
#<category word>               # product category word
#{product.name}                # brand word (read from session_state.json)
```

Tag format: directly after body (after CTA), one space between each tag:
```
#<generic> #<scene> #{product.name} #<category>
```

**Prohibited**: do not create new topics (only use existing platform topics), do not pile up unrelated tags.

---

## §6 Image Copy (Text-to-Image)

Use XHS Creator Center's built-in "文字配图" (Text-to-Image) feature to generate a cover image — no external AI image needed.

Image copy requirements:
- Title (large text): same as or slightly simplified from note title, ≤ 12 characters
- Subtitle (small text): supplementary description or keywords, ≤ 20 characters
- Background style: choose "tech" or "minimal" theme (matches technical content)

Text-to-image invocation flow: see `references/phase5-publish.md §2`.

---

## §7 HTML Preview Template

After writing, generate HTML preview to display in conversation (do not open a browser):

```html
<div style="font-family:sans-serif;max-width:375px;border:1px solid #eee;border-radius:12px;padding:16px;background:#fff">
  <div style="font-size:15px;font-weight:bold;color:#333;margin-bottom:12px">
    📱 Note Preview
  </div>
  <div style="background:#f8f8f8;border-radius:8px;padding:12px;margin-bottom:12px">
    <div style="font-size:13px;font-weight:600;color:#111;margin-bottom:8px">{TITLE}</div>
    <div style="font-size:12px;color:#555;line-height:1.8;white-space:pre-wrap">{BODY}</div>
  </div>
  <div style="font-size:11px;color:#999">
    Chars: {CHAR_COUNT} / 1000 &nbsp;|&nbsp; Title: {TITLE_LEN} / 20
  </div>
  <div style="margin-top:8px;font-size:11px;color:#ff2442">
    {TAGS}
  </div>
</div>
```

Field notes:
- `{TITLE}` — note title (show char count, highlight red if > 20 chars)
- `{BODY}` — body text (preserve line breaks)
- `{CHAR_COUNT}` — body character count
- `{TITLE_LEN}` — title character count
- `{TAGS}` — topic tag list

---

## §8 User Approval Flow

After showing the preview, ask:

```
Preview above. Publish?
- "ok" / "publish" — proceed to Phase 5
- "edit: <instruction>" — apply instruction, re-preview
- "draft" — save as draft, don't publish
- "skip" — skip this post
```

When user inputs `edit: <instruction>`:
1. Identify edit scope (title / body / tags / full)
2. Apply instruction
3. Show preview again, ask again

**After writing all selected topics**, enter Phase 5 for batch publishing (not per-post).
