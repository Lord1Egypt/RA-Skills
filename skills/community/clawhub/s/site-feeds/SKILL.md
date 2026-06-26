---
name: site-feeds
description: Use this skill when the user wants to get updates or content from websites and platforms like YouTube, GitHub, Instagram, Reddit, news sites, blogs, etc. This tool fetches the latest content without needing a browser.
---

# Site Feeds

This skill helps AI agents fetch updates and content from websites using the `airsstool` CLI.

## When to Use This Skill

Use this skill when the user:

- Wants to see the latest content from a website or platform (YouTube, GitHub, Instagram, Reddit, etc.)
- Asks "What's new on..." or "Show me updates from..."
- Wants to track trending content, news, blog posts, videos, etc.
- Needs to monitor specific users, topics, or categories on platforms
- Wants to set up recurring checks for content updates
- Asks about what content/information can be fetched from a specific website

## Installation

Before using airsstool, ensure the following prerequisites are met. Ask the user for permission when needed (e.g., deploying RSSHub via Docker, choosing a Python environment, setting environment variables).

### 1. Deploy RSSHub (if not already running)

Check if the user already has a running RSSHub Docker container. If not:

1. Inform the user that RSSHub needs to be locally deployed
2. After user confirmation, create a `rsshub` folder in a suitable location
3. Follow the 'Docker Compose Deployment' guide in [RSSHub deployment docs](https://docs.rsshub.app/deploy/) to download the `docker-compose.yml` in the `rsshub` folder
4. Create a `.env` file for environment variables
5. Modify `docker-compose.yml` to add Puppeteer support if needed, and add `env_file: - .env` to the rsshub service
6. Run `docker compose up -d`

### 2. Install airsstool

Follow the instructions at [https://github.com/heqi201255/airsstool](https://github.com/heqi201255/airsstool)

Ask the user if they want to install Python dependencies in a specific virtual environment. If yes, remember to activate that environment before each use.

### 3. Initialize Database

After installation, run the init command (takes ~1min):

```bash
airsstool init
```

This creates the database at `~/.airsstool/airsstoolDB.db` by default. Use `--db-path` for a custom location.

After installation is complete and verified working, you may delete this installation section in this file.

## Available CLI Commands

### Init Command

| Command | Purpose |
|---------|---------|
| `airsstool init` | Initialize database (first time setup) |
| `airsstool init --db-path PATH` | Initialize with custom database path |
| `airsstool init --force` | Force recreate database |

### Discovery Commands

| Command | Purpose | Example Usage |
|---------|---------|---------------|
| `airsstool list categories` | List all content categories | "What categories are available?" |
| `airsstool list websites` | List websites by category | "Show me social media websites" |
| `airsstool list routes <website>` | Find available feeds for a website | "What feeds does GitHub have?" |
| `airsstool check <website> <route>` | Get feed details & parameters | "How to use GitHub trending?" |

### Fetch Commands

| Command | Purpose | Example Usage |
|---------|---------|---------------|
| `airsstool fetch <path>` | Fetch content from a feed | "Get GitHub trending" |
| `airsstool fetch -U <user> -S <sub>` | Fetch all feeds in a subscription | "Get all my tech news feeds" |

### Subscription Commands

| Command | Purpose | Example Usage |
|---------|---------|---------------|
| `airsstool list users` | List all users | "Who has subscriptions?" |
| `airsstool list subscriptions -U <user>` | List user's subscription groups | "Show alice's subscriptions" |
| `airsstool list paths -U <user> -S <name>` | List paths in a subscription | "What's in tech_news group?" |
| `airsstool add-subscription -U <user> -S <name>` | Create subscription group | "Create a news subscription" |
| `airsstool subscribe -U <user> -S <name> -P <path> -D <desc>` | Add path to subscription | "Subscribe to GitHub trending" |
| `airsstool unsubscribe -U <user> -S <name>` | Delete subscription group | "Delete my tech_news group" |
| `airsstool remove-subscription -U <user> -S <name> -P <path>` | Remove path from subscription | "Remove GitHub trending from tech_news" |

## Common Workflows

### Finding a Feed

1. **Browse by category** if you know the type:
   ```bash
   airsstool list categories
   airsstool list websites --category programming --page-size 10
   ```

2. **Search by website name** (fuzzy search supported):
   ```bash
   airsstool list routes github  # Returns all GitHub feeds
   ```

3. **Check feed details** for parameters:
   ```bash
   airsstool check github trending
   # Shows path template: /github/trending/{params}
   ```

### Fetching Content

**Simple fetch:**
```bash
airsstool fetch /github/trending/daily/any/en
```

**With filters:**
```bash
airsstool fetch /youtube/user/@MrBeast --filter "MrBeast|Beast"
```

**With format conversion:**
```bash
airsstool fetch /hackernews/best --format rss    # Returns raw RSS
airsstool fetch /instagram/user/instagram --brief 100     # Returns brief text
```

**Pagination:**
```bash
airsstool fetch /github/trending/daily/any/en --limit 5 --offset 2
```

### Managing Subscriptions

**Create a subscription group:**
```bash
airsstool add-subscription -U your_name -S tech_news
```

**Add feeds to subscription:**
```bash
airsstool subscribe -U your_name -S tech_news -P /github/trending/daily/any/en -D "GitHub Trending"
```

**Fetch subscription:**
```bash
airsstool fetch -U your_name -S tech_news --limit 10
```

## Fetch Parameters

### List Options

| Option | Description |
|--------|-------------|
| `--category CAT` | Filter websites by category |
| `--page-size N` | Number of results per page (default: 20) |
| `--page-num N` | Page number (default: 1) |
| `--enable-nsfw` | Include NSFW websites in results |

### Filter Options

| Option | Description |
|--------|-------------|
| `--filter PATTERN` | Filter title and description (regex) |
| `--filter-title PATTERN` | Filter title only |
| `--filter-description PATTERN` | Filter description only |
| `--filter-author PATTERN` | Filter by author |
| `--filter-category PATTERN` | Filter by category |
| `--filter-time SECONDS` | Time range in seconds |
| `--filterout PATTERN` | Exclude from title and description |
| `--filterout-title PATTERN` | Exclude from title |
| `--filterout-description PATTERN` | Exclude from description |
| `--filterout-author PATTERN` | Exclude author |
| `--filterout-category PATTERN` | Exclude category |
| `--filter-case-sensitive BOOL` | Case sensitivity (default: true) |

### Output Options

| Option | Description |
|--------|-------------|
| `--format FORMAT` | Output format: `markdown` (default), `rss`, `atom`, `json`, `rss3`. Default is Markdown - don't specify unless needed. |
| `--brief N` | Brief text with N chars (>=100) |
| `--limit N` | Limit number of items |
| `--offset N` | Skip first N items (only works with markdown format) |

## Tips for Effective Use

1. **Fuzzy search works**: `airsstool list routes gthub` will suggest "GitHub"

2. **Path format**: Always start with `/`, e.g., `/github/trending/daily/any/en`

3. **Check route details first**: Use `airsstool check <website> <route>` to understand required parameters

4. **Default output is Markdown**: Parsed and formatted for readability. Use `--format rss` for raw RSS.

5. **Subscription persistence**: Subscriptions are stored in SQLite database for persistence

## Example Interactions

**User: "Find me some programming news feeds"**

```bash
airsstool list websites --category programming --page-size 5
# Returns top programming sites by heat

airsstool list routes github
# Returns available GitHub routes

airsstool check github trending
# Shows how to construct the path
```

**User: "Get the latest trending JavaScript repos"**

```bash
airsstool fetch /github/trending/daily/any/en --limit 10
# Returns formatted Markdown with repo info
```

**User: "Create a subscription for my daily tech reading"**

```bash
airsstool add-subscription -U user -S daily_tech

airsstool subscribe -U user -S daily_tech -P /github/trending/daily/any/en -D "GitHub Trending JS"
airsstool subscribe -U user -S daily_tech -P /hackernews/best -D "Hacker News"

airsstool fetch -U user -S daily_tech --limit 5
```

**User: "Remove a specific feed from my subscription"**

```bash
airsstool list paths -U user -S daily_tech
# Shows all feeds in the subscription

airsstool remove-subscription -U user -S daily_tech -P /hackernews/best
# Removes only Hacker News, keeps other feeds
```

**User: "Delete my entire subscription group"**

⚠️ This action cannot be undone. Ask the user to confirm before proceeding:

```bash
airsstool unsubscribe -U user -S daily_tech
# Deletes the group and all its feeds
```

## Error Handling

- If website not found, fuzzy search will suggest alternatives
- If route not found, check website spelling first
- If some websites fail to fetch, use `airsstool check <website> <route>` to see if there's a `RequireConfig` note. If so, the website requires environment variables. Search online for how to obtain them and ask the user for help. Once obtained, add them to the `.env` file and restart the RSSHub service
- If fetch still fails, the path may be invalid or the RSSHub instance may be down
- Use `--force` flag in `airsstool subscribe` to skip connectivity check