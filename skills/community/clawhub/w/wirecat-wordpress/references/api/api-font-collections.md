<!-- Generated from the API manifest and the command tree by pnpm generate. Do not edit. -->

# WordPress API: font-collections

## `wordpress api font-collections-list [options]`

- What: getWpV2FontCollections — read (GET /wp/v2/font-collections)
- Call: `GET /wp/v2/font-collections`, effect: read
- Pages: page number: send `page` (query), one more for each page; page size in `per_page` (query)

| Flag | Required | What |
|---|---|---|
| `--context <value>` | no | Scope under which the request is made; determines fields present in response. |
| `--page <value>` | no | Current page of the collection. |
| `--per-page <value>` | no | Maximum number of items to be returned in result set. |
| `--all` | no | read every page, as the API pages it |
