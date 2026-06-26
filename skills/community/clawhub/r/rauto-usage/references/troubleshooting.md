# Rauto Troubleshooting

Use this file when users report failures, wrong output, or UI confusion.

## Connection failures

### `Failed to connect: async ssh2 error: Disconnected`

1. Verify host reachability and SSH service.
2. Verify SSH port (`--ssh-port` or Web `port` field), default should be `22`.
3. Verify username/password and optional enable password.
4. Verify device profile matches vendor behavior.

### "Web port 3000 overrides SSH port 22"

- Clarify: Web server port (`rauto web --port 3000`) is HTTP port only.
- SSH port always comes from connection fields (`--ssh-port` / Web `port` input).

## Template and tx issues

### Template not found

1. Run `rauto templates list`.
2. Confirm file exists under `~/.rauto/templates/commands/`.
3. Confirm template name/path is correct.

### Tx rollback errors

1. Per-step mode:
   - Ensure rollback list aligns with command list.
   - Empty rollback command is allowed and will be skipped.
2. Whole-resource mode:
   - Ensure `resource_rollback_command` exists.
   - Ensure `trigger_step_index` is valid.

## Recording and replay issues

### Missing fields in record entries

1. Ensure recording is not disabled.
2. Prefer `full` when deep event diagnostics are required.
3. Verify in raw JSONL view for full fields.

### Replay cannot find command

1. Use `--list` (CLI) or `List Records` (Web) first.
2. Match exact command string and mode if mode filter is used.

## History and interactive issues

### History list empty

1. Ensure operations were executed with a selected saved connection.
2. Check connection history limit and filters.

### Interactive tab no response

1. Ensure session started successfully.
2. Ensure connection fields or saved connection are valid.
3. Stop and re-start session if prompt state is stale.

## Backup/restore issues

### Backup list empty

- Run `rauto backup create` first.
- Verify `~/.rauto/backups/` exists and is readable.

### Restore did not match expectation

- Use merge restore first (`Restore (Merge)`).
- Use replace restore only for full reset (`Restore (Replace)` / `--replace`).
- Re-check connections/templates/profiles after restore.

### Download backup fails

- Ensure selected archive is from backup list (not random path).
- Refresh backup list and retry.

## UI style/interaction issues

### Styling looks broken

1. Rebuild Tailwind output when in source workflow.
2. Hard-refresh browser.

### Drawer/floating actions not visible

- Ensure required state is present (for recording drawer visibility, device context must be selected).
