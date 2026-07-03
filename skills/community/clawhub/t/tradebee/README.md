# Tradebee OpenAPI Skills Bundle

This repository contains the unified `tradebee` skill for the Tradebee Website Builder Open API, plus the underlying per-capability implementation directories used by that unified entrypoint.

Users should invoke `tradebee` as the primary skill. The subdirectories remain as internal capability modules so the repository can keep clear boundaries between individual API operations.

## Unified Entry Policy

- `tradebee` is the only unified external skill entrypoint for new Tradebee capabilities.
- Any newly added capability must be wired into the root [index.js](./index.js), [skill.json](./skill.json), and [SKILL.md](./SKILL.md).
- New capability directories may still be added for implementation isolation, but they are not the primary publish target.
- Action naming inside `tradebee` should continue using the existing hyphenated pattern such as `products-read` and `visitor-recent`.

## Included Capabilities

| Capability | Directory | Purpose |
|------------|-----------|---------|
| `languages-get` | `languages-get` | Get enabled site languages |
| `rule-get` | `rule-get` | Read tenant HTML generation rules for one language and one scene |
| `blog-create` | `blog-create` | Create and publish a blog |
| `blog-read` | `blog-read` | Read blog list data |
| `blog-delete` | `blog-delete` | Move blogs to the recycle bin by ID list |
| `bloggroup-create` | `bloggroup-create` | Create and publish a blog group |
| `bloggroup-read` | `bloggroup-read` | Read blog group list data |
| `bloggroup-delete` | `bloggroup-delete` | Delete blog groups by ID list |
| `custompage-create` | `custompage-create` | Create and publish a custom page |
| `custompage-read` | `custompage-read` | Read custom page list data |
| `custompage-update` | `custompage-update` | Update an existing custom page |
| `custompage-delete` | `custompage-delete` | Move custom pages to the recycle bin by ID list |
| `productsgroup-create` | `productsgroup-create` | Create and publish a product group |
| `productsgroup-update` | `productsgroup-update` | Update an existing product group |
| `productsgroup-delete` | `productsgroup-delete` | Delete product groups by ID list |
| `productsgroup-read` | `productsgroup-read` | Get published product groups |
| `products-read` | `products-read` | Read product list data |
| `products-create` | `products-create` | Create new products |
| `products-update` | `products-update` | Update existing products |
| `products-delete` | `products-delete` | Move products to the recycle bin |
| `inquiry-read` | `inquiry-read` | Read inquiry list data |
| `visitor-recent` | `visitor-recent` | Read recent visitor data |
| `keywords-rank` | `keywords-rank` | Read keyword ranking analytics |

## Repository Principles

- Publish and use `tradebee` as the unified skill.
- Keep one directory per capability where implementation isolation helps maintenance.
- Keep each capability directory focused on `index.js`, `skill.json`, and `SKILL.md`.
- Keep the root `index.js`, root `skill.json`, and root `SKILL.md` aligned with every supported action.
- Keep request validation lightweight in `index.js` and let the server perform detailed business validation when possible.
- Use shared dependency patterns across capabilities, especially language selection and product group selection.

## Required Authentication

The unified `tradebee` skill and its underlying capability modules require a Tradebee API key.

Recommended environment variable:

```text
BEE_API_KEY
```

Never provide API keys in tool inputs, prompts, examples, logs, or chat text. Configure only `BEE_API_KEY` in the environment. Tradebee requests send site and business data to the external Tradebee Website Builder API, so only send the minimum data needed for the user's stated task.

## HTML Fragment Rule Source

For any generated HTML fragment in:

- `blog.description`
- `products.description`
- `productsgroup.section.top`
- `productsgroup.section.bottom`
- `custompage.content`

the caller should first call `rule-get` with the exact selected `language` and the exact matching `scene`.

`rule-get` call requirements:

- `language` is required
- `scene` is required
- reuse the exact `language` value already selected for the create or update action
- do not guess, translate, normalize, or replace the `language` value
- do not invent, shorten, translate, or rename any `scene` value
- use only the fixed scene mapping below. Do not call the current frontend website domain for this rule API.

Minimal request body:

```json
{
  "action": "rule-get",
  "language": "en",
  "scene": "products.description"
}
```

Required execution order:

1. Select the exact site `language` first.
2. Select the exact fixed `scene` that matches the target HTML field.
3. Call `rule-get`.
4. Generate the HTML fragment only after `rule-get` returns successfully.

Failure rule:

- If `rule-get` fails, do not continue by guessing colors, fonts, links, layout, or other fragment rules.
- Stop and report the rule-call failure instead of generating a fragment from assumptions.

Expected scene mapping:

- `blog.description` -> `blog.description`
- `products.description` -> `products.description`
- `productsgroup.section.top` -> `productsgroup.section.top`
- `productsgroup.section.bottom` -> `productsgroup.section.bottom`
- `custompage.content` -> `custompage.content`

The returned rule payload is the source of truth for all fragment-generation constraints.

The caller should:

- follow the full returned rule payload, not only part of it
- not guess, replace, shorten, rename, or partially ignore returned rule fields
- not hardcode assumptions here about future rule details, because the rule payload returned by `rule-get` may add new constraints later without requiring `tradebee` changes

## Typical Workflows

### Product Operations

1. Use `languages-get` to select the site language.
2. Use `productsgroup-create` only after explicit user confirmation of language and product group payload.
3. Use `productsgroup-update` only after explicit user confirmation of language and product group payload.
4. Use `productsgroup-delete` only after explicit user confirmation of language and product group IDs.
5. Use `productsgroup-read` to select a valid leaf product group when needed.
6. Use `products-create` to create a product.
7. Use `products-update` to update an existing product.
8. Use `products-delete` to move products to the recycle bin.

### Blog, Inquiry, and Visitor Operations

1. Use `languages-get` when a downstream action requires language selection.
2. Use `bloggroup-create` only after explicit user confirmation of language and blog group payload.
3. Use `bloggroup-read` to retrieve blog group data.
4. Use `blog-read` to retrieve blog data.
5. Use `blog-create` only after explicit user confirmation of language and blog payload.
6. Use `blog-delete` only after explicit user confirmation of language and blog IDs.
7. Use `bloggroup-delete` only after explicit user confirmation of language and blog group IDs.
8. Use `inquiry-read` to retrieve inquiry data.
9. Use `visitor-recent` to retrieve recent visitor data.

### Custom Page Operations

1. Use `languages-get` when a downstream action requires language selection.
2. Use `custompage-read` to retrieve one exact custom page or list custom pages.
3. Use `custompage-create` only after explicit user confirmation of language and custom page payload.
4. Use `custompage-update` only after explicit user confirmation of language, target custom page ID, payload, and backup behavior.
5. Use `custompage-delete` only after explicit user confirmation of language and custom page IDs.

### SEO and Ranking Operations

1. Use `keywords-rank` to retrieve keyword ranking records and history.

## Directory Layout

```text
tradebee/
  blog-create/
  blog-delete/
  blog-read/
  blog-update/
  bloggroup-create/
  bloggroup-delete/
  bloggroup-read/
  bloggroup-update/
  custompage-create/
  custompage-delete/
  custompage-read/
  custompage-update/
  inquiry-read/
  keywords-rank/
  languages-get/
  productsgroup-create/
  productsgroup-delete/
  productsgroup-read/
  productsgroup-update/
  products-create/
  products-delete/
  products-read/
  products-update/
  rule-get/
  visitor-recent/
  
  README.md
  bundle.json
  index.js
  package.json
  SKILL.md
  skill.json
  validation.js
  Web.config
```

## Publishing Guidance

This repository should evolve around a single publishable unified skill: `tradebee`.

- User experience: one skill, multiple actions.
- Maintenance model: add capability modules underneath, then expose them through `tradebee`.
- Recommended naming pattern:
  - unified skill name: `tradebee`
  - action names: keep the existing hyphenated naming

## Notes

- `blog-create` is a high-impact publishing action and requires explicit user confirmation before execution.
- `blog-update` is a high-impact update action and requires explicit user confirmation before execution.
- `blog-delete` moves blogs to the recycle bin and requires explicit user confirmation before execution.
- `bloggroup-create` is a high-impact publishing action and requires explicit user confirmation before execution.
- `bloggroup-update` is a high-impact update action and requires explicit user confirmation before execution.
- `bloggroup-delete` is a destructive action and requires explicit user confirmation before execution.
- `custompage-create` is a high-impact publishing action and requires explicit user confirmation before execution.
- `custompage-update` is a high-impact update action and requires explicit user confirmation before execution.
- `custompage-delete` moves custom pages to the recycle bin and requires explicit user confirmation before execution.
- `productsgroup-create` is a high-impact publishing action and requires explicit user confirmation before execution.
- `productsgroup-update` is a high-impact update action and requires explicit user confirmation before execution.
- `productsgroup-delete` is a destructive action and requires explicit user confirmation before execution.
- `products-create` is a high-impact publishing action and requires explicit user confirmation before execution.
- `products-update` is a high-impact update action and requires explicit user confirmation before execution.
- `products-delete` moves products to the recycle bin instead of permanently deleting them and requires explicit user confirmation before execution.
- `products-update` and `products-create` share similar request structures, but `update` requires `products_id`.
- `rule-get` is the required source of truth before generating any supported HTML fragment and should not be skipped or replaced with assumptions.
- `languages-get` should be used first when a downstream action depends on the exact site language.
- When adding a new capability later, update the root action enum, root routing logic, and root documentation in the same change.

