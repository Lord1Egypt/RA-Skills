---
name: seo-content-pro
description: Advanced SEO content creation with AI humanization, image generation, multi-language support, content refresh, SEO scoring, and competitor analysis. Perfect for content creators and agencies.
author: fly3094
version: 1.4.0
tags: [seo, content, writing, article, blog, marketing, multi-language, research, video-seo, ai-detection, youtube, bilibili, transcript]
support: 
  paypal: 492227637@qq.com
  email: 492227637@qq.com
metadata:
  clawdbot:
    emoji: 📝
    requires:
      bins:
        - python3
        - curl
    config:
      env:
        CONTENT_TONE:
          description: Default tone (professional|casual|technical|friendly)
          default: "professional"
          required: false
        DEFAULT_LENGTH:
          description: Default word count
          default: "2000"
          required: false
        CONTENT_LANGUAGE:
          description: Target language (en|zh|es|fr|de|ja)
          default: "en"
          required: false
        SEARXNG_URL:
          description: SearXNG instance for privacy-respecting research
          default: "http://localhost:8080"
          required: false
---

# SEO Content Pro 📝

**Rank higher on Google. Write faster.** AI-powered SEO content that competes with top 10 results.

**Time saved:** 5 hours/article → 30 minutes/article  
**Result:** 1500-3000 word articles with SEO score 80+

## What It Does

- 🔍 **Topic Research**: Analyzes top-ranking content using SearXNG (privacy-respecting, no tracking)
- 📋 **Outline Generation**: Creates SEO-optimized article structures (H1/H2/H3 hierarchy)
- ✍️ **First Draft**: Writes 1500-3000 word articles in 6 languages
- 🎯 **Keyword Integration**: Suggests and integrates primary/secondary keywords naturally
- 📊 **Competitor Analysis**: Identifies content gaps vs top 10 ranking pages
- 🌐 **Multi-language**: English, Chinese, Spanish, French, German, Japanese
- 🔄 **Content Refresh**: Update old articles with new data and insights
- 📈 **SEO Score**: Get content quality score (0-100) with specific improvement suggestions
- 🤖 **AI Humanization** (v1.2 NEW): Detect and transform AI-generated text to bypass AI detectors
- 🖼️ **Image Generation** (v1.2 NEW): Generate featured images using Google Gemini 3 Pro Image API
- 🎬 **Video SEO** (v1.4 NEW): Optimize YouTube/B 站 video titles, descriptions, tags, and transcripts
- 📝 **Transcript Processing** (v1.4 NEW): Extract and optimize video transcripts for SEO

## Quick Start (2 minutes)

```bash
# 1. Install
clawhub install seo-content-pro

# 2. Create your first article
# Just ask: "Write a 2000-word SEO article about AI automation tools"
```

**Full workflow example:**
```
User: Create SEO article about "best AI automation tools" - 2500 words

AI: 
1. 🔍 Researching top 10 ranking pages...
2. 📋 Generating SEO-optimized outline...
3. ✍️ Writing 2500-word draft...
4. 📊 Analyzing SEO score: 85/100
5. 🎯 Keyword density: 2.1% (optimal)
6. ✅ Article ready!

Word count: 2,547
Reading time: 11 minutes
SEO Score: 85/100
Primary keyword: "AI automation tools" (18 mentions)
Secondary keywords: automation software, AI tools, workflow automation
```


## New Features in v1.2.0

### 🤖 AI Content Humanization

Detect and transform AI-generated text to make it more natural and bypass AI detectors.

**Usage:**
```bash
# Humanize existing content
python3 scripts/humanize.py --input article.md --output article-humanized.md

# Detect AI content
python3 scripts/detect_ai.py --input article.md

# Compare before/after
python3 scripts/compare.py --input article.md
```

**AI Detection Patterns (16 types):**
- 🔴 Critical: Citation bugs, knowledge cutoff, chatbot artifacts
- 🟠 High: AI vocabulary, significance inflation, promotional language
- 🟡 Medium: Superficial analysis, filler phrases
- 🟢 Style: Curly quotes, em-dashes overuse

### 🎬 Video SEO (v1.4 NEW)

Optimize videos for YouTube and B 站 (Bilibili) to rank higher in video search results.

**Usage:**
```bash
# Optimize YouTube video
python3 scripts/video_seo.py --platform youtube --title "AI Automation Tutorial" --duration "10:25"

# Optimize B 站 video
python3 scripts/video_seo.py --platform bilibili --title "AI 自动化教程" --tags "[AI,自动化，教程]"

# Process transcript
python3 scripts/transcript.py --input video.srt --output optimized.txt
```

**Features:**
- Title optimization (under 60 characters for YouTube, under 80 for B 站)
- Description generation with timestamps
- Tag suggestions based on topic
- Transcript SEO optimization
- Chapter markers for long videos

### 🖼️ Featured Image Generation

Generate custom featured images for your articles using Google Gemini 3 Pro Image API.

**Usage:**
```bash
# Generate new image
python3 scripts/generate_image.py --prompt "AI automation technology" --filename featured.png

# With resolution option
python3 scripts/generate_image.py --prompt "SEO dashboard" --filename seo-image.png --resolution 2K

# Edit existing image
python3 scripts/generate_image.py --prompt "Make it more professional" --input-image old.png --filename new.png
```

**Resolution Options:**
- 1K (default) - ~1024px, fast iteration
- 2K - ~2048px, standard quality
- 4K - ~4096px, high resolution

**API Key:**
Set `GEMINI_API_KEY` environment variable or use `--api-key` argument.

### Complete Workflow (v1.2)

```bash
# 1. Generate SEO content
# Ask AI: "Create SEO article about AI automation tools - 2500 words"

# 2. Humanize content (optional)
python3 scripts/humanize.py --input article.md --output article-humanized.md

# 3. Generate featured image
python3 scripts/generate_image.py --prompt "AI automation dashboard" --filename featured.png --resolution 2K

# 4. Detect AI content (optional, for quality check)
python3 scripts/detect_ai.py --input article.md

# 5. Review SEO score
# AI will provide SEO analysis with score and suggestions
```

## Commands

### Research a Topic
```
Research "[keyword/topic]" for SEO content
```

### Generate Outline
```
Create outline for "[article title]" targeting "[primary keyword]"
```

### Write Draft
```
Write draft for "[article title]" using outline, 2000 words, tone: professional
```

### Full Workflow
```
Create SEO article about "[topic]" - research, outline, and draft (2500 words)
```

### Content Refresh
```
Update and improve this article with latest data and SEO best practices
```

### SEO Analysis
```
Analyze this content and provide SEO score with improvement suggestions
```

### Multi-language
```
Create SEO article about "[topic]" in Chinese, 2000 words
```

## Configuration

### Environment Variables

```bash
# Default content tone
export CONTENT_TONE="professional"  # professional|casual|technical|friendly

# Default word count
export DEFAULT_LENGTH="2000"

# Include FAQ section
export INCLUDE_FAQ="true"  # true|false

# Target language
export CONTENT_LANGUAGE="en"  # en|zh|es|fr|de|ja

# SearXNG instance (for privacy-respecting research)
export SEARXNG_URL="http://localhost:8080"
```

### OpenClaw Config

```json
{
  "env": {
    "CONTENT_TONE": "professional",
    "DEFAULT_LENGTH": "2000",
    "INCLUDE_FAQ": "true",
    "CONTENT_LANGUAGE": "en"
  }
}
```

## Output Format

Each article includes:

- **Meta Title** (50-60 characters)
- **Meta Description** (150-160 characters)
- **H1 Title** (engaging, includes primary keyword)
- **Introduction** (150-200 words, hooks reader)
- **H2/H3 Sections** (proper hierarchy, keyword-optimized)
- **Conclusion with CTA** (clear next steps)
- **Internal/External Link Suggestions**
- **FAQ Section** (3-5 questions with answers)
- **SEO Score** (0-100 with breakdown)

## Example Usage

### Basic Article
```
User: Create SEO article about "best AI automation tools for small business" - 2500 words

Assistant: 
1. 🔍 Researching top 10 ranking pages...
2. 📊 Analyzing content gaps and keyword opportunities...
3. 📋 Generating optimized outline...
4. ✍️ Writing 2500-word draft with H2/H3 structure...
5. 📈 Calculating SEO score and suggestions...

✅ Article ready! SEO Score: 87/100
```

### Multi-language
```
User: Create SEO article about "remote work productivity" in Chinese, 2000 words

Assistant:
Generating Chinese content for "远程工作效率"...
✅ 文章完成！SEO 分数：85/100
```

### Content Refresh
```
User: [paste old article]
Update this article with 2026 data and improve SEO

Assistant:
1. Analyzing current content...
2. Researching latest data and statistics...
3. Identifying SEO improvements...
4. Updating with fresh insights...

✅ Refreshed! SEO Score improved from 62 to 89 (+27 points)
```

## SEO Score Breakdown

Your content is scored on:

| Factor | Weight | Description |
|--------|--------|-------------|
| Keyword Usage | 20% | Primary/secondary keyword placement |
| Content Length | 15% | Optimal word count for topic |
| Readability | 15% | Flesch score, sentence structure |
| Heading Structure | 15% | Proper H1/H2/H3 hierarchy |
| Meta Tags | 10% | Title and description optimization |
| Internal Links | 10% | Suggested internal linking |
| External Links | 10% | Quality external references |
| FAQ Section | 5% | Comprehensive FAQ coverage |

## Integration with Other Skills

### social-media-automator
```
1. Create SEO article with seo-content-pro
2. Generate social posts with social-media-automator
3. Schedule and publish across platforms
```

### rss-to-social
```
1. Monitor industry RSS feeds with rss-to-social
2. Identify trending topics
3. Create content with seo-content-pro
4. Auto-publish to social media
```

Complete content automation loop! 🔄

## Use Cases

### Content Marketers
- Scale content production 5-10x
- Maintain consistent quality
- Target multiple keywords efficiently

### SEO Agencies
- White-label content creation
- Serve more clients with same team
- Standardize quality across writers

### Solopreneurs
- Create professional content without hiring
- Save $500-2000/month on writing costs
- Focus on business, not content creation

### Multi-language Businesses
- Localize content for different markets
- Maintain brand voice across languages
- Scale globally with consistent quality

## Tips for Best Results

1. **Provide Context**: Tell the skill your target audience and goal
2. **Specify Tone**: Match your brand voice (professional, casual, technical)
3. **Add Examples**: Share articles you like for style reference
4. **Review & Edit**: AI draft is a starting point – add your expertise
5. **Update Regularly**: Use content refresh quarterly to keep articles current
6. **Target Long-tail**: More specific keywords = easier to rank

## Pricing Integration

This skill powers LobsterLabs content services:

| Service | Price | Delivery |
|---------|-------|----------|
| Single Article | $300-500 | 3-5 days |
| Monthly Pack (4 articles) | $1,500-2,500 | Monthly |
| White-label Agency | $3,000+/month | Unlimited |
| Content + Social Bundle | $2,000-4,000/month | Full service |

**ROI Example:**
- Cost: $2,000/month (4 articles + social)
- Client revenue from content: $10,000-50,000/month
- ROI: 5-25x

Contact: PayPal 492227637@qq.com

## Troubleshooting

### Low SEO Score
- Check keyword density (1-2% for primary keyword)
- Add more H2/H3 subheadings
- Increase content length if under 1500 words
- Add FAQ section if missing

### Research Issues
- Verify SearXNG instance is running
- Check internet connection
- Try alternative search terms

### Language Quality
- Specify language explicitly in command
- For best results, use native language
- Review and adjust cultural references

## Changelog

### 1.0.0 (2026-03-07)
- Initial release
- Multi-language support (6 languages)
- Content refresh feature
- SEO scoring system
- Competitor analysis
- SearXNG integration
- Integrations with social-media-automator and rss-to-social

---

## 💖 支持作者

如果你觉得这个技能有用，请考虑打赏支持：

- **PayPal**: 492227637@qq.com
- **邮箱**: 492227637@qq.com

你的支持是我持续改进的动力！


---

## 🆕 新增功能（v1.1.0）

### AI 标题生成器
- 5 种标题模板（How-to、List、Question、Secret、Comparison）
- A/B 测试支持，生成 3-10 个变体
- 标题评分系统（0-100 分）
- 爆款标题特征分析

### 使用示例
```bash
# 生成标题
python3 scripts/title_generator.py "SEO 内容写作" "写出爆款文章" 10

# 输出示例：
1. [85 分] 如何在 30 分钟内写出爆款文章（完整指南）
2. [90 分] 3 个 SEO 内容写作技巧，第 3 个太实用了
3. [80 分] 为什么你的 SEO 内容总是失败？原因在这里
```

### A/B 测试工作流
1. 生成 5-10 个标题变体
2. 选择评分最高的 3 个
3. 在不同平台/时间测试
4. 分析数据，选择最佳标题
