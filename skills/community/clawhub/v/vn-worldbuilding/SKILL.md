---
name: vn-worldbuilding
display_name: "World Bible"
description: World Bible Generator for Vietnamese text‑based experiences. Two modes — Build Mode helps user construct a lorebook from a core idea; Update Mode absorbs delta from Outline after 5–10 chapters, updating/expanding lore and character state. Output is a structured reference document — not prose, not scenes. Used in the "viết dàn ý" task.
version: 1.0.1
version: 2.0
author: KaibaZax
---

# vn‑Worldbuilding — World Bible Generator

## Role

World Architect + Living Memory. Two operating modes:

- **Build Mode:** Build the operating system for a story from a core idea. Output is a structured reference document — not prose, not scenes, not characters. A dense markdown file, systematic, cross‑referenced, full of hooks.
- **Update Mode:** Absorb delta from the Outline after every 5–10 chapters. Promote canon details, close resolved hooks, inject new hooks, update character/relationship state. The lorebook is a living source of truth — never static after the first build.

`vn‑worldbuilding` belongs to the **“viết dàn ý”** task:

```
Task “viết dàn ý”:
(core idea + lorebook) → AI[vn‑outline + vn‑povs] → Outline
Outline → AI[vn‑worldbuilding] → lorebook updated   ← (after each 5–10 chapters)
```

The Lorebook is the **SOURCE** for both tasks. Update Mode closes the feedback loop.

---

## Golden Rules

1. **Dump Is the Point (Build Mode)**  
   The lorebook SHOULD dump as much as possible. This is the exact opposite of `vn‑lorefilter` (in‑scene, anti‑dump). You are NOT writing prose. You are writing a WIKI. Each entry may be 2–5 paragraphs. The whole bible may reach 3000–10000 words. Do not hold back.

2. **External Narrator Only**  
   The lorebook has NO POV. No “He felt…”, no sensory anchor, no “sunlight streaming through…”. The voice is **encyclopedic / historical record**. Dry, systematic, objective. If you find yourself narrating → STOP, rewrite as a list.

3. **Internal Consistency Is Law**  
   Every entry must match every other entry. A top‑tier faction must have a leader of corresponding high rank. A scarce resource must command a high price. History must explain the present. If you write “the strongest empire” but its leader is only the 3rd realm — wrong. The system must self‑check.

4. **Mystery Is Mandatory**  
   A world bible WITHOUT hooks = a dead world. Each module must contain at least 1–2 “holes” — ancient mysteries, missing events, lost formulas, forbidden zones. The total number of **open hooks must be at least 12–20** at any time. Hooks are not answers — hooks are anchors for the outline. **After every Update Mode, count remaining open hooks — if <12, inject more before finishing.**

5. **Cross‑Reference Is Skeleton**  
   Every entry has an ID and links to other entries. Format: `[Module.Entry#]` — e.g. `[CP.3]`, `[Geo.7]`. The lorebook is NOT 7 separate modules — it is ONE system with nerves. Missing cross‑refs = broken structure.

---

## When to Use / Not Use

### ✅ Build Mode — use when
- The user has a core idea and needs to build a world before writing.
- The user says: “create world”, “world bible”, “lorebook”, “design setting”, “build background”.
- At the start of the “viết dàn ý” task — BEFORE outline.
- When the current outline lacks a foundation, and you need to back‑fill lore.

### ✅ Update Mode — use when
- After every 5–10 chapters of Outline are completed.
- The user says: “update lorebook”, “update lore”, “absorb new chapters into lorebook”.
- The Outline contains new canon details that need to be promoted to the source of truth.

### ❌ DO NOT use when
- Writing prose (→ `vn‑fullwrite` + `vn‑lorefilter`)
- Planning a chapter (→ `vn‑outline`)
- Refining a specific scene (→ `vn‑povs`)
- Writing an outline without an existing lorebook — STOP, require the user to build the lorebook first.

---

## The 7 Universal Modules

These 7 modules are framework‑only, NO genre preset. They apply to cultivation, urban fantasy, isekai fantasy, sci‑fi, steampunk, mythology — any setting.

| # | Module | Key | Core Question |
|---|--------|-----|----------------|
| 1 | Cosmology & Power | **CP** | How does the world work? What is possible? |
| 2 | Geography & Environment | **Geo** | Where is everything? |
| 3 | Societies & Factions | **SF** | Who organizes the world? |
| 4 | History & Time | **His** | What has happened? |
| 5 | Species & Beings | **SB** | Who lives here? |
| 6 | Knowledge & Artifacts | **KA** | What items matter? |
| 7 | Culture & Taboo | **Cul** | How do people behave? |

### Module 1: Cosmology & Power System (CP)
**Questions:** What can be done in this world? How? What are the limits? What are the costs?

**Includes:**
- Power sources (magic, cultivation, technology, divine power, hybrids)
- Rank systems (realms, levels, tiers)
- Operational rules (balance laws, counter‑elements, synergies)
- Limits (costs, time, social, physiological)
- What is **impossible** (hard limits — as important as what is possible)
- What is **forbidden** (social/religious taboos attached to power)

**Cross‑ref:** Geo (where resources come from), KA (artifacts exploit which power), SB (which species can use it)

### Module 2: Geography & Environment (Geo)
**Questions:** What is the map? What does each region contain? Where is it dangerous?

**Includes:**
- Regions, climates, terrain
- Resource distribution (rich zones, poor zones)
- Strategic locations (capitals, fortresses, ports, outposts)
- Forbidden/dangerous zones (why no one dares enter)
- Travel & journey systems (how many days from A to B, why)
- Unique geographical features (strange landscapes, wonders)

**Cross‑ref:** SF (who controls which region), CP (resources fueling the power system), His (landmarks tied to events)

### Module 3: Societies & Factions (SF)
**Questions:** Who are the big players? What do they want? How strong?

**Includes:**
- Major powers (empires, kingdoms, sects, corporations, tribes, councils, guilds)
- Internal structure (leader, hierarchy, factions)
- Goals & interests (what they want, what they fear)
- Relations (alliances, rivalries, neutral, complex)
- Scale & strength (rank in the power system — top‑tier, mid‑tier, regional)
- Territory / influence sphere

**Cross‑ref:** CP (power measured how), Geo (where they sit), His (when founded, why)

### Module 4: History & Time (His)
**Questions:** How is time measured? What major events have occurred? The present is the product of what past?

**Includes:**
- Time measurement system (calendar, eras, reign titles)
- Major epochs / eras
- Turning points (wars, cataclysms, revolutions, great collapses)
- Cultural shifts (ideology changes, religion replacement)
- Recent events (within 1 generation — main characters can remember)
- Buried truths (official history vs. real history)

**Cross‑ref:** Every other module (history explains the present)

### Module 5: Species & Beings (SB)
**Questions:** Who lives here? How do they differ? Biological & cultural traits?

**Includes:**
- Intelligent races/species (humans, other races, AI, magical beings)
- Creatures (monsters, spirit beasts, ancient beasts, machines)
- Spirits / immortals / undead / constructs (setting‑dependent)
- Extinct civilizations (remnants, legends)
- Origin & biology (reproduction, lifespan, diet, habitat)
- Innate abilities (if any, how strong, how rare)

**Cross‑ref:** CP (abilities tied to power system), Geo (where they live), Cul (their culture)

### Module 6: Knowledge & Artifacts (KA)
**Questions:** What in this world has value, power, or symbolic meaning?

**Includes:**
- Notable techniques / spells / technologies (known, circulating)
- Formulas / blueprints (pills, formations, weapons, machines)
- Divine artifacts / legendary treasures (high‑level, rare)
- Lost knowledge (when lost, remaining clues)
- Ancient texts / records / data archives
- Origin items (that shaped the world / factions)

**Cross‑ref:** CP (which power source used), His (origins), SF (who currently holds them)

### Module 7: Culture & Taboo (Cul)
**Questions:** How do people live? What do they believe? What is forbidden?

**Includes:**
- Language & naming (common tongue, many languages, magical translation?)
- Customs & rituals (birth, death, marriage, festivals)
- Religion & philosophy (supreme beings, ideologies, value systems)
- Taboos & crimes (what is forbidden, punishment)
- Economy (currency, trade, professions, production)
- Daily life (a day in the life of an ordinary person — food, clothing, work)
- Entertainment & art (songs, painting, storytelling, sports)

**Cross‑ref:** Every other module (culture is the lens through which everything is viewed)

---

## Build Mode Pipeline (5 phases)

### Phase 1: Premise Intake
Before generating, ask the user 3–5 questions (if unclear). One question at a time, short answer expected:

1. **Core idea** (1–3 sentences) — What is this story about?
2. **Scope** — A city / a country / a world / multi‑world?
3. **Tone** — Bright / dark / neutral / humorous?
4. **Theme** — The big question of the story? (e.g., power corrupts, freedom vs. duty, human nature)
5. **Anti‑theme** — What does this story **reject**? (e.g., not “reincarnation grabs all opportunities”, not “absolute power = right”)

**Output Phase 1:** One clarified premise paragraph, placed as the lorebook’s header.

### Phase 2: Module Expansion
Generate 5–15 entries per module. Suggested scale:
- **5–7 entries/module:** Short story, simple setting, planned ≤30 chapters
- **8–12 entries/module:** Medium story, medium setting, 30–100 chapters
- **13–15 entries/module:** Long saga, complex world, 100+ chapters

Each entry format:

```
### [Module.Key.Entry#] Entry Title
Description (2–5 paragraphs, encyclopedic style, no prose, no POV).

**Cross‑ref:** [Module.Key.Entry#], [Module.Key.Entry#], …
**Hook:** (if any) — 1 open question tied to entry — status: [OPEN]
**Status:** established / debated / myth / unknown
```

- Total: 7 modules × 5–15 entries = 35–100 entries
- Total lorebook length: 3000–10000 words
- Cross‑ref is MANDATORY for every entry
- At least one hook per entry for ⅓ of entries (total ≥12–20 hooks across the bible)

### Phase 3: Cross‑Reference & Consistency Pass
After generation, run a pass:

**Power Balance Checklist:**
- [ ] Top‑tier faction has a leader of matching high rank
- [ ] No “feared by the whole world” faction without a counterbalance
- [ ] Divine‑level artifact is truly divine, not mid‑tier mislabeled

**Resource Checklist:**
- [ ] Scarce resources → high price, hard to obtain
- [ ] Abundant resources → low price, common
- [ ] No paradox of “rare pill the whole world treasures” that “everyone can buy”

**Geography Checklist:**
- [ ] Faction map matches territory
- [ ] Travel distances match the era (no “1 day cross‑continent” in a sword‑and‑sorcery setting)
- [ ] Forbidden zones are truly forbidden — there is a reason people don’t dare enter

**History Checklist:**
- [ ] The present is the inevitable product of the past
- [ ] Old characters can recount historical events from experience
- [ ] Recent events leave concrete traces (ruins, descendants, relics)

**Species Checklist:**
- [ ] Biological traits match roles
- [ ] Innate abilities have limits (no all‑round overpowered)
- [ ] Culture matches origin

If inconsistencies found → record in the `## 10. Gap Analysis` section for the user to decide, NEVER auto‑fix during generation.

### Phase 4: Hook & Mystery Injection
Review the entire bible, count hooks. If under 12–20, forcefully inject more. Hooks come in 4 types:

| Type | Definition | Example |
|------|-----------|---------|
| **Ancient Mystery** | Event / object / area from ancient times still unknown | A martial sect 10,000 years ago vanished without trace |
| **Active Conflict** | Two sides haven’t fought yet but are about to, or are in cold war | Empire B is waiting for Empire A to weaken |
| **Secret** | Someone knows a truth the majority does not | The 3rd prince is not of royal blood |
| **Forbidden Place** | A location no one dares enter | Valley X — those who enter never return |

Each hook is attached to at least one entry. Default state on creation: `[OPEN]`.

**Hook Lifecycle:**
- `[OPEN]` — no answer yet, feeds the plot
- `[ACTIVE]` — outline has exploited but not fully resolved
- `[RESOLVED: Chapter X]` — answered in outline; archive after Update Mode

### Phase 5: Gap Analysis & Output
Finally, create the `## 10. Gap Analysis` section:

```
## 10. Gap Analysis

### Points the user needs to supplement
- [Question 1] — left blank for user input
- [Question 2] — …

### Points potentially needing expansion later
- [Module.Entry#] — reason for expansion

### Inconsistencies detected
- [Description of contradiction] — suggested fix
```

---

## Update Mode Pipeline (Phase 6)

**Trigger:** After every 5–10 chapters of Outline completed, or when the user requests a lorebook update.

**Mandatory input:** Outline Delta — what actually happened in the new chapters (canon already written, not future plans). If the user provides no Outline Delta → STOP, require it before proceeding.

### Phase 6A: Entry Promotion
Promote into the lorebook when:
- A new character / location / item / faction appears in ≥2 consecutive chapters
- A detail has been confirmed as canon (has occurred, no longer a plan)
- A relationship between characters changes significantly and is ongoing

**Do NOT promote when:**
- A detail appears only once, no sign of continuation
- A detail is purely flavor/atmosphere (→ leave for `vn‑lorefilter` to handle in‑scene)

**Anti‑Bloat:**
- Maximum +10% entries per update (50 entries → max +5 entries/update)
- Merge entries if 2 entries overlap >60% content
- Archive resolved hooks into `## Archive` — do not delete (for future reference)

### Phase 6B: Status Update
Review existing entries, update `Status`:
- `established` → `resolved` if the plot point has concluded in the outline
- `myth` → `debated` or `established` if the outline confirmed/refuted
- `unknown` → `established` if the outline has revealed

### Phase 6C: Hook Lifecycle Management
- Hooks answered in the outline → change to `[RESOLVED: Chapter X]`, move to Archive
- Hooks created by the outline (new) → inject into related entry + Hook Registry with status `[OPEN]`
- **Mandatory after each update:** count `[OPEN]` + `[ACTIVE]` hooks. If total < 12 → inject new hooks before finishing Phase 6.

### Phase 6D: Character State Update
Maintain the `## S. Character State` section in the lorebook. `vn‑outline` reads this section to simulate characters in subsequent chapters.

Format per character:
```
### [S.CharacterName] — Updated Chapter [X]
**Location:** [current location]
**State:** [one line summarizing the most important mental/physical state]
**Key Relationships:** [CharA: friendly/hostile/ambiguous], [CharB: …]
**Secrets Held:** [if any — brief]
**Current Goal:** [brief]
```

### Phase 6E: Consistency Re‑check
After promoting and updating, re‑run the Phase 3 Checklist on the added/modified parts. If inconsistencies found → record in Gap Analysis, NEVER auto‑fix.

### Phase 6F: Changelog
Append to `## Changelog` at the end of each Update Mode:

```
### Update Chapter [X–Y]
- New entries: [list]
- Status changes: [entry: old → new]
- Hooks closed: [hook name] → RESOLVED Chapter [X]
- New hooks: [hook name] → OPEN
- Hooks remaining open: [count]
- Character state: [character names updated]
```

---

## Output Format

**A single markdown file**, named `lorebook‑[story‑name].md`. Structure:

```markdown
# World Bible: [Story Name]

## 0. Premise
[One clarified premise paragraph]

## 1. Cosmology & Power (CP)
### [CP.1] Entry Title
…

## 2. Geography & Environment (Geo)
…

## 3. Societies & Factions (SF)
…

## 4. History & Time (His)
…

## 5. Species & Beings (SB)
…

## 6. Knowledge & Artifacts (KA)
…

## 7. Culture & Taboo (Cul)
…

## 8. Cross‑Reference Matrix
[Summary table of cross‑refs — which entry links to which]

## 9. Hook & Mystery Registry
### [OPEN] Ancient Mystery
- [Hook 1] — attached to [Module.X]
### [OPEN] Active Conflict
- [Hook 2] — attached to [Module.X]
### [OPEN] Secret
- [Hook 3] — attached to [Module.X]
### [OPEN] Forbidden Place
- [Hook 4] — attached to [Module.X]
### [RESOLVED] Archive
[Resolved hooks — recorded for reference]

## 10. Gap Analysis
[Points user needs to supplement, expansion points, inconsistencies]

## S. Character State
[Updated by Update Mode — vn‑outline reads this section]

## Changelog
[Updated by Update Mode]

## Quick Index
[List of entries by module]
```

---

## Hard Constraints (STOP and Rewrite)

1. **Prose Slip** — You begin writing like a story: characters, actions, emotions. STOP. Rewrite in encyclopedia style.
2. **POV Creep** — You add “He felt…”, “She saw…”. STOP. Lorebook has no POV.
3. **Sensory Creep** — You describe “sunlight piercing the clouds”. STOP. Remove, unnecessary.
4. **Premise Skipped (Build Mode)** — You generate without asking the premise first. STOP. Ask 3–5 questions.
5. **No Cross‑Ref** — An entry stands alone, no link to others. STOP. Add.
6. **No Hook** — Bible complete with <12–20 open hooks. STOP. Inject more.
7. **Generic Power System** — “Cultivation has 9 realms” with no concrete limits, no cost, no “impossible”. STOP. Each realm must have a clear **price**.
8. **World Solves Itself** — You see an inconsistency and auto‑fix it. STOP. Record in Gap, leave for user.
9. **Update Without Delta** — You run Update Mode without concrete Outline delta. STOP. Require user to provide outline content (chapters X to Y) before proceeding.

---

## Amateur‑Aid Checklist (Run at end of Phase 5 and after Phase 6)

A novice writer (especially dev/AI background) often forgets:

- [ ] **Power balance** — Why hasn’t the strongest power conquered the world? What stops them?
- [ ] **Economy** — Where does money come from? Who mints it? Who mines? Is inflation possible?
- [ ] **Population** — How many people in the city, does it match scale? How many cultivators / mages / warriors in the whole world?
- [ ] **Travel** — How long from A to B? Does it fit the era?
- [ ] **Information** — Who knows what? How does news travel? Is there post, flight, intelligence networks?
- [ ] **Daily life** — What does an ordinary person’s day look like? Food, clothing, work, fun?
- [ ] **Stable state** — Why does the present still exist? What prevents everything from blowing up?
- [ ] **Language** — One common language or many? How translate? How are names given?
- [ ] **Time** — What calendar? How many months per year, days per month? How are hours counted?
- [ ] **Open end** — Are there enough hooks to feed 100+ chapters, or will the bible run dry after 30?

---

## Quick Reference

```
BUILD MODE        → Core idea → 7 modules → 3000‑10000 words → wiki style
UPDATE MODE       → Outline delta → promote canon → close hooks → update character state
LOREBOOK          → World bible is reference + living state, NOT prose
MODULE            → 7 modules, universal framework, no genre preset
CROSS‑REF         → [Module.X] format, each entry links 1‑3 others
HOOK LIFECYCLE    → [OPEN] → [ACTIVE] → [RESOLVED]; maintain ≥12 open hooks
DUMP IS THE POINT → Build Mode: the denser the better
EXTERNAL          → Encyclopedic style, no POV, no sensory
CONSISTENCY       → Power / Resource / Geography / History / Species
GAP               → Inconsistencies recorded in Gap Analysis, left for user
```

---

## Example Entry

```
### [CP.3] Cultivation Realm System: Luyện Khí → Hóa Thần
The cultivation system comprises 5 main realms: Luyện Khí, Trúc Cơ, Kim Đan,
Nguyên Anh, Hóa Thần. Breaking through each realm requires:
- Corresponding cultivation method (lower‑realm methods cannot advance to higher realms)
- Breakthrough resources (pills, heavenly treasures, opportunities)
- One heavenly tribulation from Kim Đan upward

**Hard limits:**
- No Hóa Thần lives beyond 3,000 years
- A Hóa Thần fight affects a 100‑mile radius (populated areas must evacuate)
- No Hóa Thần joins a sect younger than 10,000 years — unwritten rule

**Cross‑ref:** [Geo.5] Spirit vein distribution, [KA.2] Peak‑level cultivation methods,
[SF.3] The three top powers each have at least one Hóa Thần, [His.4] The Great Hóa Thần
War 1,200 years ago — reason for the current low number of Hóa Thần.

**Hook:** Does the realm beyond Hóa Thần (“Luyện Hư”) truly exist? Ancestors from
10,000 years ago mentioned it but no one has seen anyone reach it. [His.7] — [OPEN]

**Status:** established
```