---
name: social-post-generator
description: Take a blog post URL or text and generate social media posts from it. Use when repurposing content for Twitter, LinkedIn, or creating promotional posts.
metadata:
  {
    "openclaw":
      {
        "requires": { "bins": ["curl"] },
        "install": [],
      },
  }
---

# Social Post Generator

Transform blog posts and articles into social media content — tweets, LinkedIn posts, and viral hooks.

## Environment Variables

| Variable | Required | Default | Description |
|----------|----------|---------|-------------|
| `PLATFORM` | No | `twitter` | Target platform: `twitter` or `linkedin` |
| `TONE` | No | `professional` | Tone of voice: `professional`, `casual`, or `technical` |
| `BRAND_NAME` | No | — | Brand/person name for attribution |
| `HASHTAGS` | No | — | Comma-separated default hashtags |

## Scripts

### generate.sh — Generate Posts

Generates 5 social media posts from an article URL or text.

```bash
./scripts/generate.sh <url_or_text_file>
```

**Output:** 5 formatted posts ready to publish.

### thread.sh — Create Twitter Thread

Generates a thread of connected tweets from an article.

```bash
./scripts/thread.sh <url_or_text_file>
```

**Output:** Numbered thread tweets with proper formatting.

### hook.sh — Create Viral Hooks

Generates attention-grabbing opening hooks for social posts.

```bash
./scripts/hook.sh <url_or_text_file>
```

**Output:** 10 hook variations to test.

## Usage Example

```bash
export PLATFORM=twitter
export TONE=casual
export BRAND_NAME="MyBrand"

# Generate 5 tweets from an article
./scripts/generate.sh https://example.com/blog/post

# Create a thread
./scripts/thread.sh article.txt

# Get viral hooks
./scripts/hook.sh article.txt
```

## Notes

- Uses web_fetch to extract content from URLs
- Each platform has character limits (Twitter: 280, LinkedIn: 3000)
- Generates hashtag suggestions based on content
- Output is copy-paste ready with line breaks
- Add `--dry-run` to any script to preview without saving
