# ✍️ SagaSmith Module Generator

[English](README.md) | [中文](README-cn.md)

**D&D 5e Adventure Module AI Generator**

> One sentence → a complete, runnable D&D adventure with chapter structure, NPC wants & secrets, foreshadowing chains, DC values, and monster stats.

Standalone skill, zero dependencies, pure `SKILL.md`. Compatible with Claude Code, Codex, Cursor, Copilot, OpenClaw, Hermes — any agent supporting the SKILL.md standard.

---

## Ecosystem

| Repo | Role |
|------|------|
| ✍️ **SagaSmith-module-gen-skills** (this repo) | Standalone module generation skill |
| 🎲 [SagaSmith-agent](https://github.com/dajiaohuang/SagaSmith-agent) | Complete AI DM runtime |
| 📦 [SagaSmith-skills](https://github.com/dajiaohuang/SagaSmith-skills) | Full skill pack |

---

## Not an "Idea Generator"

Most AI module tools produce a paragraph of prose — no structure, no numbers, no level design.

SagaSmith Module Generator produces **complete, import-ready module files**:

- ✅ Chapter-organized `# heading` structure (direct `dnd_module action=import`)
- ✅ Room-level `####` sub-headings with type tags (`room` / `statblock` / `list`)
- ✅ Full NPC dimensions: `name / race / class / alignment / want / fear / secret`
- ✅ Foreshadowing-recovery table + faction network + ending branches
- ✅ DC values + monster stat blocks + magic items
- ✅ Scene index JSON export (DM navigates without querying a database)

---

## 5 Types × 25 Paradigms

| Type | Chapters | Default Paradigms | More Paradigms | Output |
|------|----------|-------------------|----------------|--------|
| 🎯 **One-shot** | 1 | Five-Room Dungeon | Heist, Mystery, Reverse Dungeon | 1 session, 3-6h |
| 📖 **Short** | 3 | Three-Act | Kishōtenketsu, Race Against Time, Island Design | 3-8 sessions |
| 📚 **Medium** | 5 | Hero's Journey | Plot Point, Faction Turn, Fish Tank | 2-4 month campaign |
| 🏰 **Long** | 8 | Double Triangle | Conspyramid, Megadungeon, Technoir | 6+ month campaign |
| 🗺️ **Sandbox** | 4-6 regions | Hexcrawl | Node-Based, Blorb, Decision-Based | Open exploration |

---

## Paradigm Reference

| Driver | Paradigm | One-liner |
|--------|----------|-----------|
| Space | **Five-Room Dungeon** | Entrance guardian → puzzle/RP → trick/setback → boss → reward |
| Space | **Hexcrawl** | Hex grid map, each hex has encounters & locations |
| Space | **Megadungeon** | Multi-level dungeon, looping routes, internal factions |
| Story | **Three-Act** | Establish → Confront → Resolve. Ch.2 midpoint twist |
| Story | **Hero's Journey** | Ordinary world → cross threshold → trials → abyss → return |
| Story | **Double Triangle** | Ch.1-4 Rise → Ch.5-6 Fall → Ch.7-8 Redemption |
| Story | **Kishōtenketsu** | Introduce → develop → twist → harmony. No antagonist required |
| Story | **Seven-Point Story** | Hook → PT1 → Pinch1 → Midpoint → Pinch2 → PT2 → Resolution |
| Play | **Heist** | Intel → planning → execution → complication → escape |
| Play | **Mystery** | Hook → 3 locations → 3 clues per node → reveal (Three Clue Rule) |
| Play | **Conspyramid** | 6-layer conspiracy + 6-layer response pyramid |
| Play | **Faction Turn** | Factions advance independently of players |
| Play | **Race Against Time** | Clock: X rounds to complete Y |
| Character | **Plot Point** | Main episodes + character personal arcs in parallel |
| Character | **Fish Tank** | Events + factions in place; players are the variable dropped in |
| Character | **Blorb** | Prep entities, not plots. Prep > rules > improv |
| Hybrid | **Iceberg Diagram** | Surface hook → hidden depths |
| Hybrid | **Reverse Dungeon** | Players defend, monsters attack |

---

## Usage Examples

### One-shot — Single Session

```
User: Generate a level 2 Halloween one-shot, Five-Room Dungeon,
      scarecrow spirits as the villain

Agent:
✅ Params: One-shot · Five-Room Dungeon
   Theme: Halloween/Pumpkin Farm · Villain: Scarecrow Spirits (CR 1 ×3)
   Level: 2 · Tone: Horror-comedy

[Generating → modules/pumpkin_horror.md]

Output summary:
📜 The Pumpkin Horror
   Scene 1: Harvest Festival (Guardian — missing children hook)
   Scene 2: The Old Mill's Riddle (Puzzle — scarecrow speaks in anagrams)
   Scene 3: The Living Pumpkin Patch (Twist — scarecrows are victims)
   Scene 4: Barn Boss Fight (Climax — real mastermind: a Green Hag)
   Scene 5: Festival's End (Reward — villagers' gratitude + 1 magic item)
```

### Short — Three-Act Campaign

```
User: Generate a level 5 desert tomb short module, Kishōtenketsu,
      mummy lord as villain

Agent:
✅ Params: Short (3 Ch) · Kishōtenketsu (起承转合)
   Theme: Desert/Ancient Tomb · Villain: Mummy Lord + Scarab Swarms
   Level: 5 · Twist: mummy is guarding something far worse

[Generating 3 chapters → 3 scenes each → modules/desert_tomb.md]

Output summary:
📜 The Seal Beneath the Sands
   Ch.1「起」— Oasis caravan's plea, three NPCs with hidden agendas
   Ch.2「承」— Descent into the buried pyramid, 5 trap rooms
   Ch.3「転」— The mummy isn't the enemy — the true threat lies beneath
             the seal. Ending branches: Release / Reinforce / Destroy
   Appendix: NPC dimensions · 4 foreshadowed payoffs · Mummy Lord stat block
```

### Medium — Five-Chapter Campaign

```
User: Generate a medium module, level 7 urban politics, Hero's Journey

Agent:
[Step M1] Generating skeleton...
   5 chapter outline · 4 factions · 12 NPCs (full want/fear/secret)
   See modules/city_of_masks_skeleton.md — review and approve.

User: The Ch.2 villain's motivation is weak — make him blackmailed

Agent:
✅ Adjusted: the council speaker is blackmailed by Zhentarim

[Step M2] Generating Ch.1-3 body...
   Ch.1 Ordinary World · Ch.2 Crossing the Threshold · Ch.3 Trials
   See modules/city_of_masks_ch1-3.md

[Step M3] Generating Ch.4-5 + appendix...
   Ch.4 The Abyss · Ch.5 Return
   Foreshadowing table (5-chapter chain) · Faction evolution timeline
   ✅ Final: modules/city_of_masks.md
```

### Long — Eight-Chapter Epic

```
User: Generate a long module, 1-20 fantasy epic, Double Triangle

Agent:
[Step L1] Concept + Double Arc Outline...
   Villain timeline (8 chapters) · Dual-arc structure · Ch.4 false victory
   Ch.8 multiple endings (4 branches) · 22 NPCs with personal arcs
   See modules/the_last_circle_concept.md

[After 5 progressive steps...]

✅ Final module: modules/the_last_circle.md
   📊 8 chapters · 48 scenes · 22 NPCs · 12 foreshadowing chains
   👤 2-3 personal scenes per PC · Boss: four phases
```

### Sandbox — Open World

```
User: Generate a sandbox — Viking-themed archipelago exploration

Agent:
[Step S1] World skeleton...
   6 regions · 3 factions · Random encounter table (1d12)
   See modules/viking_isles_world.md

User: Generate the northern region

Agent:
[Step S2] Region: North · Frostbone Isles
   Terrain: frozen island chain controlled by dragonborn clans
   Factions: White-Frost Tribe · Event lines ×3
   Locations: Dragonbane Harbor · Frostwhisper Cave · Elders' Hall · Geyser Shrine
   ✅ Appended to modules/viking_isles.md
```

---

## Quick Install

```bash
# Claude Code / Codex / Cursor / Copilot
npx skills add dajiaohuang/SagaSmith-module-gen-skills

# ClawHub
npx clawhub install sagasmith-modulegen
```

---

## Credits

- [ackiles/dnd-dm-skill](https://github.com/ackiles/dnd-dm-skill) — D&D DM skill pioneer
- The 25 paradigms draw from decades of TRPG community design (Five-Room Dungeon, Three Clue Rule, Hexcrawl, etc.)

---

## License

MIT
