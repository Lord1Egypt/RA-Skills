English | [中文](./README.md)

# web-to-FIM

> Convert any web link or local file into structured Markdown, and store it in three destinations: Obsidian Vault, Feishu Cloud Docs, and Tencent IMA Knowledge Base.

## Core Features

### Supported Sources (7 URL Types + Local Files)

| Source | URL Pattern | Fetch Method |
|--------|------------|-------------|
| X/Twitter | `x.com` / `twitter.com` | x-tweet-fetcher (verbatim transcript) |
| WeChat Article | `mp.weixin.qq.com` | markitdown + mobile UA fallback |
| Feishu Wiki | `*.feishu.cn/wiki/` | WebFetch full transcript |
| Xiaohongshu | `xiaohongshu.com` / `xhslink.com` | markitdown |
| Weibo | `weibo.com` | markitdown |
| YouTube | `youtube.com` / `youtu.be` | markitdown |
| Any Webpage | other `http(s)://` URLs | markitdown |

Local file support: PDF, Word, PPT, Excel, images, audio, CSV/JSON/XML, etc.

### Three Destinations

| Destination | Environment Variable | Description |
|-------------|---------------------|-------------|
| Obsidian Vault | `OBSIDIAN_VAULT_PATH` | Local Markdown + frontmatter + tags |
| Feishu Cloud Docs | `FEISHU_APP_ID` + `FEISHU_APP_SECRET` | Cloud team collaboration |
| Tencent IMA | `IMA_OPENAPI_CLIENTID` + `IMA_OPENAPI_APIKEY` | AI-native knowledge base (FIM) |

## Quick Start

```bash
# Install dependencies
pip install markitdown requests python-dotenv

# Convert and save to all three destinations
python3 scripts/web_to_all.py --url "<url_or_path>"

# Convert with custom title
python3 scripts/web_to_all.py --url "<url>" --title "Custom Title"

# Save to Obsidian only
python3 scripts/web_to_all.py --url "<url>" --no-feishu --no-ima
```

## Environment Variables

```bash
# Obsidian Vault path (optional, has default)
export OBSIDIAN_VAULT_PATH=~/Obsidian-Vault/00-Inbox

# Feishu credentials
export FEISHU_APP_ID="your_app_id"
export FEISHU_APP_SECRET="your_app_secret"

# IMA credentials (v3.0 - OpenAPI v1.1.7)
export IMA_OPENAPI_CLIENTID="your_client_id"
export IMA_OPENAPI_APIKEY="your_api_key"

# Optional: IMA knowledge base name (default: FIM知识库)
export IMA_KB_NAME="FIM知识库"
```

> Credentials must be configured via environment variables, never hardcoded. Legacy variable names `IMA_CLIENT_ID` / `IMA_API_KEY` are still supported as fallback.

## Usage Examples

```bash
# X/Twitter tweet
python3 scripts/web_to_all.py --url "https://x.com/user/status/123"

# WeChat article
python3 scripts/web_to_all.py --url "https://mp.weixin.qq.com/s/xxxxx"

# Feishu wiki
python3 scripts/web_to_all.py --url "https://xxx.feishu.cn/wiki/xxxxx"

# Local PDF file
python3 scripts/web_to_all.py --url "C:\docs\report.pdf"

# Only convert to Markdown, no storage
python3 scripts/web_to_md.py --url "<url>" --output output.md
```

## Trigger Words

转文档、抓网页存飞书、网页转文档、web to feishu、url转文档、文件转飞书、存到ima、存到obsidian、web to fim、三处存放。

Triggered when the user provides any URL or local file and requests conversion to a document.

## Verify Connections

```bash
# Verify Feishu connection
python scripts/feishu_client.py --action test

# Verify IMA connection
python scripts/ima_client.py --action test
```

## IMA Smart Routing (v3.0)

| source_url Type | IMA Storage Method | Reason |
|----------------|-------------------|--------|
| WeChat / General webpage | `import_urls` (server-side fetch) | Preserve images and layout |
| X/Twitter | Plain text note (verbatim transcript) | Skill rule requires verbatim |
| Feishu wiki | Plain text note (verbatim transcript) | Requires login, IMA cannot fetch |

## Version History

- **v3.1.0**: Batch mode checkpoint recovery; Obsidian frontmatter auto tags; generalized tweet structured conversion; subprocess 120s timeout; improved WeChat content extraction
- **v3.0.0**: IMA switched to knowledge base two-step flow; WeChat/webpage with images (import_urls); added Feishu wiki source; WeChat anti-scraping fallback
- **v2.x**: Basic three-destination storage; X/Twitter verbatim transcript; Feishu Cloud Docs integration

See [CHANGELOG.md](./CHANGELOG.md) for details.

## License

MIT-0 (c) 2026 EdwardWason
