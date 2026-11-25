<!-- Generated from the API manifest and the command tree by pnpm generate. Do not edit. -->

# WordPress API: template-parts

## `wordpress api template-parts-create [options]`

- What: postWpV2TemplateParts — write (POST /wp/v2/template-parts)
- Call: `POST /wp/v2/template-parts`, effect: write
- Permission keys: `template-parts.publish`
- Body: `PostWpV2TemplatePartsRequest`, required

| Flag | Required | What |
|---|---|---|
| `--body <json>` | no | the request body as JSON; - reads it from stdin |
| `--body-file <path>` | no | the request body from a JSON file; - is stdin |

## `wordpress api template-parts-list [options]`

- What: getWpV2TemplateParts — read (GET /wp/v2/template-parts)
- Call: `GET /wp/v2/template-parts`, effect: read

| Flag | Required | What |
|---|---|---|
| `--area <value>` | no | Limit to the specified template part area. |
| `--context <value>` | no | Scope under which the request is made; determines fields present in response. |
| `--post-type <value>` | no | Post type to get the templates for. |
| `--wp-id <value>` | no | Limit to the specified post id. |

## `wordpress api template-parts-lookup-list [options]`

- What: getWpV2TemplatePartsLookup — read (GET /wp/v2/template-parts/lookup)
- Call: `GET /wp/v2/template-parts/lookup`, effect: read

| Flag | Required | What |
|---|---|---|
| `--is-custom <value>` | no | Indicates if a template is custom or part of the template hierarchy |
| `--slug <value>` | yes | The slug of the template to get the fallback for |
| `--template-prefix <value>` | no | The template prefix for the created template. This is used to extract the main template type, e.g. in \`taxonomy-books\` extracts the \`taxonomy\` |
