---
name: wordpress-api-pro
version: 3.9.5
license: MIT-0
description: |
  Production-grade WordPress REST API integration for managing posts, pages, media, WooCommerce products, Elementor content, SEO meta, ACF, and JetEngine fields.
  Use when you need to retrieve, draft, create, or update WordPress content programmatically on sites where the user has provided explicit credentials.
  For any operation that writes to a live site, get explicit user approval for the target site, post/product IDs, and final action before executing.
  Prefer drafts first. Run batch operations in dry-run mode first; use --execute only after review. Remote URL media downloads and local file reads are restricted by safety boundaries.
  Also includes a no-auth Tier-1 site audit (PageSpeed, SSL, security headers, CMS/PHP fingerprint, SEO basics) for cold pre-sale checks, and authenticated plugin/SEO-stack discovery.
permissions:
  env:
    - "WP_URL / WP_SITE_URL, WP_USERNAME / WP_USER, WP_APP_PASSWORD (auth)"
    - "WP_CONFIG (optional sites.json path), WP_ALLOWED_FILE_ROOTS (file-read scope)"
    - "WP_ALLOW_REMOTE_URLS, WP_REQUIRE_HTTPS, WP_REQUIRE_ALLOWLIST, PAGESPEED_API_KEY"
    - "WP_ALLOW_HTTP (comma-separated HOST LIST, never a blanket value), WP_ALLOW_RAW_META"
    - "WP_ALLOW_PROXY (use a configured HTTP(S) proxy for audit/media fetches; off by default because the proxy, not this skill, then decides what it connects to — with it on, URLs and redirect targets are still validated but addresses are not)"
  network:
    - "Outbound HTTPS to the configured WordPress site(s) /wp-json/ REST API — plaintext http:// to a non-local host is refused unless that exact host is named in WP_ALLOW_HTTP"
    - "https://www.googleapis.com/pagespeedonline (site_audit only)"
    - "site_audit reaches the audited site over http:// or https://; every address it connects to, redirects included, must be globally reachable (is_global) and none of loopback, private, link-local, multicast, reserved or unspecified — CGNAT/shared address space (100.64.0.0/10) is refused too. The validated address is the one dialled, so a name cannot resolve differently between the check and the connection; TLS is still verified against the hostname. HTTP(S)_PROXY is ignored for these fetches unless WP_ALLOW_PROXY=1, since a proxy resolves the target itself. Response bodies are capped at 5 MB"
  filesystem:
    - "Read-only, scoped to WP_ALLOWED_FILE_ROOTS (default: cwd)"
  shell: "wp_cli.py spawns python3 <script> subprocesses (subprocess.run with an argv list; no shell interpreter, never shell=True). wp.sh is a bash wrapper around it."
---

# WordPress API Pro

Manage WordPress sites through the REST API. Runs as an OpenClaw skill or in Claude Code.

## Running in Claude Code

This skill runs the `scripts/*.py` directly, from wherever the skill is installed
(`~/.claude/plugins/` for a plugin install, `~/.claude/skills/wordpress-api-pro/`
for the repo's `bash INSTALL.sh` — that installer lives in the git repo, not in
the packaged skill):

- **Auth:** export `WP_URL` / `WP_USERNAME` / `WP_APP_PASSWORD`, or use `config/sites.json` for multi-site.
- **Dependencies:** the ACF / SEO / JetEngine / plugin-detection scripts need `requests` (`python3 -m pip install -r requirements.txt`, ideally in a venv). The pin is a RANGE, `requests>=2.32.3,<3`, not an exact version or a hash lock. That is deliberate: an exact pin stops users receiving patch-level security fixes for the dependency whose advisory is the reason for the lower bound, and this skill has no lockfile-refresh process to compensate. The trade is reproducibility for patchability.
   2.32.0 fixed CVE-2024-35195, where a `Session` that made one `verify=False` request silently skipped certificate verification for every later request to that host, and 2.32.3 closes out that line's follow-up regressions. The core post/page/media/WooCommerce/batch scripts use the stdlib only.
- **Local dev sites** (e.g. `http://site.local`, `localhost`, `*.test`, `*.localhost`) work over plaintext http. Any other host must be https:// unless you name it: `WP_ALLOW_HTTP=staging.example.com` (comma-separated for several). A blanket `WP_ALLOW_HTTP=1` is refused — it used to permit every host, so one variable set for one staging box covered production too.
- **Pairs with the Elementor MCP kit** (`siteagent-elementor-studio`): build page structure with the MCP, then do media uploads, SEO meta, custom fields, and WooCommerce here.

## Safety rules

- **Never publish or update live content without explicit user approval.** Confirm target site, IDs, fields, and status.
- **Use least-privilege credentials.** Prefer a dedicated WordPress user/application password scoped to the required role.
- **Do not store production credentials in the repo.** Use environment variables when possible.
- **Protect config files.** If you create `config/sites.json`, keep it local, untracked, and `chmod 600 config/sites.json`.
- **Batch changes are dry-run by default.** Add `--execute` only after reviewing the dry-run output.
- **A created WooCommerce product is a draft.** WooCommerce publishes a product whose status is omitted; `woo_products.py --action create` sends `draft` unless you pass `--status publish`, and prompts at a TTY before a live one (`--yes` skips, non-interactive runs are never prompted).
- **Targeting every site is blocked by default.** Add `--allow-all` only when the user explicitly approved all configured sites.
- **Local file reads are restricted.** `--content-file` and media uploads can read only from the current working directory by default. Set `WP_ALLOWED_FILE_ROOTS` to opt into another safe directory.
- **Remote media URLs are opt-in.** `upload_media.py` requires `--allow-remote-url` or `WP_ALLOW_REMOTE_URLS=1`, allows HTTPS only, and blocks private/local network hosts.
- **Raw SEO meta keys are refused by default.** `seo_meta.py` writes only keys in the Rank Math / Yoast allowlist; anything else fails, because a typo'd friendly name would otherwise create a junk postmeta row or overwrite a key another plugin owns. Set `WP_ALLOW_RAW_META=1` to write raw keys with a warning. ACF/JetEngine custom-field keys are unaffected — arbitrary keys are their intended API.
- **Interactive publish confirmation on TTY.** `create_post.py` and `update_post.py` prompt for confirmation before `--status publish` when run interactively. Pass `--yes` / `-y` to bypass. Non-interactive/agent runs are unchanged.

## Authentication

Recommended environment variables:

```bash
export WP_URL="https://example.com"
export WP_USERNAME="wp-api-user"
read -rs WP_APP_PASSWORD
export WP_APP_PASSWORD
```

Application Password setup:
1. Open `https://your-site.example/wp-admin/profile.php`.
2. Create a new Application Password for a dedicated API user.
3. Copy it once and store it in a secret manager or environment variable.
4. Rotate/revoke it when no longer needed.

## Quick start

### Read/list posts

```bash
python3 scripts/get_post.py --post-id 123
python3 scripts/list_posts.py --per-page 10 --status publish
```

### Create a draft

```bash
python3 scripts/create_post.py \
  --title "Draft title" \
  --content "Draft content" \
  --status draft
```

### Update a post after approval

```bash
python3 scripts/update_post.py \
  --post-id 123 \
  --title "Approved title" \
  --content "Approved content" \
  --status draft
```

### Read content from a local file safely

By default the file must be under the current working directory:

```bash
python3 scripts/update_post.py \
  --post-id 123 \
  --content-file ./content/post-123.html \
  --status draft
```

To opt into another safe folder:

```bash
export WP_ALLOWED_FILE_ROOTS="/absolute/path/to/approved-content"
python3 scripts/update_post.py --post-id 123 --content-file /absolute/path/to/approved-content/post.html
```

## Multi-site configuration

Copy the template locally:

```bash
cp config/sites.example.json config/sites.json
chmod 600 config/sites.json
```

Use a dedicated user per site and keep `app_password` values local only.

```json
{
  "sites": {
    "sample-site": {
      "url": "https://example.com",
      "username": "wp-api-user",
      "app_password": "",
      "description": "Sample site; put the real credential only in local config/sites.json"
    }
  },
  "groups": {
    "sample": ["sample-site"]
  }
}
```

### CLI wrapper

```bash
./wp.sh --list-sites
./wp.sh sample-site get-post --id 123
./wp.sh sample-site update-post --id 123 --status draft
```

Group operations require an explicit flag:

```bash
./wp.sh sample --execute-group update-post --id 123 --status draft
```

If the group is named `all`, add `--allow-all` only after explicit approval:

```bash
./wp.sh all --execute-group --allow-all update-post --id 123 --status draft
```

## Batch operations

Batch mode is dry-run unless `--execute` is present:

```bash
python3 scripts/batch_update.py \
  --group sample \
  --post-ids 123,456 \
  --status draft
```

Apply after review:

```bash
python3 scripts/batch_update.py \
  --group sample \
  --post-ids 123,456 \
  --status draft \
  --execute
```

Targeting every site requires explicit opt-in:

```bash
python3 scripts/batch_update.py \
  --group all \
  --allow-all \
  --post-ids 123 \
  --status draft
```

## Media upload

Local file upload, restricted to allowed file roots:

```bash
python3 scripts/upload_media.py \
  --file ./media/image.jpg \
  --title "Image title"
```

Remote URL upload, explicit opt-in and HTTPS-only:

```bash
python3 scripts/upload_media.py \
  --file https://cdn.example.com/image.jpg \
  --allow-remote-url \
  --title "Image title"
```

## Plugin integrations

- `scripts/detect_plugins.py` — detect ACF, Rank Math, Yoast, JetEngine.
- `scripts/acf_fields.py` — read/write ACF fields.
- `scripts/seo_meta.py` — read/write Rank Math and Yoast SEO metadata.
- `scripts/jetengine_fields.py` — read/write JetEngine custom fields.
- `scripts/site_audit.py` — no-auth Tier-1 website audit (PageSpeed/SSL/security headers/CMS+PHP/SEO basics). Public probes only; run cold pre-sale.
- `scripts/describe_cpt.py` — discover a CPT's rest_base, taxonomies, and field keys (read-only).
- `scripts/seed_content.py` — batch-create CPT entries with ACF/Jet fields, taxonomies, and featured images from a JSON dataset. **Dry-run by default; pass `--execute` to write.**
- `scripts/elementor_content.py` — read/update Elementor `_elementor_data`.
- `scripts/woo_products.py` — manage WooCommerce products.

## Seeding dynamic content (CPT)

For dynamic sites (JetEngine/ACF listings), populate the entries the listings render:

1. `describe_cpt.py --post-type projects` — learn the rest_base, taxonomies, field keys.
2. Write a JSON dataset (array of `{post_type, title, content, status, terms, featured_image, acf, jet}`).
3. `seed_content.py --dataset data.json` — review the dry-run plan (no writes, stdlib-only).
4. `seed_content.py --dataset data.json --execute` — create (drafts by default).

Notes: the CPT, taxonomies, and ACF field-groups must already exist (admin-side).
`featured_image` accepts a media id or a URL/path (URL fetch needs `--allow-remote-url`).
`--execute` needs the `requests` dependency (used by the ACF/Jet writers). Re-running
creates duplicates (no upsert yet).

## Verification before live writes

Before any live mutation:
1. Confirm the site URL.
2. Confirm post/page/product IDs.
3. Confirm fields and status.
4. Prefer `draft` unless the user explicitly approves `publish`.
5. Run dry-run for batch operations.
6. Keep a backup/export for critical content.
