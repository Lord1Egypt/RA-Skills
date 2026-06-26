# Workflow Reference — xhsfenxi v2.0

---

## Source Ladder

Use sources in this order whenever possible:

### Level A — Primary public evidence

Highest trust for visible claims:

- Xiaohongshu search result pages
- creator homepage/profile pages
- user-provided screenshots from Xiaohongshu
- user-provided post links that are actually accessible

What you can safely claim from Level A:
- visible follower / note counts shown on page
- visible account ID / self-introduction
- visible recent titles / visible public engagement numbers
- posting cadence clues visible on page
- obvious content categories
- brand symbols and signature phrases (like "（劲爆）")

### Level B — Secondary public clues

Use as support, never as backend truth:

- podcast interviews
- encyclopedia entries
- public creator bios elsewhere
- analytics websites / public creator databases
- public brand collaboration listings

What Level B is good for:
- filling identity / background context
- confirming repeated themes
- spotting public commercialization clues
- triangulating a bigger narrative

### Level C — Synthesis / inference

Allowed only when clearly framed as interpretation.

Examples:
- "This account behaves more like a Type A 荒诞美学 creator than a Type B 共鸣命名 creator."
- "The recurring topic logic appears to be: contrast × literary naming × unified symbol."
- "The transferable lesson is not the tone, but the framing system."

Never present Level C synthesis as raw observed fact.

---

## Standard Execution Runbook

### Step 1 — Confirm the deliverable

Choose one or more:
- structured report
- viral topic formula
- archetype classification
- comparison report
- customized learning report
- Word / business version

### Step 2 — Capture the minimum task brief

Minimum useful brief:
- creator name
- available links or screenshots
- target output format
- whether a business Word version is required

### Step 3 — Archetype pre-classification

Before deep analysis, make a preliminary archetype call using visible signals:

| Signal | Likely archetype |
|--------|-----------------|
| Unified brand symbol/tag on every post | Type A 荒诞美学型 |
| High-production video, absurdist or philosophical content | Type A 荒诞美学型 |
| Posts name vague emotions or life stages | Type B 共鸣命名型 |
| Titles feel like thoughtful questions or redefinitions | Type B 共鸣命名型 |
| Titles contain conflict words ("骗子", "不要脸", "装") | Type C 现实策略型 |
| Content breaks unspoken workplace/relationship/money rules | Type C 现实策略型 |
| Mix of resonance + strategy | Mixed B+C |

### Step 4 — Research in layers

1. Find the account and public homepage/search data
2. Save visible account facts (follower count, note count, visible titles, engagement)
3. Pull representative visible titles — note brand symbols, title patterns
4. Add external public clues only where helpful
5. Record limitations before interpretation

### Step 5 — Extract the account system (Five Layers)

Always map these five layers:

1. **Identity** — who the creator is framed as; any self-labeling strategy
2. **Audience contract** — why people follow them; what emotional/strategic need is met
3. **Topic system** — what recurring problems/desires they cover; 3–6 topic models
4. **Expression system** — title formulas, brand symbols, opening patterns
5. **Transferability** — what another account can actually learn; what must not be copied

### Step 6 — Produce the right file

#### Structured report

Recommended top-level sections:
1. Account snapshot
2. Archetype classification + rationale
3. Positioning judgment
4. Audience and demand
5. Content pillars
6. Title / hook system (including brand symbol analysis)
7. Narrative structure
8. Commercialization clues
9. What to learn
10. What not to copy
11. Conclusion
12. (Optional) Full note list sorted by engagement

#### Viral topic formula

Recommended top-level sections:
1. Why this creator produces strong topics (archetype-based)
2. Total formula
3. 3–6 recurring topic models
4. Title formulas
5. Body structure formulas
6. Distribution / comment trigger clues
7. How to migrate it to another account
8. 10–30 topic directions

#### Comparison report (2–3+ accounts)

Recommended top-level sections:
1. Why compare these creators together
2. Archetype map (each creator's type)
3. Shared foundations
4. Key differences
5. Hybrid formula
6. Which path fits which use case
7. Suggested topic directions
8. Final recommendation

---

## Archetype-Specific Analysis Lenses

### Type A — 荒诞美学型

Focus questions:
- What is the brand symbol? (unified tag, phrase, or visual marker)
- How does the title create contrast? (grand × mundane, serious × absurd)
- Where does the humor come from? (earnest treatment of absurd things)
- What is the underlying philosophical/emotional core?
- Why is replication hard? (visual sensibility, accumulated aesthetic)

Key learning for other accounts:
- Find your own "brand symbol" — a unifying tag that creates recognition
- Train "contrast naming" — don't describe the place, name the feeling
- Practice "absurdist framing" — pick topics that are ridiculous when taken seriously

---

### Type B — 共鸣命名型

Focus questions:
- What life stages or emotional states does the account name?
- How does private experience become universal proposition?
- What are the signature conceptual phrases?
- What is the "new way to understand yourself" users get?

Key learning for other accounts:
- Practice "命题化" — reframe personal experience as a universal human situation
- Build a personal vocabulary of named states ("Odyssey时期", etc.)
- The formula: experience → proposition → naming → judgment → resonance

---

### Type C — 现实策略型

Focus questions:
- What real-world rules does the account break open?
- How does the self-labeling strategy work? (antifragile identity)
- What is the conflict word in each title?
- What is the "can-do action" users walk away with?

Key learning for other accounts:
- Find your "reality母题" — the real困境 you speak to
- Practice rewriting weak framings into strong rule-breaking framings
- The formula: 困境 → 说破 → 规则 → 策略 → 爽感

---

## Limitation Language

Use direct wording like:
- "This round is based primarily on public homepage/search-page evidence."
- "Single-post detail pages were not stably accessible due to platform risk control."
- "Third-party figures are used as directional clues, not audited backend data."
- "Archetype classification is based on visible patterns; the creator may operate differently at the full content level."

---

## Deep-Dive Upgrade Path

If the user wants finer analysis, ask for 3–10 representative posts, ideally with:
- screenshots of cover + title
- screenshots of body pages / subtitles
- comments screenshots
- transcript or summary if video-based

Then upgrade from account-level to post-level analysis.

---

## Word Output Workflow

### Overview

Always generate Markdown first, then convert to Word. Iterating Markdown is cheaper than re-generating DOCX.

### Script Selection Guide

Use the workflow archive scripts at:
```
openclaw_cosmo/afa/小红书分析与工作流归档/02-Word生成与目录修复脚本/
```

| Script | Use when |
|--------|----------|
| `build_docx6.py` | Default — most stable, use this first |
| `build_docx.py` → `build_docx5.py` | Earlier iterations, kept for reference/debugging |
| `inspect_docx.py` | Inspect internal XML, bookmarks, link structure |
| `fix_final2.py` | Final TOC / attribute fix after build |
| `fix_attrs.py` | Fix XML namespace attribute writing errors |
| `fix_wrong.py` | Targeted corrections for known wrong output |
| `check_it.py` | Verify output correctness |

### Word TOC Fix Checklist

When a generated .docx has broken TOC links:

1. Run `inspect_docx.py` — check `word/document.xml` for bookmark names and link types
2. Verify heading bookmarks use format `_TocH1_XXX` (not `#_TocH1_XXX`)
3. Verify internal links use Word-native anchor style, not external URL rels
4. If `elem.set()` errors appear, use full namespace: `elem.set('{' + W_NS + '}id', value)`
5. Run `fix_final2.py` after any XML edits
6. Test by opening in Word — click TOC entries to verify jump

### Common Errors

| Error | Cause | Fix |
|-------|-------|-----|
| Bookmark name wrong format | Missing `_TocH1_` prefix | Rename via `fix_attrs.py` |
| `anchor` contains `#` | Wrong anchor format | Strip `#` prefix |
| TOC uses external link rels | Used `http://` link type for internal jump | Switch to `w:instr` field or anchor |
| Duplicate headings in body | TOC headings accidentally inserted into body | Use `fix_wrong.py` to clean |
| Namespace attribute error | Missing full namespace URI in `elem.set()` | Use `'{' + W_NS + '}id'` form |

### Best Practice

- Keep only `build_docx6.py` as the production script
- Keep all earlier versions as debugging reference, not for production
- One Markdown → one `build_docx6.py` call → inspect → fix if needed
