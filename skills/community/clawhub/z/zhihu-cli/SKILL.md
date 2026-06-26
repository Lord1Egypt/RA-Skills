---
name: zhihu-cli
description: Command-line tool for searching, reading, and interacting with Zhihu (知乎). Supports hot topics, content search, article reading, user info, and Browser Relay-based voting/following.
---

# Zhihu CLI

A CLI tool for interacting with Zhihu (知乎) content.

## Installation

```bash
# Install globally
npm install -g zhihu-cli

# Or use npx
npx zhihu-cli <command>
```

## Commands

| Command | Description |
|---------|-------------|
| `zhihu login` | Auto-extract cookies from Chrome |
| `zhihu whoami` | Check login status |
| `zhihu set-cookie <cookie>` | Set cookie manually |
| `zhihu hot` | Get hot topics |
| `zhihu search <keyword>` | Search content |
| `zhihu topics <keyword>` | Search topics |
| `zhihu read <url>` | Read answer/article |
| `zhihu user <token>` | Get user info by url_token |
| `zhihu vote <url>` | Browser Relay vote instructions |
| `zhihu follow [url]` | Browser Relay follow instructions |
| `zhihu post` | Browser Relay post instructions |

## Features

- 🔍 Search Zhihu content
- 🔥 Get hot topics
- 📖 Read answers/articles
- 👤 View user info
- 👍 Vote (via Browser Relay)
- 👣 Follow users (via Browser Relay)
- 🔐 Auto cookie extraction from Chrome

## Cookie Setup

### Option 1: Auto (recommended)
```bash
zhihu login
```
Opens Chrome and extracts cookies automatically.

### Option 2: Manual
```bash
zhihu set-cookie "your_zhihu_cookie_string"
```

## Browser Relay Operations

Some operations (vote, follow, post) require Browser Relay due to API limitations.

### Setup
1. Ensure OpenClaw Browser Relay is connected
2. Use the respective command to get instructions

### Voting
```bash
zhihu vote <answer_url>
```
Then click the vote button in browser or use JS:
```javascript
const btn = document.querySelector('button[class*="VoteButton"]');
if (btn) btn.click();
```

### Following
```bash
zhihu follow <user_url>
```
Or click the follow button in browser.

## API Limitations

Zhihu has restricted API access for:
- Vote/unvote (use Browser Relay)
- Follow/unfollow (use Browser Relay)
- Comments (partially available)

Read operations (search, hot, read, user) work via API.

## Examples

```bash
# Get hot topics
zhihu hot

# Search for Python tutorials
zhihu search Python教程

# Read an answer
zhihu read https://www.zhihu.com/question/123456/answer/789012

# Get user info
zhihu user lightislost

# Check login
zhihu whoami
```

## Notes

- Cookie is stored in `~/.zhihu-cookie`
- Some features require login (votes, follows)
- Browser Relay provides more reliable write operations
