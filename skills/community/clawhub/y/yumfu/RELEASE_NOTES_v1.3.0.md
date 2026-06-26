# YumFu v1.3.0 Release Notes

## 🎮 Major Update: Deep Narrative Engine (DNE)

### Overview
YumFu v1.3.0 introduces the **Deep Narrative Engine** - a complete overhaul of how stories are structured across all game worlds. Every choice now leads somewhere meaningful. No more dead ends.

---

## ✨ New Features

### Deep Narrative Engine (DNE)
- **30+ decision nodes** per character arc (previously ~5-8)
- **6-8 unique endings** per world (previously 2-3)
- **Three-arc story structure**: Establishment → Development → Climax
- **NPC Memory System**: NPCs remember your choices and react accordingly
- **Four consequence types**: Immediate / Delayed / Cumulative / Hidden

### New World: F15 Down - Azure Peninsula War 🛵
- Modern military strategy RPG set in fictional Middle East
- Dual-path system: Strategic (Defense Minister) + Frontline (14 combat roles)
- Command & Conquer RTS visual aesthetic
- **14 frontline combat roles**:
  - F-15 Fighter Pilot
  - A-10 Warthog Pilot  
  - B-2 Spirit Stealth Bomber Pilot ⭐NEW
  - B-21 Raider Bomber
  - Destroyer Captain
  - Submarine Commander
  - Falcon Special Forces
  - Shadow Operative (Black Ops)
  - Flying Moped Operator (Asymmetric warfare) ⭐
  - Drone Operator (MQ-9 Reaper)
  - Combat Medic
  - Tank Commander
  - Artillery Officer
  - Naval Gunner

### Character Creation System
- New unified `create_character.py` script
- Supports all worlds with world-specific role options
- Auto-generates portrait prompts in world's art style
- 5-step interactive creation: Name → Faction → Role → Personality → Background

### Content Policy System
- All worlds now have fictional names/factions/locations
- No real politicians or historical figures
- Clear moral complexity without political bias
- Full `CONTENT_POLICY.md` documentation

---

## 🎨 Art Style Updates

### F15 Down: Command & Conquer Aesthetic
- Style: Stylized 3D renders (NOT photorealistic)
- Heroic character portraits
- Isometric tactical maps
- Dramatic cinematic lighting
- Red/Blue faction color coding

### Art Style Guide
- New `ART_STYLE_GUIDE.md` for F15 Down
- Reference games: C&C Generals, Red Alert, DEFCON
- Avoid: photorealistic military photography

---

## 📖 Story Improvements

### F15 Down - Alibaba Storyline
- **8 possible endings**: Exile / War Correspondent / Underground Leader / Double Agent / Peace Ambassador / Martyr / Ordinary Life / Avenger
- **30-day narrative arc**
- Three arcs: Survival (Day 5-10) → Identity (Day 10-20) → Choice (Day 20-30)
- Hidden stats: Anger / Exposure / Father Relationship / International Attention

### All Worlds Updated
- Xiaoao Jianghu: 6 endings, 30-day arc
- Harry Potter: 6 endings, 7-year arc
- Warrior Cats: 6 endings, four-season arc
- LOTR (coming soon): 6 endings planned
- 倚天屠龙记 (coming soon): 6 endings planned

---

## 🐛 Bug Fixes
- Fixed image generation not auto-triggering at key story moments
- Fixed messages not being sent to Telegram after image generation
- Fixed character names being too close to real figures (now fully fictional)

---

## 📁 New Files
- `DEEP_NARRATIVE_ENGINE.md` - Complete DNE design spec
- `worlds/f15-down/` - New world directory (9 files)
- `worlds/f15-down/CONTENT_POLICY.md` - Content guidelines
- `worlds/f15-down/ART_STYLE_GUIDE.md` - Visual style guide
- `worlds/f15-down/frontline_roles.json` - 14 combat roles
- `worlds/f15-down/alibaba_storyline.md` - Alibaba arc design
- `scripts/create_character.py` - Unified character creation
- `docs/CHARACTER_CREATION.md` - Character creation docs

---

## 📊 Stats
- Total worlds: 4 active + 2 coming soon
- Total decision nodes designed: 150+
- Total unique endings: 38
- New combat roles: 14
- Lines of world data: 3,500+
