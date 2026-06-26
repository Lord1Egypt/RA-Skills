# Security Policy

## Account binding model

- First login must run `bind` and save bound UID fingerprint.
- Every upload must pass `check` before cloud write.
- UID mismatch => block upload and alert.
- The OpenList-style uploader reuses the QuarkPan cookie jar, so the existing UID binding guard remains mandatory before upload.

## Upload safety model

- Default upload path is OpenList-style non-parallel whole-file upload via `scripts/backup/quark-openlist-upload.py`.
- Keep `CLOUD_SPLIT_FALLBACK=0` for production backups.
- Do not use QuarkPan's old large-file `parallel_upload` + synthetic `X-Oss-Hash-Ctx` path as default; it can reach multipart completion and then fail `file/upload/finish` with `43001 request cpp error`.
- Upload logs must not expose Quark cookies, auth keys, preview URLs, or share tokens.
- Cloud upload failure remains non-fatal for local backup success; failed cloud jobs may be retried later.

## Rotation (changing Quark account)

Use explicit two-step flow only:
1. `rotate-arm --ttl-min 10` to generate one-time token.
2. Re-login to target account.
3. `rotate-apply --token <token> --confirm YES_I_UNDERSTAND`.

If token expired or missing, rotation is denied.

## Snapshot safety model

- Never auto-create snapshots on schedule.
- Prompt weekly; create only on explicit owner request.
- Keep 2-3 known good snapshots.
- Require explicit confirmation for rollback.

## Restore safety model

- Always run `--dry-run` before real apply.
- Keep rollback checkpoint before apply.
- Treat cloud upload failure separately from local backup status.
