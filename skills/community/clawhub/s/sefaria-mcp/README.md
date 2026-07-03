# Sefaria MCP Server

[![npm version](https://img.shields.io/npm/v/sefaria-mcp-server.svg)](https://www.npmjs.com/package/sefaria-mcp-server)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

An MCP (Model Context Protocol) server that provides access to [Sefaria](https://www.sefaria.org)'s library of Jewish texts - Torah, Talmud, Mishnah, Midrash, and thousands of commentaries.

Use this server to give Claude, Cursor, Windsurf, or any MCP-compatible AI assistant the ability to search, read, and explore Jewish texts.

## Features

- 📖 **Read any text** - Torah, Talmud, Mishnah, Midrash, Halacha, Kabbalah
- 🔍 **Full-text search** - Search across all texts in English or Hebrew
- 📚 **Get commentaries** - Rashi, Ramban, Ibn Ezra, and hundreds more
- 📅 **Daily learning** - Daf Yomi, Parsha, daily Rambam, and more
- 🔗 **Cross-references** - Find connections between texts

## Installation

```bash
npm install -g sefaria-mcp-server
```

Or run directly with npx:

```bash
npx sefaria-mcp-server
```

The installed CLI binary is also available as `sefaria-mcp`:

```bash
npx -y -p sefaria-mcp-server sefaria-mcp
```

## Configuration

No API key is required. The server uses Sefaria's public API.

### Claude Desktop

Add to `~/Library/Application Support/Claude/claude_desktop_config.json` (macOS) or `%AppData%\Claude\claude_desktop_config.json` (Windows):

```json
{
  "mcpServers": {
    "sefaria": {
      "command": "npx",
      "args": ["-y", "sefaria-mcp-server"]
    }
  }
}
```

### Cursor

Add to `.cursor/mcp.json` in your project:

```json
{
  "mcpServers": {
    "sefaria": {
      "command": "npx",
      "args": ["-y", "sefaria-mcp-server"]
    }
  }
}
```

## Tools

### get_text

Get text by reference with Hebrew and English.

```
Reference formats:
- Torah: "Genesis 1:1", "Exodus 20:1-10"
- Talmud: "Berakhot 2a", "Shabbat 31a"
- Mishnah: "Mishnah Avot 1:1"
- Midrash: "Genesis Rabbah 1:1"
- Commentary: "Rashi on Genesis 1:1"
```

### search

Full-text search across all texts.

```
Examples:
- "love your neighbor"
- "tikkun olam"
- "ואהבת לרעך כמוך"
```

### get_links

Get commentaries and cross-references for a verse.

### get_parsha

Get this week's Torah portion.

### get_calendars

Get today's learning schedule (Daf Yomi, Parsha, daily Rambam, etc.).

### get_book_info

Get metadata about a book (structure, categories).

### get_related

Get related topics and community source sheets.

## Examples

Ask Claude:

> "What does Genesis 1:1 say? Show me the Hebrew and commentaries."

> "Search for texts about loving your neighbor"

> "What's this week's parsha?"

> "What's today's Daf Yomi?"

> "Find all the commentaries on Leviticus 19:18"

## Development

```bash
git clone https://github.com/abeperl/sefaria-mcp-server
cd sefaria-mcp-server
npm install
npm run build
npm start
```

## Credits

- Powered by [Sefaria](https://www.sefaria.org) - the free, open-source library of Jewish texts
- Built with the [Model Context Protocol](https://modelcontextprotocol.io) SDK

## License

MIT
