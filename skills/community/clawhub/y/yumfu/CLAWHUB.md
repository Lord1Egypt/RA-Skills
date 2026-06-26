# 🌍 YumFu - Multi-World Text Adventure MUD

<div align="center">

**Choose Your Adventure** | **选择你的冒险**

[![License: GPL v3](https://img.shields.io/badge/License-GPLv3-blue.svg)](https://www.gnu.org/licenses/gpl-3.0)
[![ClawHub](https://img.shields.io/badge/ClawHub-yumfu-purple)](https://clawhub.ai/skills/yumfu)
[![Version](https://img.shields.io/badge/version-1.0.0-green)](https://github.com/yumyumtum/yumfu)

*Play epic text adventures with AI-generated art across multiple fantasy universes*

</div>

---

## 🎮 What is YumFu?

**YumFu** is a **multi-world text adventure MUD (Multi-User Dungeon)** that combines:
- 📖 **Rich storytelling** in authentic genre styles (Wuxia, Fantasy, Feral Cats)
- 🎨 **AI-generated artwork** for every key scene
- 🗣️ **Natural language** gameplay (no need to memorize commands!)
- 🌐 **Bilingual** support (中文 & English)
- 💾 **Persistent saves** across sessions
- 🤝 **Multiplayer** PvP and co-op (OpenClaw only)

### 🌐 Available Worlds

<table>
<tr>
<td width="50%" valign="top">

#### 🇨🇳 **Chinese Wuxia** (中文武侠)

- ⚔️ **笑傲江湖** (Swordsman) - Mt. Hua, Wudang, Shaolin
- 🗡️ **倚天屠龙记** (Heaven Sword & Dragon Saber) - Ming Cult, Wudang *(NEW!)*
- 🐉 **射雕英雄传** (Legend of the Condor Heroes) *(coming soon)*

**Style**: 水墨武侠风 (Ink wash painting aesthetic)

</td>
<td width="50%" valign="top">

#### 🇬🇧 **English Fantasy** (英文奇幻)

- ⚡ **Harry Potter** - Hogwarts, four houses, wizarding duels
- 🐱 **Warrior Cats** - ThunderClan, RiverClan, warrior code
- 🗡️ **Lord of the Rings** - Middle-earth, Fellowship *(NEW!)*
- 🐉 **Game of Thrones** - Westeros, Iron Throne *(NEW!)*

**Style**: Watercolor storybook / Semi-realistic illustration

</td>
</tr>
</table>

---

## ✨ Key Features

### 🗣️ **Natural Language Gameplay**
```
You don't need commands!

❌ Old way: /yumfu fight wild boar
✅ New way: "I want to attack the goblin with my sword"

❌ Old way: /yumfu train 华山剑法  
✅ New way: "我想去找风清扬学独孤九剑"
```

### 🎨 **AI-Generated Scene Art**
Every significant moment gets a beautiful illustration:
- 🏞️ New location arrivals
- 👤 NPC encounters
- ⚔️ Combat starts
- 📚 Training completions
- 🎭 Plot milestones

**Example**:
![Warrior Cats Nursery](assets/screenshots/warrior-cats-nursery.png)
*ThunderClan kits playing in the nursery - Auto-generated with Warrior Cats art style*

### 💾 **Persistent Character Progression**
- **Level 1-100** skill trees
- **Multiple save slots** per world
- **Cross-session memory** (your progress is never lost!)
- **Relationship tracking** with NPCs

### 🤝 **Multiplayer Support** *(OpenClaw only)*
- **PvP duels** - Challenge other players
- **Co-op teams** - Form fellowships/sects
- **Shared world state** - Actions affect everyone
- **Cross-platform** - Telegram, Discord, WhatsApp groups

---

## 🚀 Quick Start

### Installation
```bash
clawhub install yumfu
```

### Requirements
- **Python 3.x** with `uv` (for image generation)
- **GEMINI_API_KEY** (optional, for AI art - free tier available)
- **OpenClaw** (for full multiplayer support)

### First Game
Just say:
```
"I want to play a wuxia adventure"
"Let's start a Harry Potter game"
"Play Warrior Cats"
```

Your AI agent will:
1. ✅ Load the YumFu skill
2. ✅ Guide you through character creation
3. ✅ Generate your first scene artwork
4. ✅ Begin your adventure!

---

## 📖 Example Gameplay

### ⚔️ 笑傲江湖 (Wuxia Example)

**Commands** (optional):
```
> /yumfu train 华山剑法
你在思过崖苦练剑法，突然领悟了「有凤来仪」...
[华山剑法] Lv1 → Lv2
```

**Natural Language** (recommended):
```
> "我想去找风清扬学独孤九剑"
你登上思过崖，一位白发老者正在对弈...

> "向风清扬行礼，请求传授剑法"
风清扬看了你一眼："有点根骨，先破解这三招。"
[开始] 剑法测试
```

*AI generates: Misty mountain peak with lone swordsman, Chinese ink wash style*

---

### ⚡ Harry Potter (Fantasy Example)

**Commands** (optional):
```
> /yumfu train Expelliarmus
You practice the Disarming Charm in the Room of Requirement...
[Expelliarmus] Lv1 → Lv2
```

**Natural Language** (recommended):
```
> "I want to explore the Forbidden Forest"
You step past Hagrid's hut into the shadowy woods...

> "Cast Lumos to light the way"
Your wand-tip ignites! Spiders scatter in the silver glow.
[Learned] Lumos (Basic Light Charm)
```

*AI generates: Dark forest path with glowing wand light, watercolor style*

---

### 🐱 Warrior Cats (Feral Cat Example)

**Natural Language**:
```
> "I want to go on a border patrol with my mentor"
Willowpelt nods. "Follow me to the ShadowClan border, Rushpaw."

> "Sniff the air for enemy scent"
You taste the wind... RiverClan! Fresh markers, less than a sunrise old.
[Learned] Scent Tracking
```

*AI generates: Forest border scene with feral cats, semi-realistic illustration*

---

## 🎯 Game Systems

### 📊 **Character Progression**
- **Level 1-100** with XP system
- **Skill trees** unique to each world
- **Faction reputation** (华山派、Slytherin、ThunderClan)
- **Achievement system** (14+ achievements per world)

### ⚔️ **Combat System**
- **Turn-based** with dice rolls (1d20 + modifiers)
- **Multiple combat styles** (剑法、咒语、爪击)
- **Transparent mechanics** - see all dice results!
- **PvP support** - challenge other players

### 👥 **NPC Relationships**
- **Affection/Loyalty tracking** (0-100%)
- **Dynamic dialogue** based on relationship
- **Quest givers** and mentors
- **Romance options** *(in some worlds)*

### 🗺️ **World Exploration**
- **Multiple locations** per world (20+ areas)
- **Hidden secrets** and easter eggs
- **Cross-world references** (find connections between universes!)

---

## 🛠️ Technical Highlights

### 🔧 **Unified Save/Load System**
YumFu includes production-ready save/load scripts:
```bash
# Load user progress
uv run scripts/load_game.py --user-id {id} --universe xiaoao

# Save user progress  
echo '{...}' | uv run scripts/save_game.py --user-id {id} --universe xiaoao
```

**Features**:
- ✅ Automatic backups before overwriting
- ✅ UTF-8 support (中文、emoji、special characters)
- ✅ Emergency fallback to `/tmp` if primary path fails
- ✅ Multi-user tested (5 concurrent users, 0 conflicts)

See `scripts/SAVE_LOAD_REFERENCE.md` for full API.

---

### 🎨 **AI Art Generation**
Each world has its own signature art style:

| World | Style | Engine |
|-------|-------|--------|
| 笑傲江湖 | 水墨武侠风 (Ink wash) | Gemini 3 Pro Image |
| Harry Potter | Watercolor storybook | Gemini 3 Pro Image |
| Warrior Cats | Semi-realistic feral cats | Gemini 3 Pro Image |
| LOTR | Fantasy oil painting | Gemini 3 Pro Image |
| Game of Thrones | Medieval realistic | Gemini 3 Pro Image |

**Auto-trigger rules**:
- New location → Generate
- NPC encounter → Generate
- Combat start → Generate
- Training complete → Generate
- Plot milestone → Generate

---

## 🌍 Platform Compatibility

### ✅ **Full Support: OpenClaw**
- Multiplayer (PvP, teams, shared world)
- Auto-send images to Telegram/Discord/WhatsApp
- Persistent saves across devices
- Natural language + commands

### ⚠️ **Partial Support: Claude Code / Native Claude**
- Single-player only
- Manual image viewing (copy file path)
- Text-only mode available (`YUMFU_NO_IMAGES=1`)

---

## 📂 Project Structure

```
yumfu/
├── SKILL.md                 # Full agent instructions
├── README.md                # GitHub documentation
├── CLAWHUB.md              # This file (ClawHub page)
├── LICENSE                  # GPLv3
├── worlds/                  # World configurations
│   ├── xiaoao.json          # 笑傲江湖
│   ├── harry-potter.json    # Harry Potter
│   ├── warrior-cats.json    # Warrior Cats
│   ├── lotr.json            # Lord of the Rings (NEW!)
│   └── game-of-thrones.json # Game of Thrones (NEW!)
├── i18n/                    # Localization
│   ├── zh.json              # Chinese UI
│   └── en.json              # English UI
├── scripts/
│   ├── generate_image.py    # AI art generation
│   ├── save_game.py         # Unified save system
│   ├── load_game.py         # Unified load system
│   └── SAVE_LOAD_REFERENCE.md
└── assets/
    └── screenshots/         # Example images
```

---

## 🗺️ Roadmap

### ✅ **Phase 1** (Complete)
- [x] Chinese wuxia (笑傲江湖、倚天屠龙记)
- [x] English fantasy (Harry Potter, Warrior Cats, LOTR, GoT)
- [x] Bilingual UI
- [x] Unified save/load system
- [x] Natural language gameplay
- [x] AI art generation

### 🚧 **Phase 2** (In Progress)
- [ ] More Chinese worlds (射雕英雄传、天龙八部)
- [ ] More English worlds (The Witcher, Naruto, Star Wars)
- [ ] Cross-world easter eggs
- [ ] Advanced multiplayer (guilds, raids)

### 🔮 **Phase 3** (Future)
- [ ] Community-contributed worlds
- [ ] Custom world editor
- [ ] Character import across worlds
- [ ] Voice narration (TTS integration)

---

## 🤝 Contributing

Want to add a new world? See [MULTI-WORLD-DESIGN.md](MULTI-WORLD-DESIGN.md) for the template!

**Ideas for new worlds**:
- 🥷 Naruto (ninja villages, jutsu system)
- 🌌 Star Wars (Jedi/Sith, Force powers)
- 🏛️ Greek Mythology (gods, quests, Olympus)
- 🤖 Cyberpunk 2077 (netrunners, corpo)
- 🧙 The Witcher (monster hunting, Signs, alchemy)

---

## 📜 License

**GPLv3** - This ensures YumFu and all derivative works remain open source forever.

- ✅ Free to use, modify, and distribute
- ✅ Commercial use allowed
- ⚠️ Derivative works must also be GPLv3

See [LICENSE](LICENSE) for full text.

---

## 🔗 Links

- **GitHub**: https://github.com/yumyumtum/yumfu
- **ClawHub**: https://clawhub.ai/skills/yumfu
- **Issues**: https://github.com/yumyumtum/yumfu/issues
- **Discord**: *(Join the OpenClaw community!)*

---

<div align="center">

**江湖路远，侠之大者！**  
**The adventure awaits, brave wizard!**  
**May StarClan light your path!**

⚔️🪄🐱

*Made with ❤️ by @yumyumtum*

</div>
