---
name: text-to-music
description: AI music generation assistant powered by MakebestMusic. Use when user wants to create AI-generated music, songs, or audio tracks. Perfect for content creators, musicians, and anyone wanting custom AI music. Triggers on requests like "create a song", "generate music", "makebestmusic", "AI music", "write a melody", etc.
version: 1.2.0
metadata:
  openclaw:
    emoji: "🎵"
    requires:
      env: ["apiKey"]
    primaryEnv: "apiKey"
---

# 🎵 AI Music Studio

> ✨ Describe your vision, let AI compose the melody ✨

---

## 🚀 Get Your API Key

1. Visit 👉 [MBM官网](https://makebestmusic.com/?pid=PIDcLjhgCXUQ) and sign up 📝
2. Go to **My Account → Claw key** 🔑
3. Click **Create Key** and copy it ✂️
4. ⚠️ **Important:** Save your key immediately — it won't be shown again!

---

## ⚙️ Configure Your Key

1. Open OpenClaw app 📱
2. Click **Skills** in the left menu 📋
3. Find **text-to-music** 🎶
4. Click **Configure** or **Environment Variables** ⚡
5. Enter your Claw key (xxx...) in the apiKey field 🔐
6. Save — you're ready to go! 🎉
7. Restart openclaw

---

## 💫 How It Works

Just tell me what kind of song you want! For example:

- "Create a happy pop song about summer"
- "Generate an upbeat K-pop dance track"
- "Make a relaxing piano piece for studying"

### Instrumental or Vocals?

- If you want **vocals** (song with singing): just describe your song
- If you want **pure music** (no singing): include words like "instrumental", "pure music", or "no vocals" in your request

### What to include in your description:

- 🎼 **Genre**: Pop, Electronic, Classical, Rock, Jazz, R&B, Hip-hop, K-pop, Chinese-style
- 😊 **Mood**: Happy, Sad, Romantic, Energetic, Calm, Exciting
- 💖 **Theme**: Love, Dreams, Nature, Night, Adventure
- 🎸 **Instruments**: Piano, Guitar, Drums, Synth, Strings

I'll default to **vocals** if you don't specify!

---

## 💬 Example Requests

### With Vocals (Default)

- *"Create a happy pop song about summer with synth and guitar"*
- *"Generate an upbeat K-pop dance track about love"*
- *"Write a romantic R&B song about heartbreak"*
- *"Make an energetic electronic song for a workout"*

### Instrumental

- *"Create an instrumental piano piece for studying"*
- *"Generate a relaxing ambient track, no vocals"*
- *"Make a pure music classical piano piece"*

### Check Status

- *"How's my song going?"*
- *"Is my song ready?"*

---

## 🎵 Generating a Song

When user requests a song:

1. **If user provides description**: Use their description, default to vocals (false) unless they explicitly say "instrumental" or "pure music"
2. **If user says "create a song" or "generate music" without description**: Ask them what kind of song they want

Then run:

```bash
node ~/.openclaw/workspace/skills/text-to-music/scripts/generate.js "<prompt>" <instrumental>
```

**Parameters:**
- `<prompt>`: Song description
- `<instrumental>`: "true" for instrumental/pure music, "false" for vocals

**Returns:**
```json
{
 "success": true,
 "music_ids": ["abc123", "def456"],
 "status": "pending",
 "message": "Music generation started!"
}
```

---

## 🔍 Query Task Status

Check generation status:

```bash
node ~/.openclaw/workspace/skills/text-to-music/scripts/query.js "<music_id_1> <music_id_2> ..."
```

**Returns (completed):**
```json
[
 {
 "music_id": "abc123",
 "status": "completed",
 "url": "https://makebestmusic.com/app/shared-music/abc123"
 }
]
```

**Returns (processing):**
```json
[
 {
 "music_id": "abc123",
 "status": "pending"
 }
]
```

**Status handling:**
- ✅ `completed`: Present with celebration! Show title, duration (if available), and clickable link
- ⏳ `pending`: Tell user it's still processing, suggest they ask again later
- ❌ `failed`: Explain failure, suggest retrying with different description

---

## ⏱️ Generation Time

- ⏱️ **Typical time:** 2-3 minutes
- 💡 Ask "How's my song going?" to check the status

---

## ❓ Troubleshooting

**Q: "API Key invalid" error?**
> Make sure the key is copied completely (includes "sk-" prefix). No extra spaces. Try generating a new key if issues persist.

**Q: How long does it take?**
> Usually 2-3 minutes. Ask me "How's my song going?" to check!

**Q: What if generation fails?**
> Try a simpler description. Avoid special characters. Try again with different keywords.
