# rune-slides

> Rune L3 Skill | media | model: tier:mid


# slides

> **RUNE COMPLIANCE**: Before ANY code response, you MUST:
> 1. Classify this request (CODE_CHANGE | QUESTION | DEBUG | REVIEW | EXPLORE)
> 2. Route through the correct Rune skill (see skill-router routing table)
> 3. Follow the skill's workflow — do NOT freelance or skip steps
> Violation: writing code without skill routing = incorrect behavior.

## Platform Constraints

- SHOULD: Monitor your context usage. If working on a long task, summarize progress before context fills up.
- MUST: Before summarizing/compacting context, save important decisions and progress to project files.
- SHOULD: Before ending, save architectural decisions and progress to .rune/ directory for future sessions.

## Purpose

Generates structured slide decks as Marp-compatible markdown. The agent analyzes context (feature, sprint, tutorial) and produces a JSON slide schema, then calls `build-deck.js` to convert it to presentation-ready markdown. The script standardizes output format — preventing agent freestyle errors when context runs low.

## Triggers

- User says "create slides", "make presentation", "demo deck", "sprint review slides", "tech talk"
- `/rune slides` — manual invocation
- Called by other skills needing presentation output

## Called By (inbound)

- `marketing` (L2): launch presentations, product demos
- `video-creator` (L3): slide-based video storyboards
- User: direct invocation

## Calls (outbound)

None — pure L3 utility.

## Executable Instructions

### Step 1: Analyze Context

Determine the presentation type from the user's request:

| Context | Template | Typical Slides |
|---------|----------|---------------|
| Feature demo | Demo walkthrough | Problem → Solution → Architecture → Live demo → Next steps |
| Sprint review | Sprint summary | Goals → Completed → Metrics → Blockers → Next sprint |
| Tech talk | Teaching format | Hook → Concept → Deep dive → Code examples → Takeaways |
| Tutorial | Step-by-step | Intro → Prerequisites → Step 1-N → Summary → Resources |
| Pitch | Persuasion | Problem → Market → Solution → Traction → Ask |

### Step 2: Generate JSON Schema

Create a JSON file following this schema:

```json
{
  "title": "Presentation Title",
  "author": "Author Name (optional)",
  "theme": "default|gaia|uncover",
  "slides": [
    {
      "type": "title|content|code|diagram|image|quote|section",
      "heading": "Slide Heading",
      "body": "Markdown body text",
      "notes": "Speaker notes (optional)",
      "code": { "lang": "javascript", "source": "console.log('hi')" },
      "diagram": "graph LR; A-->B"
    }
  ]
}
```

**Slide types:**
- `title` — opening slide with `# heading`
- `content` — standard slide with `## heading` + body
- `code` — slide with syntax-highlighted code block
- `diagram` — slide with Mermaid diagram
- `image` — slide with image reference in body
- `quote` — slide with blockquote formatting
- `section` — section divider with `# heading`

Save the JSON to a temporary file (e.g., `slides.json`).

### Step 3: Build Deck

Execute the build script:

```bash
node .openclaw/rune/skills/rune-slides-scripts/build-deck.js --input slides.json --output deck.md
```

The script outputs Marp-compatible markdown with:
- Marp frontmatter (`marp: true`, theme)
- Slide separators (`---`)
- Speaker notes as HTML comments
- Code blocks with language hints
- Mermaid diagram blocks

### Step 4: Present Result

Show the user:
1. The generated `deck.md` file path
2. How to preview: `npx @marp-team/marp-cli deck.md --preview` (or any Marp viewer)
3. How to export PDF: `npx @marp-team/marp-cli deck.md --pdf`

**Fallback**: If `.openclaw/rune/skills/rune-slides-scripts/build-deck.js` is unavailable, generate the Marp markdown directly — the script is an optimization, not a hard dependency.

## Output Format

```markdown
---
marp: true
theme: default
---

# Presentation Title

Author Name

---

## Slide Heading

Slide body content

<!-- notes: Speaker notes here -->
```

## Sharp Edges

| Failure Mode | Severity | Mitigation |
|---|---|---|
| build-deck.js not found | LOW | Agent generates Marp markdown directly (fallback) |
| Invalid JSON input | MEDIUM | Script exits 1 with parse error — agent fixes JSON and retries |
| Marp not installed | LOW | Script outputs plain .md — user installs Marp CLI separately |
| Too many slides (>30) | MEDIUM | Agent should split into multiple decks or summarize |

## Constraints

1. Output MUST be valid Marp markdown (parseable by `@marp-team/marp-cli`)
2. DO NOT embed build-deck.js source in this skill — call it via `.openclaw/rune/skills/rune-slides-scripts`
3. DO NOT require Marp installation — output is standard markdown that Marp can consume
4. Keep slide count reasonable (5-15 for demos, 10-25 for talks)
5. Always include speaker notes for non-trivial slides

## Returns

| Artifact | Format | Location |
|----------|--------|----------|
| Slide schema | JSON | `slides.json` (temporary) |
| Presentation deck | Marp Markdown | `deck.md` or user-specified path |

## Done When

- Presentation type identified (demo/sprint/talk/tutorial/pitch)
- JSON schema generated with correct slide types
- build-deck.js executed (or fallback markdown generated)
- Output file path presented to user
- Preview/export commands provided

## Cost Profile

~500-1500 tokens input, ~300-800 tokens output. Sonnet for quality copy and structure.

---
> **Rune Skill Mesh** — 64 skills, 203 connections + 40 signals, 14 extension packs
> [Landing Page](https://rune-kit.github.io/rune) · [Source](https://github.com/rune-kit/rune) (MIT)
> **Rune Pro** ($49 lifetime) — product, sales, data-science, support packs → [rune-kit/rune-pro](https://github.com/rune-kit/rune-pro)
> **Rune Business** ($149 lifetime) — finance, legal, HR, enterprise-search packs → [rune-kit/rune-business](https://github.com/rune-kit/rune-business)