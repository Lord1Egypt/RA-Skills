# openclaw-skill-x-twitter

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Node.js](https://img.shields.io/badge/Node.js-%3E%3D18-green.svg)](https://nodejs.org/)
[![X/Twitter](https://img.shields.io/badge/X%2FTwitter-API%20v2-blue.svg?logo=x)](https://developer.x.com/)
[![OpenClaw Skill](https://img.shields.io/badge/OpenClaw-Skill-orange.svg)](https://clawhub.ai)
[![ClawHub](https://img.shields.io/badge/ClawHub-x--twitter--by--altf1be-orange)](https://clawhub.ai/skills/x-twitter-by-altf1be)
[![GitHub last commit](https://img.shields.io/github/last-commit/ALT-F1-OpenClaw/openclaw-skill-x-twitter)](https://github.com/ALT-F1-OpenClaw/openclaw-skill-x-twitter/commits/main)
[![GitHub issues](https://img.shields.io/github/issues/ALT-F1-OpenClaw/openclaw-skill-x-twitter)](https://github.com/ALT-F1-OpenClaw/openclaw-skill-x-twitter/issues)
[![GitHub stars](https://img.shields.io/github/stars/ALT-F1-OpenClaw/openclaw-skill-x-twitter)](https://github.com/ALT-F1-OpenClaw/openclaw-skill-x-twitter/stargazers)

OpenClaw skill for X/Twitter — post tweets, threads, and media via X API v2.

By [Abdelkrim BOUJRAF](https://www.alt-f1.be) / ALT-F1 SRL, Brussels 🇧🇪 🇲🇦

## Table of Contents

- [Features](#features)
- [Quick Start](#quick-start)
- [Setup](#setup)
- [Commands](#commands)
- [Security](#security)
- [ClawHub](#clawhub)
- [License](#license)
- [Author](#author)
- [Contributing](#contributing)

## Features

- **Post tweets** — text with optional image attachment
- **Post threads** — multi-tweet threads from inline args or file
- **Reply to tweets** — respond to specific tweets
- **Verify connection** — check API credentials and account info

## Quick Start

```bash
# 1. Clone
git clone https://github.com/ALT-F1-OpenClaw/openclaw-skill-x-twitter.git
cd openclaw-skill-x-twitter

# 2. Install
npm install

# 3. Configure
cp .env.example .env
# Edit .env with your X API credentials

# 4. Use
node scripts/xpost.mjs verify
node scripts/xpost.mjs tweet "Hello world!"
```

## Setup

### Prerequisites

- Node.js 18+
- X/Twitter developer account with Free tier (or higher)
- API keys (Bearer Token, Consumer Key/Secret, Access Token/Secret)

## Commands

```bash
# Post a tweet
node scripts/xpost.mjs tweet "Hello world!"

# Post with image
node scripts/xpost.mjs tweet "Check this out" --media ./image.png

# Reply to a tweet
node scripts/xpost.mjs tweet "Great post!" --reply 1234567890

# Post a thread (inline)
node scripts/xpost.mjs thread "Tweet 1" "Tweet 2" "Tweet 3"

# Post a thread (from file, separated by ---)
node scripts/xpost.mjs thread --file ./my-thread.md

# Verify connection
node scripts/xpost.mjs verify
```

See [SKILL.md](./SKILL.md) for full command reference.

### Usage with OpenClaw

Once installed as a skill, use natural language:

> "Tweet: Just shipped a new feature! 🚀"

> "Post this thread about our SharePoint integration"

> "Reply to that tweet saying thanks"

## Security

- API keys stored in `.env` file (never committed)
- No secrets or tokens printed to stdout
- OAuth 1.0a user context for tweet operations

## ClawHub

Published as: `x-twitter-by-altf1be`

```bash
clawhub install x-twitter-by-altf1be
```

## License

MIT — see [LICENSE](./LICENSE)

## Author

Abdelkrim BOUJRAF — [ALT-F1 SRL](https://www.alt-f1.be), Brussels 🇧🇪 🇲🇦
- GitHub: [@abdelkrim](https://github.com/abdelkrim)
- X: [@altf1be](https://x.com/altf1be)

## Contributing

Contributions welcome! Please open an issue or PR.
