---
name: story-english
version: 1.0.0
author: jiajiaoy
homepage: https://clawhub.ai/skills/story-english
description: "Learn English through serialized fiction — follow a story you actually want to read, with vocabulary embedded naturally in each episode. Mystery, city life, and sci-fi series. A2–B2 levels."
keywords:
  - learn English
  - English learning
  - English story
  - story-based learning
  - serialized novel
  - English reading
  - vocabulary in context
  - English fiction
  - English for beginners
  - English intermediate
  - IELTS vocabulary
  - TOEFL reading
  - English practice
  - immersive English
  - English novel
  - 英语学习
  - 英语小说
  - 英语阅读
  - 沉浸式英语
  - 趣味英语
  - 追剧学英语
  - 小说学英语
  - 英语词汇
  - 每日英语
  - 英语故事
---

# Story English

Learn English by following a story you actually want to read. Each episode is real fiction — mystery, city life, sci-fi — with vocabulary woven naturally into the narrative. No drills. No textbook sentences. Just a story that keeps you coming back for the next episode.

## How it works

Each episode:
- **350–500 words** of genuine fiction that advances the plot
- **5–8 vocabulary words** highlighted and explained in context
- **1 grammar spotlight** — one pattern, shown naturally in the story
- **3 comprehension questions** at the end
- **Cliffhanger ending** so you actually want to read Episode 2

## Series

**🕵️ The Shanghai Files** — Noir mystery. Rookie detective. Rain-soaked streets. Cases that don't add up.
**🏙️ City of Dreamers** — Four friends navigating jobs, love, and adulthood in a new city.
**🚀 Starfall** — Year 2157. A research vessel. The wrong destination. Six crew who must figure it out.

## Levels

| Level | For | Vocabulary |
|-------|-----|-----------|
| A2 | Beginners | Simple sentences, 5 words/episode |
| B1 | Intermediate | Idioms welcome, 6 words/episode |
| B2 | Upper-intermediate | Advanced vocab, 8 words/episode |

## Commands

```bash
# Browse series and how to start
node scripts/series.js

# Start Episode 1 (default: Shanghai, B1 level)
node scripts/episode.js

# Choose series and level
node scripts/episode.js --series shanghai --level B1 --chapter 1
node scripts/episode.js --series city --level A2 --chapter 1
node scripts/episode.js --series starfall --level B2 --chapter 1

# Continue your story (paste state from previous episode)
node scripts/episode.js --series shanghai --chapter 3 --state '{"last_scene":"..."}'

# Review vocabulary (flashcard mode)
node scripts/vocab.js --mode review --words "suspicious,eerie,witness"

# Vocabulary quiz
node scripts/vocab.js --mode quiz

# English output
node scripts/episode.js --lang en
```
