# X Profile Deep Dive

Deep profile analysis for X/Twitter accounts using OpenClaw.

## Features

- 📊 **Data Collection**: Fetch tweets, followings, and followers via tweety-ns
- 🏷️ **AI Classification**: LLM-powered thematic categorization of tweets
- 📝 **Comprehensive Dossier**: Generate detailed Chinese-language profile reports
- 🔍 **Network Analysis**: Map user's social connections and influence
- 💡 **Content Insights**: Identify key themes and posting patterns

## Prerequisites

- OpenClaw agent environment
- Python 3.8+
- tweety-ns library (`pip3 install tweety-ns`)
- Twitter/X cookies for authentication

## Installation

### Via ClawHub (Recommended)

```bash
clawhub install x-profile-deep-dive
```

### Manual Installation

1. Clone to `~/.openclaw/skills/x-profile-deep-dive`
2. Install dependencies:
   ```bash
   pip3 install tweety-ns
   ```
3. Set up Twitter cookies at `<WORKSPACE>/config/twitter_cookies.json`

## Usage

Talk to your OpenClaw agent:

```
深挖 @elonmusk
Analyze Twitter profile @paulg
生成 @sama 的画像报告
```

The skill will:
1. Collect recent tweets and network data
2. Classify content by themes
3. Generate a comprehensive Chinese report with relevance scoring

## Configuration

Set environment variables for custom paths:

- `TWITTER_COOKIES_PATH`: Path to Twitter cookies JSON file
- `TWITTER_SESSION_DIR`: Directory for tweety session data

## License

MIT License - see [LICENSE](LICENSE) file
