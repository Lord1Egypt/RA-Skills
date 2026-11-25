<!-- Generated from the API manifest and the command tree by pnpm generate. Do not edit. -->

# WordPress API: block-directory

## `wordpress api block-directory-search-list [options]`

- What: getWpV2BlockDirectorySearch — read (GET /wp/v2/block-directory/search)
- Call: `GET /wp/v2/block-directory/search`, effect: read
- Pages: page number: send `page` (query), one more for each page; page size in `per_page` (query)

| Flag | Required | What |
|---|---|---|
| `--context <value>` | no | Scope under which the request is made; determines fields present in response. |
| `--page <value>` | no | Current page of the collection. |
| `--per-page <value>` | no | Maximum number of items to be returned in result set. |
| `--term <value>` | yes | Limit result set to blocks matching the search term. |
| `--all` | no | read every page, as the API pages it |
