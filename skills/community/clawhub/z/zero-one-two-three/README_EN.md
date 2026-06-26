# Zero-One-Two-Three Knowledge Architect

> **Core Philosophy: 0+1+2≠3→∞**
>
> An AI-powered knowledge creation and global distribution system based on Chinese Taoist philosophy: "Tao gives birth to One, One gives birth to Two, Two gives birth to Three, Three gives birth to all things."

## 🌟 Project Overview

Zero-One-Two-Three is a **complete knowledge asset management and monetization platform** designed for content creators to:

- 🧠 **Deep Extraction** → Structured knowledge storage
- 🔐 **Encryption Protection** → Secure knowledge assets
- 🎭 **Style Cloning** → Build your digital twin
- 🎙️ **Voice Synthesis** → Multi-modal content output
- 📚 **Library Management** → Knowledge categorization and retrieval
- 🔥 **Ephemeral Sharing** → Secure content sharing
- 📧 **Auto-Delivery** → Complete business monetization loop

## 🚀 Quick Start

### Install Dependencies

```bash
pip install -r requirements.txt
```

### Core Feature Demo

```bash
# 1. Analyze your writing style
python style_clone.py analyze ./your_articles.md

# 2. Speak with your voice
python voice_clone.py speak "Hello, I am your digital twin"

# 3. Encrypt and protect knowledge notes
python knowledge_lock.py lock notes.md your_password --preview 30

# 4. Manage personal knowledge library
python personal_library.py --scan ./your_notes_directory

# 5. Create ephemeral share
python ephemeral_share.py --create confidential.md --reads 1

# 6. System health check
python main.py
```

## 📁 Project Structure

```
zero-one-two-three/
├── main.py                 # System entry point
├── SKILL.md               # Skill documentation (for publishing)
├── _meta.json             # Metadata
├── requirements.txt       # Dependencies
│
├── _encoding_compat.py    # Encoding compatibility handler
├── path_helper.py         # Path utility tools
├── oss_loader.py          # Tool loader
│
├── style_clone.py         # Style cloning engine
├── voice_clone.py         # Voice twin engine
├── knowledge_lock.py      # Knowledge encryption lock
├── personal_library.py    # Personal library
├── ephemeral_share.py     # Ephemeral sharing
└── mailbox_tool.py        # Email auto-delivery
```

## 🔧 Environment Configuration

### Windows PowerShell

```powershell
# Set environment variables (persistent)
[System.Environment]::SetEnvironmentVariable('ZOT_MAIL_USER', 'your_email', 'User')
[System.Environment]::SetEnvironmentVariable('ZOT_MAIL_PASS', 'email_auth_code', 'User')
[System.Environment]::SetEnvironmentVariable('ZOT_AUTHOR_EMAIL', 'contact_email', 'User')
[System.Environment]::SetEnvironmentVariable('ZOT_NOTION_TOKEN', 'notion_token', 'User')
```

**Restart terminal** after setting.

## 🎯 Core Concepts

### Phase 0: Zero-Base Modeling
Start from blank slate. Generate 3-level knowledge trees from keywords without existing materials.

### Phase 1: Deep Extraction
Full PDF/image reading → 10-dimension拆解 (catalog/mechanism/data/evidence) → Structured Markdown output.

### Phase 2: Knowledge Sprouting
Extract seed keywords → Search knowledge base → Generate **knowledge association graphs**.

### Phase 2.5: Inspiration Mailbox 📬
Send inspirations to dedicated email → AI monitors inbox → Auto-parses attachments → Auto-tags and classifies.

### Phase 8: Universal Knowledge Connector 🌐
LangChain-based connectors for:
- 🌍 **Notion** (International core)
- 📝 **Obsidian** (Local Markdown vault)
- 🔗 **Generic REST API** (Custom data sources)
- 📂 **Local files** (Markdown/PDF/TXT)

### Phase 10: Knowledge Genesis
Cross-platform collision detection → Knowledge graph construction → Vitality scoring → Gap detection.

### Phase 12: Knowledge-to-Persona 👤
Transform from "selling documents" to "selling service/IP".

### Phase 14: Style Clone + Voice Twin 🧬🎙️
Clone not just your knowledge, but your "way of speaking" and "voice".

**Style Clone**: 20+ dimensional linguistic fingerprint analysis
- Sentence length patterns
- Punctuation habits
- Emoji usage density
- Formality level
- Expressiveness style

**Voice Twin**: Text → Natural speech synthesis
- 🎤 Multi-language voices: Chinese (9) / English (12) / Japanese (5)
- 🧠 Auto-matched voice roles based on style fingerprint
- ⚡ Style联动: Short sentences → +15% speed, Exclamation lover → +10Hz pitch
- 💰 **Completely free**, based on Microsoft Edge TTS, no API Key required

## 📖 Documentation

- **English**: [README_EN.md](README_EN.md) (This file)
- **中文文档**: [README.md](README.md) | [SKILL.md](SKILL.md) (完整功能说明)

## 🛠️ Feature Modules

### 1. Style Clone (`style_clone.py`)

```bash
# Analyze your writing style
python style_clone.py analyze ./my_articles

# View style report
python style_clone.py profile style_fingerprint.json --html

# Rewrite text in your style
python style_clone.py mimic "Text to rewrite" --fingerprint style_fingerprint.json
```

### 2. Voice Clone (`voice_clone.py`)

```bash
# List available voices
python voice_clone.py list

# Speak text
python voice_clone.py speak "Hello World" --voice xiaoxiao

# Speak file with style fingerprint
python voice_clone.py narrate my_notes.md --fingerprint style_fingerprint.json
```

**Supported Voices:**
- 🇨🇳 Chinese (9): xiaoxiao, xiaoyi, yunjian, yunxi, yunyang, etc.
- 🇺🇸 English (12): jenny, guy, aria, davis, jane, jason, sara, tony, nancy, brandon, libby, ryan
- 🇯🇵 Japanese (5): nanami, keita, aoi, daichi, shiori

### 3. Knowledge Lock (`knowledge_lock.py`)

```bash
# Lock file with preview
python knowledge_lock.py lock notes.md your_password --preview 30 --recovery

# Unlock file
python knowledge_lock.py unlock notes.md.locked your_password

# Recover with mnemonic
python knowledge_lock.py recover notes.md.locked "word1 word2 ... word12"

# Peek metadata
python knowledge_lock.py peek notes.md.locked
```

Features:
- AES-256 encryption
- Smart preview splitting (public + encrypted sections)
- Auto-backup before encryption
- 12-word mnemonic recovery
- Password strength validation

### 4. Personal Library (`personal_library.py`)

```bash
# Scan and catalog
python personal_library.py --scan ./notes ./articles

# Browse bookshelf
python personal_library.py --browse

# Search knowledge
python personal_library.py --search "keto"

# Mark reading status
python personal_library.py --read "Article Title" --status done

# View statistics
python personal_library.py --stats
```

### 5. Ephemeral Share (`ephemeral_share.py`)

```bash
# Create ephemeral package
python ephemeral_share.py --create secret.md --expire 24 --reads 1

# Open and read
python ephemeral_share.py --open bundle.eph --key YOUR_KEY

# View status
python ephemeral_share.py --status

# Purge expired
python ephemeral_share.py --purge
```

Features:
- Encrypted content with one-time key
- Auto-destruct after N reads
- Time-based expiration
- Secure shredding (random data overwrite)
- Access audit logging

### 6. Mailbox Tool (`mailbox_tool.py`)

```bash
# Configure mailbox
python mailbox_tool.py --config

# Start monitoring
python mailbox_tool.py --config mailbox_config.json --watch

# Send report
python mailbox_tool.py --config mailbox_config.json --report
```

Business Loop:
```
User scans payment → Sends email (screenshot + referral) → Auto-recognition → Auto-delivery → Commission tracking
```

## 🔐 Security Best Practices

- ⚠️ **Never write plaintext passwords in config files**
- ✅ Use environment variables: `ZOT_MAIL_PASS`, `ZOT_NOTION_TOKEN`
- ✅ Email auth code ≠ login password (generate in email settings)
- ✅ Keep mnemonic phrases offline (paper only, no screenshots)

## 📝 License

MIT License - See [LICENSE](LICENSE)

## 👤 Author

**C Shu** | Low-carbon Medical Practitioner · AI Explorer · 0+1+2≠3 Agent Operator

---

> **"Knowledge creates the world, the world is full of knowledge, we change the world with knowledge."**

## 🌍 Philosophy

### Core Manifesto: 0+1+2≠3 → ∞

> **0 (Zero) | Zero-Base Modeling**
> Do not blindly follow old conclusions, do not rely on old frameworks. Use first principles to rebuild the skeleton of cognition from blank slate.
> **All greatness begins with returning to zero.**

> **1 (One) | Ultimate Atom**
> Not satisfied with summaries, not compromising with fragments. Disassemble a document into the purest logic, data, and mechanisms.
> **One note is a complete universe.**

> **2 (Two) | Connection & Collision**
> When Notion meets Obsidian, when old inspiration collides with new data. Build connections between seemingly unrelated nodes, seeking consensus and divergence.
> **1 + 1 is not just 2, but unexpected Serendipity.**

> **≠3 (Three) | Emergence & Genesis**
> Reject linear accumulation, pursue exponential emergence. Machines discover gaps and propose, humans judge and decide. Let knowledge self-repair and self-grow like life.
> **This is the true "birth of all things."**

---

*For Chinese documentation, see [README.md](README.md)*
