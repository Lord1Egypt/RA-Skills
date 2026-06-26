# Core Endpoints

Use this file as the core route map. It is intentionally broad, but no static file can be the full live endpoint list because plugins and custom code add routes.

Primary docs:

- WordPress REST API reference: <https://developer.wordpress.org/rest-api/reference/>
- Route and endpoint handbook: <https://developer.wordpress.org/rest-api/extending-the-rest-api/routes-and-endpoints/>

## Discovery

Always start with:

- `GET /wp-json/`

The index exposes:

- `namespaces`
- `routes`
- site metadata such as name, description, URL, and authentication details exposed by the site

## Core Route Families

The main namespace on current installs is usually `wp/v2`.

Common core collections and item routes include:

- `/wp/v2/posts`
- `/wp/v2/pages`
- `/wp/v2/media`
- `/wp/v2/comments`
- `/wp/v2/categories`
- `/wp/v2/tags`
- `/wp/v2/users`
- `/wp/v2/search`
- `/wp/v2/settings`
- `/wp/v2/types`
- `/wp/v2/statuses`
- `/wp/v2/taxonomies`
- `/wp/v2/blocks`
- `/wp/v2/block-types`
- `/wp/v2/block-renderer`
- `/wp/v2/templates`
- `/wp/v2/template-parts`
- `/wp/v2/patterns`
- `/wp/v2/pattern-directory/patterns`
- `/wp/v2/global-styles`
- `/wp/v2/global-styles/themes`
- `/wp/v2/themes`
- `/wp/v2/plugins`
- `/wp/v2/font-families`
- `/wp/v2/font-faces`
- `/wp/v2/menu-locations`
- `/wp/v2/menus`
- `/wp/v2/navigation`
- `/wp/v2/revisions`
- `/wp/v2/posts/<id>/autosaves`
- `/wp/v2/pages/<id>/autosaves`

Some routes appear only on newer core versions, certain configurations, or when the corresponding feature is active.

## Batch Namespace

WordPress also exposes:

- `/batch/v1`

Use this only when the target site supports the batch pattern you need and you have verified the request shape.

## Common Query Controls

Many collection routes accept combinations of:

- `context`
- `page`
- `per_page`
- `search`
- `include`
- `exclude`
- `orderby`
- `order`
- `slug`
- `status`

Common response shapers:

- `_fields`
- `_embed`

## Practical Rule

If the task says "every endpoint", split the problem:

1. use this file for the core family names
2. use `scripts/inspect-rest-api.sh` against the target site for the actual live route list
3. inspect plugin namespaces separately instead of assuming their route structure
