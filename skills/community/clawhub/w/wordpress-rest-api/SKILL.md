---
name: wordpress-rest-api
description: Work with the WordPress REST API for route discovery, authentication, reads and writes, core endpoint selection, and custom namespace inspection. Use when a WordPress task needs `/wp-json`, application passwords, cookie or nonce auth, post or media endpoints, settings access, or live discovery of plugin-defined REST routes.
metadata: {"openclaw":{"emoji":"🌐"}}
---

# WordPress REST API

Use this skill when the correct interface is HTTP against a WordPress site, not shell access with `wp`.

This skill is built around two facts:

- WordPress core ships a large REST surface under `/wp-json`
- the truly complete endpoint list is site-specific because plugins and custom code can register more routes

Treat the reference files as the core map and use the discovery script for the live map.

## Use This Skill For

- inspecting `/wp-json` on a live site
- choosing the right core route before writing code or automation
- authenticating with application passwords for machine-to-machine calls
- checking cookie and nonce-based admin flows
- inspecting custom plugin routes and namespaces
- figuring out which methods and args a route accepts
- designing or reviewing `register_rest_route()` implementations

## Do Not Use This Skill For

- normal shell-based site administration when `wp` access already exists
- WP-CLI command or package development
- pretending the static reference files can enumerate plugin routes on every site

## Workflow

### 1. Discover The Live Route Index

Start with:

```bash
scripts/inspect-rest-api.sh --site https://example.com
```

This fetches the site index at `/wp-json/`, prints the namespaces, and lists the live routes that site exposes.

If you need one route only:

```bash
scripts/inspect-rest-api.sh --site https://example.com --route /wp/v2/posts
scripts/inspect-rest-api.sh --site https://example.com --route /wp/v2/posts --method OPTIONS
```

Read [references/core-endpoints.md](references/core-endpoints.md) before assuming a core route name from memory.

### 2. Choose The Right Auth Model

Default rule:

- external automation: use application passwords over HTTPS
- logged-in browser admin flow: use cookie auth plus nonce handling
- public read-only data: use unauthenticated GET only when the site exposes it intentionally

Read [references/auth-and-discovery.md](references/auth-and-discovery.md).

### 3. Prefer Core Namespaces First

Core routes are more stable than plugin routes.

Common starting points:

- posts, pages, media, comments, categories, tags
- users and settings when authenticated
- templates, template parts, patterns, and block-editor related routes on newer installs
- plugins and themes only when the target site and permissions allow them

### 4. Inspect Custom Routes Live

For plugin or theme APIs, do not guess.

Use the discovery index and `OPTIONS`:

```bash
scripts/inspect-rest-api.sh --site https://example.com --route /my-namespace/v1/report --method OPTIONS
```

Then read [references/custom-route-rules.md](references/custom-route-rules.md) if you are implementing or reviewing the server-side route registration.

### 5. Keep Calls Small And Explicit

Default patterns:

- use `?_fields=` to trim large responses
- use `page`, `per_page`, `search`, `orderby`, and `order` instead of client-side filtering when possible
- check pagination headers such as `X-WP-Total` and `X-WP-TotalPages`
- use `OPTIONS` before write automation when you do not control the site code

## Files

- `scripts/inspect-rest-api.sh`: discover the live route index or inspect a single route with GET or OPTIONS
- `references/core-endpoints.md`: core route families worth checking before you inspect plugin namespaces
- `references/auth-and-discovery.md`: application passwords, cookie auth, nonces, and route discovery rules
- `references/custom-route-rules.md`: implementation-side guidance for registering or reviewing custom routes
