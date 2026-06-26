# Unsplash Skill for Claude Code

A Claude Code skill for searching and fetching high-quality photos from Unsplash with automatic attribution.

## Features

- **Search photos** by keyword with advanced filters (orientation, color, sorting)
- **Random photos** for variety and inspiration
- **Download tracking** as required by Unsplash API guidelines
- **Automatic attribution** in both plain text and HTML formats
- **No Python dependencies** - Pure shell scripts using curl and jq
- **Self-contained** - All code in the skill directory

## Quick Start

### 1. Installation

```bash
./install.sh
```

This installs the skill to `~/.claude/skills/unsplash/`.

Or manually:
```bash
mkdir -p ~/.claude/skills/unsplash
cp -r * ~/.claude/skills/unsplash/
chmod +x ~/.claude/skills/unsplash/scripts/*.sh
```

### 2. Set API Key

Get your free API key from [Unsplash Developers](https://unsplash.com/developers).

Create a `.env` file in your project root:

```
UNSPLASH_ACCESS_KEY=your_access_key_here
```

The skill automatically loads `.env` from your project root.

### 3. Test It

```bash
cd ~/.claude/skills/unsplash
./scripts/search.sh "sunset"
```

You should see JSON output with photo data and attribution.

## Usage

### Search Photos

```bash
./scripts/search.sh "mountain landscape"
```

With filters:
```bash
./scripts/search.sh "sunset" 1 5 latest landscape
```

Parameters: `query [page] [per_page] [order_by] [orientation] [color]`

### Random Photos

```bash
./scripts/random.sh "nature" 3
```

Parameters: `[query] [count] [orientation]`

### Track Downloads

```bash
./scripts/track.sh PHOTO_ID
```

Call this when users actually download an image (required by Unsplash).

## In Claude Code

Once installed and configured, Claude will automatically use this skill when you request photos:

```
User: Find me some landscape photos of mountains
Claude: [Uses /unsplash skill to search and returns results with attribution]

User: Get 5 random nature photos
Claude: [Uses /unsplash skill to fetch random photos]
```

You can also invoke it explicitly:
```
/unsplash search mountain landscape
/unsplash random nature 5
```

## Attribution Requirements

**CRITICAL:** All Unsplash images require attribution. The skill automatically includes:

- `attribution_text`: Plain text attribution
- `attribution_html`: HTML formatted attribution with links

Always include one of these when displaying images. Example:

```html
<img src="photo_url">
<p>Photo by <a href="...">Photographer Name</a> on <a href="...">Unsplash</a></p>
```

## Dependencies

Required tools (standard on macOS/Linux):
- `bash` - Shell interpreter
- `curl` - HTTP client (pre-installed on macOS/Linux)
- `jq` - JSON processor

Install jq if missing:
```bash
# macOS
brew install jq

# Ubuntu/Debian
sudo apt-get install jq

# Other systems
# See: https://stedolan.github.io/jq/download/
```

## Rate Limits

- **Demo mode**: 50 requests/hour
- **Production mode**: 5,000 requests/hour (requires app approval from Unsplash)

## Project Structure

```
unsplash-skill/
├── SKILL.md                    # Main skill definition (used by Claude)
├── README.md                   # This file
├── install.sh                  # Installation script
├── .env.example                # API key template
├── .gitignore                  # Git ignore file
├── scripts/
│   ├── lib/
│   │   └── common.sh          # Shared functions
│   ├── search.sh              # Search photos
│   ├── random.sh              # Random photos
│   └── track.sh               # Track downloads
└── examples/
    └── usage-examples.md      # Detailed usage patterns
```

## Documentation

- **SKILL.md** - Complete skill documentation for Claude
- **examples/usage-examples.md** - Detailed usage examples and workflows
- **Unsplash API Docs** - https://unsplash.com/documentation
- **API Guidelines** - https://help.unsplash.com/en/articles/2511245-unsplash-api-guidelines

## Examples

### Basic Search
```bash
./scripts/search.sh "coffee"
```

### Landscape Photos Only
```bash
./scripts/search.sh "nature" 1 10 relevant landscape
```

### Blue-toned Images
```bash
./scripts/search.sh "abstract" 1 5 relevant "" blue
```

### Random Travel Photos
```bash
./scripts/random.sh "travel" 5 landscape
```

### Complete Workflow
```bash
# Search
photos=$(./scripts/search.sh "workspace" 1 5)

# Get first photo details
photo=$(echo "$photos" | jq -c '.[0]')
photo_id=$(echo "$photo" | jq -r '.id')
photo_url=$(echo "$photo" | jq -r '.urls.regular')
attribution=$(echo "$photo" | jq -r '.attribution_html')

# Display image with attribution
echo "Image: $photo_url"
echo "Credit: $attribution"

# Track download if user downloads
./scripts/track.sh "$photo_id"
```

See [examples/usage-examples.md](examples/usage-examples.md) for more detailed examples.

## Troubleshooting

### "ERROR: UNSPLASH_ACCESS_KEY not set"

You haven't set the API key. Run:
```bash
export UNSPLASH_ACCESS_KEY="your_key_here"
```

Add it to `~/.zshrc` or `~/.bash_profile` to persist.

### "jq: command not found"

Install jq:
```bash
brew install jq  # macOS
sudo apt-get install jq  # Ubuntu/Debian
```

### "ERROR: Rate limit exceeded"

You've hit the 50 requests/hour limit with demo credentials. Either:
1. Wait an hour
2. Get your own API key for 5,000 requests/hour

### "ERROR: Invalid API key"

Your API key is incorrect. Double-check:
1. You copied the full key from Unsplash
2. There are no extra spaces or quotes
3. The key is active (not revoked)

### Scripts not executable

```bash
chmod +x scripts/*.sh
```

## Development

### Testing

Set your API key:
```bash
export UNSPLASH_ACCESS_KEY="your_key_here"
```

Run tests:
```bash
# Test search
./scripts/search.sh "test" 1 1

# Test random
./scripts/random.sh "nature" 1

# Test error handling
unset UNSPLASH_ACCESS_KEY
./scripts/search.sh "test"  # Should show error
```

### Contributing

This skill follows Claude Code skill best practices:
- Shell-based for portability
- Minimal dependencies (curl + jq)
- Clear error messages
- Comprehensive documentation
- Proper attribution handling

## License

MIT License - See individual file headers for details.

## Credits

- Photos provided by [Unsplash](https://unsplash.com)
- Built for [Claude Code](https://claude.ai/code)

## Links

- [Unsplash API](https://unsplash.com/developers)
- [Unsplash Guidelines](https://help.unsplash.com/en/articles/2511245-unsplash-api-guidelines)
- [Claude Code Documentation](https://docs.anthropic.com/claude/docs)
