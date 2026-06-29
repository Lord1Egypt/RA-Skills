---
name: essay-writing
description: "Chinese argumentative essay and op-ed writing skill. Produces polished content for Zhihu (知乎), WeChat Official Accounts (公众号), Xiaohongshu (小红书), and Douyin (抖音). This skill should be used when users ask to write argumentative essays, social commentary, opinion pieces, Zhihu answers, public account articles, RED notes, or short-video scripts. Not suitable for pure narrative (fiction/novels), formal academic papers, official documents, press releases, or slide copy."
agent_created: true
---

# Essay-Writing — Chinese Argumentative Essay Skill

## Purpose

Produce long-form Chinese argumentative content that meets the editorial standards of
Zhihu and WeChat Official Accounts. Every piece must deliver at least one of three
forms of value: deeper understanding, cognitive upgrade, or actionable insight.

## Why This Skill Has a User Profile Step

AI writing tools share one fatal weakness: **everyone using the same prompt gets
the same voice.** Same structure, same analogies, same "balanced" tone. The
result is homogenized content (同质化) — readable, competent, but indistinguishable
from any other AI-written piece.

The antidote is **specificity that belongs to one person.** A real experience.
A real scene. A real opinion that someone actually holds — not a diplomatically
hedged "some people say X, others say Y."

This skill therefore requires loading a user profile before writing, and a privacy
review after writing. These steps are not optional — they are what separate "an
AI article" from "your article."

---

## Core Workflow

To execute any writing request, follow this pipeline in order:

0. **Load or collect user profile** — Before writing, check if a user profile
   exists at `~/.workbuddy/essay_writing_profile.md`. If found, load it and extract
   the identity anchor, experiential scenes, style preferences, and no-go zones.
   If not found, prompt the user with:
   > "这篇文章需要你的个人素材来避免 AI 同质感。你有配置过写作身份档案吗？
   > 我可以给你一份模板：**轻量版 30 秒填完**（身份 + 语气 + 一句话经历），
   > 或者完整版 5 分钟（含风格配方和禁用区）。你想用哪个？
   > 也可以你现在随口说几句你的身份和相关经历，这篇文章我就能写得和你的气质一致。"
   - User picks 轻量版 → load `assets/user_profile_template.md`, use Quick-Start section only (fields: identity, tone, one key experience).
   - User picks 完整版 → load `assets/user_profile_template.md`, use Full Template section.
   - User provides ad-hoc input → treat as temporary profile for this article only.
   If the user declines, proceed without personal material but clearly note that
   the article will sound generic.
   See [User Profile & Privacy Review](#user-profile--privacy-review) for full
   details on how to use the profile.

1. **Analyze the topic & detect the platform** — Identify the genre (argumentative
   essay, commentary, social critique), target readership, and core proposition.
   Cross-reference with the user profile: does the user have relevant experience
   or a natural stance on this topic?

   **Platform detection** — Determine the target platform immediately after topic
   analysis. Platform determines length, tone, paragraph density, and structural
   conventions. Follow the priority rule:
   - User names a platform → use that platform's rules
   - "回答"/"问题" → 知乎
   - "推文"/"公众号" → 公众号
   - "笔记"/"小红书" → 小红书
   - "脚本"/"短视频"/"口播" → 抖音
   - None of the above → default to 知乎 (argumentative essays naturally land as 知乎 answers)
   - Multiple platforms mentioned → 知乎 as primary, note differences at end

   For full platform rules (person, length, paragraph density, title anti-patterns,
   structural differences), load `references/platform_adaptation.md`.

2. **Retrieve source material** — Extract relevant experiences, data points, and
   substantiated facts. PRIORITIZE material from the user profile (real scenes and
   experiences) over generic data — a personal scene beats a statistic every time.
   Never fabricate.

   **Data sourcing strategy** (follow this hierarchy):

   a. **User-provided data** (highest priority). If the user includes data in their
      request or profile, use it directly. Verify relevance and source credibility.
      If uncertain about a data point the user provided, ask: "你提到的这个数据，
      方便确认一下来源吗？"

   b. **Web search** (when data is missing). Use web search to find recent,
      authoritative sources. Prioritize: academic studies with named institutions
      and sample sizes, government statistics, reputable media, established
      research institutions. Cross-check: if only one source reports a number,
      treat it as unverified. When citing, state the institution, sample size,
      and year — never a bare number.

   c. **Flag data gaps** (never fabricate). If neither user nor web provides
      usable data for a key claim, do NOT invent. Either: (i) restructure the
      argument to not depend on that claim, or (ii) state honestly in the article:
      "关于这一点，我没有找到可靠的数据。以下论述基于逻辑推演，你读的时候自己判断。"
      Or ask the user directly: "这部分我需要数据支撑。你有相关数据吗？还是我先基于
      逻辑推演写？"

   **Statistical discipline (hard rules):**

   - **No precise numbers without sources.** "87.3%的人..." is fabrication unless
     backed by a named study. Round to significant figures.
   - **Correlation ≠ causation.** If a study shows correlation, do not phrase it
     as causation. "X与Y相关" is not "X导致Y".
   - **Beware the base rate fallacy.** A 95% accurate test with 1% prevalence
     yields mostly false positives. Do not cite accuracy without base rate.
   - **Selection bias.** "高考状元追踪" is not representative of "高分人群".
     Acknowledge what the sample can and cannot represent.
   - **Temporal validity.** 2010 data does not support 2024 claims unless you
     explain why the relationship should be stable over time.
   - **Geographic validity.** US/EU study conclusions do not automatically apply
     to Chinese contexts. State the transfer conditions explicitly, or do not
     transfer.
   - **Never use the phrase "研究表明" without naming the study.** The vaguer the
     attribution, the less credible the claim. "一项针对XX的研究表明" is insufficient
     — name the institution, year, and sample.

3. **Build the skeleton** — Structure the article as a three-act arc:
   *Opening slash* → *Progressive layering* → *Aphoristic close*.
   Plan where user's personal scenes will land (opening, mid-argument grounding,
   or closing).

4. **Flesh out with scenes** — Replace every abstract generalization with a concrete
   scene. USER SCENES FIRST: deploy all usable scenes from the user profile before
   reaching for generic examples or invented scenes. Replace empty argument with
   data or verified fact.

5. **Self-audit** — Run through the checklist item by item. Do not deliver until
   all checks pass.

6. **Privacy review** — After generating the draft, PAUSE and present a privacy
   review to the user BEFORE delivering the final article. This is a mandatory
   step — never skip it. For details, see [Privacy Review Process](#privacy-review-process).

## Three-Layer Principles

### Layer 1 — Readability: Clear to the educated general reader

The target reader has roughly the literacy of a Chinese university graduate. The
prose must be clear without being simplistic, and sophisticated without pedantry.
The reader should finish thinking "this person pointed out something I hadn't
considered," not "this person is showing off terminology" or "what was the point."

**Core expression techniques** — For full patterns, anti-patterns, and detailed
examples, load `references/writing_techniques.md`.

| Technique | Purpose |
|-----------|---------|
| Opening slash | Core contradiction or counterintuitive judgment in the first 1-3 lines — no warm-up |
| Rhetorical hammer | Single rhetorical question at a key pivot that forces the reader to confront an implication |
| Short punch / long release | Short sentences build urgency; follow with a longer sentence for resolution |
| Analogy — see first, then think | Concrete visual image from a different domain before mapping to the abstract concept |
| Aphoristic close | Standalone quotable line (under 25 chars) at the end of a section or entire piece |

**Rhythm control:** Never allow three or more consecutive paragraphs of the same
rhythm. After a barrage of short sentences, follow with a long settling paragraph.
After abstract analysis, follow with a scene that grounds it.

**Anti-AI-voice discipline (3 core rules):**
For the complete guide with 50+ examples and platform-specific patterns,
load `references/anti_ai_voice.md`.

1. **No structural numbering** — Never 第一/第二/第三, 首先/其次/最后, 原因有几层.
   Use scene progression instead.
2. **No banned words** — 值得注意的是, 更重要的是, 从某种意义上说, 在一定程度上,
   综上所述 — these words expose AI immediately. Full banned-word list in
   `references/anti_ai_voice.md` §3.5.
3. **Let judgments stand alone** — No self-defense (我不是在说你, 我不想回避),
   no fake citations (某位哲人, 周导说), no over-explanation after a strong sentence.
   Trust the reader.

### Layer 2 — Thinking Mode: First principles + factual discipline

The value of an argumentative essay lies in demonstrating a causal chain the reader
has not walked before. Minimize "preaching principles"; maximize knowledge logic.

**First-principles toolkit:**

- **First principles thinking**: Decompose to foundational axioms, then rebuild upward
- **Economic principles**: Supply/demand, incentives, costs, substitution
- **Core social psychology**: Conformity, confirmation bias, anchoring effect

**Thinking techniques** — For full guide with detailed examples, load `references/thinking_toolkit.md`:

- **Concept manufacturing**: Don't describe a phenomenon — name it. Coin a term (max 4
  characters) as the article's skeleton. E.g., "景观产品" / "被动关系" / "系统冗余".
- **Producer mindset**: Don't just say "this is wrong" — reverse-engineer how a scene
  was produced. Walk the reader through: who made this → why → how do they profit →
  what would you have thought if you didn't break it down.
- **Dirty word strategy**: In key judgment moments, use one crude-but-precise word
  (e.g. "shi上雕花", "脱裤子放屁") to break the reader's expectation of "formal writing."
  Max 3 per article. Must be more precise than any polite alternative.
- **Binary framework**: Instead of giving advice ("you should do X"), give a
  classification framework. "All things fall into two categories: A and B."
  The reader applies it to their own life. E.g., limited vs unlimited responsibility,
  passive vs active relationships.
- **Trace the money**: For any social phenomenon, ask: who pays → what do they get →
  what are non-payers doing. Money is the one part of the "invisible hand" you can
  actually see.

**Factual discipline (hard rules):**

- Verified facts are the only admissible grounds. If a fact cannot be confirmed, do not use it
- Data ≠ fact. When citing data, state explicitly what it demonstrates and what it does NOT demonstrate
- Precise probabilistic predictions are not credible — avoid them
- Post-truth vigilance: concealing part of the truth = manufacturing false impressions
- Theory discipline: Thinkers' ideas are tools, not authorities
- Complexity boundary: When a system has too many variables, do not force a single causal explanation

### Layer 3 — Value: Must deliver at least one of three types

- **Deeper understanding**: The reader says "so that's how it works"
- **Cognitive upgrade**: The reader realizes a cognitive framework is flawed — "I was wrong about this"
- **Actionable**: Give a judgment criterion or action framework the reader can use immediately

**Anti-patterns (what to reject):** Pure emotional resonance, pure opinion listing,
pure information repackaging with no original angle.

## Scene-Body Technique (场景体)

Replace summary with scene. Let the image carry the argument.

| Summary (weak) | Scene (strong) |
|----------------|----------------|
| He gets physical symptoms when stressed | When stressed, his hair falls out, acne breaks out, he says he's fine |
| High school is intensely pressurized | Asleep on the metro — not tired, total system overload |
| University demands independent choice | I waited and waited for a homeroom teacher to talk to me. Nothing ever came |

**Four rules for scene writing:**

1. Use images, not labels
2. Use spoken vernacular, not written-formal register
3. Use rhythm, not rhetorical ornament
4. Do not fear leaving things unsaid — negative space is itself a force

**Placement in the article:**
- **Opening scene** — Replace "with the development of society"-style throat-clearing.
  When user profile scenes are available, the opening scene should come from the user's
  real experience whenever possible. A real scene outguns any invented one.
- **Mid-argument scene** — Ground an abstract conclusion so it lands
- **Closing scene** — Freeze-frame an image instead of a summary

**Scene source priority:**
1. User profile scenes (real, lived, irreplaceable)
2. Publicly verifiable real-world scenes (news events, historical moments)
3. Constructed scenes (invented but plausible — use only when 1 and 2 are exhausted)

## Structure Template

```
# [Title]

[Opening scene: 1-3 lines, make the slash]

[Layer 1: Dissect the phenomenon]
[Short-sentence advance + rhetorical hammer]

[Layer 2: Trace cause and effect]
[Analogy — let the reader see first, then think]

[Layer 3: Value flip — cognitive upgrade or action framework]
[Aphoristic close or scene freeze-frame]
```

**Common variants:**
- **Contrast structure** — Juxtapose two opposing realities side by side
- **Demystification structure** — Take a widely accepted idea and dismantle it layer by layer
- **Paradox structure** — Start with a contradiction, then resolve it through deeper logic

## Delivery Checklist

Before delivering any article, verify each item:

1. **Opening slash?** Do the first three sentences provoke a "huh?" reaction?
2. **Scenes present?** At least three concrete images/scenes?
3. **Rhetorical hammer?** At least one rhetorical question at a key pivot?
4. **Aphoristic close?** A standalone quotable line at the end?
5. **Clear causal chain?** Can the reader follow from start to finish without getting lost?
6. **Hard facts?** Every key argument backed by confirmed facts?
7. **Value increment?** Does the reader gain understanding / cognitive upgrade / actionability?
8. **Rhythm variety?** No three consecutive paragraphs of the same rhythm?
9. **Scene-body fidelity?** Are scenes images rather than labels?
10. **Domestic trivia cut?** Unless the topic directly requires it, no intimate family-conflict details
11. **No structural numbering?** No 第一/第二/第三 or 首先/其次/最后?
12. **No banned words?** No 值得注意的是, 更重要的是, 从某种意义上说, 在一定程度上,
    综上所述, 说白了 (beyond once)?
13. **No fake citations?** Every named source is real; no invented 某导/某学者?
14. **No self-defense?** No 我知道这听起来像, 这不是在说你不好, 我不想回避?
15. **Em-dash density?** Full article ≤3 em-dashes?
16. **Ellipsis density?** Full article ≤1 ellipsis?
17. **Quote abuse?** No random 引号 for casual emphasis (only for direct speech or coined terms)?
18. **Semicolon density?** No consecutive multi-sentence semicolon chains?

If any item fails, revise before delivering.

### Output Format

Default output is **Markdown**. Use:
- `#` for article title (single H1)
- `##` for major section breaks (if platform supports it — 知乎 does, 小红书 does not)
- `**bold**` for emphasis in 知乎/公众号; minimal bold in 小红书 (visual clutter)
- `> ` blockquote for key quotable lines when platform supports it
- Single blank line between paragraphs
- No trailing `---` section dividers (they read as "AI-generated")
- No `* * *` centered dividers ever

If the user requests **plain text**, strip all Markdown formatting and use blank lines
for section separation only. The prose itself does not change — only the wrapping.

---

## User Profile & Privacy Review

### Purpose

Two problems are solved here, and they are the same problem:

1. **Homogenization (同质化)**: Without personal material, every article produced
   by this skill sounds like "an AI wrote it." The prose may be competent, but
   it has no signature, no edge, no lived texture. Readers can smell it.

2. **Privacy**: Personal material that makes writing distinctive is also personal
   material that can compromise privacy. The solution is not to avoid personal
   material. The solution is a structured review step.

### The profile file

The user maintains a profile at `~/.workbuddy/essay_writing_profile.md`. A blank
template is provided in `assets/user_profile_template.md` for first-time setup.

The profile contains four sections:

| Section | Content | Writing impact |
|---------|---------|----------------|
| Identity anchor | 1-2 sentences describing the writer's real situation | Gives the article a genuine "I" — a specific person writing from a specific place |
| Experiential scenes | 3-10 concrete personal scenes (not opinions) | The raw material for scene-body technique — these are the images that carry arguments |
| Style preferences | Tone, humor, sentence rhythm, cultural references | Counters AI's default "balanced" voice |
| No-go zones | What must never appear | Prevents privacy breaches before they happen |

### How to use the profile during writing

1. **Before writing**: Read the profile. Identify which scenes and which identity
   elements are relevant to the current topic. Do NOT use scenes that don't fit
   — a forced personal anecdote is worse than none.

2. **During writing**: The identity anchor shapes the opening stance (what kind of
   person is making this argument?). The experiential scenes replace generic examples
   in the scene-body slots. The style preferences override AI default language habits.

3. **If no profile exists**: Ask once. If the user provides ad-hoc material (a few
   sentences in chat), treat that as a temporary profile for this article only.
   If the user declines entirely, proceed but flag the homogenization risk.

### Privacy Review Process

**This step is mandatory. Never skip it.**

After generating the article draft and passing the self-audit checklist, pause
and present the following to the user:

```
---

📋 隐私审核 — 以下内容包含你的个人信息，请逐条确认是否可以公开发布：

1. [具体个人信息1] — 出现在：[文章位置/段落]
   - 敏感度：🟢 低 / 🟡 中 / 🔴 高
   - [ ] 可以发布 [ ] 需要修改（请说明怎么改） [ ] 删除此项

2. [具体个人信息2] — 出现在：[文章位置/段落]
   - 敏感度：🟢 低 / 🟡 中 / 🔴 高
   - [ ] 可以发布 [ ] 需要修改（请说明怎么改） [ ] 删除此项

...
```

**Rules for the privacy review:**

- List EVERY piece of personal information used in the article. DO NOT assume
  something is "safe enough" — let the user decide.
- Personal information includes: identity details, specific experiences, locations,
  time periods, professional context, family references, emotional states tied to
  identifiable situations.
- Mark sensitivity honestly:
  - 🟢 Low: General professional context, broad life stage (e.g., "I work in tech"),
    personality traits, stylistic preferences
  - 🟡 Medium: Specific but not uniquely identifying (e.g., industry + role, city,
    approximate age range, non-controversial experiences)
  - 🔴 High: Uniquely identifying (specific company, specific event, financial
    details, family members, health information)
- After the user responds, modify ONLY the items the user flags. If the user says
  "approve all," deliver the article as-is.
- If removing an item would create a logical gap in the article, fill the gap
  with a generic scene or data point — do NOT leave a hole.
- After the user's final approval, deliver the complete article.

### Example privacy review

User profile contained: "I taught physics for 6 years at a county-level high school"
and "I quit my job at ByteDance in 2023."

Generated article uses both. The review:

```
📋 隐私审核 — 以下内容包含你的个人信息，请逐条确认：

1. "在县城中学教了六年物理" — 出现在：开篇场景，第二段
   - 敏感度：🟡 中（县级中学 + 学科 + 年限组合可能被熟人识别）
   - [ ] 可以发布 [ ] 需要修改（请说明怎么改） [ ] 删除此项

2. "2023年从字节跳动离职" — 出现在：第三段，论证中段
   - 敏感度：🔴 高（具体公司名 + 具体时间 — 极可能被识别）
   - [ ] 可以发布 [ ] 需要修改（请说明怎么改） [ ] 删除此项
```

The user might respond: "1 可以，2 改成'从一家大厂离职'就行。"

The AI then modifies only item 2 and delivers the final article.
