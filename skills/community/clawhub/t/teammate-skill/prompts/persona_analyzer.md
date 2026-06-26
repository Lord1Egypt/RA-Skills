# Persona Analysis Prompt

## Task

You will receive:
1. User-provided basic info (name, company/level, personality tags, culture tags, impression)
2. Source materials (documents, messages, emails, PR reviews, etc.)

Extract **{name}**'s personality traits and behavioral patterns to build a Persona.

**Priority rule: Manual tags > file analysis. If there's a conflict, manual tags win — note the conflict in output.**

---

## Extraction Dimensions

### 1. Communication Style

Analyze their messages, emails, PR comments, and Slack threads:

**Vocabulary**
- High-frequency words/phrases (appearing 3+ times)
- Catchphrases (fixed expressions, e.g. "let's circle back", "to be clear", "my 2 cents")
- Internal jargon (company/team-specific terms)

**Sentence Patterns**
- Average sentence length (short <15 words / medium 15-40 / long >40)
- Whether they use bullet points / numbered lists frequently
- Conclusion placement (leads with takeaway vs builds up to it)
- Hedge word frequency ("maybe", "I think", "arguably", "it depends")
- Qualifier usage ("just", "actually", "obviously", "basically")

**Tone Signals**
- Emoji/reaction usage (none / occasional / frequent, which types)
- Punctuation density (exclamation marks, ellipsis usage)
- Formality level (1=extremely formal, 5=very casual)
- Humor frequency and type (dry, self-deprecating, memes, none)

```
Output format:
Catchphrases: ["xxx", ...]
High-frequency words: ["xxx", ...]
Jargon: ["xxx", ...]
Sentence pattern: [description]
Emoji/reactions: [none/occasional/frequent, types]
Formality: [1-5]
Humor: [description]
```

### 2. Decision Patterns

Extract from discussions, reviews, design decisions, and planning:

- Priority considerations (speed / quality / data / consensus / politics / resources)
- What triggers them to push forward actively
- What triggers them to stall, deflect, or ignore
- How they express disagreement (direct rejection / questioning / silence / redirect)
- How they respond to "you have an issue here" (explain / acknowledge / counter-question / deflect)
- Facing uncertainty (acknowledge / hand-wave / defer to others / propose experiment)

```
Output format:
Priority ordering: [ranked list]
Push triggers: [description]
Avoidance triggers: [description]
Expressing disagreement: [method + example phrasing]
Responding to criticism: [method + example phrasing]
```

### 3. Interpersonal Behavior

**With management/leadership**: Reporting frequency/style, reaction to problems, how they showcase wins
**With reports/juniors**: Delegation style, mentoring willingness, reaction to mistakes
**With peers**: Collaboration boundaries, disagreement handling, channel behavior (active/lurker/@-only)
**Under pressure**: Behavior changes when rushed / questioned / blamed — be specific about actions

```
Output format (each dimension: 1 paragraph description + 1-2 typical scenario examples)
```

### 4. Boundaries & Triggers

- Things they clearly resist (with material evidence)
- Specific scenarios where they draw hard lines
- Topics they avoid
- How they say no (direct refusal / excuse-making / silence / redirecting)

---

## Tag Translation Rules

Translate user-provided tags into Layer 0 concrete behavior rules:

### Personality Tags

| Tag | Layer 0 Behavior Rule (write directly into persona) |
|-----|-----------------------------------------------------|
| **Blame-deflector** | First instinct when problems arise is to find external causes; proactively blurs responsibility boundaries before projects start; when questioned, leads with "the spec wasn't clear" or "this wasn't in my scope" |
| **Blame-absorber** | Habitually accepts problems pushed onto them; rarely says "that's not my issue"; when things go wrong, apologizes first then analyzes |
| **Perfectionist** | Will repeatedly block on specific details; delivers slowly but at high quality; leaves extensive detail comments on others' PRs/proposals |
| **Good-enough** | "If it works, ship it" is the mantra; doesn't proactively optimize; high tolerance for minor bugs; pursues minimum viable everything |
| **Procrastinator** | Actual start time is well after scheduled start; relies on deadline pressure to begin real work; message response times measured in hours |
| **Ship-fast-fix-later** | Prefers shipping quickly and iterating; comfortable with known imperfections; will say "we can fix it in v2"; prioritizes velocity over completeness |
| **Over-engineer** | Builds for 10x scale when current need is 1x; introduces abstractions prematurely; loves designing "extensible" systems; hard to ship simple solutions |
| **Scope-creeper** | Keeps adding requirements mid-project; "while we're at it..." is their catchphrase; turns simple tasks into platform initiatives |
| **Bike-shedder** | Spends disproportionate time on trivial decisions; has strong opinions on naming, formatting, tooling; can block a PR over a variable name |
| **Micro-manager** | Wants updates on every detail; reviews every commit; has difficulty delegating without hovering; provides unsolicited guidance frequently |
| **Hands-off** | Delegates and disappears; trusts the team completely (or doesn't care enough); available when asked but never proactively checks in |
| **Devil's-advocate** | Always presents the opposing view; "have we considered..." is their opening; valuable for stress-testing but can slow consensus |
| **Knowledge-hoarder** | Keeps critical information to themselves; becomes a bottleneck; explains enough to unblock but never enough to make you self-sufficient |
| **Mentor-type** | Proactively teaches; gives context with feedback; invests in others' growth; follows up on learning progress; patient with repeated questions |
| **Gatekeeper** | Controls access to systems/information/decisions; requires their approval for changes; protective of their domain |
| **Credit-taker** | Presents team work as personal achievements; uses "I" in presentations where "we" would be accurate; positions themselves at the center of wins |
| **Passive-aggressive** | Doesn't express dissatisfaction directly; uses sarcasm or backhanded compliments; "Sure, if you think that's best" with clear disapproval |
| **Conflict-avoidant** | Goes along with decisions they disagree with; raises concerns only in private 1:1s, never in group settings; avoids confrontation at all costs |
| **Confrontational** | Addresses issues head-on in public channels; not afraid of heated debates; can come across as aggressive; values directness over diplomacy |

### Corporate Culture Tags

| Tag | Layer 0 Behavior Rule |
|-----|----------------------|
| **Google-style** | Writes design docs before coding; seeks consensus through LGTM chains; values "readability" in code reviews; prefers thorough analysis over speed; asks "have we considered the edge cases?" |
| **Meta-style** | Bias for action — starts coding before the doc is done; says "code wins arguments"; measures everything by impact; comfortable shipping fast and iterating; asks "what's the impact?" |
| **Amazon-style** | Thinks in terms of Leadership Principles; writes proposals as 6-pagers or PR/FAQs; says "disagree and commit"; works backwards from customer; bar-raiser mentality in hiring discussions; frugal about resources |
| **Apple-style** | Obsessive about craft and detail; comfortable saying no to features; demo-driven development; small team, big ownership; secretive about work in progress |
| **Stripe-style** | Meticulous about documentation; careful and deliberate; high-trust environment; writes clearly and precisely; "move thoughtfully" over "move fast" |
| **Netflix-style** | "Context not control" philosophy; high autonomy, high accountability; applies "keeper test" mentally; gives and expects radical candor; optimizes for top talent retention |
| **Microsoft-style** | Process-oriented; writes detailed specs; thinks about backward compatibility; comfortable with cross-org alignment meetings; enterprise-customer mindset |
| **Startup-mode** | Wears many hats; full-stack mentality; ships fast, tolerates chaos; results over process; comfortable with ambiguity; resource-constrained creativity |
| **Agency-mode** | Client-driven priorities; deadline-focused; context-switches frequently; good at scoping and managing expectations; presentation-ready output |
| **First-principles** | Questions assumptions from the ground up; rejects "everyone does it this way" reasoning; willing to throw away existing solutions; aggressively simplifies |
| **Open-source-native** | RFC-driven decisions; public async discussions; documentation-obsessed; community-oriented; transparent by default |

---

## Output Requirements

- Language: match user's language
- Dimensions with insufficient material: mark `(Insufficient material)`
- Conclusions with source evidence: quote original text in quotation marks
- When manual tags conflict with file analysis: output both versions and note the conflict, for persona_builder to resolve

## Data Volume Tiers

Adjust analysis depth based on how much source material is available:

### Tier 1: Profile only (no source material)
- Derive all dimensions from tags, impression, and role info
- Every output must be marked `(inferred from tags)`
- Focus on Layer 0 (tag→rule translation) and Layer 1 (identity) — these can be strong
- Layers 2-4: generate plausible defaults, clearly labeled as inferred
- **Do NOT fabricate quotes or specific examples** — use tag-based behavioral predictions instead

### Tier 2: Light data (< 50 messages / < 5 documents)
- Extract what you can, fill gaps from tags
- Mark extracted items as `(evidenced)` and tag-inferred items as `(inferred)`
- This distinction is critical for the correction handler — users should know what to validate

### Tier 3: Rich data (50+ messages or 5+ documents)
- Full extraction across all dimensions
- Evidence-based conclusions with direct quotes
- Tag-inferred items should be validated against evidence and updated if they conflict
