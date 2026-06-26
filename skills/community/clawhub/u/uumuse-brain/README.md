# uumuse-brain

> **Your AI just got a brain.**
> Connect your documents. Ask from anywhere. Get answers with sources.

Upload PDFs, docs, and web pages to [UUMuse](https://uumuse.ai). Then ask your OpenClaw agent about them — from Telegram, Slack, WhatsApp, or anywhere.

## Install

First make sure Node.js LTS is installed:

```bash
node -v
npm -v
```

macOS / Linux / WSL:

```bash
npx clawhub@latest install uumuse-brain
```

Windows PowerShell / CMD:

```powershell
npx.cmd clawhub@latest install uumuse-brain
```

You'll be prompted to enter your UUMuse API key. Get one at [uumuse.ai → Account → API Keys](https://uumuse.ai/account/api-keys).

Important: `clawhub install` installs the Skill files, but may not persist your MCP server config or API key into `mcporter.json` / `openclaw.json`. To make UUMuse keep working after restarting OpenClaw or opening a new window, also add the MCP config shown below.

The MCP server runs through `npx -y uumuse-mcp`. This downloads and caches the npm package on demand; it is normal for `npm list -g uumuse-mcp` to show no global install.

### Manual Install

Copy the `uumuse-brain` folder to your OpenClaw skills directory.

macOS / Linux / WSL:

```bash
git clone https://github.com/UUMuse/uumuse-mcp
cp -r uumuse-mcp/packages/uumuse-brain ~/.openclaw/skills/
```

Windows PowerShell:

```powershell
git clone https://github.com/UUMuse/uumuse-mcp
New-Item -ItemType Directory -Force "$env:USERPROFILE\.openclaw\skills" | Out-Null
Copy-Item -Recurse .\uumuse-mcp\packages\uumuse-brain "$env:USERPROFILE\.openclaw\skills\"
```

Then set your API key in OpenClaw config. This persistent MCP config is required for reliable startup.

macOS / Linux / WSL MCP command:

```json
{
  "command": "npx",
  "args": ["-y", "uumuse-mcp"]
}
```

Windows MCP command:

```json
{
  "command": "npx.cmd",
  "args": ["-y", "uumuse-mcp"]
}
```

### Verify MCP Server

macOS / Linux / WSL:

```bash
printf '%s\n' \
'{"jsonrpc":"2.0","id":1,"method":"initialize","params":{"protocolVersion":"2024-11-05","capabilities":{},"clientInfo":{"name":"smoke-test","version":"0.0.0"}}}' \
'{"jsonrpc":"2.0","method":"notifications/initialized","params":{}}' \
'{"jsonrpc":"2.0","id":2,"method":"tools/list","params":{}}' \
| UUMUSE_API_KEY="sk-uu-your-key" npx -y uumuse-mcp
```

Windows PowerShell:

```powershell
$payload = @(
  '{"jsonrpc":"2.0","id":1,"method":"initialize","params":{"protocolVersion":"2024-11-05","capabilities":{},"clientInfo":{"name":"smoke-test","version":"0.0.0"}}}',
  '{"jsonrpc":"2.0","method":"notifications/initialized","params":{}}',
  '{"jsonrpc":"2.0","id":2,"method":"tools/list","params":{}}'
) -join "`n"

$env:UUMUSE_API_KEY = "sk-uu-your-key"
$payload | npx.cmd -y uumuse-mcp
Remove-Item Env:UUMUSE_API_KEY
```

Expected result: `serverInfo.name` is `uumuse`, and the response lists 13 `uumuse_*` tools.

## What It Does

Once installed, your OpenClaw agent automatically knows when and how to use your knowledge bases. The current MCP server exposes 13 tools:

| Tool | What it does | Cost |
|------|-------------|------|
| `uumuse_workspaces` | List your workspaces | Free |
| `uumuse_files` | List files in a workspace | Free |
| `uumuse_search` | Semantic search across documents | Free |
| `uumuse_ask` | AI answer with source citations | Per token (UT) |
| `uumuse_status` | Show account, plan, UT balance, quota, and referral info | Free |
| `uumuse_read_file` | Read a file's extracted text content | Free |
| `uumuse_upload` | Create/upload a text file into a workspace | Free |
| `uumuse_edit_file` | Replace a file's text content | Free |
| `uumuse_delete_file` | Delete a file from a workspace | Free |
| `uumuse_append` | Append text to an existing file | Free |
| `uumuse_remember` | Save a memory/fact for future answers | Free |
| `uumuse_recall` | Search saved memories | Free |
| `uumuse_forget` | Forget a saved file/memory item | Free |

## Usage Examples

### From Telegram / WhatsApp / Slack

```
You: What does my Q3 report say about revenue?

Agent: Based on your Q3 financial report, revenue grew 23% YoY to $4.2M,
driven by enterprise contract expansion...

Sources:
1. Q3-financial-report-2026.pdf: "Revenue reached $4.2M..."
2. board-meeting-notes.docx: "Q3 highlights include 23% growth..."
```

```
You: Search my workspace for anything about pricing strategy

Agent: Found 3 relevant documents:
1. pricing-v3.pdf (score: 0.92) — "Tiered pricing model with..."
2. competitive-analysis.docx (score: 0.87) — "Competitor pricing ranges..."
3. product-roadmap.pdf (score: 0.81) — "Pricing changes planned for..."
```

## Self-Hosted UUMuse

If you run UUMuse on your own infrastructure, set the custom API URL during install or in your OpenClaw config:

```
uumuse_api_url: https://your-domain.com/open
```

## How It Works

This skill connects to [UUMuse](https://uumuse.ai) through the [uumuse-mcp](https://www.npmjs.com/package/uumuse-mcp) MCP Server. The skill provides:

- **`skill.json`** — Declares the MCP server dependency and configuration schema
- **`SKILL.md`** — Teaches your agent *when* and *how* to use knowledge base tools

The actual tool implementation runs via the `uumuse-mcp` npm package (installed automatically).

## Pricing

- **Search, list workspaces, list files**: Free (no UT cost)
- **AI-generated answers** (`uumuse_ask`): Billed per token, same as web usage
- **Free tier**: 50 ask queries / month
- **Pro/Team/Enterprise**: Higher quotas, optional branding removal

See [uumuse.ai/pricing](https://uumuse.ai/pricing) for details.

## Links

- [UUMuse](https://uumuse.ai) — AI Knowledge Workspace
- [uumuse-mcp on npm](https://www.npmjs.com/package/uumuse-mcp) — MCP Server package
- [GitHub](https://github.com/UUMuse/uumuse-mcp) — Source code
- [API Docs](https://uumuse.ai/docs) — Open API documentation

## License

MIT
