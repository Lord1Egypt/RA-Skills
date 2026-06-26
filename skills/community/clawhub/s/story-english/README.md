# Story English — Learn English Through Serialized Fiction

> Follow a story you actually want to read. Vocabulary embedded naturally in every episode. Mystery, city life, sci-fi. A2–B2 levels.

[![clawhub](https://img.shields.io/badge/clawhub-story--english-blue)](https://clawhub.ai/skills/story-english)
[![openclaw](https://img.shields.io/badge/openclaw-skill-orange)](https://openclaw.ai)

## The Problem

Traditional English learning is boring. Vocabulary lists feel like homework. Textbook sentences are fake. You study for a week, then quit.

Story English flips it: you read because you want to know what happens next — and vocabulary learning is just part of the ride.

## What it does

**Real fiction** — each episode reads like published literature, not a textbook  
**Natural vocabulary** — words appear in context first, then explained after  
**Serialized format** — cliffhangers and continuity, like following a TV show  
**3 series to choose from** — mystery, city life, sci-fi  
**3 difficulty levels** — A2 / B1 / B2  
**Grammar spotlight** — one pattern per episode, shown in context  
**Quiz mode** — test retention after reading  
**Vocabulary review** — flashcard review of words from recent episodes  

## The 3 Series

| | Series | Genre | Best for |
|-|--------|-------|---------|
| 🕵️ | **The Shanghai Files** | Noir mystery | B1–B2, atmospheric readers |
| 🏙️ | **City of Dreamers** | Slice of life | A2–B1, conversational English |
| 🚀 | **Starfall** | Sci-fi adventure | B1–B2, IELTS/TOEFL prep |

## Each Episode Includes

```
📖 Story (350–500 words)     — real fiction with bolded vocabulary
📚 Vocabulary (5–8 words)    — IPA, definition, story quote, new example  
💡 Grammar Spotlight (1)     — one pattern explained in context
✅ Quick Check (3 questions)  — comprehension + vocab-in-use
🎬 Next Episode Preview       — the hook that brings you back
📦 State                      — JSON to continue your story next session
```

## Installation

```bash
openclaw install story-english
```

## Usage

```bash
# Browse series
node scripts/series.js

# Start Episode 1
node scripts/episode.js --series shanghai --level B1 --chapter 1
node scripts/episode.js --series city --level A2 --chapter 1
node scripts/episode.js --series starfall --level B2 --chapter 1

# Continue story (paste state from last episode)
node scripts/episode.js --series shanghai --chapter 4 --state '{"last_scene":"..."}'

# Vocabulary review
node scripts/vocab.js --mode review
node scripts/vocab.js --mode quiz
```

## Keywords

learn English · English learning · English story · serialized fiction · story-based learning · English reading · vocabulary in context · English novel · immersive English · IELTS vocabulary · TOEFL reading · English practice · English for beginners · English intermediate · 英语学习 · 英语小说 · 英语阅读 · 沉浸式英语 · 追剧学英语 · 小说学英语 · 趣味英语 · 英语词汇 · 每日英语 · 英语故事 · 英语听说读写

---

Built for [OpenClaw](https://openclaw.ai) · Published on [clawhub.ai](https://clawhub.ai/skills/story-english)
