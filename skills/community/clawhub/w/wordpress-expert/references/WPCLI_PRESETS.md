# WP-CLI allowlist presets (`wpCliProfile` / `wpCliAllowPrefixes`)

OpenClaw tool **`wordpress_wp_cli`** only allows commands whose **token prefix** is in a list. Resolution **order**:

1. **`wpCliAllowPrefixes`** (plugin config): if **at least one** entry → **replaces** everything else (defaults and profile).
2. Else **`wpCliProfile`**: named preset → built-in list in the plugin (`openclaw-wordpress-tools/src/wp-cli-presets.ts`, kept in sync with this file).
3. Else **builtin-default** (as `builtin-default` below).

**Important:** With a manual `wpCliAllowPrefixes` list, everything you want allowed (including `core version`) must appear in the list.

Each string is a prefix of **tokens after `wp`**, space-separated, e.g. `"post list"` allows `wp post list …`.

Global **blocklist** (always denied, even in custom lists): e.g. `eval`, `eval-file`, `shell`, `cli`; for `db` e.g. `query`, `reset`, `clean`, `import`, `export`. See plugin README.

---

## Preset: `builtin-default` (no config)

If you set **no** `wpCliAllowPrefixes` and **no** `wpCliProfile`, these apply (equivalent prefixes). Optional explicit:

```json5
wpCliProfile: "builtin-default",
```

- `core version`
- `core is-installed`
- `post list`
- `post get`
- `plugin list`
- `theme list`
- `option get`
- `user list`

**Risk:** low (mostly read-only).

---

## Preset: `extended-read`

Explicit list if you want defaults plus **read-only** expansion.

**Short (profile instead of long list):**

```json5
wpCliProfile: "extended-read",
```

**Or** manual `wpCliAllowPrefixes`:

```json5
wpCliAllowPrefixes: [
  "core version",
  "core is-installed",
  "core verify-checksums",
  "post list",
  "post get",
  "page list",
  "page get",
  "plugin list",
  "theme list",
  "option get",
  "user list",
  "rewrite list",
  "db tables",
  "db check",
  "db size",
],
```

**Note:** `db tables` / `db check` / `db size` are allowed while the second token is **not** on the blocklist.

---

## Preset: `content-staging`

For **staging**: create/edit posts. **Do not** blindly use on production.

**Short:**

```json5
wpCliProfile: "content-staging",
```

**Or** manual:

```json5
wpCliAllowPrefixes: [
  "core version",
  "post list",
  "post get",
  "post create",
  "post update",
  "post delete",
  "page list",
  "page get",
  "page create",
  "page update",
  "media list",
  "media get",
  "media import",
],
```

**Risk:** medium to high (`post delete`, `media import`). Backup and explicit user approval in chat per [SAFETY.md](SAFETY.md).

---

## Preset: `staging-admin`

Plugin/theme lifecycle on **staging** (activation, install from wordpress.org).

**Short:**

```json5
wpCliProfile: "staging-admin",
```

**Or** manual:

```json5
wpCliAllowPrefixes: [
  "core version",
  "plugin list",
  "plugin status",
  "plugin activate",
  "plugin deactivate",
  "plugin install",
  "plugin update",
  "theme list",
  "theme activate",
  "theme install",
  "theme update",
  "cache flush",
  "rewrite flush",
  "option get",
],
```

**Risk:** high—changes live site behavior and can pull updates. Do not mix with production URLs in the same OpenClaw config without review.

---

## Preset: `dev-local`

**Local** development only (scaffold, i18n). **`eval` / `eval-file` are always blocked** in the plugin and must not be in allowlists.

**Short:**

```json5
wpCliProfile: "dev-local",
```

**Or** manual:

```json5
wpCliAllowPrefixes: [
  "core version",
  "scaffold plugin",
  "scaffold post-type",
  "scaffold taxonomy",
  "i18n make-pot",
  "i18n make-json",
],
```

Optional only if needed: `package install` (WP-CLI packages; own risk). Keep list minimal and extend deliberately.

---

## `openclaw.json` snippet

```json5
plugins: {
  entries: {
    "wordpress-site-tools": {
      enabled: true,
      config: {
        wordpressPath: "/path/to/wp-installation",
        wpCliProfile: "content-staging",
        // Power user (replaces profile when non-empty):
        // wpCliAllowPrefixes: [ "core version", "post list", ... ],
      },
    },
  },
},
```

`wordpressPath` can override `WORDPRESS_PATH` from the environment (see plugin README).

---

## OpenClaw alignment

- Plugin config follows schema in [openclaw.plugin.json](../../openclaw-wordpress-tools/openclaw.plugin.json) (`configSchema`).
- Changes to `openclaw.json` (allowlists, plugin config): **`openclaw gateway restart`**—see [CONNECTING.md](CONNECTING.md) / [README.md](../README.md) (gateway vs chat; `/new` does not replace restart).

See also [CONNECTING.md](CONNECTING.md).
