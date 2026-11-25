<!-- Generated from the API manifest and the command tree by pnpm generate. Do not edit. -->

# WordPress API: global-styles

## `wordpress api global-styles-revisions-get [options]`

- What: getWpV2GlobalStylesByParentRevisionsById — read (GET…
- Call: `GET /wp/v2/global-styles/{parent}/revisions/{id}`, effect: read

| Flag | Required | What |
|---|---|---|
| `--parent <value>` | yes | parent |
| `--id <value>` | yes | id |
| `--context <value>` | no | Scope under which the request is made; determines fields present in response. |

## `wordpress api global-styles-revisions-list [options]`

- What: getWpV2GlobalStylesByParentRevisions — read (GET…
- Call: `GET /wp/v2/global-styles/{parent}/revisions`, effect: read
- Pages: page number: send `page` (query), one more for each page; page size in `per_page` (query)

| Flag | Required | What |
|---|---|---|
| `--parent <value>` | yes | parent |
| `--context <value>` | no | Scope under which the request is made; determines fields present in response. |
| `--offset <value>` | no | Offset the result set by a specific number of items. |
| `--page <value>` | no | Current page of the collection. |
| `--per-page <value>` | no | Maximum number of items to be returned in result set. |
| `--all` | no | read every page, as the API pages it |
