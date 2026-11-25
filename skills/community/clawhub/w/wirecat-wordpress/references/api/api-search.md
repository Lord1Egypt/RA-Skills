<!-- Generated from the API manifest and the command tree by pnpm generate. Do not edit. -->

# WordPress API: search

## `wordpress api search-list [options]`

- What: getWpV2Search — read (GET /wp/v2/search)
- Call: `GET /wp/v2/search`, effect: read
- Pages: page number: send `page` (query), one more for each page; page size in `per_page` (query)

| Flag | Required | What |
|---|---|---|
| `--context <value>` | no | Scope under which the request is made; determines fields present in response. |
| `--exclude <value>` | no | Ensure result set excludes specific IDs. |
| `--include <value>` | no | Limit result set to specific IDs. |
| `--page <value>` | no | Current page of the collection. |
| `--per-page <value>` | no | Maximum number of items to be returned in result set. |
| `--search <value>` | no | Limit results to those matching a string. |
| `--subtype <value>` | no | Limit results to items of one or more object subtypes. |
| `--type <value>` | no | Limit results to items of an object type. |
| `--all` | no | read every page, as the API pages it |
