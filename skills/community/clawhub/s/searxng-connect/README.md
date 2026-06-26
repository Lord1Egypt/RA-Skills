# SearXNG Connect Skill

A comprehensive SearXNG API wrapper for OpenClaw.

## Features

- ✅ **Privacy-focused**: All searches go through your SearXNG instance
- ✅ **Rate limiting**: Automatic throttling to avoid overwhelming your SearXNG instance
- ✅ **Caching**: Local cache for frequently searched terms (1 hour expiry)
- ✅ **Error handling**: Graceful fallbacks and detailed error messages
- ✅ **Multiple categories**: general, news, science, files, images, videos, music, social media, it
- ✅ **Time filters**: year, month, week, day, hour, 24h, 7d, 30d
- ✅ **Language support**: Multiple language support (default: en)
- ✅ **Safe search**: Enable/disable safe search filtering
- ✅ **Python-based**: Uses requests library for robust HTTP handling

## Installation

The skill auto-installs dependencies:

```bash
cd ~/.openclaw/...../skills/searxng-connect
./execute.sh "test query"
```

This will:
1. Check for Python 3.9+
2. Install `requests` library if needed
3. Create cache directory if it doesn't exist

## Configuration

Edit `skill-config.json` to customize your SearXNG instance:

```json
{
  "default_instance": "https://your-searxng-instance.com/",
  "cache_enabled": true,
  "cache_expiry": 3600,
  "rate_limit": 2.0
}
```

**Important**: Replace `https://your-searxng-instance.com/` with your actual SearXNG instance URL.

## Usage

### Manual Testing

```bash
# Basic search
./execute.sh "TypeScript tutorials"

# Search with category
./execute.sh "Space Invaders" --categories images

# Search with time range
./execute.sh "latest AI news" --time-range month

# Specific language
./execute.sh "python programming" --language fr

# Page 2 results
./execute.sh "search query" --pageno 2

# Disable safe search
./execute.sh "adult content" --no-safesearch
```

### Return Format

The script returns JSON:

```json
{
  "results": [
    {
      "title": "Example Result",
      "url": "https://example.com",
      "snippet": "Brief description...",
      "content": "Full content (max 5000 chars)...",
      "img_url": "https://example.com/image.jpg",
      "engine": "duckduckgo",
      "score": 0.95
    }
  ],
  "metadata": {
    "from_cache": false,
    "query": "search query",
    "count": 10,
    "categories": ["general"],
    "time_range": "month"
  },
  "status": "success"
}
```

### Error Response

```json
{
  "error": "Error message here",
  "status": "error"
}
```

## Categories

- `general`: General web search (default)
- `news`: News articles
- `science`: Scientific content
- `files`: File search
- `images`: Images
- `videos`: Videos
- `music`: Music
- `social media`: Social media content
- `it`: IT and technology

## Time Ranges

- `year`: Last year
- `month`: Last month
- `week`: Last week
- `day`: Last 24 hours
- `hour`: Last hour
- `24h`: Last 24 hours
- `7d`: Last 7 days
- `30d`: Last 30 days

## Architecture

### Files

- `SKILL.md`: Skill documentation
- `execute.sh`: Bash wrapper for OpenClaw invocation
- `searxng.py`: Python API client
- `skill-config.json`: Skill configuration
- `README.md`: This file

### Python Class: `SearXNGClient`

```python
client = SearXNGClient(base_url="https://your-searxng-instance.com/")
result = client.search(
    query="TypeScript",
    categories=["general"],
    time_range="month",
    language="en",
    safesearch=True,
    pageno=1
)
```

### Key Methods

- `search(query, categories, time_range, ...)`: Execute a search
- `_get_cache_key(query, **params)`: Generate cache key
- `_load_from_cache(cache_key)`: Load from cache
- `_save_to_cache(cache_key, results)`: Save to cache
- `_parse_html_response(html)`: Parse HTML responses

## Rate Limiting

The client enforces a rate limit of 2 requests per second by default. This helps:
- Avoid overwhelming your SearXNG instance
- Prevent rate limiting from SearXNG itself
- Ensure fair usage

You can adjust this in `skill-config.json`:

```json
{
  "rate_limit": 3.0
}
```

## Caching

Results are cached for 1 hour by default. Cache directory: `~/.openclaw/searxng-cache/`

Cache benefits:
- Faster repeated searches
- Reduced API calls to SearXNG
- Offline fallback for recent queries

## Error Handling

The script handles various error conditions:

- **Network errors**: Timeout, connection failures
- **API errors**: Invalid queries, rate limiting
- **Python errors**: Missing dependencies
- **Cache errors**: File I/O failures

All errors return structured JSON with `error` and `status` fields.

## Security Considerations

1. **No tracking**: SearXNG does not track user behavior
2. **No cookies**: No cookies stored by the client
3. **Configurable**: You control which instance is used
4. **Rate limiting**: Prevents abuse of your SearXNG instance

## Troubleshooting

### "requests library not installed"
```bash
pip install requests
```

### SearXNG connection timeout
- Check your SearXNG instance is running
- Verify network connectivity
- Increase timeout in `searxng.py` (default: 10s)

### Cache not working
- Check permissions on `~/.openclaw/searxng-cache/`
- Delete cache: `rm -rf ~/.openclaw/searxng-cache/*`

### Python version too old
- Install Python 3.9+: `sudo apt-get install python3.9`

## Testing

Test the skill:

```bash
# Run a basic search
./execute.sh "OpenClaw SearXNG"

# Test with different parameters
./execute.sh "TypeScript" --categories general --time_range week

# Test error handling (empty query)
./execute.sh ""

# Test JSON output (no args - shows help)
./execute.sh
```

## License

MIT License - feel free to use and modify as needed.

---

**Version**: 1.0.0
**Author**: rdeangel
**Last Updated**: 2026-03-05
