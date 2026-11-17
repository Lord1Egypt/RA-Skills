---
name: webstudio-cms
description: "Set up, administer, build, design, and publish with Webstudio (self-hosted or Cloud). Covers install/self-hosting, the Builder UI, the programmatic build path (writing Webstudio-native build objects into Postgres), styling and design tokens, assets, publishing, domains, and advanced features (CMS, data variables, forms, integrations). Use when working on a Webstudio site, installing/configuring one, building or fixing pages, applying styles, editing the canvas, uploading assets, managing domains, or publishing. Triggers: webstudio, cms, build pages in webstudio, webstudio publish, webstudio style, webstudio asset, webstudio domain, webstudio install, webstudio self-host."
---

# Webstudio Self-Hosted CMS

Build pages by writing Webstudio-native build objects into the Postgres `Build` row,
then publish via the publisher API. This skill manages a self-hosted Webstudio
instance (Docker Compose) and everything you can do with it.

## Quick Reference

| Topic | File |
|-------|------|
| Install / self-host setup, CLI, deploy | `install.md` |
| Security boundaries, credentials, approval gates | `security.md` |
| Authenticated PostgREST migration | `postgrest-auth.md` |
| Stack, services, health, gotchas | `database.md` (stack) |
| Build table schema, PostgREST, load/commit | `database.md` |
| Element tree, pages, instances, props | `build-objects.md` |
| Styling, css-data parser, tokens, breakpoints | `styling.md` |
| Pages, folders, assets, MinIO storage | `assets-pages.md` |
| Publishing, domains, auth tokens | `publishing.md` |
| Canvas verification, Playwright audit | `verification.md` |
| Full documented API surface | `api.md` |
| The Builder UI (canvas, navigator, modes) | `ui-builder.md` |
| Webstudio design system (tokens, variables) | `design.md` |
| Advanced features (CMS, variables, forms, AI) | `features.md` |

Read the file for the area you're working in BEFORE touching the build. The master
file stays lean on purpose - detail lives in the per-area files.

## Where things live

This skill is generic to any self-hosted Webstudio deployment. Replace the placeholders
with your own values before relying on them:

- Deployment: `<your-dir>/docker-compose.yml` and its deployment-managed secret/config sources.
  Do not read `.env` automatically; see `security.md`.
- This skill folder: the skill itself (publishable as-is, pure markdown - no runnable code)

## Critical Rules

1. **Read `security.md` before any login, database write, asset change, domain change, or publish.**
2. **Identify the PostgREST profile before acting.** Broad internal `anon` privileges plus
   Docker-network isolation are the current community self-host default. Preserve that capability
   when required, but never expose it. Read the validation status and bounded-use procedure in
   `postgrest-auth.md`. Treat its JWT profile as a staged migration until it passes the documented
   disposable-stack test; do not revoke `anon` first and break the Builder.
3. **Do not discover credentials.** Use an existing authenticated session or a credential that the
   operator explicitly authorizes through an approved secret-injection mechanism. Never read,
   print, log, commit, or paste secret values.
4. **Get explicit approval before external or production changes.** Publishing, DNS changes,
   account changes, and destructive database or asset operations require a named target and a
   final user confirmation.
5. **Use the official CLI/MCP for native project edits when the Builder supports it.** Use direct
   database operations only as the documented self-hosted maintenance fallback.
6. **One fix per turn. Save a NEW named copy after every change.** Never overwrite in place.
7. **Resolve one exact draft by project ID and build ID.** Never update every row whose
   `deployment` is null.
8. **Back up the exact row before a direct database edit.** Use a transaction, bound parameters,
   optimistic concurrency, and an exact one-row result. Roll back on any mismatch.
9. **Never hand-write a style value.** Use Webstudio's own css-data parser (see `styling.md`).
10. **When you mutate instances, preserve every loaded namespace and metadata field.** Direct SQL
   must also advance `version`, `lastTransactionId`, and `updatedAt` as Webstudio does.
11. **Every styled element needs a bound local style source** in `styleSourceSelections`, or the
   style silently won't apply.
12. **Styles are element-scoped with no cascade.** Apply every needed property to every target
   instance; don't rely on inheritance.
13. **Publish SSG (`buildMode:"ssg"`), not SSR** unless the operator has deliberately configured
   the additional SSR runtime boundary.
14. **Verify with canvas DOM measurements, not eyeballs.** Text-only, no images into the model.
15. **Assets upload to MinIO** (S3-compatible); they are not stored in Postgres.

## Standard Workflow

1. Confirm the target deployment and authorization boundary (`security.md`).
2. Prefer the official CLI/MCP linked with a project-scoped Build-access share link.
3. Use `meta.index`, request only the needed tools, and dry-run supported mutations.
4. Make the requested change in Webstudio's native model and verify the committed version.
5. If the CLI/MCP cannot perform the operation, use the exact-row database fallback in
   `database.md`; do not silently switch to anonymous PostgREST.
6. Verify by inspecting the canvas DOM or XML (`verification.md`).
7. Publish only after separate explicit approval (`publishing.md`).

## Memory

Operator/instance-specific preferences are not part of this published skill. The
skill is generic; any local customization lives in your own deployment notes,
not here.
