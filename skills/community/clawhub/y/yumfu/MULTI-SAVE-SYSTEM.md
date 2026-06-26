# Multi-World Save System

## 🗂️ Separate Saves Per World

Each universe has its own save directory to prevent conflicts:

```
~/clawd/memory/yumfu/saves/
├── xiaoao/
│   ├── user-123456789.json      # 笑傲江湖存档
│   └── world-state.json          # 笑傲江湖世界状态
├── warrior-cats/
│   ├── user-123456789.json      # Warrior Cats存档
│   └── world-state.json          # ThunderClan共享状态
├── harry-potter/
│   ├── user-123456789.json      # Harry Potter存档
│   └── world-state.json          # Hogwarts共享状态
└── ...
```

---

## 📝 Save File Structure

### Example: Xiaoao Jianghu Save
```json
{
  "version": 2,
  "user_id": "123456789",
  "language": "zh",
  "universe": "xiaoao",
  "character": {
    "name": "小虾米",
    "level": 15,
    "faction": "华山派",
    "skills": ["华山剑法", "紫霞神功"],
    "location": "华山思过崖",
    "quests": ["剑宗复仇"]
  },
  "stats": {
    "hp": 250,
    "mp": 180,
    "attack": 85,
    "defense": 60
  }
}
```

### Example: Warrior Cats Save
```json
{
  "version": 2,
  "user_id": "123456789",
  "language": "en",
  "universe": "warrior-cats",
  "character": {
    "name": "Rushpaw",
    "age_moons": 8,
    "rank": "apprentice",
    "clan": "ThunderClan",
    "mentor": "Graystripe",
    "skills": ["Forest Stalking", "Branch Leaping"]
  },
  "stats": {
    "hp": 80,
    "stamina": 60,
    "battle_skill": 40,
    "agility": 55
  }
}
```

---

## 🔄 World Switching Commands

### Switch to Another World
```bash
/yumfu switch <world-id>
```

**Examples:**
```bash
# Switch to Warrior Cats
/yumfu switch warrior-cats

# Switch back to Xiaoao Jianghu
/yumfu switch xiaoao

# Switch to Harry Potter
/yumfu switch harry-potter
```

**Result:**
```
🌍 Switching from 笑傲江湖 to Warrior Cats...
✅ Save game for 小虾米 (Lv15) saved.
🐱 Loading Warrior Cats...

No save found for Warrior Cats. Start new game? (Y/N)
```

---

### List All Your Saves
```bash
/yumfu saves
```

**Output:**
```
📂 Your Saves:

1. 笑傲江湖 (Xiaoao Jianghu)
   - Character: 小虾米
   - Faction: 华山派
   - Level: 15
   - Last played: 2026-04-02 20:30

2. Warrior Cats
   - Character: Rushpaw
   - Clan: ThunderClan
   - Rank: Apprentice (8 moons)
   - Last played: 2026-04-01 18:45

Reply /yumfu load <number> to switch.
```

---

### Load Specific Save
```bash
/yumfu load <number>
```

**Example:**
```bash
/yumfu load 2
→ Loads Warrior Cats save

You pad into ThunderClan camp. Graystripe nods at you.
"Ready for training, Rushpaw?"
```

---

## 🛡️ Save Isolation & Protection

### Automatic Universe Detection
```
# When you /yumfu continue
→ System checks last played world
→ Loads correct save automatically

# If you trained "华山剑法" in Xiaoao
→ It's saved to saves/xiaoao/user-*.json

# When you switch to Warrior Cats
→ 华山剑法 is NOT in your Warrior Cats save
→ Separate skill trees, separate progressions
```

### Error Prevention
```bash
# If you try to use Xiaoao skills in Warrior Cats
> /yumfu train 华山剑法

❌ Error: Skill "华山剑法" not found.
You are currently in: Warrior Cats
Available skills: Forest Stalking, Swimming, Battle Moves, etc.

💡 Hint: Use /yumfu switch xiaoao to return to 笑傲江湖.
```

---

## 🎮 Recommended Workflow

### Scenario 1: Play Multiple Worlds Simultaneously
```bash
# Morning: Play Xiaoao (Chinese wuxia)
/yumfu switch xiaoao
/yumfu continue
> 修炼华山剑法，探索思过崖...

# Evening: Play Warrior Cats (English)
/yumfu switch warrior-cats
/yumfu continue
> Hunt mice, attend Gathering, battle ShadowClan...
```

### Scenario 2: Start New World After Beating One
```bash
# Beat Xiaoao Jianghu
[恭喜！你已击败东方不败，成为武林至尊！]

# Start fresh in Warrior Cats
/yumfu switch warrior-cats
[New game started. Welcome to ThunderClan, young kit...]
```

### Scenario 3: Quick Switch Between Games
```bash
# Auto-switch to last played world
/yumfu continue
→ Loads Warrior Cats (last played 5 minutes ago)

# Explicit switch
/yumfu switch xiaoao
/yumfu continue
→ Loads 笑傲江湖 progress
```

---

## 🔧 Technical Details

### Save File Naming Convention
```
saves/<universe-id>/user-<telegram-id>.json
```

**Why?**
- ✅ No file name conflicts between worlds
- ✅ Easy to manage multiple characters
- ✅ Automatic backup per world (scripts/backup.sh)

### World State Isolation
```
saves/xiaoao/world-state.json        # 笑傲江湖 shared NPCs
saves/warrior-cats/world-state.json  # ThunderClan shared state
```

**Benefit:**
- Killing "洪七公" in Xiaoao **does NOT** affect Warrior Cats
- Each world has independent timeline and events

### Version Migration
```
# v1 saves (old, single-world)
~/clawd/memory/yumfu-save.json

# v2 saves (new, multi-world)
~/clawd/memory/yumfu/saves/<world>/user-*.json

# Auto-migration script
/yumfu migrate
→ Converts v1 → v2, moves to saves/xiaoao/
```

---

## 🎯 Summary

| Command | Effect |
|---------|--------|
| `/yumfu switch <world>` | Switch to another universe |
| `/yumfu saves` | List all your saves |
| `/yumfu load <num>` | Load specific save |
| `/yumfu continue` | Resume last played world |
| `/yumfu save` | Manual save (auto-saves on quit) |

**Key Points:**
1. ✅ **Each world has separate save files**
2. ✅ **Skills/items don't mix between worlds**
3. ✅ **Switch anytime without losing progress**
4. ✅ **Auto-detects last played world**
5. ✅ **Local backup per world (Git)**

---

**Play 笑傲江湖 in the morning, hunt with ThunderClan at night!** 🌏⚔️🐱
