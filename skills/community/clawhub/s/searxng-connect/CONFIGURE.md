# SearXNG Connect Skill - Configuration Guide

## 1. Configure Your SearXNG Instance

Edit `skill-config.json` and replace the default instance URL with your actual SearXNG URL:

```json
{
  "default_instance": "https://your-searxng-instance.com/",
  "cache_enabled": true,
  "cache_expiry": 3600,
  "rate_limit": 2.0
}
```

**Replace**: `https://your-searxng-instance.com/` → Your actual SearXNG URL

## 2. Test the Skill

```bash
cd ~/.openclaw/...../skills/searxng-connect
./execute.sh "test search"
```

## 3. Verify Installation

Run `openclaw doctor` and check for "Eligible: 16 skills" (or similar).

## 4. Use in OpenClaw

When you need web search, the skill will automatically be available.

### Usage Examples

- `Search the web` - General web search
- `Search news about X` - Filter by category
- `Search for Y with time range` - Add time filter
- `Search with language Z` - Specify language

## Default Settings

- **Cache**: Enabled (1 hour expiry)
- **Rate Limit**: 2 requests/second
- **Categories**: general, news, science, files, images, videos, music, social media, it
- **Language**: English (default)

## Privacy

This skill uses SearXNG, a privacy-respecting meta search engine. All searches go through your self-hosted instance - no tracking, no cookies, no ads.

## Troubleshooting

**SearXNG not working?**
- Check your SearXNG instance is running and accessible
- Verify the URL in `skill-config.json`
- Test with curl: `curl "https://your-searxng-instance.com/search?q=test"`

**Python not working?**
- Install Python 3.9+: `sudo apt-get install python3`
- Install requests: `pip install requests`

**Skill not detected?**
- Restart OpenClaw: `openclaw gateway restart`
- Run `openclaw doctor` to check for errors

---

**Author**: rdeangel
**Version**: 1.0.0
**Clawhub Package**: searxng-connect
