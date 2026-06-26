# Command Cookbook

## 1) Quark login and account binding

```bash
scripts/backup/quarkpan-login.sh
scripts/backup/quark-account-guard.sh bind --confirm YES_I_UNDERSTAND
scripts/backup/quark-account-guard.sh status
```

## 2) Workspace backup + cloud upload

Current Quark cloud upload path uses the OpenList-style non-parallel whole-file uploader:

- uploader: `scripts/backup/quark-openlist-upload.py`
- wrapper: `scripts/backup/upload-quarkpan.sh`
- config: `CLOUD_SPLIT_FALLBACK=0`, `QUARK_OPENLIST_UPLOADER=.../quark-openlist-upload.py`
- account safety: still runs QuarkPan auth status + account binding guard before upload

```bash
scripts/backup/backup-cron.sh daily
scripts/backup/backup-cron.sh weekly
```

Manual cloud-upload smoke test:

```bash
scripts/backup/upload-cloud.sh /path/archive.tar.gz /path/archive.tar.gz.sha256 smoke-openlist
```

## 3) Restore validation (must dry-run first)

```bash
scripts/backup/restore-quarkpan.sh --from-index /root/.openclaw/backup/indexes/cloud-daily-YYYY-MM-DD.txt --dry-run
```

## 4) Lighthouse snapshot (manual only)

Create snapshot:
```bash
scripts/backup/lighthouse-snapshot-create.sh --wait
```

Prune old snapshots (dry-run):
```bash
scripts/backup/lighthouse-snapshot-prune.sh --keep 2
```

Prune apply:
```bash
scripts/backup/lighthouse-snapshot-prune.sh --keep 2 --apply
```

Rollback snapshot (danger):
```bash
scripts/backup/lighthouse-snapshot-apply.sh --snapshot-id lhsnap-xxxx --confirm YES_I_UNDERSTAND
```

## 5) System-state docs package

```bash
scripts/backup/system-state-backup.sh
```
