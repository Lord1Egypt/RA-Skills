# Authentication and account sites

Read early for an actual Vibbit analysis, resource query, or production task. Discussion, dry runs, and explicitly local-only work do not require setup. See [API client](api-client.md) for installation paths.

## Select the account site

The single Skill supports both official sites. Their accounts, API keys, credits, products, and assets are independent. Conversation language and the deliverable's target market do not change the site.

Selection order: an explicit `--region cn|global` / `VIBBIT_REGION` or host API override; saved selection (including a single legacy regional key); a website hint supplied with `--site`; international default for a new installation without context. A conflicting explicit region and `VIBBIT_BASE_URL` is rejected before any network call. Website hints never replace an existing site.

Website installation prompts carry their source:

- China: `--site https://app.vibbit.cn`, with [China API Keys](https://app.vibbit.cn/api-keys).
- International: `--site https://app.vibbit.ai`, with [international API Keys](https://app.vibbit.ai/api-keys).
- A direct GitHub/terminal installation with no existing configuration uses the international site.

```bash
node "$VIBBIT_SKILL_DIR/scripts/vibbit.js" auth_status
node "$VIBBIT_SKILL_DIR/scripts/vibbit.js" auth_status --site https://app.vibbit.cn
```

These offline commands report the selected site, `selection_source`, credential source, and correct account links without displaying the key. Credential priority is `VIBBIT_API_KEY`, then `VIBBIT_OPENAPI_KEY`, then the selected site's private file. If configured, use `auth_status --check` once before the first operation, then reuse the verified configuration.

When upgrading from 2.15, a single existing `cn.json` or `global.json` remains selected without moving its key. If both exist without a saved selection, explicitly choose the account before making requests. Do not infer the right account from balances, language, or a failed login. Never try a key at the other site automatically.

## Configure and continue

If missing credentials, preserve the task using [account continuation](account-continuation.md), then open the supported setup entry. Prefer native host credential settings when available. Do not invent a settings page or ask for a key in chat. On an accessible local macOS/Linux computer:

```bash
node "$VIBBIT_SKILL_DIR/scripts/vibbit.js" auth_setup --open --lang en
node "$VIBBIT_SKILL_DIR/scripts/vibbit.js" auth_setup --open --site https://app.vibbit.cn --lang zh-CN
```

Use the actual website hint, if present, and a page language matching the conversation (`en` or `zh-CN`). The language flag never changes the account site. The local page displays the selected website, links to that site's API Keys, and lets the user choose the other official site. A fixed host region/base locks the site to that environment. Switching a page's site clears the input before a new key is pasted. The user creates and pastes the key; the agent must not inspect the field, clipboard, or request body.

Verification calls only the selected site's `GET /health`, with redirects disabled. Only a successful verification and save changes the remembered site. Cancellation, rejection, or network failure preserves existing credentials and selection. Keep the setup process alive with a supported persistent session for up to ten minutes. If opening fails, show its `setup_url`; expiry is not success. Success returns `configured=true, verified=true` and the actual site, so continue without another health call.

The helper listens only on `127.0.0.1` with a random session URL and closes on success, cancellation, or expiry. Do not publicly forward its port. Credentials are unencrypted private files under `~/.vibbit/credentials/` (directory 0700, files 0600): `cn.json`, `global.json`, and an `account.json` selection without a key. They stay outside the Skill during updates. `VIBBIT_CONFIG_DIR` can select another absolute private directory outside projects, Skills, synced folders, and release packages.

On Windows, shared devices, cloud agents, containers, and remote hosts without an accessible local browser, use the host's credential settings in the actual execution environment. Pair the key with `VIBBIT_REGION=cn` or `VIBBIT_REGION=global`. Existing environment keys take priority, so the local form refuses to save a key that would be overridden. If a pre-upgrade host key was configured without a region/base, set its site explicitly before verification; an opaque key cannot identify its origin.

Missing shell variables do not prove the user never configured a key. Check the user-identified host injection and execution environment without dumping configuration files, environment values, or shell profiles. Never put keys in chat, command arguments, request files, or journals; never create keys for the user through browser automation.

## Switch, clear, and verify

For an explicit switch to an already configured site:

```bash
node "$VIBBIT_SKILL_DIR/scripts/vibbit.js" account_select --region cn
```

This verifies that site's credential before remembering it. If it has no key, open `auth_setup --region cn --open` instead. Use `global` for the international site. A per-command `--region` overrides only that call; `account_select` or successful setup persists the choice. Host environment overrides still take priority; change those through their original settings.

Saved keys are bound to their exact official API base and never follow custom destinations. Custom `VIBBIT_BASE_URL` environments require matching host credentials and have no guessed website links. After an account/site switch, refresh private products, avatars, voices, and other resource IDs. Resume an old task using its original account/base, as required by [task lifecycle](task-lifecycle.md).

A successful health check proves authentication and reachability, not every model, permission, or sufficient credits. A 401 needs credential attention; a 403 may involve IP allowlists, permissions, or task ownership. On an explicit removal request, `auth_clear` deletes only the selected site's local key; it neither edits environment variables nor revokes the server key. Revocation happens on the API Keys page.

[Authentication reference](https://vibbit.apifox.cn/514565013e0) · [Troubleshooting](troubleshooting.md)
