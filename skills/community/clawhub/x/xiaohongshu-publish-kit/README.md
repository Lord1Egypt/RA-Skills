# 小红书自动发布工具包 (Xiaohongshu Publish Kit)

Complete automation toolkit for publishing content to Xiaohongshu (小红书) via OpenClaw browser automation.

## 🚀 Quick Start

### 1. Installation
```bash
# Install via ClawHub
clawhub install xiaohongshu-publish-kit

# Or manual installation
git clone https://github.com/yourrepo/xiaohongshu-publish-kit
cp -r xiaohongshu-publish-kit ~/.openclaw/workspace/skills/
```

### 2. Setup Browser
```bash
# Start managed browser
browser --browser-profile openclaw start

# Login to Xiaohongshu (one-time setup)
browser --browser-profile openclaw navigate https://creator.xiaohongshu.com
# Scan QR code to login, session will persist
```

### 3. Publish Content
```bash
# Basic publishing
python3 scripts/publish.py \
  --title "Your Title (≤20 chars)" \
  --content "Your content (≤1000 chars)" \
  --image "/path/to/cover.jpg"

# AI daily news example
python3 examples/daily_news.py
```

## 📁 Structure

```
xiaohongshu-publish-kit/
├── SKILL.md              # Skill documentation
├── README.md             # This file
├── scripts/              # Core scripts
│   ├── publish.py        # Main publisher
│   └── cover_generator.py # Cover image generator
└── examples/             # Usage examples
    └── daily_news.py     # AI daily news publisher
```

## 🔧 Scripts

### `scripts/publish.py`
Main publishing script with full automation pipeline.

**Usage:**
```bash
python3 scripts/publish.py --title "标题" --content "内容" --image "图片路径"
```

### `scripts/cover_generator.py`
Generate tech-style cover images for posts.

**Usage:**
```bash
python3 scripts/cover_generator.py --title "AI热点" --date "2026.03.17" --style tech_blue
```

### `examples/daily_news.py`
Complete example for AI daily news publishing workflow.

**Usage:**
```bash
python3 examples/daily_news.py
```

## 📋 Platform Requirements

Xiaohongshu has strict content requirements:

- **Title**: Maximum 20 characters
- **Content**: Maximum 1000 characters  
- **Images**: 1-18 images, max 32MB each
- **Formats**: png/jpg/jpeg/webp (no gif)
- **Resolution**: ≥720x960, recommended 3:4 to 2:1 ratio

## 🛠️ Browser Automation Details

This toolkit uses OpenClaw browser automation with specific techniques:

### Tab Switching
```bash
# Must use JS evaluation, not direct click
browser --browser-profile openclaw evaluate --fn "() => {
  const tabs = document.querySelectorAll('.creator-tab');
  // Find and click image-text tab
}"
```

### Title Input
```bash
# Use native input setter for proper React state update
browser --browser-profile openclaw evaluate --fn "() => {
  const el = document.querySelector('input[placeholder*=\"标题\"]');
  const setter = Object.getOwnPropertyDescriptor(window.HTMLInputElement.prototype, 'value').set;
  setter.call(el, 'Title Text');
  el.dispatchEvent(new Event('input', {bubbles:true}));
}"
```

### Content Editor
```bash
# Rich text editor requires innerHTML + events
browser --browser-profile openclaw evaluate --fn "() => {
  const el = document.querySelector('.ql-editor, [contenteditable=true]');
  el.innerHTML = '<p>Content</p><p><br></p><p>#Tags</p>';
  el.dispatchEvent(new Event('input', {bubbles:true}));
}"
```

## 🎨 Cover Generation

The toolkit includes automatic cover generation with:

- **Tech Blue Style**: Blue-purple gradient for tech news
- **Security Red Style**: Red-black gradient for security topics
- **Custom HTML**: Fully customizable templates
- **Browser Rendering**: Uses OpenClaw browser for image capture

## 📱 Integration Examples

### Cron Job
```bash
# Add to crontab for daily publishing
0 9 * * * cd ~/.openclaw/workspace/skills/xiaohongshu-publish-kit && python3 examples/daily_news.py
```

### OpenClaw Skill Integration
```python
# In your OpenClaw skill
from xiaohongshu_publish_kit.scripts.publish import publish_to_xiaohongshu

def handle_publish_request(title, content, image_path):
    return publish_to_xiaohongshu(title, content, image_path)
```

## 🔍 Troubleshooting

### Publishing Failed
- Check title length (≤20 chars)
- Verify image format and size
- Ensure browser is logged in
- Check network connection

### Image Upload Failed
- Confirm image is in `/tmp/openclaw/uploads/`
- Check file format (png/jpg/jpeg/webp)
- Verify file size (<32MB)

### Browser Issues
- Restart browser: `browser --browser-profile openclaw restart`
- Re-login if session expired
- Check for popup dialogs blocking UI

## 📄 License

MIT License - Feel free to use, modify and distribute.

---

**Disclaimer**: This tool is for educational and legitimate use only. Please comply with Xiaohongshu platform rules and applicable laws.