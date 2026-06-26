# Xiaohongshu MCP Client
English | [简体中文](./README.zh-CN.md)

A Python client for Xiaohongshu MCP (Model Context Protocol) REST API, providing a comprehensive command-line interface for managing Xiaohongshu accounts and interacting with the platform.

## Features

- **Account Management**
  - Add, remove, list, and switch between multiple accounts
  - Import and export cookies
  - Track last used time and account notes
  - **Automatic username detection** - auto-detects current login nickname when username is not provided
  - **Current account management** - easily check and switch between accounts

- **Login Management**
  - Check login status
  - Get login QR code
  - Logout (clear cookies)

- **Content Publishing**
  - Publish image content with images and tags
  - Publish video content
  - Support for visibility settings

- **Feed Management**
  - List recommended feeds
  - Search feeds by keyword
  - Get detailed feed information

- **Interaction**
  - Post comments on feeds
  - Reply to comments on feeds

- **User Information**
  - Get current user profile
  - Get other user profiles

## Installation

### Prerequisites
- Python 3.12+
- Xiaohongshu MCP server running (default: `http://localhost:18060`)

### Install from source
```bash
cd xiaohongshu-aio
uv sync
uv run xhs --help
```

### Install from PyPI (Recommended)
```bash
uv tool install xiaohongshu-aio
```

### Install and Start MCP Server
1. Download MCP server: `xhs mcp download`
2. Start MCP server: `xhs mcp start`
3. Check status: `xhs mcp status`

## Usage

### Command Structure
```bash
xhs <command> [options]
```

### Account Management
```bash
# List all accounts
xhs account list

# Add a new account (auto-detects username from current login)
xhs account add

# Add a new account with custom username and notes
xhs account add --username myaccount --notes "My personal account"

# Remove an account
xhs account remove --username myaccount

# Switch to another account
xhs account switch --username myaccount

# Import cookies for an account (auto-detects username)
xhs account import

# Import cookies with custom username
xhs account import --username myaccount

# Get current account
xhs account current
```

### Login Management
```bash
# Check login status
xhs login status

# Check login status with custom server URL
xhs login status --base-url http://localhost:18060

# Get login QR code
xhs login qrcode

# Logout
xhs login logout
```

### Publishing Content
```bash
# Publish image content
xhs publish "Title" "Content" "https://example.com/image1.jpg" "https://example.com/image2.jpg" --tags food,travel

# Publish video content
xhs publish "Video Title" "Video content" "C:\path\to\video.mp4" --is-video

# Publish with custom server URL
xhs publish "Title" "Content" "https://example.com/image.jpg" --base-url http://localhost:18060
```

### Feed Management
```bash
# List feeds
xhs feed list

# Search feeds
xhs feed search --keyword "coffee"

# Get feed detail
xhs feed detail --feed-id "feed123" --xsec-token "token123"

# Use custom server URL
xhs feed list --base-url http://localhost:18060
```

### Interaction
```bash
# Post a comment
xhs interact comment "feed123" "token123" --content "Great post!"

# Reply to a comment
xhs interact reply "feed123" "token123" --comment-id "comment_id" --content "Reply content"

# Use custom server URL
xhs interact comment "feed123" "token123" --content "Great post!" --base-url http://localhost:18060
```

### User Information
```bash
# Get current user profile
xhs user me

# Get other user profile
xhs user profile --user-id "user123" --xsec-token "token123"

# Use custom server URL
xhs user me --base-url http://localhost:18060
```

### MCP Server Management
```bash
# Download MCP server
xhs mcp download

# Test MCP connection
xhs mcp test

# Start MCP server
xhs mcp start

# Stop MCP server
xhs mcp stop

# Restart MCP server
xhs mcp restart

# Check MCP server status
xhs mcp status
```

## Configuration

You can configure the client using environment variables:

| Environment Variable | Default Value | Description |
|---------------------|---------------|-------------|
| `XHS_MCP_BASE_URL`  | `http://localhost:18060` | MCP server base URL (preferred) |
| `XHS_BASE_URL`      | `http://localhost:18060` | MCP server base URL (fallback) |
| `XHS_TIMEOUT`       | `60` | HTTP request timeout in seconds |
| `XHS_VERIFY_SSL`    | `true` | Whether to verify SSL certificates |

## Project Structure

```
xiaohongshu-aio/
├── src/
│   └── xiaohongshu_aio/
│       ├── __init__.py          # Package initialization
│       ├── client.py            # REST API client
│       ├── account.py           # Account management
│       ├── cli.py               # Command-line interface
│       └── mcp_service.py       # MCP server management
├── pyproject.toml               # Project configuration
├── README.md                    # This file
├── README_en.md                 # English README
└── user_cookies.json            # Account cookies storage
```

## Dependencies

- `httpx` - Modern HTTP client
- `typer` - Command-line interface
- `pydantic` - Data validation
- `pydantic-settings` - Settings management
- `rich` - Rich console output

## Acknowledgments

This project is based on the [xiaohongshu-mcp](https://github.com/xpzouying/xiaohongshu-mcp) project. Thanks to the original project author for their contribution.

## License

MIT
