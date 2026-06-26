# YumFu - Multi-World MUD 🌍⚔️🧩

[![License: GPL v3](https://img.shields.io/badge/License-GPLv3-blue.svg)](https://www.gnu.org/licenses/gpl-3.0)
[![Security](https://img.shields.io/badge/security-audited-green.svg)](SECURITY.md)
[![Safe Code](https://img.shields.io/badge/code-no%20eval-brightgreen.svg)](SECURITY.md)
[![ClawHub](https://img.shields.io/badge/ClawHub-yumfu-purple)](https://clawhub.ai/skills/yumfu)
[![Multiplayer](https://img.shields.io/badge/multiplayer-Telegram%20%26%20Discord-blue)](https://clawhub.ai/skills/yumfu)
[![Support via Stripe](https://img.shields.io/badge/Support-Stripe-635BFF?style=flat&logo=stripe&logoColor=white)](https://buy.stripe.com/8x26oHc329ha6GvaiggjC00)

> **A chat-native multiplayer RPG skill for OpenClaw.**
>
> Play inside Telegram groups, Discord, or other chat surfaces with:
> - **AI-generated scene art**
> - **voice / narrated story delivery**
> - **illustrated storybooks and demos**
> - **shared world state for group play**

**Think:** _MUD + AI art + voice story + multiplayer group chat chaos._

## Why YumFu gets attention

Most chat games are either command-heavy, single-player, or visually flat.
YumFu is different because it treats chat as the actual game surface:

- players can progress with **natural language**, not just rigid commands
- major turns can arrive with **matching AI scene art**
- sessions can become **audio stories** and **illustrated storybooks**
- worlds are built for **shared multiplayer play**, not just solo prompting

That makes YumFu easier to show, easier to share, and much more fun to demo
than a typical text RPG.

## Fast pitch

Add YumFu to a group chat and people can:

- team up on quests
- duel each other in PvP
- play in different worlds and tones
- generate memorable scenes worth screenshotting
- turn a session into something replayable or shareable later

## Live demos

- **Storybook index:** <https://yumyumtum.github.io/yumfu/storybooks/>
- **Featured demo — Journey to the West / White Bone:**
  <https://yumyumtum.github.io/yumfu/storybooks/journey-to-west-white-bone/>
- **Blog / showcase notes:** <https://yumyumtum.github.io/yumfu/blog/>
- **Community Discord:** <https://discord.gg/g6zBMHpP8>

![YumFu Fun Discord QR](docs/community/yumfu-fun-discord-qr.jpg)

## ✨ Why YumFu feels different

- 🎨 **Automatic AI scene art** — major moments can arrive with matching world-specific illustrations
- 🎧 **Audio story delivery** — turns can be turned into voice bubbles / narrated story audio
- 📚 **Art storybooks** — your sessions can become shareable illustrated storybooks and PDFs
- 🌐 **Storybook demos** — publishable HTML demos can live under `docs/storybooks/` for GitHub Pages showcase
  - Live index: <https://yumyumtum.github.io/yumfu/storybooks/>
  - Featured demo: <https://yumyumtum.github.io/yumfu/storybooks/journey-to-west-white-bone/>
- 👥 **Multiplayer-first** — play inside group chats with PvP, teams, and shared world state
- 🌍 **Multi-world, multi-language** — wuxia, magic school, epic fantasy, modern war, myth, comedy
- 💬 **Natural language play** — just talk instead of memorizing commands

## 💖 Support YumFu

If YumFu helped you or made you smile, you can support future development here:

[Donate via Stripe](https://buy.stripe.com/8x26oHc329ha6GvaiggjC00)

---

## 🌍 Worlds to Explore

| World | Genre | Language | Status |
|-------|-------|----------|--------|
| ⚔️ **笑傲江湖** (Xiaoao Jianghu) | Wuxia martial arts | 中文 | ✅ Playable |
| ⚡ **Harry Potter** | Magic school | English | ✅ Playable |
| 🐱 **Warrior Cats** | Animal clan survival | English | ✅ Playable |
| 🛵 **F15 Down: Azure Peninsula War** | Modern military | 中/EN | ✅ Playable |
| 🦞 **龙虾三国** (Three Kingdoms) | Historical strategy | 中文 | ✅ Playable |
| 🗡️ **倚天屠龙记** (Heaven Sword & Dragon Saber) | Wuxia romance | 中文 | ✅ Playable |
| 🐉 **Game of Thrones** | Dark fantasy politics | English | ✅ Playable |
| 🧙 **Lord of the Rings** | Epic fantasy quest | English | ✅ Playable |
| 🐒 **西游记** (Journey to the West) | Mythological RPG | 中文/EN | ✅ Playable |
| 🩲 **内裤超人** (Captain Underpants) | Comedy chaos RPG | 中/EN | ✅ Playable |
| 🏹 **射雕英雄传** (Legend of Condor Heroes) | Jin Yong wuxia | 中文 | 🚧 Coming |

---

## 👥 Multiplayer in Telegram Groups

YumFu is built for **group play**. Add it to any Telegram group and everyone adventures in the same world:

- 🤝 **Team up** — form parties, tackle quests together
- ⚔️ **PvP duels** — challenge friends to fights
- 🌍 **Shared world** — your actions affect everyone (kill a boss, it stays dead)
- 🏆 **Leaderboards** — compete for top rank in your group
- 💬 **Natural language** — no slash commands mid-game, just chat!

### How to start in a group

```
1. Add your OpenClaw bot to a Telegram group
2. Alice: /yumfu start  →  Bot: Choose your world... [AI art]
3. Bob:  /yumfu start  →  Bot: Bob joins! Alice is in 洛阳城
4. Alice: 我要与玩家切磋！  →  Bot: ⚔️ PvP 开始！[Epic battle scene]
```

**Works on**: Telegram groups · Discord · WhatsApp · Any OpenClaw platform

---

## 🚀 Installation

### OpenClaw (Recommended)

For Telegram, Discord, WhatsApp, and other OpenClaw platforms:

```bash
clawhub install yumfu
```

Then start playing:
```
/yumfu start
```

### Standalone (GitHub)

For local development or non-OpenClaw use:

```bash
git clone https://github.com/yumyumtum/yumfu.git
cd yumfu
uv sync

# Optional: Enable AI image generation
export GEMINI_API_KEY="your-key-here"

# Start playing
/yumfu start
```

**Requirements**:
- Python 3.10+
- [uv](https://github.com/astral-sh/uv) package manager
- (Optional) Google Gemini API key for AI images

---

## 🔒 Data Storage

YumFu stores all game data **locally** on your machine:

- ✅ **Game saves**: `~/clawd/memory/yumfu/saves/`
- ✅ **AI images**: `~/.openclaw/media/outbound/yumfu/`
- ✅ **Session logs**: `~/clawd/memory/yumfu/sessions/` (for storybook generation)
- ✅ **No telemetry or tracking**
- ✅ **Open source**: Fully auditable (GPLv3)

**External API**: Google Gemini (optional, for AI image generation only)

---

## 🎨 World Showcase

<table>
<tr>
<td width="50%">

### 🛵 F15 Down: Azure Peninsula War
![F15 Down Showcase](docs/showcase/showcase-f15down.jpg)
*Modern military chaos — damaged aircraft, desert coastline, command decisions, frontline survival*

</td>
<td width="50%">

### 🐉 Game of Thrones / Dorne
![Game of Thrones Dorne Showcase](docs/showcase/showcase-got-dorne.png)
*Political danger in Sunspear — desert palaces, noble intrigue, dangerous private choices*

</td>
</tr>
<tr>
<td width="50%">

### ⚔️ Chinese Wuxia
![Chinese Wuxia](docs/showcase/showcase-xiaoao-jianghu.png)
*Ancient martial arts world — traditional temples, misty mountains, heroic swordsmen*

</td>
<td width="50%">

### ⚡ Wizard School
![Wizard School](docs/showcase/showcase-harry-potter.png)
*Magical academy — enchanted halls, underground chambers, spell practice, house rivalries*

</td>
</tr>
</table>

### 🩸 Sengoku / Honnō-ji Showcase

![Honnō-ji Beheading Showcase](docs/showcase/showcase-honnouji-beheading.jpg)
*One-stroke execution at Honnō-ji — a high-drama Sengoku turn with loot, politics, and aftermath choices.*

- English scene write-up: [docs/showcase/honnouji-beheading.md](docs/showcase/honnouji-beheading.md)

*All showcase images are generated from real YumFu gameplay with world-specific art direction.*

### 📖 Live Storybook Demo

- **Journey to the West — White Bone**
  - <https://yumyumtum.github.io/yumfu/storybooks/journey-to-west-white-bone/>
- **All storybook demos**
  - <https://yumyumtum.github.io/yumfu/storybooks/>

---

## 🌎 Available Worlds

YumFu offers multiple fantasy universes to explore. Each world has unique gameplay mechanics, art styles, and storylines.

### 🇨🇳 Chinese Wuxia & Historical (中文武侠/历史)
- ⚔️ **Swordsman Tales** (笑傲江湖) - Martial arts sects, honor duels, legendary techniques
- 🦞 **Lobster Three Kingdoms** (龙虾三国) - Three Kingdoms era strategy, 5 roles, weapons/mounts/ultimate skills ✅ **NEW**
- 🗡️ **Dragon & Sword Epic** (倚天屠龙记) - Ancient artifacts, mystical powers *(coming soon)*

### 🇬🇧 Western Fantasy
- ⚡ **Wizard School** - Magic academy, four houses, spell duels
- 🐱 **Warrior Clans** - Feline tribes, forest territories, clan politics
- 🗡️ **Middle-earth Quest** - Epic journey, fellowship, ancient evil ✅
- 🐉 **Medieval Kingdoms** - Political intrigue, noble houses, throne wars ✅
- 🐺 **Monster Hunter** - Witcher-inspired adventures *(coming soon)*

### 🪖 Modern Military (现代军事)
- 🛵 **F15 Down: Azure Peninsula War** - Fictional Middle East conflict, dual-path strategy/frontline combat, Command & Conquer aesthetic ✅ **NEW**
  - Play as **Defense Minister** (strategic decisions) or **14 frontline roles** (F-15 pilot, B-2 bomber, flying moped operator, drone operator, special forces...)
  - 30+ decision nodes, 8 unique endings, NPC memory system
  - Art style: Command & Conquer Generals RTS aesthetic

---

## 🚀 Quick Start

### Installation

**For OpenClaw Users** (Telegram, Discord, etc.):
```bash
clawhub install yumfu
```

**For GitHub Users**:
```bash
# Clone the repository
git clone https://github.com/yumyumtum/yumfu.git
cd yumfu

# Install dependencies
uv sync

# Optional: Set up AI image generation
export GEMINI_API_KEY="your-key-here"

# Start playing!
/yumfu start
```

**Quick Links**:
- 📦 ClawHub: [clawhub.ai/skills/yumfu](https://clawhub.ai/skills/yumfu)
- 🐙 GitHub: [github.com/yumyumtum/yumfu](https://github.com/yumyumtum/yumfu)
- 📖 Documentation: See [SKILL.md](SKILL.md) for full agent instructions

---

### 🎮 Two Ways to Play

**Option 1: Commands** (Classic MUD style)
```bash
/yumfu start
/yumfu look
/yumfu fight wild boar
```

**Option 2: Natural Language** (Just talk!)
```
"I want to explore the forest"
"Attack the goblin with my sword"
"Talk to Dumbledore about the Elder Wand"
"我想去华山派学剑法"
```

**💡 Pro Tip**: You don't need to use `/yumfu` commands! Your AI agent understands natural language. Just describe what you want to do in the game, and the agent will handle it.

---

### 📖 Setup Steps

**Step 1: Choose Language** | **选择语言**
```
🌍 Welcome to YumFu! | 欢迎来到YumFu！

1. 中文 (Chinese)
2. English

Reply: /yumfu lang 1  (or just say "Chinese please")
```

**Step 2: Choose Your World** | **选择世界**
```
Choose your realm:

1. ⚔️ 笑傲江湖 (Xiaoao Jianghu)
2. ⚡ Wizard School Universe
3. 🐱 Warrior Clans

Reply: /yumfu world 3  (or just say "I want to play Warrior Clans")
```

**Step 3: Start Your Adventure!**

---

## ✨ Features

- 🗣️ **Natural Language** - Just talk; no need to memorize command syntax
- 🌍 **Multi-language** - Chinese & English
- 🎭 **Multiple universes** - Wuxia, wizard school, epic fantasy, modern war, myth, comedy
- 🎨 **Automatic AI image generation** - scenes can arrive with world-matched art
- 🎧 **Audio story mode** - gameplay turns can be delivered as narrated voice bubbles / story audio
- 📚 **Art storybooks** - session logs can be turned into illustrated HTML / PDF storybooks
- 🤝 **Multiplayer** - PvP, teams, shared world state (OpenClaw-first)
- 💾 **Save system** - Multiple save slots per world

---

## 🎮 Core Systems

- **Character progression** - Level 1-100, skill trees
- **Combat system** - Turn-based with strategy
- **Faction reputation** - Join houses/sects, earn respect
- **Legendary artifacts** - Elder Wand, One Ring, Nine Yin Manual...
- **NPC interactions** - Dumbledore, Gandalf, Dongfang Bubai...

---

## 平台兼容性 | Platform Compatibility

**✅ Full support: OpenClaw**
- Multiplayer (PvP, teams)
- Auto-send images
- Telegram groups

**⚠️ Partial support: Claude Code / Native Claude**
- Single-player only
- Manual image viewing
- See `COMPATIBILITY.md`

---

## 配置 | Configuration

**Required:**
- `GEMINI_API_KEY` (for AI art generation, optional)
- Python 3.x + `uv` (to run image scripts)

**Optional:**
- `YUMFU_NO_IMAGES=1` - Text-only mode (no API key needed)

---

## 📂 Project Structure

```
yumfu/
├── worlds/              # World configurations
│   ├── xiaoao.json      # 笑傲江湖
│   └── harry-potter.json # Wizard School
├── i18n/                # Localization
│   ├── zh.json          # Chinese UI
│   └── en.json          # English UI
├── scripts/
│   ├── generate_image.py  # AI art generation
│   └── backup.sh          # Local save backup
├── SKILL.md             # Full documentation
├── MULTI-WORLD-DESIGN.md # Design philosophy
└── COMPATIBILITY.md     # Platform guide
```

---


## 🎯 Example Gameplay

### 笑傲江湖 (Xiaoao Jianghu)

**Using Commands:**
```
你来到华山派，宁中则看着你说："孩子，江湖险恶，好好修炼。"
[获得] 华山剑谱（初级）
[体力] 100/100  [内力] 50/50

> /yumfu train 华山剑法
你在思过崖苦练剑法，突然领悟了「有凤来仪」...
[华山剑法] Lv1 → Lv2
```

**Using Natural Language:**
```
> "我想去找风清扬学独孤九剑"
你登上思过崖，一位白发老者正在对弈...

> "向风清扬行礼，请求传授剑法"
风清扬看了你一眼："有点根骨，先破解这三招。"
[开始] 剑法测试
```

---

### Wizard School

**Using Commands:**
```
You arrive at Diagon Alley. Ollivander peers at you curiously.
"Ah, a new wand-bearer. Let me see..."
[Obtained] Phoenix Feather Wand
[HP] 100/100  [MP] 50/50

> /yumfu train Expelliarmus
You practice the Disarming Charm in the Room of Requirement...
[Expelliarmus] Lv1 → Lv2
```

**Using Natural Language:**
```
> "I want to explore the Forbidden Forest"
You step past Hagrid's hut into the shadowy woods...

> "Cast Lumos to light the way"
Your wand-tip ignites! Spiders scatter in the silver glow.
[Learned] Lumos (Basic Light Charm)
```

---

### Warrior Clans

**Using Commands:**
```
You pad into ThunderClan camp. Firestar looks at you with warm eyes.
"Welcome, young kit. You will train hard to become a warrior."
[Obtained] Apprentice Name: Rushpaw
[HP] 100/100  [Stamina] 50/50

> /yumfu hunt mouse
You crouch low in the undergrowth, tail still. A mouse scurries by...
[Success!] You caught a plump mouse for the fresh-kill pile!
[Forest Stalking] Lv1 → Lv2
```

**Using Natural Language:**
```
> "I want to go on a border patrol with my mentor"
Willowpelt nods. "Follow me to the ShadowClan border, Rushpaw."

> "Sniff the air for enemy scent"
You taste the wind... RiverClan! Fresh markers, less than a sunrise old.
[Learned] Scent Tracking
```

---

**💡 Remember**: Commands like `/yumfu fight` are optional shortcuts. You can always just talk to your agent naturally!

---

## 🤝 Contributing

Want to add a new world? See `MULTI-WORLD-DESIGN.md` for the template!

Ideas for new worlds:
- Naruto (ninja villages)
- Star Wars (Jedi/Sith)
- Greek Mythology (gods & heroes)
- Cyberpunk 2077 (netrunners & corpo)

---

## 🔗 More YumSkills

Looking for more AI skills? Check out the **[YumSkills Collection](https://github.com/yumyumtum/YumSkills)**:

| Skill | Description | Category |
|-------|-------------|----------|
| [📊 yumstock](https://github.com/yumyumtum/YumSkills/tree/main/yumstock) | Three-pillar weighted US stock analysis with macro-gated Buy/Hold/Sell verdicts | Markets |
| [🦅 yumetfeagle](https://github.com/yumyumtum/YumSkills/tree/main/yumetfeagle) | ETF sector rotation scanner with Eagle's Pick recommendations | Markets |
| [🎋 zen-koan-daily](https://github.com/yumyumtum/YumSkills/tree/main/zen-koan-daily) | Daily Zen Buddhist koan with AI ink wash art and TTS audio | Spirituality |
| [🌱 Continuance](https://github.com/yumyumtum/YumSkills/tree/main/Continuance) | Daily spiritual guidance from The Book of Continuance | Spirituality |

**Install via ClawHub**:
```bash
clawhub install yumstock
clawhub install yumetfeagle
clawhub install zen-koan-daily
clawhub install continuance
```

---

## 📜 License

**YumFu** is licensed under the [GNU General Public License v3.0 (GPLv3)](LICENSE).

This means:
- ✅ You can **use, modify, and distribute** this software freely
- ✅ You can use it for **commercial purposes**
- ⚠️ If you distribute modified versions, you **must**:
  - Release the source code under GPLv3
  - Include the original copyright notice
  - State what changes you made

**TL;DR**: Open source forever, derivative works must also be open source.

See the [full license text](LICENSE) for details.

---

**江湖路远，侠之大者！** | **The adventure awaits, brave wizard!** ⚔️🪄
