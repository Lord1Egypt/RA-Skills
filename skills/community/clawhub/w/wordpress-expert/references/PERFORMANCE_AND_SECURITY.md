# Performance and security (agent checklist)

Short, actionable items for agents working on WordPress via OpenClaw. For **coding rules**, see [PLUGIN_DEV_PLAYBOOK.md](PLUGIN_DEV_PLAYBOOK.md) and [SAFETY.md](SAFETY.md).

**Handbooks:** [Optimization](https://developer.wordpress.org/advanced-administration/performance/optimization/), [Security](https://developer.wordpress.org/apis/security/).

## When to load

- Slow queries, high TTFB, or “site feels heavy”.
- Hardening before launch, credential hygiene, upload hardening.
- Reviewing custom SQL or loops in theme/plugin code.

## Performance

### Queries

- **N+1:** avoid `get_post_meta` inside loops over posts—batch with `update_post_meta_cache`, custom queries, or object caching patterns ([WP_Query optimization](https://developer.wordpress.org/reference/classes/wp_query/)).
- **`WP_Query` flags:** when pagination counts are not needed, `no_found_rows => true`; disable meta/term caches if unused (`update_post_meta_cache`, `update_post_term_cache`).
- **`fields => 'ids'`** when only IDs are needed.

### Caching

- **Transients** for expensive computed lists—sensible TTL, clear on relevant updates when possible.
- **Object cache** (Redis/Memcached) when host provides it—do not assume in generic skill instructions; mention when detected via `wordpress_connection_check` / site docs.

### Assets

- Enqueue scripts/styles with **`wp_enqueue_*`** and version (`filemtime` or plugin version).
- Avoid loading admin assets on the front end and vice versa.

### Media

- Prefer **`wordpress_media_upload`** when allowed instead of shell `curl` for media—clearer auth and limits.

## Security

### Data handling

- **Sanitize** input; **escape** output (context-appropriate functions).
- **Capabilities** + **nonces** for admin and AJAX actions.
- **`$wpdb->prepare`** for all SQL with variables—never concatenate raw user input into queries.

### File uploads

- Validate mime/extension per project rules; store outside webroot when the architecture requires it; never execute uploaded PHP.

### REST

- **`permission_callback`** must reflect minimum privilege for the operation.
- Do not expose internal paths or secrets in REST responses—align with MU helper’s minimal fields ([MU_HELPER.md](MU_HELPER.md)).

### Credentials

- Application passwords and Basic auth only via env/config—[AUTH.md](AUTH.md). Never echo secrets in tool output or chat.

## WP-CLI / exec

- Prefer **`wordpress_wp_cli`** within allowlist over free `exec` for predictable operations.
- Destructive maintenance (`cache flush`, `rewrite flush`)—staging first; see [WPCLI_PRESETS.md](WPCLI_PRESETS.md) and [SAFETY.md](SAFETY.md).

## Verification

After changes: measure with before/after if tools allow (e.g. `curl -w "%{time_total}"`), or ask the user to verify in staging. Read-after-write for code edits: [WORKFLOWS.md](WORKFLOWS.md).
