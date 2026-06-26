---
name: wordpress-oauth
description: Start and complete WordPress.com OAuth and publish posts through the WordPress.com REST API. Use when you need to generate an authorization URL, exchange callback code for an access token, validate token health, or publish draft/published posts to a WordPress.com or Jetpack-connected site.
---

# WordPress OAuth Skill

Use this skill to run a human-in-the-loop OAuth flow and publish posts with a stored bearer token.

## Files in this skill

- Script: `{baseDir}/wp_oauth_skill.py`
- OAuth state store: `{baseDir}/oauth_state.json`
- Credential store: `{baseDir}/credentials.json`

This skill stores state and credentials in files inside this skill directory.

## Commands

Run the script with Python 3:

```bash
python3 {baseDir}/wp_oauth_skill.py --help
```

### 1) Begin OAuth

```bash
python3 {baseDir}/wp_oauth_skill.py begin-oauth \
  --client-id "$WPCOM_CLIENT_ID" \
  --redirect-uri "$WPCOM_REDIRECT_URI" \
  --scope "posts media" \
  --blog "$WPCOM_SITE"
```

Returns `auth_url` and `state`. Open the URL, approve access, then copy the callback URL.

### 2) Exchange Token

```bash
python3 {baseDir}/wp_oauth_skill.py exchange-token \
  --client-id "$WPCOM_CLIENT_ID" \
  --client-secret "$WPCOM_CLIENT_SECRET" \
  --redirect-uri "$WPCOM_REDIRECT_URI" \
  --callback-url "https://example/callback?code=...&state=..."
```

Validates CSRF `state`, exchanges code for token, and writes credentials to `{baseDir}/credentials.json`.

### 3) Token Info

```bash
python3 {baseDir}/wp_oauth_skill.py token-info --client-id "$WPCOM_CLIENT_ID"
```

Checks token validity with WordPress token-info endpoint.

### 4) Publish Post

```bash
python3 {baseDir}/wp_oauth_skill.py publish-post \
  --site "$WPCOM_SITE" \
  --title "My post" \
  --content "<p>Hello from OpenClaw</p>" \
  --status draft
```

Publishes a post via `POST /rest/v1.1/sites/$site/posts/new` using the stored token.

## Recommended flow

1. Run `begin-oauth`.
2. Open `auth_url` in browser and authorize.
3. Paste callback URL into `exchange-token`.
4. Optionally run `token-info`.
5. Run `publish-post`.

## Security notes

- Never share `credentials.json` or client secrets.
- Keep first test posts as `draft`.
- Re-run `begin-oauth` if callback state fails or auth code expires.
