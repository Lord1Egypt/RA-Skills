# Authentication

## Principles

- **Never** put passwords, application passwords, or tokens in chat, Git, or skill files.
- Use **environment variables** or OpenClaw **`skills.entries.<key>.env`** (host runs). In the **sandbox**, set the same secrets/env under **`agents.defaults.sandbox.docker.env`** (or per agent) as needed—see [OPENCLAW_INTEGRATION.md](OPENCLAW_INTEGRATION.md) and [Skills config](https://docs.openclaw.ai/tools/skills-config).

**Connecting an existing site:** Steps and two topologies (REST-only vs REST+WP-CLI on the gateway host) in [CONNECTING.md](CONNECTING.md). OpenClaw: [Skills](https://docs.openclaw.ai/tools/skills), [Skills config](https://docs.openclaw.ai/tools/skills-config).

## Recommended schema (REST)

| Variable | Meaning |
|----------|---------|
| `WORDPRESS_SITE_URL` | Site **base URL** (no trailing slash), e.g. `https://staging.example.com` or with subdirectory `https://example.com/blog`—REST resolves as `{URL}/wp-json/...` |
| `WORDPRESS_USER` | Username for Basic Auth + application password |
| `WORDPRESS_APPLICATION_PASSWORD` | Generated from the WP user profile (not the login password) |

WordPress: Users → Profile → create **Application Passwords**; enforce HTTPS.

The OpenClaw plugin **`wordpress-site-tools`** uses the same three variables for REST (**`wordpress_rest_request`**, **`wordpress_media_upload`**) and for the auth part of **`wordpress_connection_check`**, or optionally `baseUrl` / `user` / `applicationPassword` in `plugins.entries.wordpress-site-tools.config` (see `openclaw-wordpress-tools/README.md`).

Example (illustration only—never commit values):

```bash
curl -sS -u "$WORDPRESS_USER:$WORDPRESS_APPLICATION_PASSWORD" \
  "$WORDPRESS_SITE_URL/wp-json/wp/v2/posts?per_page=1"
```

## WP-CLI

No application password is required when `wp` runs **on a host with access to the installation**. Typically:

- **`WORDPRESS_PATH`**: Directory from which `wp` runs (used as `cwd` by **`wordpress_wp_cli`**) or a fixed `--path=` in documented **`exec`** calls.
- Optional override: `plugins.entries.wordpress-site-tools.config.wordpressPath`.
- Broader WP-CLI commands (beyond the default allowlist): `wpCliAllowPrefixes` in the same plugin config (replaces defaults when non-empty). Presets: [WPCLI_PRESETS.md](WPCLI_PRESETS.md).

See `.env.example` in the skill root.

## Local `.env`

Do **not** commit a `.env` file in the skill directory (see `.gitignore`). Optional: symlink to a secrets store outside the repo.
