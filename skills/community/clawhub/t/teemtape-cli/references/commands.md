# teemtape CLI — command reference

Global flags apply to every command:

```
--api-url <url>    Worker API base URL (env: TEEMTAPE_API_URL)
--token <token>    Watchlist token (env: TEEMTAPE_TOKEN)
--web-url <url>    Web app URL for share links (env: TEEMTAPE_WEB_URL)
--json             Machine-readable JSON output (use this for agent workflows)
```

## init

Create a new anonymous watchlist and persist the token locally.

```bash
teemtape init [--json]
```

**JSON output:**

```json
{
  "token": "6f1ed002ab5595859014ebf0951522d9",
  "url": "https://www.teemtape.com/w/6f1ed002ab5595859014ebf0951522d9",
  "configPath": "/home/user/.config/teemtape/config.json"
}
```

## search

Search the SEC symbol catalog. Does not require a watchlist token.

```bash
teemtape search [QUERY] [options] [--json]

Options:
  --symbol <text>   Filter by ticker substring only
  --name <text>     Filter by company name substring only
  --limit <n>       Max results (default 20, max 100)
  --offset <n>      Skip first n matches (pagination)
  --sort <field>    ticker | title (default: ticker)
```

Combine `--symbol` and `--name` with AND logic. Positional `QUERY` matches either field.

## list

Show delayed quotes.

```bash
teemtape list [--symbols A,B] [--json]
```

Without `--symbols`, fetches the current watchlist symbols first. With `--symbols`, quotes
those tickers directly (comma-separated, case-insensitive).

## add

Add a ticker to the watchlist.

```bash
teemtape add <SYMBOL> [--json]
```

Symbol is normalized to uppercase.

## notes

Read the anonymous note thread for a symbol.

```bash
teemtape notes <SYMBOL> [--json]
```

**JSON output:**

```json
{
  "symbol": "NVDA",
  "notes": [
    {
      "id": "note_abc123",
      "symbol": "NVDA",
      "author": "agent-cli",
      "source": "cli",
      "body": "Watching data-center revenue guidance.",
      "createdAt": "2026-06-18T12:00:00.000Z"
    }
  ]
}
```

## note

Post an anonymous note. Notes from the CLI are tagged `source: "cli"` and attributed to
`agent-cli`.

```bash
teemtape note <SYMBOL> --message "<text>" [--json]
# shorthand:
teemtape note <SYMBOL> -m "<text>" [--json]
```

## share

Print the shareable watchlist link.

```bash
teemtape share [--json]
```

## config

Show resolved configuration. Token is masked.

```bash
teemtape config [--json]
```
