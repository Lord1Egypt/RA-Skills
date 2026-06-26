# TwitterShots Skill 1.0.0

An Agent Skill for generating high-quality screenshots of Twitter/X posts.

## Features

- Convert tweet links into beautiful PNG/SVG/HTML screenshots
- Support multiple aspect ratios (1:1, 4:5, 16:9, etc.) for different social platforms
- Toggle between light and dark themes
- Customize background, hide stats, and more styling options

## Install

First, get your API key from [TwitterShots Account Settings](https://twittershots.com/settings/keys), then follow the guide for your platform.

### Cursor

Skills live in `~/.cursor/skills/`. Clone this repo directly into that folder:

```bash
git clone https://github.com/twittershots/skills.git ~/.cursor/skills/twittershots
```

Then add your API key to `~/.cursor/mcp.json` or your shell profile:

```bash
export TWITTERSHOTS_API_KEY="your_api_key_here"
```

Cursor will auto-detect skills in that directory. The skill triggers automatically when you paste a tweet URL in the chat.

### Claude Code (claude.ai / Claude desktop)

Skills live in `~/.claude/skills/`. Clone this repo:

```bash
git clone https://github.com/twittershots/skills.git ~/.claude/skills/twittershots
```

Add your API key to your shell profile (`~/.zshrc` or `~/.bashrc`):

```bash
export TWITTERSHOTS_API_KEY="your_api_key_here"
source ~/.zshrc
```

Claude will read `SKILL.md` from the skills directory and invoke the skill when relevant.

### OpenClaw

Skills live in `~/.openclaw/skills/`. Clone this repo:

```bash
git clone https://github.com/twittershots/skills.git ~/.openclaw/skills/twittershots
```

Set the API key:

```bash
export TWITTERSHOTS_API_KEY="your_api_key_here"
```

OpenClaw will auto-discover skills in the `~/.openclaw/skills/` directory by reading their `SKILL.md` frontmatter.

### Manual / Other Agents

Clone anywhere and point your agent's skill path to the directory:

```bash
git clone https://github.com/twittershots/skills.git /path/to/your/skills/twittershots
export TWITTERSHOTS_API_KEY="your_api_key_here"
```

The only required file is `SKILL.md` — load it into your agent's context and it will know how to use the TwitterShots API.

### Verify Installation

Paste a tweet URL in chat to confirm everything works:

```
Screenshot this tweet: https://twitter.com/elonmusk/status/1617979122625712128
```

### CLI Usage

You can also run the bundled Python script directly without an agent:

```bash
export TWITTERSHOTS_API_KEY="your_api_key_here"
python scripts/screenshot_tweet.py 1617979122625712128 --theme dark
python scripts/screenshot_tweet.py https://x.com/user/status/1617979122625712128 --format png --aspect-ratio 4:5
```

## Usage

Simply paste a tweet URL or ID in AI chat, and the Agent will automatically invoke this Skill to generate a screenshot:

```
twittershots https://twitter.com/username/status/1617979122625712128
```

### Examples

You can also specify format, theme, or aspect ratio:

```
Screenshot this tweet in dark mode: https://x.com/user/status/1617979122625712128
```

```
Generate a 4:5 ratio PNG of tweet 1617979122625712128 for Instagram
```

## Project Structure

```
.
├── SKILL.md                    # Skill definition and API documentation
├── scripts/
│   └── screenshot_tweet.py     # Command-line tool
└── README.md                   # About this skill
```

## Get API Key

Get your API key from the [TwitterShots Account Settings](https://twittershots.com/settings/keys) page.

---

Built for AI Agent · Powered by [TwitterShots](https://twittershots.com)
