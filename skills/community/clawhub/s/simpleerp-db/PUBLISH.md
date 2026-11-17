# ClawHub publish checklist — simpleerp-db

Before uploading to [clawhub.ai](https://clawhub.ai):

1. **SKILL.md** has `name`, `description`, `version`, and `metadata.openclaw`.
2. All env vars used in scripts appear in `requires.env` or `envVars` in frontmatter.
3. **`.clawhubignore`** excludes `node_modules/`, `.env`, `output/`, and `schema/TABLES.sql`.
4. No binary files in the bundle (no `oracledb` `.node` files); total size under 50MB.
5. Publish: `clawhub skill publish ./simpleerp-db` or upload the folder via the ClawHub web UI.
6. Fresh-install test: `npm install` → copy `.env.example` to `.env` → `npm run setup` → `npm run sql -- "SELECT 1 FROM DUAL"`.

On **Windows PowerShell**, if `npm` is blocked: `Set-ExecutionPolicy RemoteSigned -Scope Process` (current session only), or run `node scripts/setup.mjs` directly.

Published skills are licensed under **MIT-0** per ClawHub policy.
