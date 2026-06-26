---
name: social-copy-generator
version: 2.0.0
description: |
  Generate platform-optimized social media copy for product launches. One input, 14 platform outputs (Twitter/X, LinkedIn, Hacker News, Reddit, Xiaohongshu, Jike, WeChat Moments, Weibo, Zhihu, Bilibili, Douyin, Video Account, Telegram, and more). Auto-generates an HTML page with one-click copy buttons. Supports Chinese and English bilingual content.
tags: ["social-media", "copywriting", "marketing", "twitter", "xiaohongshu", "wechat"]
metadata: {"openclaw":{"emoji":"📝"}}
---

# Social Copy Generator

Generate social media copy for multiple platforms from a single product description. Output as an HTML page with one-click copy buttons.

## When to use

When the user wants to:
- Promote a project/product on social media
- Generate copy for multiple platforms at once
- Create platform-specific marketing content
- Launch an open source project with social posts

## How it works

1. User describes their product/project
2. Generate platform-optimized copy for each target platform
3. Output an HTML file with styled cards and copy buttons
4. Open in browser for easy copy-paste

## Supported Platforms

| Platform | Style | Limits |
|----------|-------|--------|
| Twitter/X | Concise, thread format for long content | 280 chars/tweet |
| Jike (即刻) | Developer community, dry content | No limit |
| Xiaohongshu (小红书) | Casual, emoji-rich, comparison-heavy | No limit |
| WeChat Moments (朋友圈) | Personal, conversational | No limit |
| Video Account (视频号) | Title + description for video | Title < 30 chars |
| LinkedIn | Professional, achievement-focused | No limit |
| Reddit | Low-key, helpful, anti-self-promo | Title + body |
| Hacker News | Show HN, ultra-minimal | Title only ~80 chars |
| Product Hunt | Tagline + description | Tagline < 60 chars |
| V2EX | Chinese dev community, technical | Title + body |
| Juejin (掘金) | Tutorial-style article intro | Title + summary |
| Dev.to | English dev blog, tutorial-style | Title + summary |

## Output Format

Generate an HTML file with:
- Styled cards per platform with platform-colored tags
- `white-space: pre-wrap` text areas (no extra whitespace when copying)
- One-click copy buttons using `navigator.clipboard`
- Toast notification on copy
- Mobile responsive layout

## HTML Template

```html
<!DOCTYPE html>
<html lang="zh">
<head>
<meta charset="UTF-8">
<title>[Product] - Social Media Copy</title>
<style>
body { font-family: -apple-system, sans-serif; max-width: 700px; margin: 40px auto; padding: 0 20px; background: #f5f5f5; }
.card { background: #fff; border-radius: 12px; padding: 24px; margin-bottom: 24px; box-shadow: 0 2px 8px rgba(0,0,0,0.1); }
.copy-area { background: #fafafa; border: 1px solid #e0e0e0; border-radius: 8px; padding: 16px; white-space: pre-wrap; font-size: 15px; line-height: 1.6; user-select: all; }
button { background: #000; color: #fff; border: none; border-radius: 8px; padding: 10px 20px; font-size: 14px; cursor: pointer; margin-top: 12px; }
.toast { position: fixed; top: 20px; left: 50%; transform: translateX(-50%); background: #333; color: #fff; padding: 10px 24px; border-radius: 8px; display: none; z-index: 99; }
</style>
</head>
<body>
<!-- cards here -->
<script>
function copyText(id) {
  navigator.clipboard.writeText(document.getElementById(id).innerText);
  const t = document.getElementById('toast');
  t.style.display = 'block';
  setTimeout(() => t.style.display = 'none', 1500);
}
</script>
</body>
</html>
```

## Platform Copy Guidelines

### Twitter/X
- HARD LIMIT: 280 chars total (CJK = 2 chars each, emoji = 2 chars, URL = 23 chars fixed by t.co)
- MUST count characters before output. If over 280, ruthlessly cut until under
- NO blank lines between sections — every newline costs a character
- NO bullet lists — too wasteful. Use short flowing sentences
- Lead with a hook (question or bold claim), not product name
- One short URL at end (counts as 23 chars regardless of length)
- 2-3 hashtags max, on same line as URL
- Optional: suggest a thread for details if content can't fit

### Xiaohongshu
- Start with relatable question
- Use emoji section headers (📊🔧💡🔗)
- ✅ for checklist items
- Comparison data (before/after)
- End with call to action
- Separate tags line

### Jike
- Developer-focused, no fluff
- Bullet points with •
- Include install commands
- Target audience at end

### WeChat Moments
- Conversational tone
- No emoji overload
- Explain the "why" not just "what"
- GitHub link at end

### Video Account
- Title: under 30 chars, hook + number
- Description: numbered steps
- Hashtags at end

### Reddit
- Title: descriptive, no clickbait (mods will remove)
- Body: explain what it does, why you built it, how to install
- Tone: humble, "I made a thing" energy — NOT "ultimate/best/amazing"
- Mention trade-offs or limitations honestly
- End with "Feedback welcome" or "Happy to answer questions"
- Target subs: r/ClaudeAI, r/LocalLLaMA, r/programming, r/commandline
- NEVER say "check it out!" or "you need this!" — instant downvote

### Hacker News
- Show HN format: "Show HN: [name] – [one-line description]"
- Title MUST be under 80 chars, no emoji, no hype
- Comment body: 2-3 paragraphs max. What, why, how, link
- Technical audience — lead with the interesting technical detail
- No marketing language whatsoever

### Product Hunt
- Tagline: under 60 chars, punchy, describes the value
- Description: 2-3 sentences, what + how + who it's for
- First Comment: founder story, why you built it, what's next

### V2EX
- Post in /t/programmer or /t/share
- Title: 直接说是什么，别标题党
- Body: 技术向，说清楚原理和用法
- 附 GitHub 链接
- 语气平实，不要过度推销

### Juejin (掘金)
- Title: 教程风格 "xxx 实现 xxx" 或 "xxx 使用指南"
- Summary: 1-2 句话说清楚解决什么问题
- Body hint: 可以写成教程文章，带代码块和截图
- Tags: Claude Code, 开发工具, 效率提升

### Dev.to
- Title: "How I..." or "Building..." style, descriptive
- Summary: 1-2 sentences, what problem it solves
- Tags: claudecode, opensource, productivity, cli
- Conversational but technical tone

## Example prompts
- "Generate social media posts for my new project"
- "Write copy to promote this tool on Twitter and Xiaohongshu"
- "Create launch posts for all platforms"
- "帮我写社交媒体推广文案"
