# Z.AI Web Search API - Quick Start

> For detailed configuration instructions, see [README.md](README.md)

## 30-Second Quick Setup

### 1. Get API Key

Visit [https://open.bigmodel.cn](https://open.bigmodel.cn) to register and get an API Key

### 2. Create Config File

```bash
# Enter skill folder
cd ~/.openclaw/skills/zai-web-search

# Copy example and edit
cp config.json.example config.json
```

**⚠️ Important**: `config.json.example` contains comments. Please remove all `//` comments after copying, otherwise it will error.

### 3. Fill in API Key

Open `config.json` and replace the `apiKey` field:

```json
{
  "apiKey": "paste your API Key here"
}
```

## Start Using

```bash
# Search
zai-search "Harbin Ice and Snow World 2026"

# More results
zai-search "React tutorial" --count 20

# Specify engine
zai-search "artificial intelligence" --engine search_pro
```

## Cheat Sheet

| Command | Description |
|---------|-------------|
| `-e, --engine` | Search engine: `search_std` / `search_pro` / `search_pro_sogou` / `search_pro_quark` |
| `-c, --count` | Result count: 1-50 |
| `-r, --recency` | Time filter: `oneDay` / `oneWeek` / `oneMonth` / `oneYear` / `noLimit` |
| `-s, --content` | Content length: `medium` / `high` |
| `-d, --domain` | Limit domain |
| `-i, --intent` | Enable intent recognition |
| `-j, --json` | JSON output |
| `-k, --compact` | Compact output |
| `-h, --help` | Help |

## Engine Selection

| Engine | Description |
|--------|-------------|
| `search_std` | Zhipu basic edition, fast |
| `search_pro` | Zhipu pro edition, best quality |
| `search_pro_sogou` | Sogou search |
| `search_pro_quark` | Quark search |

## Pricing Information

Official pricing: [https://open.bigmodel.cn/pricing](https://open.bigmodel.cn/pricing)
