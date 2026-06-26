# Slice Themes

The Slice product (`voxflow.studio/apps/slice`) ships 13 visual themes. Same deck JSON, thirteen different looks. Pick by platform fit and content mood — not by content topic.

## Quick Picker

| Theme id | Label | Platform fit | Pick when… |
|---|---|---|---|
| `paper-slide` | 纸面 | 抖音 · 视频号 · 小红书 | Knowledge / management / investing / psychology / philosophy. Content needs "stop and think for a beat". |
| `editorial-mag` | 编辑刊 | 知乎 · 公众号 · LinkedIn | Long commentary, policy analysis, profile features, deep industry reports. Wants Atlantic / NYT-magazine credibility. |
| `bold-poster` | 大字海报 | X · Threads · LinkedIn | One-line takes, investing calls, product judgments, controversial claims, data flashes. The scroll has to stop. |
| `notion-card` | Notion 卡 | 公众号 · 飞书 · 知识星球 | Methodology notes, SOPs, knowledge-base teardowns, product retros, tutorial roundups. Looks like serious notes. |
| `brutalist` | 粗野 | X · Mastodon · 独立播客 | Hard takes, tech critiques, podcast episode posters, culture commentary, contrarian positions. Refuses polish. |
| `glass-dark` | 玻璃夜 | 抖音 · 视频号 · TikTok | AI / tech, future narratives, night-mood content, cinematic interviews, gaming / digital. OLED-first. |
| `editorial-stencil` | 编辑·海报 | LinkedIn · 知乎 · 公众号 | Agency-pitch posters, brand keynote notes, opinion essays that want letterbox cinema feel + dual-tone heavy display. |
| `broadsheet` | 财经刊 | LinkedIn · 知乎 · 雪球 | Market commentary, macro analysis, earnings teardowns, fund-manager letters. FT salmon paper + drop-cap = automatic finance credibility. |
| `blueprint` | 蓝晒图 | 少数派 · 知乎 · GitHub | Engineering / architecture explainers, system design teardowns, dev tooling reviews. Cyan grid + orange dimension marks = "this is a spec, not a vibe". |
| `daisy-pastel` | 雏菊 | 小红书 · 微博 · 即刻 | Lifestyle, self-care, journaling, soft-skill posts, anything that wants to feel hand-drawn and approachable. Cream + pink + tiny stars. |
| `showa-catalog` | 昭和目录 | 小红书 · B 站 · 播客 | 70s city-pop nostalgia, music recs, retro book reviews, podcast covers, weekend essays. Rainbow stripes + sun stamp. |
| `photo-feature` | 摄影刊 | 小红书 · 知乎 · 微博 | Travel diaries, place-based reportage, photography commentary, scene-setting pieces. **Needs `imageUrl` per card** — falls back to SVG stub when missing (plumbing pending). |
| `atmospheric` | 深夜刊 | 微博 · 即刻 · 播客 | Late-night essays, romantic prose, mood pieces, podcast teasers. Black ground + a single warm spotlight + pink serif italic. |

## Theme Details

### `paper-slide` — 纸面

**Visual signature**: Aged paper texture · serif red headlines · hand-drawn vermilion stamps. Reads halfway between "reading-notebook" and "old-newspaper column" — knowledge feel, trust feel.

**Why it works on 抖音 / 视频号 / 小红书**: Algos no longer reward static text cards, but narrated paper-card video with paged TTS rhythm still ships. Measured completion rate ~30% above pure-subtitle version.

**Good for**: 管理学拆解 · 投资札记 · 心理科普 · 人物访谈节选 · 读书笔记 · 原创随笔

**Skip for**: Pure entertainment / fast hooks — pick `bold-poster` or `brutalist` instead.

### `editorial-mag` — 编辑刊

**Visual signature**: Cream page · serif italic pulls · magazine-grade whitespace · thin column rules · restrained horizontal dividers. Lifted from The Atlantic / The New Yorker / NYT Magazine.

**Why it works on 知乎 / 公众号 / LinkedIn Pulse**: Both algos and readers favour "serious, restrained, professional" layout. Magazine vibe is automatic credibility.

**Good for**: 商业评论 · 政策解读 · 人物特稿 · 行业深度报告 · 长篇书评 · 专栏文章

**Skip for**: Fast hooks / clickbait — `bold-poster` or `glass-dark` will pop more.

### `bold-poster` — 大字海报

**Visual signature**: Left-edge accent block · heavy bold display · oversized numerals as anchors. Page weight is pinned to 1–2 sentence takes — read in one beat, retweet in the next.

**Why it works on X / Threads / LinkedIn**: Slide-feeds don't pause longer than a second. Fewer chars carrying heavier judgement = "stop-and-screenshot" energy. Poster is the natural shape.

**Good for**: 投资观点 · 产品判断 · 一句话洞察 · 数据快报 · 争议论断 · 行业预测

**Skip for**: Long step-by-step reasoning — pick `editorial-mag` or `paper-slide`.

### `notion-card` — Notion 卡

**Visual signature**: Pure white background · warm-grey ink · blue accent rule · top-left page-icon. Lifted directly from Notion document layout: 64px grid, Notion warm-grey body, Notion blue.

**Why it works on 公众号 / 飞书 / 知识星球**: Audiences in "professional knowledge community" surfaces already read Notion-style as "this is real, structured notes". Conversion lift comes free.

**Good for**: 方法论笔记 · SOP 文档 · 知识体系拆解 · 产品复盘 · 教程总结 · Toolkit 推荐

**Skip for**: Emotional / viral-pace content — pick `paper-slide` or `glass-dark`.

### `brutalist` — 粗野主义

**Visual signature**: Pure black/white · 6px hard borders · NO.NN black labels · raw display type. Sourced from 90s zine covers + indie-podcast posters. Refuses to flatter.

**Why it works on X / Mastodon / 独立播客**: Audiences are saturated on polished mini-cards. "Refuses to look produced" pops harder in the feed — recognition factor an order of magnitude over cute aesthetic.

**Good for**: 硬核观点 · 技术批判 · 播客海报 · 文化评论 · 独立宣言 · 争议立场

**Skip for**: Warm / commercial pitches — pick `glass-dark` or `editorial-mag`.

### `glass-dark` — 玻璃夜

**Visual signature**: Deep purple-to-blue gradient · twin radial purple glows · half-transparent glassmorphism icon blocks · purple text-shadow glow. Looks like it was generated inside your phone's dark mode.

**Why it works on 抖音 / TikTok / 视频号**: Visual weight of dark content on OLED screens is markedly higher than light content; glass-dark naturally outweighs in the feed — especially during nighttime peak.

**Good for**: AI / 科技 · 未来叙事 · 夜间情绪 · 电影感人物 · 游戏 / 数字 · 深夜散文

**Skip for**: Policy / education tone — pick `editorial-mag` or `notion-card`.

### `editorial-stencil` — 编辑·海报

**Visual signature**: Cream base bracketed by black letterbox bars · dual-tone heavy display (one word in accent, the rest in ink) · Roman-numeral dateline · agency-pitch poster geometry.

**Why it works on LinkedIn / 知乎 / 公众号**: Reads as "agency keynote / brand manifesto" rather than "social card" — pops in professional feeds without resorting to clickbait weight.

**Good for**: 品牌发布 · 主题演讲笔记 · 观点海报 · 战略复盘 · 行业宣言

**Skip for**: Casual journaling — pick `daisy-pastel` or `paper-slide`.

### `broadsheet` — 财经刊

**Visual signature**: FT salmon paper · heavy serif headlines · drop-cap first letter · red DATELINE tag · column rule. Lifted from Financial Times / Economist front pages.

**Why it works on LinkedIn / 知乎 / 雪球**: Finance audiences already read salmon paper as "real markets writing". Drop-cap + dateline buy ~5 seconds of attention before the reader decides if the take is worth reading.

**Good for**: 市场评论 · 宏观分析 · 财报拆解 · 基金经理信 · 行业观察

**Skip for**: Fast viral hooks — pick `bold-poster` or `brutalist`.

### `blueprint` — 蓝晒图

**Visual signature**: Cyan engineering-blue ground · white grid overlay · orange dimension labels · annotation-style callouts. Looks like a printed blueprint.

**Why it works on 少数派 / 知乎 / GitHub**: Dev / engineering audiences read blueprint as "this is a spec, not a vibe". Lets technical content arrive without the usual SaaS-aesthetic overhead.

**Good for**: 系统设计 · 架构图说明 · 工具拆解 · 开发流程 · 工程笔记

**Skip for**: Emotional or narrative content — pick `atmospheric` or `editorial-mag`.

### `daisy-pastel` — 雏菊

**Visual signature**: Cream ground · hand-drawn daisies + tiny stars · soft pink accent · rounded display type. Reads as journal / sticker book.

**Why it works on 小红书 / 微博 / 即刻**: Lifestyle / self-care feeds reward hand-made warmth. Stickers + cream + pink registers as "real human wrote this" before the first character is read.

**Good for**: 生活方式 · 自我成长 · 手帐分享 · 软话题 · 暖心小记

**Skip for**: Finance / engineering — pick `broadsheet` or `blueprint`.

### `showa-catalog` — 昭和目录

**Visual signature**: 70s city-pop palette · colored circle stacks · rainbow diagonal stripes · sun stamp · retro catalog typography. Closer to a Showa-era record-shop flyer than a slide.

**Why it works on 小红书 / B 站 / 播客**: Nostalgia spike is its own algorithm-friendly hook. Music / book / podcast recs land warmer here than on any "professional" theme.

**Good for**: 音乐推荐 · 书单 · 怀旧随笔 · 播客封面 · 周末长文

**Skip for**: Hard news / policy — pick `editorial-mag` or `broadsheet`.

### `photo-feature` — 摄影刊

**Visual signature**: Full-bleed photograph backdrop · gradient overlay anchoring the bottom · heavy serif title · travel-magazine pacing.

**Why it works on 小红书 / 知乎 / 微博**: Photo-led posts already win in lifestyle / travel verticals. Slice's job is to add a narrated card rhythm without losing the photograph's weight.

**Good for**: 旅行游记 · 在地报道 · 摄影评论 · 场景描写 · 城市观察

**Limitation (current)**: The renderer reads `card.imageUrl` for the backdrop image; until the plumbing for per-card photo upload ships, missing `imageUrl` falls back to a generic SVG stub. Use `paper-slide` or `editorial-mag` if you cannot supply photographs.

**Skip for**: Pure text takes — the theme leans on the image; weak photos make the layout feel empty.

### `atmospheric` — 深夜刊

**Visual signature**: Black ground · one warm-light cone from the top · pink serif italic title · late-night essay restraint. Looks like a single page lit by a desk lamp.

**Why it works on 微博 / 即刻 / 播客**: Late-night reading windows reward mood over information density. Atmospheric concedes the "loud feed" lane and rewards the lurkers scrolling at 1 a.m.

**Good for**: 深夜随笔 · 情感长文 · 朗读节选 · 文学摘录 · 播客预告

**Skip for**: Daytime / data-heavy content — pick `bold-poster` or `notion-card`.

## How To Pass Theme To The Renderer

The deck JSON is theme-agnostic. The theme is a separate field at the top level of the render request:

```json
{
  "theme": "editorial-mag",
  "header": "...",
  "seriesTitle": "...",
  "cards": [ /* same shape regardless of theme */ ]
}
```

Valid `theme` ids: `paper-slide` · `editorial-mag` · `bold-poster` · `notion-card` · `brutalist` · `glass-dark` · `editorial-stencil` · `broadsheet` · `blueprint` · `daisy-pastel` · `showa-catalog` · `photo-feature` · `atmospheric`. Default: `paper-slide`.

The 13-theme dispatcher only runs on the Slice cloud renderer (the web app). CLI `voxflow present` / `picstory` use a different scheme set — see SKILL.md → "CLI Approximation Route" for the closest CLI scheme per theme.
