<!-- Generated from the API manifest and the command tree by pnpm generate. Do not edit. -->

# WordPress API: pattern-directory

## `wordpress api pattern-directory-patterns-list [options]`

- What: getWpV2PatternDirectoryPatterns — read (GET /wp/v2/pattern-directory/patterns)
- Call: `GET /wp/v2/pattern-directory/patterns`, effect: read
- Pages: page number: send `page` (query), one more for each page; page size in `per_page` (query)

| Flag | Required | What |
|---|---|---|
| `--category <value>` | no | Limit results to those matching a category ID. |
| `--context <value>` | no | Scope under which the request is made; determines fields present in response. |
| `--keyword <value>` | no | Limit results to those matching a keyword ID. |
| `--offset <value>` | no | Offset the result set by a specific number of items. |
| `--order <value>` | no | Order sort attribute ascending or descending. |
| `--orderby <value>` | no | Sort collection by post attribute. |
| `--page <value>` | no | Current page of the collection. |
| `--per-page <value>` | no | Maximum number of items to be returned in result set. |
| `--search <value>` | no | Limit results to those matching a string. |
| `--slug <value>` | no | Limit results to those matching a pattern (slug). |
| `--all` | no | read every page, as the API pages it |
