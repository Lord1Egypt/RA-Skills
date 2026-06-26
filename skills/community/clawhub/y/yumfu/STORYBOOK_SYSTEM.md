# YumFu Storybook System - Complete Documentation

## 📚 Overview

The YumFu storybook system automatically records every game turn and generates beautiful PDF storybooks with complete conversation flow and images.

## 🎯 Key Features

- ✅ **Auto-logging by default** - Every turn automatically saved unless player disables storybook tracking
- ✅ **Complete conversation** - Full player input + AI response
- ✅ **Storybook-ready prose layer** - Short/raw player actions can be normalized into cleaner literary retelling for the book version
- ✅ **Image integration** - All generated art at correct positions
- ✅ **Share-safe HTML** - Storybook HTML should be a single portable file when sent to chat platforms
- ✅ **Beautiful PDF** - Professional layout via HTML → PDF
- ✅ **Session management** - Auto-creates new sessions after 2h inactivity

## 🔄 System Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                     GAME FLOW                                │
└─────────────────────────────────────────────────────────────┘

1. Player Input          "/yumfu look"
   ↓
2. AI Processes         Generate narrative + image (if needed)
   ↓
3. Logger Records       log_turn(player_input, ai_response, image)
   ↓                    → session-{id}.jsonl
4. Send Response        Reply to player

┌─────────────────────────────────────────────────────────────┐
│                  STORYBOOK GENERATION                        │
└─────────────────────────────────────────────────────────────┘

1. Read session log     session-{id}.jsonl
   ↓
2. Collect images       Copy from ~/.openclaw/media/outbound/yumfu/
   ↓
3. Generate HTML        Complete conversation flow
   ↓
4. Convert to PDF       Browser print → PDF
   ↓
5. Send to user         Telegram/Discord/etc.
```

## 📝 Core Components

### 1. SessionLogger (`scripts/session_logger.py`)

**Purpose:** Record every game turn

**Usage:**
```python
from scripts.session_logger import log_turn

log_turn(
    user_id="1309815719",
    universe="warrior-cats",
    player_input="/yumfu look",
    ai_response="You see the ThunderClan camp...",
    image="tumpaw-camp-20260403.png"  # Optional
)
```

**Storage:**
```
~/clawd/memory/yumfu/sessions/{universe}/user-{id}/session-{timestamp}.jsonl
```

**JSONL Format:**
```json
{"timestamp": "2026-04-03T00:15:23", "type": "turn", "player": "/yumfu look", "ai": "You see...", "image": "tumpaw-camp.png"}
```

### 2. Storybook Generator V3 (`scripts/generate_storybook_v3.py`)

**Purpose:** Convert session logs → HTML → PDF

**Sharing rule (important):**
- If the HTML will be sent through Telegram/Discord/other chat platforms, it must not depend on local relative image paths like `images/foo.png`.
- Prefer a single-file HTML with images embedded as data URLs.
- PDF export must be generated from a verified storybook page/tab, not from whatever browser tab happens to be active.

**Usage:**
```bash
# Auto-detect latest session
uv run scripts/generate_storybook_v3.py \
  --user-id 1309815719 \
  --universe warrior-cats

# Specify session ID
uv run scripts/generate_storybook_v3.py \
  --user-id 1309815719 \
  --universe warrior-cats \
  --session-id 20260403-001349
```

**Output:**
```
~/clawd/memory/yumfu/storybooks/{universe}/user-{id}-{timestamp}/
├── storybook.html        # preferred shareable artifact; may contain embedded image data
└── images/
    ├── tumpaw-ceremony.png
    └── tumpaw-camp.png
```

**Platform note:**
- Local browser preview can use adjacent files.
- Chat delivery should assume recipients cannot access the sender's local filesystem.
- Therefore, `storybook.html` should be treated as the primary portable artifact.

### 3. Image Generator (`scripts/generate_image.py`)

Already integrated with inline dependencies.

**Usage:**
```bash
uv run scripts/generate_image.py \
  --prompt "Tumpaw swimming in river" \
  --filename "tumpaw-swimming-20260403" \
  --style "warrior-cats"
```

## 🚀 Quick Start

### For Players

**Generate your storybook:**
```bash
/yumfu storybook
```

The AI will automatically:
1. Generate HTML from your session logs
2. Prefer HTML as the canonical shareable artifact
3. Send the HTML back to you via Telegram/Discord
4. Only produce PDF as an optional secondary export if the layout is visually confirmed good

### For Developers

**1. Test the system:**
```bash
cd ~/clawd/skills/yumfu
uv run scripts/test_storybook_integration.py
```

**2. Manual generation:**
```bash
# Generate HTML
uv run scripts/generate_storybook_v3.py \
  --user-id YOUR_ID \
  --universe warrior-cats

# Open in browser (auto-opens if webbrowser available)
# Print to PDF from browser
```

## 🛠️ Integration Guide

### In SKILL.md

The game AI **must** call `log_turn()` after every player action:

```python
# 1. Receive player input
player_input = "/yumfu look"

# 2. Generate response
ai_response = "You see the ThunderClan camp bustling with activity..."

# 3. Generate image (if triggered)
image_filename = None
if should_generate_image("location"):
    image_filename = generate_image("tumpaw-camp")

# 4. ⚠️ MANDATORY: Log the turn
from scripts.session_logger import log_turn
log_turn(
    user_id=user_id,
    universe=universe,
    player_input=player_input,
    ai_response=ai_response,
    image=image_filename
)

# 5. Send response to user
reply(ai_response)
if image_filename:
    send_image(image_filename)
```

### When to Generate Storybook

**Auto-trigger conditions:**
- Player types `/yumfu storybook`
- Character reaches major milestone (becomes warrior, leader)
- Character dies (permanent death)
- Session ends naturally
- Player inactive for 24+ hours (archive mode)
- Player explicitly retires / archives / ends the run

**Ending branch default:**
- if storybook tracking is enabled, ending / retire / archive branches should auto-generate the final HTML storybook
- preferred helper: `deliver_yumfu_turn.py --ending-storybook`
- HTML is primary; PDF is optional

## 📊 File Structure

```
~/clawd/memory/yumfu/
├── sessions/
│   └── {universe}/
│       └── user-{id}/
│           ├── session-20260403-001349.jsonl       # Raw logs
│           └── session-20260403-001349-summary.json # Metadata
├── storybooks/
│   └── {universe}/
│       └── user-{id}-{timestamp}/
│           ├── storybook.html
│           └── images/
└── saves/
    └── {universe}/
        └── user-{id}.json                           # Character data
```

## 🧪 Testing

**Run integration test:**
```bash
cd ~/clawd/skills/yumfu
uv run scripts/test_storybook_integration.py
```

**Expected output:**
```
✅ Created mock session
✅ HTML generated
✅ All content checks passed
```

## 🔍 Debugging

**Check session logs exist:**
```bash
ls ~/clawd/memory/yumfu/sessions/warrior-cats/user-1309815719/
```

**Verify log content:**
```bash
cat ~/clawd/memory/yumfu/sessions/warrior-cats/user-1309815719/session-*.jsonl | jq
```

**Test generator directly:**
```bash
cd ~/clawd/skills/yumfu
uv run scripts/generate_storybook_v3.py --user-id 1309815719 --universe warrior-cats
```

## 📦 Dependencies

**All dependencies are inline in scripts:**
- `session_logger.py` - Pure Python stdlib
- `generate_storybook_v3.py` - Pure Python stdlib
- `generate_image.py` - Uses inline `uv` dependencies:
  - `google-genai>=1.0.0`
  - `pillow>=10.0.0`

**No pip install needed** - `uv run` handles everything.

## 🎨 Storybook Output Example

**HTML Layout:**
```html
[Title Page]
Tumpaw's Adventure
Warrior Cats | Apprentice | Session: 20260403-001349

[Complete Conversation]
▶️ /yumfu start
Welcome to ThunderClan! You are born as a tiny kit...

▶️ /yumfu look
You see the ThunderClan camp bustling with activity...
[Image: ThunderClan Camp]

▶️ /yumfu train swimming
Willowpelt leads you to the river border...

🏆 Achievement Unlocked: First Catch!

[Final Stats]
Hunting: 13 | Fighting: 6 | Swimming: 15

[Relationships]
Willowpelt (❤️ 35): Mentor, proud
Firestar (❤️ 30): Sees potential
```

## 🚨 Common Issues

### "No session logs found"

**Cause:** Game didn't call `log_turn()`

**Fix:** Ensure SKILL.md integration is active (see Integration Guide)

### "Images not found"

**Cause:** Image files moved/deleted from `~/.openclaw/media/outbound/yumfu/`

**Fix:** Images must stay in outbound directory until storybook generated

### "HTML empty/broken"

**Cause:** Malformed JSONL in session log

**Fix:** Check session file with `jq`:
```bash
cat session-*.jsonl | jq
```

## 📚 Version History

- **V1** (deprecated): Basic save notes → Markdown
- **V2** (deprecated): Save notes → HTML (no dialogue flow)
- **V3** (current): Session logs → HTML with complete conversation

## 🎯 Future Enhancements

- [ ] Auto-PDF generation (no browser step)
- [ ] Multi-session storybooks (entire campaign)
- [ ] Collaborative storybooks (party adventures)
- [ ] Custom CSS themes per world
- [ ] Export to EPUB format

## 📞 Support

**Issues?** Check:
1. Session logs exist: `ls ~/clawd/memory/yumfu/sessions/.../`
2. Run test: `uv run scripts/test_storybook_integration.py`
3. Check SKILL.md for `log_turn()` calls

---

**Maintained by:** YumFu Team  
**Last Updated:** 2026-04-03  
**Version:** 3.0.0
