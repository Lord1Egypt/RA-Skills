# RSS to WeChat

English | [中文](README.md)

OpenClaw skill for converting RSS articles to WeChat Official Account format.

## Features

- ✅ Parse RSS feeds and web articles
- ✅ Generate WeChat-compatible HTML
- ✅ Configurable branding and styling
- ✅ Optional cover image generation
- ✅ Optional automated publishing

## Installation

### Method 1: Install via ClawHub (Recommended)

```bash
# Install
clawhub install rss-to-wechat

# Configure
cd rss-to-wechat
cp references/config.example.sh config.local.sh
nano config.local.sh  # Edit configuration
```

### Method 2: Manual Installation

```bash
# Clone repository
git clone https://github.com/huangbaixun/rss-to-wechat.git
cd rss-to-wechat

# Configure
cp references/config.example.sh config.local.sh
nano config.local.sh  # Edit configuration
```
nano config.local.sh  # Edit configuration
```

Once installed, OpenClaw will automatically recognize this skill. When you mention keywords like "RSS to WeChat", "publish to Official Account", etc., the AI assistant will automatically load this skill.

### Method 2: Standalone Usage

You can also use it independently in any directory:

```bash
# Clone to any directory
git clone https://github.com/huangbaixun/rss-to-wechat.git
cd rss-to-wechat

# Configure and use (same as above)
```

## Quick Start

### 1. Configuration

```bash
# Copy example config
cp references/config.example.sh config.local.sh

# Edit configuration
nano config.local.sh
```

Minimum required config:

```bash
# WeChat Official Account credentials (required)
WECHAT_APPID="your_appid"
WECHAT_APPSECRET="your_secret"

# Branding
BRAND_NAME="Your Brand"
BRAND_SLOGAN="Your Slogan"
```

### 2. Check Setup

```bash
bash scripts/rss-to-wechat.sh --check
```

### 3. Usage

```bash
# Process a specific article
bash scripts/rss-to-wechat.sh --url "https://example.com/article"

# Auto-select latest article (requires blogwatcher)
bash scripts/rss-to-wechat.sh --auto
```

## Workflow

1. **Data Preparation** (automatic)
   - Script fetches and parses article
   - Extracts title, author, content
   - Saves to JSON

2. **HTML Generation** (AI-assisted)
   - AI assistant generates WeChat-compatible HTML
   - Uses your brand configuration
   - Follows strict format requirements

3. **Cover Generation** (optional)
   - If `COVER_SKILL` configured
   - Generates 1283×383 cover image

4. **Publishing** (optional)
   - If WeChat credentials configured
   - Uploads to draft box via API

## WeChat HTML Requirements

WeChat API has strict HTML format requirements:

**Must use:**
- `<section>` and `<p>` tags (not `<div>`)
- Inline styles `style="..."`
- `<strong>` and `<em>` tags
- Complete URLs (no relative links)

**Must not use:**
- `class` or `id` attributes
- External CSS
- JavaScript
- Relative links

See `references/html-template.md` for complete template and examples.

## Documentation

- **[SKILL.md](SKILL.md)** - Main skill documentation
- **[User Guide](references/USER_GUIDE.md)** - Complete usage guide
- **[HTML Template](references/html-template.md)** - WeChat HTML format reference
- **[Config Example](references/config.example.sh)** - Configuration options

## Requirements

**Required:**
- `curl` - HTTP requests
- `jq` - JSON processing
- `pandoc` - Format conversion

**Optional:**
- `blogwatcher` - RSS feed management (for --auto mode)
- Custom cover generation script
- Custom publishing script

## Structure

```
rss-to-wechat/
├── SKILL.md              # Main skill documentation
├── README.md             # English README (this file)
├── README.zh-CN.md       # Chinese README
├── scripts/              # Executable scripts
│   ├── rss-to-wechat.sh # Main entry point
│   ├── parse-article.sh # Article parser
│   └── config.sh        # Default configuration
├── references/           # Documentation
│   ├── USER_GUIDE.md    # Complete guide
│   ├── html-template.md # HTML format reference
│   └── config.example.sh# Configuration example
└── assets/              # Output resources (empty)
```

## Configuration Options

See `references/config.example.sh` for all available options:

- RSS sources and filters
- Brand customization (name, slogan, colors)
- Path configuration
- External tool integration
- Keyword filtering

## Troubleshooting

**Error 45166 (invalid content)**
- Check HTML format compliance
- Ensure all styles are inline
- Remove class/id attributes
- Reference successful examples

**Article parsing fails**
- Check URL accessibility
- Verify no anti-scraping measures
- Try manual content extraction

**Configuration issues**
- Run `bash scripts/rss-to-wechat.sh --check`
- Verify all required tools installed
- Check WeChat credentials

## OpenClaw Integration

### Skill Triggers

This skill automatically activates when you mention:

- "RSS to WeChat"
- "publish to Official Account"
- "WeChat format"
- "get article from RSS"
- "convert to WeChat"

### Usage Examples

In OpenClaw, you can simply say:

```
"Convert this article to WeChat format: https://example.com/article"

"Select the latest article from RSS and publish to Official Account"

"Generate a WeChat article from Simon Willison's blog"
```

The AI assistant will automatically:
1. Load this skill
2. Parse article content
3. Generate WeChat-compatible HTML
4. Create cover image
5. Upload to draft box

## License

MIT License - see [LICENSE](LICENSE)

## Contributing

Issues and pull requests welcome!

## Related

- [OpenClaw](https://openclaw.ai) - AI assistant framework
- [ClawHub](https://clawhub.com) - OpenClaw skill marketplace

## Author

Huang Baixun ([@huangbaixun](https://github.com/huangbaixun))

## Acknowledgments

Thanks to the OpenClaw community for support and feedback.
