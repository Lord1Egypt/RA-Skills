# Time Clawshine — OpenClaw Time Machine

Restic-powered encrypted snapshots for OpenClaw.

Time Clawshine is a local-first time machine for agent memory, sessions, config,
and workspace state. It keeps hourly incremental snapshots, stores only changed
data, and restores by time, snapshot, or file when an agent session corrupts
state or overwrites important memory.

## Highlights

- Hourly encrypted incremental snapshots via restic
- Restore by time, snapshot ID, or individual file
- Local-only privacy defaults: Telegram, healthcheck, and update checks are off
- Integrity checks, retention, prune, and status dashboard
- Setup preview with `setup.sh --dry-run`
- Strong restore safety gate for `/`

## Best For

- Rolling OpenClaw memory back to an exact hour
- Recovering from bad sessions, corrupted context, or accidental overwrites
- Keeping a compact local recovery layer before full VM or cloud DR backups

## Not A Plain Tarball

Most simple backup skills create timestamped archives. Time Clawshine uses restic
for encryption, deduplication, snapshots, and verified restores.
