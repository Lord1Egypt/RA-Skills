---
slug: tcms-adapter
displayName: Tcms Adapter
name: tcms-adapter
version: "1.1.10"
not_for:
  - Writing the core draft from scratch (adapts an existing reviewed draft)
  - Unreviewed or unapproved drafts as input (review must happen upstream)
  - Direct publishing or channel operations (produces ready-to-publish versions only)
  - Full translation projects (channel adaptation, not document translation)
description: |
  Channel-adaptation agent. Adapts a reviewed core draft into channel-specific publish-ready versions.
  Supports: official-account version, developer-community version, Chinese social post, English X post, LinkedIn summary, sales one-pager.
  Also generates re-promotion material for existing content.
description_zh: "渠道适配器：将已审核心稿适配为各渠道可发版本（公众号版、开发者社区版、中文社媒、英文 X、LinkedIn 摘要、销售一页纸），并为已有内容生成再推广素材。"

read_when:
  - 适配
  - 改写
  - 多渠道版本
  - 渠道版本
  - 公众号版
  - 社交帖
  - 英文帖
  - 二次推广
  - adapt
  - repurpose
allowed-tools:
  - read_file
  - write_to_file
  - replace_in_file
  - web_fetch
metadata:
  openclaw:
    tags:
      - content-marketing
      - communication
      - channel-marketing
      - social-media
      - linkedin
      - wechat
      - repurposing
      - tech-product
      - b2b
disable: false
---

# Content Adapter

Adapts a reviewed core draft (or published article) into the channel-specific versions needed for publishing. Does not create from scratch — that is `content-writer`'s job.

## Two modes

**Mode A: multi-channel adaptation of new content**
Input: core draft from `content-writer`
Output: adapted versions for specified channels

**Mode B: re-promotion of existing content**
Input: URL or local file of a published article
Output: lightweight material such as social posts, opinion summaries, data-point extractions

Mode B steps:
1. [deterministic] read the published article
2. [LLM] extract 3 shareable information points (hardest data / sharpest opinion / most vivid scenario)
3. [LLM] generate material per target channel
4. [LLM] self-check (data consistent with original / product-name规范 / no sensitive info)
5. [deterministic] output to `content/adapted/repurpose/`

---

## Step 1: Confirm input and target channels [deterministic]

1. Confirm the core-draft path (or published-article URL)
2. Confirm the list of channels to adapt to
3. Read the core-draft content

When no channel is specified, default to the full set: official-account version / community version / Chinese social post ×2 / English X post ×1 / LinkedIn summary (if needed) / sales one-pager (only when case or hard data is present)

## Step 2: Read channel specs [deterministic]

Read the relevant channel-spec files on demand (`references/channel-specs/` directory), and read the brand guidelines (reuse `content-writer`'s `brand-rules.md`).

## Step 3: Adaptation generation [LLM]

Each channel version is generated independently, with no dependency between them:

### Official-account version
- Rewrite based on the core draft; reduce technical detail, add scenario description
- Scenario hook at the opening, fixed brand closing at the end
- 1500-2500 words

### Developer-community version (deterministic fine-tune)
- When the core draft is already in tech-blog style → **use the core draft directly**
- Only minor formatting tweaks; may append further-reading links at the end
- Not treated as a separate LLM task

### Chinese social post
- Extract 1 most impactful data point or scenario
- hook + core message + topic hashtags, under 300 words
- Produce 2 posts from different angles per core draft

### English X post
- Thread format (3-5 posts) or single post
- Written with English thinking, not translated from Chinese
- Keep technical terms in original; each post ≤280 characters

### LinkedIn summary
- For management audience, leans business value
- 200-300 words, professional formal tone

### Sales one-pager
- Generated only when containing customer case or hard data
- Customer challenge → solution → effect data → applicable scenario, ≤400 words

## Step 4: Self-check [LLM]

- [ ] Word-count limit
- [ ] Key data points preserved (no omission, no fabrication)
- [ ] Product-name规范
- [ ] Customer-name redaction carried through
- [ ] English version avoids Chinglish

## Step 5: Output [deterministic]

```
content/adapted/
├── YYYY-MM-{topic}-wechat.md
├── YYYY-MM-{topic}-community.md
├── YYYY-MM-{topic}-social-cn-1.md
├── YYYY-MM-{topic}-social-cn-2.md
├── YYYY-MM-{topic}-x-en.md
├── YYYY-MM-{topic}-linkedin.md     (if needed)
└── YYYY-MM-{topic}-one-pager.md    (if needed)
```

Execution summary:

> **Verify hard limits by count, not estimate.** Platform limits (character caps, image counts) are confirmed by actual length or count after generation, never by judgment.

```markdown
## Execution summary
- Core draft: [filename] ([word count] words)
- Generated: official-account ([words]) / Chinese social ×2 / English X ×1 / ...
- Not generated: [channel] (reason)
- Data-point preservation check: [N] all preserved / [M] excluded due to word limit
```

---

## Hard rules

1. **Don't fabricate data.** Data in adapted versions must come from the core draft.
2. **Don't change the core judgment.** Simplify yes, change conclusions no.
3. **Consistent product names.** All versions use the official names in `brand-rules.md`.
4. **Carry through customer redaction.** Redacted in the core draft stays redacted in all versions.
5. **Don't cross-reference other drafts.** Use only information from the current core draft.
6. **English quality.** Prefer short and accurate over verbose and stiff. Mark uncertain parts [needs confirmation].
7. **Uncertain content stays marked.** Any segment without an authoritative source keeps its [needs confirmation] marker into the final channel output; the marker is never removed to make a variant look finished.

## Failure handling

| Scenario | Handling |
|----------|----------|
| Core draft under 500 words | prompt "too little content, suggest supplementing first" |
| Core draft has no data points | mark "no hard data, suggest publishing from an opinion angle" |
| Core draft contains unredacted customer name | auto-redact and warn |
| Channel-spec file missing | generate with a generic format |

## ⚠️ Human-in-the-loop

- Mode A: official-account and LinkedIn versions go through L1-L2 approval before publishing
- Mode B: social posts go through L1 light review before publishing
- English versions marked [needs confirmation] need human proofreading before publishing

---

## 中文摘要

Content Adapter 把已审核的核心稿（或已发布文章）适配为各渠道发布版本，不负责从零创作。支持公众号版、开发者社区版、中文社交帖、英文 X 帖、LinkedIn 摘要、销售一页纸，以及存量内容二次推广物料。硬性规则：不编造数据、不改变核心判断、产品名一致、客户脱敏延续、跨稿不互引、英文宁可简短准确。
