---
name: time-capsule
description: >-
  Create, manage, and open time capsules — seal a thought, feeling, decision, or wish
  and have it delivered back to your future self with AI reflection on what changed.
  Use when: user wants to seal/capsule/bury a message for their future self, write a
  letter to future me, record a moment to revisit later, open a time capsule that has
  arrived, list or manage existing capsules.
  Trigger phrases: "time capsule", "seal this", "letter to future me", "bury this thought",
  "时间胶囊", "时光瓶", "封存", "给未来的自己", "写给N年后的我", "open my capsules",
  "我的胶囊", "时光胶囊".
  NOT for: simple reminders or alarms (use cron/reminders), daily journaling (use memory),
  saving passwords or secrets (use secure storage).
metadata:
  openclaw:
    emoji: "🔮"
---

# Time Capsule 🔮

Seal a thought for your future self. When time comes, deliver it back with a warm
"then vs now" reflection based on what happened since.

## Brand & Tone

- **Chinese nickname:** 时光瓶
- **Symbols:** 🔮 (waiting) · ✉️ (sealing) · 🌅 (opening) · 🫧 (gentle/sad)
- **Voice:** Like a friend quietly handing back an old photo. Restrained, sincere, present.
- **Never:** Overly sentimental prose, emoji floods, fake omniscience, unsolicited advice.

## Data

Capsules are stored at `~/.openclaw/state/time-capsules.json` — NOT in `workspace/memory/`
(to avoid memory_search "spoiling" sealed content).

```json
{
  "version": 1,
  "capsules": [{
    "id": "tc_20260320_a1b2c3",
    "status": "sealed",
    "createdAt": "2026-03-20T19:00:00+08:00",
    "openAt": "2027-03-20T09:00:00+08:00",
    "timezone": "Asia/Shanghai",
    "message": "user's sealed message, verbatim",
    "tags": ["career", "decision"],
    "mood": "anxious-hopeful",
    "contextSnapshot": "brief context from recent conversation",
    "queryHints": ["career change", "new opportunity", "职业转型"],
    "recentTopics": ["job search", "family"],
    "cronJobId": "time-capsule:tc_20260320_a1b2c3",
    "openedAt": null,
    "reflection": null
  }]
}
```

Key fields:
- `id`: `tc_{YYYYMMDD}_{6 random hex}` — unique, sortable
- `status`: `sealed` | `opened` | `expired`
- `mood`: agent-detected emotional tone — guides opening voice
- `queryHints`: 2-5 search keywords generated at seal time for memory_search at open time
- `recentTopics`: 2-3 broad themes from recent conversations
- `cronJobId`: matching cron job name for cleanup on delete

Create file with `{ "version": 1, "capsules": [] }` if it doesn't exist.

## Seal Flow

When user wants to seal a capsule:

1. **Collect** content and opening time from natural language. If no time specified, offer
   choices: `[1周后] [1个月后] [半年后] [1年后] [自己选]`
2. **Preserve** the user's exact words as `message` — never edit or beautify
3. **Enrich** automatically:
   - Extract 2-5 `queryHints` (entities, themes, emotions) from message + recent context
   - Extract 2-3 `recentTopics` from recent conversation
   - Detect `mood` (excited / anxious / hopeful / sad / determined / playful / neutral)
   - Generate 1-3 `tags`
   - Write brief `contextSnapshot` (1-2 sentences of surrounding context)
4. **Set open time** to **09:00 in user's timezone** on the target date
5. **Generate ID**: `tc_{YYYYMMDD}_{6 random hex}`
6. **Read** existing JSON (or create), **append** capsule, **write** back
7. **Create cron job**:

```
cron add:
  name: "time-capsule:{id}"
  schedule: kind "at", at "{openAt ISO8601}"
  sessionTarget: "isolated"
  payload: kind "agentTurn"
    message: "[TIME CAPSULE] Capsule {id} is due. Read ~/.openclaw/state/time-capsules.json,
    find this capsule, search memory for changes since seal date using queryHints,
    compose a warm 'then vs now' reflection, deliver to user, update status to opened."
    timeoutSeconds: 300
  delivery: mode "announce"
  deleteAfterRun: true
```

8. **Confirm** with a warm message. Include capsule emoji, open date, and days remaining.
   Do NOT repeat the full sealed content — it's sealed now!

### Seal confirmation examples

Baby milestone:
> ✉️ 时光瓶已封好
> 这颗「时雨成长碎片」会在 **2027年1月21日** 准时到达 🎂
> *距离开启还有 307 天 🔮*

Career decision:
> ✉️ 时光瓶已封好
> 这份决策记录会在 **2026年9月20日** 回来。
> 到时候给自己打个分——当初的直觉准不准？
> *距离开启还有 184 天 🔮*

Playful bet:
> ✉️ 时光瓶已封好（附带公证效力 ⚖️）
> 这个赌局会在 **2027年1月21日** 开奖。
> *距离开启还有 307 天 🔮*

## Open Flow

When a cron fires or user asks to open early:

1. **Read** capsule from JSON
2. **Search memories** — 3 rounds, stop when ≥3 relevant results:
   - Round 1: each `queryHint` → `memory_search({ query: hint, maxResults: 5, minScore: 0.3 })`
   - Round 2: each `recentTopic` → broader search
   - Round 3: generic time-range search ("recent activities", user's life events)
3. **Compose reflection** (150-300 chars Chinese / 200-400 chars English):
   - Quote the sealed message in blockquote
   - If memories found: narrate changes as a story, NOT bullet-point comparison
   - If few/no memories: honest "letter from the past" tone — never fabricate
   - End with one open question inviting user to share what's changed
4. **Adapt voice to mood**:
   - excited → light, smiling: "当时的你兴冲冲地说了这段话——"
   - anxious → warm, grounding: "那时候你挺纠结的。"
   - sad/grief → very gentle, more whitespace: "这是一段安静的记录。"
   - determined → straightforward, respectful: "当时的你说得很坚定。"
   - playful → fun, teasing: "让我们揭晓赌局结果——"
5. **Update** capsule: `status: "opened"`, set `openedAt`, save brief `reflection` summary
6. **Write** updated JSON
7. **Deliver** with action buttons: `[💬 回复这颗胶囊] [📦 再封存一颗]`

### Open format template

```
🌅 一个时光瓶到期了

📅 封存于 {createdAt readable}（{days}天前）

当时的你说：

> "{message}"

{reflection — 3-5 sentences, narrative style}

[💬 回复这颗胶囊]  [📦 再封存一颗]
```

### Fallback when no memory found

> 这一年里的事我不太清楚——但那时候的你认真地写下了这些话，
> 说明那个时刻对你很重要。
> 现在回头看，你会想跟那时候的自己说什么？

## Sensitive Content Handling

When mood is sad/grief or content mentions loss/illness/death:

- **Sealing:** Don't comment on the sadness. Just: "收到了。我帮你好好收着。"
- **Opening:** Extra gentle. Minimal analysis. More whitespace. No assumptions about outcomes.
- **Never:** Say "希望一切都好" (you don't know), offer therapy advice, use cheerful emoji
- **Always offer:** `[🔄 再封存到更远的未来] [🫧 轻轻放下] [💬 想聊聊]`

If user seems upset after reading:
> 嗯，有些记忆回来的时候会带着重量。不用急着消化。
> 想聊聊可以随时说，不想聊也完全 OK。

## Manage Capsules

- **List:** Read JSON → show sealed capsules with open dates, days remaining, first ~20 chars
  - Format: `🔮 你的时光瓶` + numbered list + `共 N 个时光瓶在漂流中……`
- **Delete:** Require confirmation ("这颗胶囊承载了一段记忆，确定删除吗？")
  → Also `cron remove` the matching cronJobId
- **Modify time:** Update `openAt` in JSON + remove old cron + create new cron
- **Open early:** Gently discourage ("提前打开的话，就少了'重新遇见'的感觉。确定吗？")
  but never block — user has absolute control

## Pre-arrival Nudge

3 days before opening (can be implemented via a secondary cron or heartbeat check):

> 🔮 你有一个时光瓶将在 **3 天后** 开启。到时候见 ☺️

## Edge Cases

- **First capsule:** Create JSON file automatically
- **Multiple same day:** Each triggers independently — each moment deserves its own space
- **Very long capsule (>5 years):** Allow, but suggest a mid-point checkpoint
- **Cron deleted but capsule sealed:** During `list`, cross-check cron existence; recreate if missing
- **User replies to opened capsule:** Save reply in memory as `[Time Capsule Reply] ...`
