# Installation Guide

## Prerequisites

- Python 3.11 or higher
- [uv](https://docs.astral.sh/uv/) (recommended) or pip
- Claude Desktop (for Claude integration)

---

## Option 1 — Install from GitHub (easiest)

```bash
uv tool install git+https://github.com/genoshide/wallet-mcp.git
```

Verify:
```bash
wallet-mcp --help
```

---

## Option 2 — Local Development Install

```bash
git clone https://github.com/genoshide/wallet-mcp
cd wallet-mcp

# Create environment and install deps
uv sync

# Run directly
uv run wallet-mcp
```

---

## Option 3 — pip install

```bash
pip install git+https://github.com/genoshide/wallet-mcp.git
```

---

## Configure Claude Desktop

### Step 1 — Find your config file

| Platform | Path |
|---|---|
| macOS | `~/Library/Application Support/Claude/claude_desktop_config.json` |
| Windows | `%APPDATA%\Claude\claude_desktop_config.json` |
| Linux | `~/.config/Claude/claude_desktop_config.json` |

### Step 2 — Add wallet-mcp to mcpServers

**If installed via `uv tool install`:**
```json
{
  "mcpServers": {
    "wallet-mcp": {
      "command": "wallet-mcp"
    }
  }
}
```

**If installed from local clone:**
```json
{
  "mcpServers": {
    "wallet-mcp": {
      "command": "uv",
      "args": ["--directory", "/absolute/path/to/wallet-mcp", "run", "wallet-mcp"]
    }
  }
}
```

**If using pip:**
```json
{
  "mcpServers": {
    "wallet-mcp": {
      "command": "python",
      "args": ["-m", "wallet_mcp.server"]
    }
  }
}
```

### Step 3 — Restart Claude Desktop

Close and reopen Claude Desktop. You should see **wallet-mcp** in the tools panel.

### Step 4 — Verify

Ask Claude: _"Use wallet-mcp to show me all wallet groups"_

---

## Configure Claude Code (CLI)

Add to your `~/.claude/settings.json`:

```json
{
  "mcpServers": {
    "wallet-mcp": {
      "command": "wallet-mcp"
    }
  }
}
```

Or run inline:
```bash
claude mcp add wallet-mcp -- wallet-mcp
```

---

## VPS Setup (Ubuntu/Debian)

```bash
# 1. Install Python 3.11+ and uv
sudo apt update && sudo apt install -y python3.11 python3.11-venv curl
curl -LsSf https://astral.sh/uv/install.sh | sh
source ~/.bashrc

# 2. Install wallet-mcp
uv tool install git+https://github.com/genoshide/wallet-mcp.git

# 3. Configure env
cp ~/.local/share/uv/tools/wallet-mcp/.env.example ~/.wallet-mcp/.env
nano ~/.wallet-mcp/.env   # set your RPC URLs

# 4. Secure storage
chmod 700 ~/.wallet-mcp
chmod 600 ~/.wallet-mcp/wallets.csv 2>/dev/null || true

# 5. Test
wallet-mcp &   # run in background (stdio mode won't output unless connected to MCP client)
```

---

## Environment Variables

Set in `.env` (loaded automatically) or export before running:

```bash
export SOLANA_RPC_URL=https://your-rpc.helius-rpc.com/?api-key=xxx
export EVM_RPC_URL=https://mainnet.infura.io/v3/your_key
export WALLET_DATA_DIR=/secure/path
export LOG_LEVEL=DEBUG
```

---

## Troubleshooting

**"command not found: wallet-mcp"**
```bash
# Add uv tool bin to PATH
export PATH="$HOME/.local/bin:$PATH"
```

**"Cannot connect to RPC"**
→ Set a custom RPC URL via env var or the `rpc` parameter on each tool call.

**"No wallets found"**
→ Run `group_summary` to see what labels exist. Labels are case-insensitive.

**Log file location:** `~/.wallet-mcp/wallet-mcp.log`
