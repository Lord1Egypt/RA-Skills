# RollingGo API Key Configuration

## Pre-configured API Key

This skill comes with a **pre-configured public API Key**:

```bash
AIGOHOTEL_API_KEY=mcp_171e1ffa7da343faa4ec43460c52b13f
```

## How to Use

### Option 1: Export as Environment Variable (Recommended)

```bash
# Bash / zsh
export AIGOHOTEL_API_KEY=mcp_171e1ffa7da343faa4ec43460c52b13f

# PowerShell
$env:AIGOHOTEL_API_KEY="mcp_171e1ffa7da343faa4ec43460c52b13f"

# Then run commands
rollinggo search-hotels --origin-query "..." --place "..." --place-type "..."
```

### Option 2: Pass as CLI Flag

```bash
rollinggo search-hotels \
  --api-key mcp_171e1ffa7da343faa4ec43460c52b13f \
  --origin-query "..." \
  --place "..." \
  --place-type "..."
```

### Option 3: Use in OpenClaw Skill

When using this skill in OpenClaw, the API key is automatically loaded from your `TOOLS.md` configuration:

```markdown
# In your TOOLS.md
## RollingGo Hotel Skill
- **API Key**: `AIGOHOTEL_API_KEY=mcp_171e1ffa7da343faa4ec43460c52b13f`
```

## For Bot / AI Agent Usage

When calling this skill programmatically, ensure the environment variable is set before executing any RollingGo commands:

```bash
# Example: Search hotels near Wuhan University
export AIGOHOTEL_API_KEY=mcp_171e1ffa7da343faa4ec43460c52b13f
npx --yes --package rollinggo@latest rollinggo search-hotels \
  --origin-query "Search hotels near Wuhan University" \
  --place "武汉大学" \
  --place-type "景点" \
  --check-in-date 2026-03-21 \
  --stay-nights 1 \
  --adult-count 2
```

## Notes

- This is a **public API Key** - feel free to use it for testing and development
- For production use, consider applying for your own key at: https://mcp.agentichotel.cn/apply
- The key is resolved in this order: `--api-key` flag → `AIGOHOTEL_API_KEY` env var
