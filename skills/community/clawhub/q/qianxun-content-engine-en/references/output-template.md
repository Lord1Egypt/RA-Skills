# Deconstruction Card Output Template

Every deconstruction uses this template. All fields stay even if you have no data — write "TBD" instead of skipping.

---

```markdown
# {Task ID} | {one-line title}

> Reference link: {original URL}
> Deconstructed at: {YYYY-MM-DD HH:mm}
> Platform: {Xiaohongshu / Douyin / WeChat Channels}
> Content type: {video / image}

## Metadata
- **Author**: {nickname}
- **Published**: {YYYY-MM-DD}
- **Engagement**: 👍 {liked} ｜ ⭐ {collected} ｜ 💬 {comment} ｜ 📤 {share}
- **note_id**: `{note_id}`

---

## I. Positioning

### 1. Content goal
{User-input goal, e.g., "drive in-store traffic + DM acquisition"; if not specified, write "Not specified"}

### 2. Target audience
{Persona inferred from desc / hashtags / comment behavior, 30–80 words. Example: 30-45 y/o, quality- and aesthetics-driven women who pay for materials and presence}

### 3. Viral theme
{One sentence: what this is about + why it went viral. 30–60 words}

---

## II. Deconstruction

### 4. Reference content deconstruction

{Video: by time segment; Image: by image order}

**Video example:**
```
0-2s ｜ Shot: medium
Visual: ……
Camera: locked / slow push
Caption: ……

3-5s ｜ Shot: ……
Visual: ……
```

**Image example:**
```
Image 1 (cover):
- Composition: ……
- Elements: ……
- Style: ……
- Role: ……

Image 2:
……
```

### 5. Style tags
`#xxx` `#xxx` `#xxx` (3–6 tags, comma or space-separated)

### 6. Scene tags
`xxx / xxx / xxx` (2–4 specific scenes)

### 7. Emotion hook
**Core emotion**: {Contrast / Aspiration / Identity / Healing / Cultural-pride / Practical-anxiety ...}

**Evidence**: {1-2 sentences explaining how this emotion is constructed}

### 8. Comment keywords

> Source: `comments.json`. You (agent) read raw text and classify into "ask / request / praise / objection".
> **Each entry must have raw-text evidence** — see "Comment keywords" section at the end of this doc, or SKILL.md Step 5c.

- **{keyword label}** ({N} raw comments: "text 1" "text 2" ...) — {one-line interpretation / conversion signal}
- **{keyword label}** ({N} raw comments: "text") — {interpretation}
- **⚠️ Objection · {topic}** ({N} raw comments: "text" 👍 {likes}) — {why it matters}

(If comments.json is `[]` or has `_error`, write "⚠️ Comment data not retrieved, manual fill recommended" and **don't infer from desc**)

---

## III. Copy

### 9. Reference voiceover/subtitles
{Video voiceover/subtitle original text, by paragraph or timestamp; for image posts write "N/A (image post)"}

### 10. Reference voiceover logic analysis
**Structure**:
- Layer 1 (X-X s): hook — ……
- Layer 2 (X-X s): setup — ……
- Layer 3 (X-X s): elevation — ……
- Layer 4 (X-X s): CTA — ……

**Key design choices**: {1-3 specific choices that make this copy work — contrast number opener, identity transplant, suspense ending, etc}

### 11. Reference cover copy
{Cover text}

### 12. Reference title
{title original}

### 13. Reference body copy
{desc original, preserving emojis and line breaks}

### 14. Reference hashtags
`#tag1 #tag2 #tag3 ...`

---

## IV. Takeaways

{2–5 bullets: how we'd apply this to our own content. The actual deliverable of the deconstruction.}

- ……
- ……
- ……

---
```

---

# Field definitions + Anti-Patterns

## Quick reference table

| Field | Required | Length | Form | Example |
|---|---|---|---|---|
| Task ID | ✅ | short | `AIC-{YYMMDD}-{seq}` | `AIC-260426-001` |
| Content goal | 🟡 | one line | noun phrase | drive in-store traffic + DM acquisition |
| Platform | ✅ | short | enum | Xiaohongshu / Douyin / WeChat Channels |
| Target audience | ✅ | 30–80 words | persona w/ evidence | 30-45 y/o quality-driven women paying for materials |
| Viral theme | ✅ | 30–60 words | mechanism sentence | "Uses pure visual aesthetics to convert 'watching' into 'imagining myself wearing it', activating high save intent" |
| Reference content deconstruction | ✅ | long | structured (aggregated) | see template above |
| Style tags | ✅ | 3–6 | adjectives/genres (mark "existing/new") | Old-money, Effortless, Premium, Linen |
| Scene tags | ✅ | 2–4 | noun phrases (environments) | beach vacation, urban commute, tea room |
| Emotion hook | ✅ | core + evidence | two-layer | Contrast｜Age × Achievement \| hits graph hooks |
| Comment keywords | 🟡 | 3–8 | keyword + **raw evidence** | how-do-i-buy (raw: "how do I buy this") |
| Reference voiceover | video req | original | verbatim | "I have an unusual boss…" |
| Voiceover logic analysis | video req | mid-long | **layered** structure | Layer 1 (0-12s): establishes contrast and curiosity… |
| Reference cover copy | ✅ | one line | text | "What does it feel like to wear spring?" |
| Reference title | ✅ | title | original | "Shenzhen ｜ …" |
| Reference body copy | ✅ | full | **original** (with emojis + breaks) | "OMG family! …💚" |
| Reference hashtags | ✅ | all | `#xxx` joined (from `hash_tag[].name`) | #heritage #vintage #craft |
| Takeaways | ✅ | 2–5 | bullets (mode-dependent) | see mode notes below |

---

## Anti-Patterns for subjective fields (critical)

### Viral theme
Explain **why it went viral** (mechanism), not **what it is** (description).

| ❌ Descriptive | ❌ Marketing-speak | ✅ Insight-driven |
|---|---|---|
| "Showcases new spring collection" | "Heritage aesthetic recommendation" | "Uses pure visuals to convert 'watching' into 'imagining wearing it', activating high save intent" |
| "Founder shares startup story" | "75-born female owner shows craftsmanship" | "Uses '75-born × 2000m² store' numeric contrast to anchor 'craft × scale' trust" |

**Self-check**: does your sentence explain "why this gets saved, not just liked"? No → rewrite.

### Style / Scene / Emotion-hook (most-confused trio)

| Dimension | Definition | Form |
|---|---|---|
| **Style** | how it looks/feels | adjectives, genre words |
| **Scene** | where it happens | noun phrase, environment |
| **Emotion hook** | what it stirs in the user's mind | "{emotion-class}｜{technique}" two-layer |

| ❌ Bad (isolated word, adjective stack) | ✅ Good (two-layer + mechanism) |
|---|---|
| "beauty" | **Aspiration｜atmospheric immersion** (no-voice merchandising builds "I want to own this" via pure visuals) |
| "premium" | **Identity｜transplant ('wearing this = being a certain person')** ("effortless old-money daughter energy") |
| "contrast" | **Contrast｜age × achievement** (specific numbers create identity contrast) |

### Voiceover logic analysis

Must be **layered**, not a flowing paragraph. Each layer: timestamp + one-line function.

| ❌ Flowing paragraph | ✅ Layered structure |
|---|---|
| "Opens with startup story, middle covers craftsmanship, ends with resonance, well-structured overall" | Layer 1 · Establish contrast and curiosity (0-12s): "75-born + 2000 m²" numeric contrast triggers curiosity<br>Layer 2 · Convey craftsmanship and value (12-28s): "personal QA, hand-checked" details build the master-craftsman image<br>Layer 3 · Land emotional resonance (28-39s): rises from product to emotion, completing elevation |

End with **Key design choices** (1-3 specific choices that make this copy work — contrast numbers, craft nouns, time anchors, etc).

### Target audience

Must come **with evidence**, not a vague persona.

| ❌ Vague | ✅ With evidence |
|---|---|
| "30-45 y/o aesthetic-minded women" | 30-45 y/o, heritage-aesthetic women who value materials and craftsmanship (evidence: comments cluster on "how do I buy" and color-specific items "green vest"; desc emphasizes "silk emerald, hand-beading"; save-to-like ratio 70% indicates long decision cycles) |

**Brand-aware mode**: must explicitly mark "matches segment {name} in graph/audience/segments".

### Takeaways (mode-aware)

#### Mode A · graph populated (brand-aware)
Write "how WE'd do the same theme X" — specific to brand actions.

| ❌ Generic | ✅ Brand-specific |
|---|---|
| "Numeric contrast is a good hook" | "Our '17 years founded / 25 years specialized / 200+ SKUs' can serve as our equivalent contrast, paired with founder on-camera (referencing the «pre-founding-era expertise» in graph/brand/brand-story)" |

#### Mode B · graph not populated (objective)
Write objective takeaways + actionable suggestions (not brand-specific). Each bullet: **observation → inference → recommendation** (3 segments).

```
✅ Example:
- Pure-visual merchandising can also drive high engagement (save-to-like 70%) → only works
  when product visual is strong + body copy is rich enough to compensate for missing voiceover
  → high-AOV / aesthetic-driven categories suit this formula
```

---

## Comment keyword semantic classification + anti-fabrication (you do it, no regex)

> Old version used regex to pre-extract keywords into `keywords.json`. Removed because language has infinite variants ("how do I buy" / "how much" / "is it pricey"), regex always misses; regex also can't read context ("price isn't a problem" isn't an inquiry). Permanently deprecated.
>
> Agent reads `comments.json` directly and classifies semantically — LLM is 100x better than regex, zero blindspots, zero maintenance.

### Data source

`comments.json` (already filtered by parser — `is_pinned=True` for merchant pins / anti-scam is auto-flagged and skippable; rest are real users).

### Four classes

| Class | Capture | Typical phrases |
|---|---|---|
| **ask** | Asking purchase path / price / address / hours / channels | how do I buy, how much, what's the price, where's the store, opening hours, do you sell online |
| **request** | Active need (strong intent) | need WeChat, still in stock, size sold out, need contact, restocking? |
| **praise** | Resonance / specific likes | so beautiful, want it, premium feel, elegant, tempting, gorgeous |
| **objection** | Correction / disagreement (**not neutral questions**) | please don't call this X, this is A not B, shouldn't be this expensive |

### Output format (with evidence per entry)

```
- {keyword label} ({N} raw comments: "text 1" "text 2" "text 3") — {one-line interpretation / signal judgment}
```

### Hard anti-fabrication rules

1. Each keyword must include 1-3 **original comment texts** (copy directly from comments.json, no rewriting)
2. Keywords without raw-text evidence are **not allowed** — no fabrication
3. **Questions ≠ objections**: "isn't this silk?" is neutral (goes to ask); "please don't call it 新中式" is an objection
4. Same comment can fall in multiple classes — quote it under each
5. comments.json is `[]` or has `_error` → write "⚠️ Comment data not retrieved", **don't infer from desc**

### Good vs Bad

```
✅ Good (evidence + interpretation):
- how-do-i-buy (5 raw comments: "how do I buy the green pants" "how to purchase, online?" "how do I buy this love the green") —
  highest-frequency conversion signal
- how-do-you-sell / pricing (2 raw comments: "how do you sell this" "what's the price for this set") —
  alternative phrasings of pricing inquiry
- objection-traditional-attire (1 raw comment: "this is Manchu attire, please don't call it 新中式" 👍 1) —
  only 1 comment but liked — signals tag-usage edge case

❌ Bad (no evidence / fabricated):
- how-do-i-buy, how-much, need-link (just listing words, no raw text — forbidden)

❌ Bad (misclassifying questions as objections):
- objection (comment: "is this silk?")  ← this is a question, not an objection
```

---

## Reference hashtags cleanup rules

**Source**: API's `hash_tag[].name`, NOT `topics[]` (topics is curated by algorithm, usually 1-2 entries, subset of hash_tag).

**Cleanup**:
- Use the `hash_tag` field directly — output is a clean string array (no `[话题]` render markers)
- **Don't** grep `#xxx[话题]#` from the desc text — desc has rendering markers; if you must use desc, run `sed 's/\[话题\]//g'` to clean
- Preserve API order (≈ author priority)
- Join all with `#`

```
✅ #heritage #downtown-discovery #craft
❌ #heritage[话题]# #downtown-discovery[话题]#
```
