---
name: wiro-agent-connectors
description: Connect an AI agent or MCP client to Gmail, Google Ads, Google Drive, YouTube, Instagram, LinkedIn, Shopify, Notion, WordPress, Mailchimp and 35 more services through the open-source Wiro Agent Connectors (npm @wiro-ai/wiro-agent-connectors), one stdio MCP server per service, started with npx and the user's own credentials. Covers picking the connector and its environment variables, adding it to Claude Code, Claude Desktop or Cursor, limiting it to chosen accounts, how its tools behave, and loading the modules into your own MCP host. Use when the user wants their agent to work with one of these services through MCP, asks for an MCP server for a service that has no official one, or mentions wiro-agent-connectors.
---

# Wiro Agent Connectors

`@wiro-ai/wiro-agent-connectors` is a package of MCP connectors for services that have no official MCP server. Each connector serves one service as its own stdio MCP server, started with `npx -y @wiro-ai/wiro-agent-connectors <connector>`. It needs Node.js 22 or later and reads the service's credentials from environment variables. A connector talks only to its service's API, and it never stores or logs the credentials.

Source and docs: https://github.com/wiroai/Wiro-Agent-Connectors

## Find the connector

Run the list. It prints every connector with its environment variables, the alternatives it accepts, its tools and, where it has them, its account keys:

```bash
npx -y @wiro-ai/wiro-agent-connectors --list
```

The connectors by area, named as `--list` prints them:

| Area | Connectors |
| --- | --- |
| Social and video | `bluesky`, `facebook-pages`, `instagram`, `linkedin`, `mastodon`, `pinterest`, `reddit`, `threads`, `tiktok`, `tumblr`, `twitter` (X), `youtube` |
| Ads and analytics | `google-ads`, `meta-ads`, `ga4`, `google-search-console`, `google-merchant-center` |
| Google services | `blogger`, `gmail`, `google-business`, `google-calendar`, `google-drive`, `google-play`, `firebase` |
| Mobile apps and attribution | `apple-appstore`, `adapty`, `revenuecat`, `adjust`, `roasit` |
| Writing and knowledge | `beehiiv`, `devto`, `hashnode`, `notion`, `qiita`, `kaggle` |
| Email and CRM | `apollo`, `brevo`, `mailchimp`, `sendgrid` |
| Commerce and sites | `shopify`, `woocommerce`, `wordpress`, `keepa` |
| Search and data | `serper`, `calendarific` |

No connector for the service? Check whether the service runs an MCP server of its own, or ask for one at https://github.com/wiroai/Wiro-Agent-Connectors/issues/new?template=new_connector.yml.

## Credentials

- Variables are named `<VENDOR>_<CREDENTIAL>`, such as `SERPER_APIKEY`, `GMAIL_ACCESS_TOKEN` or `WORDPRESS_APPPASSWORD`. Take the exact names from `--list`; never guess them.
- Each connector has its own page that says, step by step, where to get every credential and how to revoke it: `https://github.com/wiroai/Wiro-Agent-Connectors/blob/main/src/vendors/<connector>/README.md`.
- Let the user put the values into the client's configuration. Never ask them to paste a key, token or password into the chat, and never write one into a file that gets committed.
- Some connectors accept one of several credential sets, such as an OAuth access token or a system user token. `--list` prints them as `needs: A, or B`; one complete set is enough.
- A connector whose service signs in with OAuth reads a current access token from `<VENDOR>_ACCESS_TOKEN`. The CLI does not refresh it: the user gets it from their own OAuth app, and a new one when it expires.
- A connector without its variables still starts and lists its tools; each call then answers with the variables to set.

## Add it to the client

Add one entry per connector; several connectors run side by side.

Claude Code:

```bash
claude mcp add --transport stdio serper \
  --env SERPER_APIKEY=your-serper-api-key \
  -- npx -y @wiro-ai/wiro-agent-connectors serper
```

Cursor: `~/.cursor/mcp.json`, or `.cursor/mcp.json` in a project:

```json
{
  "mcpServers": {
    "serper": {
      "command": "npx",
      "args": ["-y", "@wiro-ai/wiro-agent-connectors", "serper"],
      "env": {
        "SERPER_APIKEY": "your-serper-api-key"
      }
    }
  }
}
```

Claude Desktop: the same entry in `claude_desktop_config.json`, with `"type": "stdio"` added to it, then quit and reopen Claude Desktop.

## Limit it to chosen accounts

Connectors whose tools act on one of several accounts (Pages, ad accounts, channels, apps) print an `accounts:` line in `--list`, such as `pages (Facebook Pages, one or more, listed by list_pages)`. To let the agent act only on the accounts the user chooses, set `CONNECTOR_ACCOUNTS` in the connector's environment to JSON keyed by those account keys:

```json
{ "pages": ["123456789012345"] }
```

The tool named on that line (here `list_pages`) lists the ids to choose from. Tools then refuse any other account before they send anything. Without `CONNECTOR_ACCOUNTS` there is no lock.

## How the tools behave

- Read tools only read. Every write tool says in its MCP annotations whether it adds, overwrites or removes; `api_request` can do any of these.
- Writes are never retried. When a write gets no clear answer, the result is `{ "outcome": "unknown", "check": "<read tool>" }`: run that read tool before you try again, so nothing goes out twice.
- A rate limit comes back with `retryAfter` in seconds. Wait that long before the next call.
- Long lists come in pages: pass `nextCursor` back as `cursor`.
- Most connectors also have `api_get` and `api_request` for the rest of the service's API, inside the connector's own origins.
- Errors are results with `isError: true` and a sentence that says what happened, plus the service's HTTP `status`.

## Load the modules into your own host

The package also exports the modules and the CLI's building blocks, for a host that runs connectors itself. Every request goes through the `fetch` the host hands the module:

```js
const { loadConnector, createGuardedFetch, originsFromCredentials } = require('@wiro-ai/wiro-agent-connectors');

async function main() {
  const calendarific = loadConnector('calendarific');
  const credentials = { apikey: process.env.CALENDARIFIC_APIKEY };
  const result = await calendarific.call('list_upcoming_holidays', { country: 'US' }, {
    credentials,
    accounts: null, // no account lock
    fetch: createGuardedFetch({
      origins: calendarific.origins,
      credentialOrigins: originsFromCredentials(calendarific, credentials),
      uploadHosts: calendarific.uploadHosts,
    }),
    log: (line) => console.error(line),
  });
  console.log(result.content[0].text);
}

main();
```

A host that uses its own `fetch` must apply the same checks as `createGuardedFetch`: the README's Credential origins and Upload hosts sections list them.
