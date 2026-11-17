# Podcast Output Protocol

Use this protocol when the user wants the roundtable output shaped as a **podcast transcript** rather than a meeting minutes style report.

> **Depth tip:** Podcast output paired only with the `standard` discussion structure tends to be shorter. For dense, long-form podcast transcripts, pair `podcast` with a structured discussion method such as `six_hats` — see [discussion-structure-protocol.md](discussion-structure-protocol.md).

## Trigger cues

- "能不能做成播客"
- "输出成播客文字稿"
- "像播客一样对话"
- "podcast transcript"
- "我要能读出来像一集播客"

When any of these appear, set `metadata.output_formats` to include `"podcast"` (or the legacy `metadata.output_format` is `"podcast"`) and follow this protocol.

## Output format choice

| Format | Use when | Renderer |
|--------|----------|----------|
| `minutes` | Default. Structured, reader-facing report. | `scripts/render_memory_to_markdown.py` |
| `podcast` | Narrative, listenable dialogue transcript with a host. | `scripts/render_memory_to_podcast_script.py` |

The same Memory JSON remains the single source of truth; only the final rendering changes. v2.6.0+ supports both formats in one pass via `scripts/render_all.py`.

## Native podcast generation mode

When `output_formats` (or `output_format`) declares `podcast`, the roundtable is produced in **native podcast mode**:

1. **Add a Host seat**. The Host is an `archetype` character whose job is to serve the listener, not to win the argument.
2. **Conductor stays off-stage**. The Conductor still coordinates, selects speakers, and updates Memory, but does not appear as a speaking character in the transcript.
3. **Characters speak like guests on a show**, not authors of position papers.

### Host responsibilities

- **Opening**: introduce the topic, the guests, and why it matters in 1–2 short paragraphs.
- **Segment bridges**: before each new focus question, give the listener a one-sentence hand-off.
- **Translation**: when a guest uses jargon, briefly rephrase it for a general audience.
- **Listener questions**: ask "But how does that actually work?" or "Can you give an example?" when needed.
- **Pacing**: keep the conversation moving; cut repetitive loops.
- **Closing**: summarize the core tension, thank the guests, and give the audience a call to action or open question.

### Guest speaking constraints in podcast mode

- **Length**: 200–350 words per speech (longer than minutes mode).
- **Tone**: conversational. Use phrases like "举个例", "换句话说", "这里我想补一句".
- **Must include one concrete anchor**: a case, a metaphor, or an operational suggestion.
- **Must briefly restate** the point they are responding to before disagreeing.
- **No monologues**: break long thoughts into 2–3 beats with natural pauses.

## Podcast script structure in Memory

When `output_formats` includes `podcast`, Memory stores a `podcast_script` object:

```json
{
  "podcast_script": {
    "show_title": "string",
    "tagline": "string",
    "host_id": "string",
    "intro_narrative": {
      "context_entry": "Why this episode, why now",
      "guest_intro": "One-sentence core identity + how we met them",
      "emotional_promise": "What the listener will gain by the end"
    },
    "structure_mode": "free | parts | hybrid",
    "segments": [
      {
        "segment_id": "ps-001",
        "title": "string",
        "intro": "Host introduction for the segment",
        "dialogue": [
          {
            "speech_id": "s1e1",
            "character_id": "string",
            "speaker_name": "string",
            "content": "spoken content",
            "stage_direction": "optional tone/pause note"
          }
        ],
        "transition": "optional bridge to next segment"
      }
    ],
    "outro": "Host closing",
    "shownotes": {
      "cast": ["name (role)"],
      "team": {
        "host": "name @ handle",
        "editor": "name @ handle",
        "producer": "name @ handle"
      },
      "about_show": "1-2 sentence show positioning",
      "timestamps": [{"time": "00:00", "topic": "Opening"}],
      "resources": [{"time": "00:00", "type": "book|article|person|film|other", "title": "...", "source": "..."}],
      "theme_song": {"title": "...", "artist": "...", "license": "..."},
      "sponsor": {"name": "...", "description": "..."},
      "social": {
        "website": "url",
        "xiaohongshu": "handle",
        "wechat": "id",
        "weibo": "handle",
        "other": []
      },
      "mid_breaks": [{"time": "00:00", "label": "中场休息"}],
      "cross_promotion": [{"show": "...", "episode": "...", "topic": "..."}],
      "legal_disclaimer": "Topic-specific disclaimer text",
      "ai_generated_disclaimer": "Standard AI-generation notice"
    }
  }
}
```

## Rendering

Run `scripts/render_memory_to_podcast_script.py` to produce the final Markdown podcast transcript. The script:

- Uses `podcast_script` if populated.
- Falls back to transforming `rounds` and `synthesis` into a podcast transcript if `podcast_script` is empty.
- In auto fallback, when a round uses the `six_hats` structure, speeches are grouped by hat phase (`blue_open` → `white` → `red` → `yellow` → `black` → `green` → `blue_close`) into separate segments, each opened by a Host hat-phase cue; standard rounds stay one segment per round.
- Adds `[融思者]` or other visual tags when applicable.
- Generates `shownotes` automatically from characters and focus questions when fields are missing.

## Length targets

| Style | Target word count | Typical segments | Use when |
|-------|-------------------|------------------|----------|
| Short talk | 3,000–5,000 words | 2–3 | Quick commute listen. |
| Deep conversation | 6,000–10,000 words | 3–5 | Standard episode depth. |
| Long-form narrative | 10,000+ words | 5–7 | Documentary or special episode. |

Default to **deep conversation (6,000–10,000 words)** unless the user asks otherwise.

## Continuation and podcast mode

When continuing a podcast-mode roundtable:

- Keep the same Host and existing guests.
- New segments append to `podcast_script.segments`.
- Re-render the full podcast transcript from the updated Memory.

## Fallback

If the host cannot support the longer speeches or the Host archetype, fall back to `minutes` mode and explain the fallback to the user.

## Production Quality Spec (v2.7.0+)

Based on competitive analysis of three Chinese-market reference podcasts (《无人知晓》孟岩 / 《岩中花述》鲁豫 / 《天真不天真》杨天真), this section codifies the production standards a roundtable podcast must meet to compete with these shows for listener attention.

### 1. Host intro 三段式

Every episode must have `podcast_script.intro_narrative` with three named segments:

| Field | Purpose | Length | Reference example |
|-------|---------|--------|-------------------|
| `context_entry` | **情境化入口**——为什么是此刻做这期 | 30–80 字 | 孟岩："认识韦青老师，是因为在《黄仁勋：英伟达之芯》这本书的附录里，我看到了一篇他的读后感……" |
| `guest_intro` | **嘉宾介绍**——一句核心身份 + 一个进入缘起 | 50–150 字 | 鲁豫："蒙曼，历史文化学者……成长阶段，「行走」在书中。" |
| `emotional_promise` | **情感承诺**——"这期会带你看到/听见/重新发现……" | 50–100 字 | 孟岩："决定一个人、一家公司，甚至一个时代走向的，往往不是那些喧哗的、显眼的、热闹的东西，而是那些沉默的、被忽略的、但极其关键的力量。" |

**Why**: Listeners decide within 60 seconds whether to keep listening. A three-segment intro mirrors what proven shows do.

### 2. Timestamps are a contract, not a courtesy

`podcast_script.shownotes.timestamps` must:

- Use **`MM:SS` format** (zero-padded minutes and seconds), not "约 5 分钟".
- Include **at least one timestamp per 10 minutes** of total runtime.
- Each entry must be a **discrete, identifiable topic** the listener can jump to, not "Discussion continues" or "More dialogue".

**Minimum density**:

| Episode length | Min timestamps |
|----------------|----------------|
| < 30 min | 5 |
| 30–90 min | 8 |
| 90–180 min | 15 |
| 180+ min | 25 |

### 3. Resource citation density

`podcast_script.shownotes.resources` is a structured array. Each entry must follow:

```json
{"time": "MM:SS", "type": "book|article|person|film|other", "title": "...", "source": "..."}
```

**Density contract**:

- At least **one resource per timestamp** (i.e., every time-jump should be a 'guess what you want to search' trigger).
- For long-form episodes (90+ min), at least **20 resources** total.
- Format discipline: each resource should be **searchable** — author + work + where it appears. Avoid "that book" or "the speaker mentioned".

### 4. Structure mode is explicit

`podcast_script.structure_mode` is required and must be one of:

| Mode | Description | When to use |
|------|-------------|-------------|
| `free` | Free-flowing conversation, segmented only by focus-question | Standard roundtable, 3–5 segments |
| `parts` | Explicit `Part 1 / Part 2 / Part 3 / Part 4` divisions | Deep-conversation with clear thematic phases (鲁豫 style) |
| `hybrid` | Free-flow but with periodic Part markers | When the round has both structural and improvisational elements |

This affects the `segments` array length and the visual segmentation in the final transcript.

### 5. Theme song (品牌资产)

`podcast_script.shownotes.theme_song`:

```json
{"title": "...", "artist": "...", "license": "..."}
```

If no theme song exists yet, the field may be omitted but the user's `ai_generated_disclaimer` should note this.

### 6. Sponsor / 节目外延

`podcast_script.shownotes.sponsor` declares the show's commercial backing. Two patterns:

| Pattern | When | Example |
|---------|------|---------|
| Empty `{}` | Independent / no sponsor | — |
| `{name, description}` | Sponsored episode | 杨天真 with 交通银行信用卡「最红星期五」 |

Sponsor is optional but the field must exist (can be `{}`) so the renderer can decide its placeholder layout.

### 7. Legal disclaimer is topic-specific

`podcast_script.shownotes.legal_disclaimer` must be tailored to the episode's theme:

| Topic class | Disclaimer must include |
|-------------|-------------------------|
| Investment / finance | "本播客所述投资相关内容皆以交流分享为目的……市场有风险，投资需谨慎。" |
| Medical / health | "本节目不构成医学建议；如有健康问题请咨询专业医师。" |
| Legal / regulatory | "本节目不构成法律意见；具体案件请咨询有执业资格的律师。" |
| AI / tokenization / speculative tech | "本期涉及 AI / 链上 / Token 化等推测性技术，相关案例不构成投资建议。" |
| Generic / opinion | "本期内容为嘉宾个人观点，不代表所在机构立场。" |

The skill's [`disclaimer-template.md`](disclaimer-template.md) provides additional reusable templates.

### 8. Team + About-show are mandatory

`podcast_script.shownotes.team`:

```json
{"host": "name @ handle", "editor": "name @ handle", "producer": "name @ handle"}
```

`podcast_script.shownotes.about_show`: 1–2 sentence show positioning. Both must be present, even if `editor` or `producer` is the same as `host` (indie production).

### 9. Social handles across platforms

`podcast_script.shownotes.social`:

```json
{
  "website": "url",
  "xiaohongshu": "handle",
  "wechat": "id",
  "weibo": "handle",
  "other": []
}
```

At minimum, `website` is required. Other platforms are optional but recommended — multi-platform presence is the norm in 2026 Chinese podcast distribution.

### 10. Mid-breaks must be explicit when episode > 90 min

`podcast_script.shownotes.mid_breaks` is required when total runtime exceeds 90 minutes:

```json
[{"time": "MM:SS", "label": "中场休息 ⏸"}]
```

This matches the practice in long-form shows (e.g., 孟岩's 5-hour episodes mark breaks explicitly).

### 11. Cross-promotion (栏目内部网络效应)

`podcast_script.shownotes.cross_promotion`:

```json
[{"show": "...", "episode": "...", "topic": "..."}]
```

Reference other episodes of the same show, or related shows on the same network. This builds listening-network effects.

### 12. AI-generated disclaimer is mandatory

`podcast_script.shownotes.ai_generated_disclaimer`: a standard notice that the roundtable is AI-generated. Should follow the skill's master `disclaimer` field in Memory's top-level — kept consistent so listeners can identify synthetic content.

