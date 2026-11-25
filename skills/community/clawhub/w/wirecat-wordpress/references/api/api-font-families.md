<!-- Generated from the API manifest and the command tree by pnpm generate. Do not edit. -->

# WordPress API: font-families

## `wordpress api font-families-create [options]`

- What: postWpV2FontFamilies — write (POST /wp/v2/font-families)
- Call: `POST /wp/v2/font-families`, effect: write
- Body: `PostWpV2FontFamiliesRequest`, required

| Flag | Required | What |
|---|---|---|
| `--body <json>` | no | the request body as JSON; - reads it from stdin |
| `--body-file <path>` | no | the request body from a JSON file; - is stdin |

## `wordpress api font-families-delete [options]`

- What: deleteWpV2FontFamiliesById — destructive (DELETE /wp/v2/font-families/{id})
- Call: `DELETE /wp/v2/font-families/{id}`, effect: destructive
- Permission keys: `font-families.delete`, `font-families.delete.force`

| Flag | Required | What |
|---|---|---|
| `--id <value>` | yes | id |
| `--force <value>` | no | Whether to bypass Trash and force deletion. |

## `wordpress api font-families-font-faces-create [options]`

- What: postWpV2FontFamiliesByFontFamilyIdFontFaces — write (POST…
- Call: `POST /wp/v2/font-families/{font_family_id}/font-faces`, effect: write
- Body: `PostWpV2FontFamiliesByFontFamilyIdFontFacesRequest`, required

| Flag | Required | What |
|---|---|---|
| `--font-family-id <value>` | yes | font\_family\_id |
| `--body <json>` | no | the request body as JSON; - reads it from stdin |
| `--body-file <path>` | no | the request body from a JSON file; - is stdin |

## `wordpress api font-families-font-faces-delete [options]`

- What: deleteWpV2FontFamiliesByFontFamilyIdFontFacesById — destructive (DELETE…
- Call: `DELETE /wp/v2/font-families/{font_family_id}/font-faces/{id}`, effect: destructive
- Permission keys: `font-families.delete`, `font-families.delete.force`

| Flag | Required | What |
|---|---|---|
| `--font-family-id <value>` | yes | font\_family\_id |
| `--id <value>` | yes | id |
| `--force <value>` | no | Whether to bypass Trash and force deletion. |

## `wordpress api font-families-font-faces-get [options]`

- What: getWpV2FontFamiliesByFontFamilyIdFontFacesById — read (GET…
- Call: `GET /wp/v2/font-families/{font_family_id}/font-faces/{id}`, effect: read

| Flag | Required | What |
|---|---|---|
| `--font-family-id <value>` | yes | font\_family\_id |
| `--id <value>` | yes | id |
| `--context <value>` | no | Scope under which the request is made; determines fields present in response. |

## `wordpress api font-families-font-faces-list [options]`

- What: getWpV2FontFamiliesByFontFamilyIdFontFaces — read (GET…
- Call: `GET /wp/v2/font-families/{font_family_id}/font-faces`, effect: read
- Pages: page number: send `page` (query), one more for each page; page size in `per_page` (query)

| Flag | Required | What |
|---|---|---|
| `--font-family-id <value>` | yes | font\_family\_id |
| `--context <value>` | no | Scope under which the request is made; determines fields present in response. |
| `--exclude <value>` | no | Ensure result set excludes specific IDs. |
| `--include <value>` | no | Limit result set to specific IDs. |
| `--offset <value>` | no | Offset the result set by a specific number of items. |
| `--order <value>` | no | Order sort attribute ascending or descending. |
| `--orderby <value>` | no | Sort collection by post attribute. |
| `--page <value>` | no | Current page of the collection. |
| `--per-page <value>` | no | Maximum number of items to be returned in result set. |
| `--search-semantics <value>` | no | How to interpret the search input. |
| `--all` | no | read every page, as the API pages it |

## `wordpress api font-families-get [options]`

- What: getWpV2FontFamiliesById — read (GET /wp/v2/font-families/{id})
- Call: `GET /wp/v2/font-families/{id}`, effect: read

| Flag | Required | What |
|---|---|---|
| `--id <value>` | yes | id |
| `--context <value>` | no | Scope under which the request is made; determines fields present in response. |

## `wordpress api font-families-list [options]`

- What: getWpV2FontFamilies — read (GET /wp/v2/font-families)
- Call: `GET /wp/v2/font-families`, effect: read
- Pages: page number: send `page` (query), one more for each page; page size in `per_page` (query)

| Flag | Required | What |
|---|---|---|
| `--context <value>` | no | Scope under which the request is made; determines fields present in response. |
| `--exclude <value>` | no | Ensure result set excludes specific IDs. |
| `--include <value>` | no | Limit result set to specific IDs. |
| `--offset <value>` | no | Offset the result set by a specific number of items. |
| `--order <value>` | no | Order sort attribute ascending or descending. |
| `--orderby <value>` | no | Sort collection by post attribute. |
| `--page <value>` | no | Current page of the collection. |
| `--per-page <value>` | no | Maximum number of items to be returned in result set. |
| `--search-semantics <value>` | no | How to interpret the search input. |
| `--slug <value>` | no | Limit result set to posts with one or more specific slugs. |
| `--all` | no | read every page, as the API pages it |

## `wordpress api font-families-update [options]`

- What: postWpV2FontFamiliesById — write (POST /wp/v2/font-families/{id})
- Call: `POST /wp/v2/font-families/{id}`, effect: write
- Body: `PostWpV2FontFamiliesByIdRequest`, required

| Flag | Required | What |
|---|---|---|
| `--id <value>` | yes | id |
| `--body <json>` | no | the request body as JSON; - reads it from stdin |
| `--body-file <path>` | no | the request body from a JSON file; - is stdin |
