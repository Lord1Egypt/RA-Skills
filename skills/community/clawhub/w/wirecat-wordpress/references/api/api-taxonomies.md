<!-- Generated from the API manifest and the command tree by pnpm generate. Do not edit. -->

# WordPress API: taxonomies

## `wordpress api taxonomies-get [options]`

- What: getWpV2TaxonomiesByTaxonomy — read (GET /wp/v2/taxonomies/{taxonomy})
- Call: `GET /wp/v2/taxonomies/{taxonomy}`, effect: read

| Flag | Required | What |
|---|---|---|
| `--taxonomy <value>` | yes | taxonomy |
| `--context <value>` | no | Scope under which the request is made; determines fields present in response. |

## `wordpress api taxonomies-list [options]`

- What: getWpV2Taxonomies — read (GET /wp/v2/taxonomies)
- Call: `GET /wp/v2/taxonomies`, effect: read

| Flag | Required | What |
|---|---|---|
| `--context <value>` | no | Scope under which the request is made; determines fields present in response. |
| `--type <value>` | no | Limit results to taxonomies associated with a specific post type. |
