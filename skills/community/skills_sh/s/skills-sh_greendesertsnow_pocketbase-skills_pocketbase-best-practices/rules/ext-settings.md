---
title: Read Settings via app.Settings(), Encrypt at Rest with PB_ENCRYPTION
impact: HIGH
impactDescription: Hardcoded secrets and unencrypted settings storage are the #1 source of credential leaks
tags: settings, configuration, encryption, secrets, PB_ENCRYPTION, extending
---

## Read Settings via app.Settings(), Encrypt at Rest with PB_ENCRYPTION

PocketBase stores every runtime-mutable setting (SMTP credentials, S3 keys, OAuth2 client secrets, JWT secrets for each auth collection) in the `_params` table as JSON. Admin UI edits write to the same place. There are two knobs that matter: (1) **how you read settings from Go/JS** - always via `app.Settings()` at call time, never captured at startup; (2) **how they are stored on disk** - set the `PB_ENCRYPTION` env var to a 32-char key so the whole blob is encrypted at rest. Without encryption, anyone with a copy of `data.db` has your SMTP password, OAuth2 secrets, and every collection's signing key.

**Incorrect (hardcoded secret, captured at startup, unencrypted at rest):**

```go
// ❌ Secret compiled into the binary - leaks via `strings ./pocketbase`
const slackWebhook = "https://hooks.slack.com/services/T00/B00/XXXX"

// ❌ Captured once at startup - if an admin rotates the SMTP password via the
//    UI, this stale value keeps trying until restart
var smtpHost = app.Settings().SMTP.Host

// ❌ No PB_ENCRYPTION set - `sqlite3 pb_data/data.db "SELECT * FROM _params"`
//    prints every secret in plaintext
./pocketbase serve
```

**Correct (env + settings lookup at call time + encryption at rest):**

```bash
# Generate a 32-char encryption key once and store it in your secrets manager
# (1Password, SOPS, AWS SSM, etc). Commit NOTHING related to this value.
openssl rand -hex 16    # 32 hex chars

# Start with the key exported - PocketBase AES-encrypts _params on write
# and decrypts on read. Losing the key == losing access to settings.
export PB_ENCRYPTION="3a7c...deadbeef32charsexactly"
./pocketbase serve
```

```go
// Reading mutable settings at call time - reflects live UI changes
func notifyAdmin(app core.App, msg string) error {
    meta := app.Settings().Meta
    from := mail.Address{Name: meta.SenderName, Address: meta.SenderAddress}
    // ...
}

// Mutating settings programmatically (e.g. during a migration)
settings := app.Settings()
settings.Meta.AppName = "MyApp"
settings.SMTP.Enabled = true
settings.SMTP.Host = os.Getenv("SMTP_HOST") // inject from env at write time
if err := app.Save(settings); err != nil {
    return err
}
```

```javascript
// JSVM
onBootstrap((e) => {
    e.next();

    const settings = $app.settings();
    settings.meta.appName = "MyApp";
    $app.save(settings);
});

// At send-time
const meta = $app.settings().meta;
```

**Secrets that do NOT belong in `app.Settings()`:**

- Database encryption key itself → `PB_ENCRYPTION` env var (not in the DB, obviously)
- Third-party webhooks your code calls (Slack, Stripe, etc) → env vars, read via `os.Getenv` / `$os.getenv`
- CI tokens, deploy keys → your secrets manager, not PocketBase

`app.Settings()` is for things an **admin** should be able to rotate through the UI. Everything else lives in env vars, injected by your process supervisor (systemd, Docker, Kubernetes).

**Key details:**
- **`PB_ENCRYPTION` must be exactly 32 characters.** Anything else crashes at startup.
- **Losing the key is unrecoverable** - the settings blob cannot be decrypted, and the server refuses to boot. Back up the key alongside (but separately from) your `pb_data` backups.
- **Rotating the key**: start with the old key set, call `app.Settings()` → `app.Save(settings)` to re-encrypt under the new key, then restart with the new key. Do this under a maintenance window.
- **Settings changes fire `OnSettingsReload`** - use it if you have in-memory state that depends on a setting (e.g. a rate limiter sized from `app.Settings().RateLimits.Default`).
- **Do not call `app.Settings()` in a hot loop.** It returns a fresh copy each time. Cache for the duration of a single request, not the process.
- **`app.Save(settings)`** persists and broadcasts the reload event. Mutating the returned struct without saving is a no-op.

Reference: [Settings](https://pocketbase.io/docs/going-to-production/#use-encryption-for-the-pb_data-settings) · [OnSettingsReload hook](https://pocketbase.io/docs/go-event-hooks/#app-hooks)
