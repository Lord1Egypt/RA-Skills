---
name: quarkpan-backup-suite
description: Build and operate a Quark/OpenList-style backup + restore workflow for OpenClaw workspaces, including QR login, account UID binding guard, whole-file cloud upload, dry-run restore, and Lighthouse snapshot policy (manual create only, weekly prompt). Use when users ask to set up/secure Quark backup automation, recovery runbooks, or share this backup capability with other OpenClaw users.
---

# QuarkPan Backup Suite

Use this skill to deploy a production-safe backup workflow with these goals:
- Keep automated workspace backups on Quark Drive.
- Use the OpenList-style non-parallel **whole-file** upload flow for cloud writes.
- Avoid QuarkPan's fragile large-file `parallel_upload` / `X-Oss-Hash-Ctx` path.
- Enforce account binding so uploads cannot silently go to a wrong account.
- Keep system rollback snapshots manual-only (no auto overwrite risk).
- Provide reproducible restore steps and distributable skill package.

## Current upload architecture

The current production path is:

1. QuarkPan remains responsible for QR login / auth status / account binding guard.
2. `upload-quarkpan.sh` runs the account guard before any cloud write.
3. Actual cloud writes use `quark-openlist-upload.py`, a standalone OpenList/Alist-compatible uploader:
   - no `parallel_upload: true`
   - no synthetic `X-Oss-Hash-Ctx`
   - uses server-returned `metadata.part_size`
   - uses server-returned `upload_url` host
   - uploads archive and `.sha256` as whole files
4. `CLOUD_SPLIT_FALLBACK=0` by default. Do not split backups unless the user explicitly requests a temporary emergency workaround.

## Workflow

1. Run preflight checks with `scripts/check_env.sh`.
2. Configure backup policy using `references/commands.md`.
3. Enforce account guard (`bind`, `check`, `rotate-*`) before uploads.
4. Verify restore path with dry-run first.
5. Keep Lighthouse snapshots manual-only; use weekly prompt policy.
6. Package/share this skill with `package_skill.py`.

## Guardrails

- Do not auto-apply destructive restore.
- Do not auto-create system snapshots by cron.
- Require explicit confirmation for snapshot creation and snapshot rollback.
- Keep cloud upload failure non-fatal for local backup success.
- Do not log or publish Quark cookies, preview URLs, or auth tokens.
- Do not revive the old QuarkPan large-file multipart path as the default uploader.

## References

- Command cookbook: `references/commands.md`
- Security and rotation policy: `references/security-policy.md`
- Sharing/export steps: `references/share.md`
