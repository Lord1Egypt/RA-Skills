---
name: wildidea
description: "V5 — Inject wild remote domains (hydrothermal vents, monasteries, bee dances, Bushmen, casinos, classical music, immune system, alchemy, polar expeditions) as concrete 'nails' and juxtapose them directly against user-domain 'counterparts'. Zero analysis/translation/abstraction between nail and counterpart. Dual gate: comfort check (would a VP wince?) + web verification (already done? reroll.)"
source: "https://github.com/liwenyu2002/wildidea"
---

# 🌐 WildIdea — Wild Ideas

## Core Philosophy

> **V5 Path (enforced):** Input → Juxtapose → Find nails → Output counterparts
>
> **nails** = a specific operation/rule/physical constraint, must include a number/event/boundary
> **counterparts** = a specific existing product/technology/feature name
> **Zero abstraction between nail and counterpart.**

**The fundamental trap of earlier versions:** every piece of "analysis" / "abstraction" / "translation" between the remote domain and the user domain is contaminated by your own thinking framework. The cure: don't think. Just juxtapose.

## Source Architecture

| Channel | Count | Reference |
|---------|-------|-----------|
| 🔵 Pre-built remote domains | 3 | `references/paradigms.md` (17 domains, prefer 7.9-7.17) |
| 🟢 Seed library (random) | 2 | `scripts/pick_seed.py` (Mao Zedong quotes → abstract structure) |
| 🟠 Random char + web search | 1 | `scripts/search_char.py` (500-character pool → Tavily search → real domain) |
| 🔍 Web verification | — | Tavily API via curl |

## Nail Rules

| ✅ Is a nail | ❌ Not a nail |
|-------------|---------------|
| "Bees: 75ms wing flutter = 1km distance" (concrete number) | "Bee communication is efficient" (analysis/summary) |
| "One lamb skin = 3-4 folio pages of parchment" (physical constraint) | "Copying is a form of cultivation" (abstract idea) |
| "Drone bee dies immediately after mating" (concrete event) | "Expendable male roles in insect society" (concept label) |
| "Shackleton abandoned all equipment to save crew" (concrete decision) | "People over assets in crisis leadership" (abstract interpretation) |

## Counterpart Rules
| ✅ Is a counterpart | ❌ Not a counterpart |
|-------------------|---------------------|
| Concrete tech/product/feature name — "iPhone Live Photos", "VSCode debugger", "Tesla Dog Mode" | Vague concept — "improve experience", "reduce friction", "better UX" |

## Core Process

### Step 0 — Quarantine the obvious

### Step 1 — Inject 3 remote channels
Run all 3 in parallel, output results as-is (no analysis):
- 🔵 Load `references/paradigms.md`, pick 3 domains (prefer 7.9-7.17: weirder the better)
- 🟢 Run `python3 scripts/pick_seed.py` → get 2 seed texts + abstract tags
- 🟠 Run `python3 scripts/search_char.py` → get real search results

### Step 2 — Juxtapose → Find nails → Find counterparts
**Forbidden: ANY analysis/abstraction/translation between nail and counterpart.** No "because", "therefore", "this means", "this implies".

Pick 1 concrete nail from each domain (the most specific operation/event/constraint).
Find 1 concrete counterpart from the user's domain.

### Step 3 — Output
Table of nail ↔ counterpart. No connecting text between them.

### Step 4 — GATES

1. **🌪️ Comfort Gate:** "Would this get pushback in a product review meeting?"
   - "Nah, makes sense" → ❌ Not wild enough. Reroll.
   - "WTF... but wait, there's something there" → ✅ Pass.

2. **🔍 Web Verification Gate:** Search if the counterpart already exists.
   - Search terms: `[counterpart name] + [domain]`
   - If a product/patent/media already implements this → 🚫 Ban. Reroll from remaining paradigms.
   - Max 3 retries per domain. If all exhausted → 🚫 Skip domain.

## Quality Gates (Hard Constraints)

1. At least 3 different source domains
2. At least 1 from seed library or random char search
3. Pass "remove remote domain test" — if the counterpart still makes sense without its nail source, delete it
4. No "it's like XX" soft commentary
5. No fabricating search results
6. At least 1 output changes the user's problem definition
7. **Comfort check fail (too reasonable) → Blocked**
8. **Web verification found existing implementation → Reroll**

## Second Iteration Mode

If user says "reroll" / "iterate" / "go deeper" / "ban and redo":

1. Build two-layer quarantine: (a) common answers, (b) all counterpart outputs from previous round
2. Reroll all 3 channels (no reusing previous seeds/domains)
3. Juxtapose normally, avoiding all banned directions
4. Output: simple bold 3-column table. No poster.

## Iteration Discipline

- ❌ No returning to banned directions ("rewording")
- ❌ No stopping before user says "deep enough"
- ✅ If user says "expand on #3" → deep-dive that single nail/counterpart relationship
- ✅ If user says "this is too safe" → delete, reroll seed, redo

## Scripts

### pick_seed.py
Picks 2 random Mao Zedong quotes from a 50-seed pool. Outputs: seed index, seed text, abstract tags.
Pitfall: Do NOT pre-filter based on user's question. Random is random.

### search_char.py
Picks 2 random Chinese characters, concatenates into a "word", searches via Tavily API.
If the search returns a real domain (linguistics, traditional craft, regional industry, etc.) → use it.
If search is empty/garbled → skip, note as 🚫.
No fabricating.

## Web Verification (Tavily)
Use curl + Tavily API to verify counterparts are novel:
```bash
curl -s "https://api.tavily.com/search" \
  -H "Content-Type: application/json" \
  -d '{"api_key": "'"$TAVILY_API_KEY"'", "query": "your search", "search_depth": "basic", "max_results": 5}'
```

## Known Issues

1. **search_char.py may yield weak results** — e.g. two random chars format a real Chinese word but it's generic. Label the domain honestly (e.g. "linguistics"). Don't retry or fabricate.
2. **Web verification loop may exhaust all paradigms** — Max 3 retries per domain. Skip honestly.
3. **Comfort check is inherently subjective** — "Would a VP wince?" If unsure → fail. Better to output fewer items than let a "reasonable" one through.
4. **do NOT use the domain as a metaphor** — "Bee dance is LIKE word of mouth" is contamination.
5. **do NOT abstract the user's problem** — Don't "reframe" or "distill essence." Leave the problem as-is.

## Poster Template
For visual output, use `templates/poster.html` with placeholder substitution.
