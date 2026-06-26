# Claude Code Hooks for stealth-browser

These hooks make stealth-browser the automatic fallback when WebFetch gets blocked. The system learns which domains block and skips WebFetch entirely on future requests.

## Setup

### 1. Copy hooks to your hooks directory

```bash
cp hooks/webfetch-preflight.sh ~/.claude/hooks/
cp hooks/webfetch-fallback.sh ~/.claude/hooks/
chmod +x ~/.claude/hooks/webfetch-preflight.sh ~/.claude/hooks/webfetch-fallback.sh
```

### 2. Add to ~/.claude/settings.json

```json
{
  "hooks": {
    "PreToolUse": [
      {
        "matcher": "WebFetch",
        "hooks": [
          {
            "type": "command",
            "command": "bash ~/.claude/hooks/webfetch-preflight.sh"
          }
        ]
      }
    ],
    "PostToolUse": [
      {
        "matcher": "WebFetch",
        "hooks": [
          {
            "type": "command",
            "command": "bash ~/.claude/hooks/webfetch-fallback.sh"
          }
        ]
      }
    ]
  }
}
```

### 3. Add to ~/.claude/CLAUDE.md

The PostToolUse hook can only catch soft blocks (HTTP 200 with challenge page content). Hard failures (403, 429, timeout) skip PostToolUse entirely. Add this rule to handle those:

```markdown
## WebFetch Fallback

When WebFetch fails with 403, 429, blocked, timeout, forbidden, access denied, or returns a
Cloudflare/bot challenge page:

1. **Add the domain to the blocklist** so future calls skip WebFetch entirely:
\`\`\`bash
echo "the-domain.com" >> ~/.claude/skills/stealth-browser/data/blocked-domains.txt
\`\`\`

2. **Retry with stealth-browser** immediately - do not ask the user:
\`\`\`bash
~/.claude/skills/stealth-browser/scripts/stealth-browser read <url>
\`\`\`
```

## How the Learning Works

```
First request to a blocked domain:
  WebFetch -> 403 error
  Claude sees error + CLAUDE.md rule
  -> Adds domain to blocklist
  -> Retries with stealth-browser

Soft block (200 + challenge page):
  WebFetch -> 200 OK (but Cloudflare challenge)
  PostToolUse hook detects challenge
  -> Adds domain to blocklist automatically
  -> Tells Claude to retry with stealth-browser

Every request after that:
  WebFetch -> PreToolUse hook checks blocklist
  -> Blocks the call immediately
  -> Claude uses stealth-browser directly (no wasted request)
```

## Blocklist

Learned domains are stored one per line in:
```
~/.claude/skills/stealth-browser/data/blocked-domains.txt
```

To manually add or remove domains, edit this file directly.
