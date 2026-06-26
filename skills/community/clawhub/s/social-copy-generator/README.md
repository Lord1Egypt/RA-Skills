# social-copy-generator

Generate platform-optimized social media copy for product launches. One input, six platform outputs 

## 安装

```bash
npx skills add dongsheng123132/social-copy-generator
```

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
| Twitter/X | Concise, technical, hashtags | 280 chars |
| Jike (即刻) | Developer community, dry content | No limit |
| Xiaohongshu (小红书) | Casual, emoji-rich, comparison-heavy | No limit |
| WeChat Moments (朋友圈) | Personal, conversational | No limit |
| Video Account (视频号) | Title + description for video | Title < 30 chars |
| LinkedIn | Professional, achievement-focused | No limit |

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
- Under 280 chars (CJK = 2 chars each)
- Lead with product name
- Use ✓ for feature bullets
- End with install command + hashtags
- Optional: thread for details

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

## Example prompts
- "Generate social media posts for my new project"
- "Write copy to promote this tool on Twitter and Xiaohongshu"
- "Create launch posts for all platforms"
- "帮我写社交媒体推广文案"

## License

MIT

## 📱 关注作者

如果这个项目对你有帮助，欢迎关注我获取更多技术分享：

- **X (Twitter)**: [@vista8](https://x.com/vista8)
- **微信公众号「向阳乔木推荐看」**:

<p align="center">
  <img src="https://github.com/joeseesun/terminal-boost/raw/main/assets/wechat-qr.jpg?raw=true" alt="向阳乔木推荐看公众号二维码" width="300">
</p>
