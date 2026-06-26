# YumFu v1.4.0 Release Notes

## 🎮 Major Update: Deep Narrative Engine + F15 Down + Gameplay Overhaul

### What's New in v1.4.0

Building on v1.3.0, this release adds the complete F15 Down world, Deep Narrative Engine rules baked into SKILL.md, and full README documentation.

---

## ✨ New Features

### 🛵 F15 Down: Azure Peninsula War (Complete World)
- **7 world data files**: factions, locations, units, events, decisions, frontline roles, world config
- **Dual-path system**: Strategic (Defense Minister) OR Frontline (14 combat roles)
- **14 frontline roles**: F-15, A-10, B-2 Spirit, B-21, Destroyer Captain, Submarine Commander, Falcon Special Forces, Shadow Operative, **Flying Moped Operator** 🛵, Drone Operator, Combat Medic, Tank Commander, Artillery Officer, Naval Gunner
- **8 unique endings**: Exile / War Correspondent / Underground Leader / Double Agent / Peace Ambassador / Martyr / Ordinary Life / Avenger
- **Art style**: Command & Conquer Generals RTS aesthetic (NOT photorealistic)
- **Content policy**: Fully fictional factions/characters/locations

### 🎭 Deep Narrative Engine (DNE)
- **30+ decision nodes** per character arc
- **6-8 unique endings** per world
- **Three-arc structure**: Establishment → Development → Climax
- **NPC memory system**: NPCs remember your choices
- **4 consequence types**: Immediate / Delayed / Cumulative / Hidden
- **No dead ends**: Every choice opens a new path (B is never "game over")
- **Mandatory image generation** at key story moments

### 📖 Alibaba Storyline (F15 Down)
- Complete 30-day arc design
- Arc 1: Survival (Day 5-10)
- Arc 2: Identity (Day 10-20)  
- Arc 3: Choice (Day 20-30)
- Hidden stats: Anger / Exposure / Father Relationship / International Attention

### 🌍 All Worlds Updated with DNE Rules

| World | Endings | Key Stats |
|-------|---------|-----------|
| 笑傲江湖 | 6 | 武功/声望/门派/爱情 |
| Harry Potter | 6 | Magic/Points/Dark Arts/Friendship |
| Warrior Cats | 6 | Rank/Honor/StarClan/Dark Forest |
| F15 Down | 8 | Anger/Exposure/Father/Media |
| 倚天屠龙记 | 6 | 武功/宝刀宝剑/六派关系 |
| LOTR | 6 | Ring Temptation/Courage/Corruption |

---

## 📚 Documentation
- Updated README with F15 Down world listing
- New `DEEP_NARRATIVE_ENGINE.md` design spec
- New `worlds/f15-down/CONTENT_POLICY.md`
- New `worlds/f15-down/ART_STYLE_GUIDE.md`
- New `docs/CHARACTER_CREATION.md`

## 🐛 Bug Fixes
- Fixed image generation not auto-triggering at key story moments
- Fixed messages not being sent to Telegram after image generation
- Fixed character names being too close to real figures (now fully fictional)
- Fixed story branches ending prematurely (DNE ensures continuation)

---

## 📊 Stats
- Total worlds: 4 active + 3 in progress
- Total decision nodes designed: 200+
- Total unique endings: 44
- New combat roles: 14
- Lines of world data: 4,000+
