# RenderMark MCP Server — Setup Guide

## Installation

```
npx -y @rendermark/mcp-server@latest
```

## Required: RenderMark API key

Get your API key from https://rendermark.app/settings/keys and save it to `~/.rendermark/config.json`:

```json
{
  "apiKey": "rm_live_your_key_here",
  "apiBaseUrl": "https://rendermark.app"
}
```

Alternatively, set the `RENDERMARK_API_KEY` environment variable. The config file takes precedence if both are set.

You can also run `setup_api_key` to authenticate via the browser.

## Optional: PDF/image export

PDF and image export requires a browser engine. Either:
- Install Chrome or Chromium locally, **or**
- Add `"browserlessApiKey": "your_key"` to `~/.rendermark/config.json`

Without a browser, all other tools (rendering, publishing, sharing) work normally.

## Optional: Google Docs publishing

To publish documents as Google Docs, add Google OAuth credentials to `~/.rendermark/config.json`:

```json
{
  "google": {
    "clientId": "your_client_id",
    "clientSecret": "your_client_secret"
  }
}
```

Then run `npx @rendermark/mcp-server auth google` to authenticate. This is only needed for the `publish_to_google_docs` tool.

## Troubleshooting

### "API key not found" or 401 errors
- Verify `~/.rendermark/config.json` exists and contains a valid `apiKey`
- Or set `RENDERMARK_API_KEY` environment variable
- Keys start with `rm_live_` — test keys (`rm_test_`) only work in development

### PDF/image export fails
- Ensure Chrome or Chromium is installed, or configure a Browserless API key
- On headless servers, use `"browserlessApiKey"` in config

### Google Docs publish fails
- Run `npx @rendermark/mcp-server auth google` to re-authenticate
- Verify OAuth credentials in config are correct
- Token may have expired — re-run auth flow

### MCP connection issues
- Verify the server is running: check Claude Settings > Extensions
- Try `npx -y @rendermark/mcp-server@latest` to ensure latest version
- Check that Node.js 18+ and npx are available
