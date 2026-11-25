<!-- Generated from the API manifest and the command tree by pnpm generate. Do not edit. -->

# WordPress API: templates

## `wordpress api templates-create [options]`

- What: postWpV2Templates — write (POST /wp/v2/templates)
- Call: `POST /wp/v2/templates`, effect: write
- Permission keys: `templates.publish`
- Body: `PostWpV2TemplatesRequest`, required

| Flag | Required | What |
|---|---|---|
| `--body <json>` | no | the request body as JSON; - reads it from stdin |
| `--body-file <path>` | no | the request body from a JSON file; - is stdin |

## `wordpress api templates-list [options]`

- What: getWpV2Templates — read (GET /wp/v2/templates)
- Call: `GET /wp/v2/templates`, effect: read

| Flag | Required | What |
|---|---|---|
| `--area <value>` | no | Limit to the specified template part area. |
| `--context <value>` | no | Scope under which the request is made; determines fields present in response. |
| `--post-type <value>` | no | Post type to get the templates for. |
| `--wp-id <value>` | no | Limit to the specified post id. |

## `wordpress api templates-lookup-list [options]`

- What: getWpV2TemplatesLookup — read (GET /wp/v2/templates/lookup)
- Call: `GET /wp/v2/templates/lookup`, effect: read

| Flag | Required | What |
|---|---|---|
| `--is-custom <value>` | no | Indicates if a template is custom or part of the template hierarchy |
| `--slug <value>` | yes | The slug of the template to get the fallback for |
| `--template-prefix <value>` | no | The template prefix for the created template. This is used to extract the main template type, e.g. in \`taxonomy-books\` extracts the \`taxonomy\` |
