---
name: seo-optimizer
version: 1.0.0
description: "SEO optimizer and compliance checker for Chinese social media. Optimizes titles, keyword density, hashtags, and scans for advertising-law banned words (广告法违禁词)."
author: ai-agent-store
license: MIT
platforms:
  - openclaw
  - cursor
  - claude-code
  - codex-cli
tags:
  - seo
  - optimization
  - compliance
  - social-media
  - chinese
price: 9
---

# SEO Optimizer — SEO 优化 & 违禁词检查

Optimize content for search visibility and check compliance with Chinese advertising regulations.

## When to Activate

Trigger when the user mentions: SEO, 关键词优化, search ranking, 违禁词检查, keyword optimization, compliance check.

## SEO Optimization Flow

### 1. Keyword Analysis
- Extract 3-5 core keywords from content
- Verify keyword popularity on each platform via search
- Recommend long-tail keyword combinations

### 2. Title Optimization
- Front-load the core keyword
- Include 1-2 long-tail keywords
- Platform-adapt: 小红书 (emoji + numbers), 知乎 (question), 公众号 (curiosity gap)

### 3. Body Optimization
- Core keyword appears naturally 3-5 times
- First paragraph contains the primary keyword
- Subtitles include keyword variations

### 4. Hashtag Optimization
- Recommend 5-10 related hashtags
- Mix: high-traffic + precise-niche + long-tail

## Banned Word Scanner (广告法违禁词)

### Absolute Claims (PROHIBITED)
最, 第一, 唯一, 首个, 顶级, 极致, 最佳, 最好, 最优, 最强,
绝对, 永久, 万能, 100%, 全网最低, 史上最, No.1

### False Promises (PROHIBITED)
保证, 承诺效果, 无效退款 (unofficial channels), 立竿见影, 药到病除

### Medical Claims (PROHIBITED for non-medical categories)
治疗, 治愈, 药效, 疗效, 处方, 诊断

### Inducement Language (RESTRICTED)
点击领取, 免费 (must be genuinely free), 秒杀 (must be real promotion)

## Output Format
```
## SEO Optimization Report

### Recommended Keywords
1. {keyword} — Est. popularity: High / Medium / Low

### Title Optimization
- Original: {original title}
- Optimized: {new title}
- Rationale: {why it's better}

### Banned Word Scan
- ✅ No banned words found / ⚠️ Found {N} banned words
- {banned word} → Suggested replacement: {alternative}

### Recommended Hashtags
{hashtag list}
```
