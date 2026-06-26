# Zen Koan Daily | 每日禅宗公案 🎋

**Daily Zen Buddhist koan with AI ink wash art and audio narration**

每日禅宗公案配AI水墨画和语音讲解

[![License: GPL v3](https://img.shields.io/badge/License-GPLv3-blue.svg)](https://www.gnu.org/licenses/gpl-3.0)
[![ClawHub](https://img.shields.io/badge/ClawHub-zen--koan--daily-purple)](https://clawhub.ai/skills/zen-koan-daily)

---

## ✨ Features | 特色功能

🎋 **Complete Koan Experience | 完整公案体验**

Every day, receive a full Zen koan lecture包括：

- 📜 **Original Text** - Classical Chinese + English translation
- 📖 **Historical Background** - Context and lineage
- 💡 **Deep Interpretation** - Traditional Zen commentary
- 🌏 **Modern Insights** - Application to contemporary life
- 🎨 **Zen Ink Wash Art** - AI-generated Chinese painting
- 🔊 **Audio Narration** - TTS in Chinese or English

---

## 🚀 Quick Start | 快速开始

### Installation | 安装

**OpenClaw:**
```bash
clawhub install zen-koan-daily
```

**Standalone:**
```bash
git clone https://github.com/yumyumtum/yumskills.git
cd yumskills/zen-koan-daily
pipx install edge-tts  # For TTS audio
export GEMINI_API_KEY="your-key"  # For images
```

### Usage | 使用

**Get today's koan:**
```
/koan
```

**Specific koan:**
```
/koan 1
```

**In English:**
```
/koan next --lang en
```

---

## 📚 Koan Collection | 公案收录

**Generation Mode:** 🤖 **Dynamic LLM Generation**

**Stored Reference Koans:** 2 examples
1. **赵州狗子** (Zhaozhou's Dog) - *The Gateless Gate* #1
   - Theme: Buddha-nature, non-dualism
   - Difficulty: Beginner
   
2. **平常心是道** (Ordinary Mind is the Way)
   - Theme: Non-seeking, naturalness
   - Difficulty: Beginner

**All Other Koans:** Generated dynamically by LLM from classical sources:
- 无门关 (The Gateless Gate) - 48 cases
- 碧岩录 (Blue Cliff Record) - 100 cases
- 从容录 (Book of Serenity) - 100 cases
- 景德传灯录 (Transmission of the Lamp)
- 五灯会元 (Five Lamps Meeting at the Source)

**Why Dynamic Generation?**
- ✅ LLM quality verified through extensive testing
- ✅ Unlimited variety from 300+ classical koans
- ✅ Fresh interpretations tailored to modern life
- ✅ No need to manually curate 50-100 entries
- ✅ Optional web search for contemporary Zen teachings

---

## 🎨 Visual Style | 视觉风格

**Chinese Zen Ink Wash (禅宗水墨画)**

- Minimalist composition with vast empty space (留白)
- Subtle black ink gradations on rice paper
- Sparse brushstrokes
- Meditative atmosphere
- Traditional calligraphy aesthetic

**Example themes:**
- Dog silhouette + bamboo + moon (Zhaozhou's Dog)
- Vast sky + simple tea cup (Ordinary Mind)
- Misty mountain + pine tree (Nature koans)

---

## 🔊 Audio | 音频

**TTS Voices:**
- **Chinese**: `zh-CN-XiaoxiaoNeural` (晓晓 - warm, contemplative)
- **English**: `en-US-AriaNeural` (Aria - calm, narrative)

**Free service:** Edge TTS (no API key needed)

---

## 📖 Example Output | 示例输出

```
🎋 每日禅宗公案 | Daily Zen Koan

━━━━━━━━━━━━━━━━━━━━━━━━

**赵州狗子**
*无门关 第1则*

━━━━━━━━━━━━━━━━━━━━━━━━

📜 **原文**

僧问赵州：「狗子还有佛性也无？」州云：「无。」

━━━━━━━━━━━━━━━━━━━━━━━━

📖 **背景**

赵州从谂禅师（778-897）是唐代著名禅师，以平实直截的禅风著称...

━━━━━━━━━━━━━━━━━━━━━━━━

💡 **白话解读**

赵州答「无」，并非否定佛性，而是斩断概念思维...

━━━━━━━━━━━━━━━━━━━━━━━━

🌏 **现代启示**

现代人陷入「有用/无用」「成功/失败」的二元思维...

━━━━━━━━━━━━━━━━━━━━━━━━

🏷️ 难度：beginner | 流派：rinzai
🔖 标签：buddha-nature, dualism, wu, 直指人心
```

**Plus:**
- 🎨 Zen ink wash painting (PNG)
- 🔊 Audio narration (MP3)

---

## 🛠️ Technical Details | 技术细节

**Stack:**
- Python 3.10+ (reference koan loader, optional)
- **LLM** (primary koan generation engine)
- Edge TTS (free TTS service)
- Google Gemini API (for ink wash images)
- Minimal JSON database (2 reference koans only)

**File Structure:**
```
zen-koan-daily/
├── scripts/
│   ├── generate_koan.py    # Main koan generator
│   ├── generate_image.py   # Zen ink wash art
│   └── generate_tts.sh     # Audio narration
├── references/
│   ├── koans.json          # Koan database
│   ├── progress.json       # Delivery tracking
│   └── templates/          # Lecture templates
├── SKILL.md                # OpenClaw agent instructions
└── README.md               # This file
```

**Progress Tracking:**
- Auto-cycles through all koans
- No repeats until full cycle complete
- Stores delivery history

---

## 📅 Daily Delivery | 每日推送

**OpenClaw Cron (recommended):**

Set up daily koan at 6:00 AM:

```json
{
  "name": "Daily Zen Koan",
  "schedule": {
    "kind": "cron",
    "expr": "0 6 * * *",
    "tz": "America/Los_Angeles"
  },
  "sessionTarget": "isolated",
  "payload": {
    "kind": "agentTurn",
    "message": "/koan next"
  }
}
```

---

## 🌏 Language Support | 语言支持

**Fully bilingual:**
- Chinese (中文) - Complete lectures with classical texts
- English - Full translations and commentary
- Mixed mode - Both languages in one output

**Commands:**
- `/koan` → Default language (Chinese)
- `/koan --lang en` → English
- `/koan --lang both` → Bilingual

---

## 🎯 Use Cases | 使用场景

1. **Daily Spiritual Practice | 每日修行**
   - Morning meditation companion
   - Contemplative reading
   - Mindfulness reminder

2. **Zen Study | 禅宗学习**
   - Progressive koan study
   - Understanding classical texts
   - Modern application

3. **Art & Philosophy | 艺术与哲学**
   - Zen aesthetic appreciation
   - Eastern philosophy exploration
   - Minimalist art inspiration

4. **Content Creation | 内容创作**
   - Daily social media posts
   - Philosophical newsletters
   - Zen-themed content

---

## 📜 License | 许可证

**GPL-3.0-or-later**

Free and open source. Use, modify, and share freely.

---

## 🙏 Credits | 致谢

**Koan Sources:**
- *The Gateless Gate* (无门关) - Wumen Huikai
- *Transmission of the Lamp* (景德传灯录)
- *Blue Cliff Record* (碧岩录)
- Classical Zen literature

**Technology:**
- Edge TTS by Microsoft
- Google Gemini AI
- OpenClaw skill framework

---

## 🔗 Related Projects | 相关项目

- **[Continuance](../continuance/)** - Daily spiritual guidance from The Book of Continuance
- **[YumFu](../yumfu/)** - Multi-world MUD game
- **[Nano Banana Pro](../nano-banana-pro/)** - AI image generation

---

*"不立文字，教外别传，直指人心，见性成佛。"*

*"Not relying on words and letters; a special transmission outside the scriptures; pointing directly to the human mind; seeing one's nature and becoming Buddha."*

— Bodhidharma | 菩提达摩

---

**Made with 🎋 by Tommy Yan**

GitHub: [@yumyumtum](https://github.com/yumyumtum)  
ClawHub: [yumyumtum](https://clawhub.ai/yumyumtum)
