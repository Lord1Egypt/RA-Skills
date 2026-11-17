# Recorder Security And Operations

## Pinned Installation

Installing the CLI is a separate user-authorized action. The skill does not download, install, or update it automatically. Use the [v0.1.0 release](https://github.com/baijian/token-stats/releases/tag/v0.1.0), not a moving latest URL or automatic source archive. The distribution repository does not include CLI implementation source.

`scripts/cli-release.json` pins archive and executable SHA-256 values for `darwin_arm64`, `darwin_amd64`, `linux_arm64`, `linux_amd64`, and `windows_amd64`. All five archives were checked against release checksums and GitHub asset digests on 2026-11-05. Checksums detect mismatches, not malicious behavior; release checksums and artifacts share a publisher. These hashes are not signatures, provenance attestations, or an independent source audit.

After approval, download the exact archive into a dedicated staging directory. Before extraction, compare SHA-256 to `archive_sha256` in the manifest, not only a freshly downloaded checksum. For Apple Silicon:

```bash
shasum -a 256 token-stats_v0.1.0_darwin_arm64.tar.gz
# Compare with the manifest, stop on mismatch, then extract.
tar -xzf token-stats_v0.1.0_darwin_arm64.tar.gz
python3 -I /absolute/path/to/token-stats-skill/scripts/token_recorder.py verify \
  --bin "$PWD/token-stats_v0.1.0_darwin_arm64/token-stats"
```

Only after successful verification, install into the approved location. Review and preserve an existing destination before replacing it. Never elevate with sudo or overwrite an unknown program automatically. Verify the final absolute binary path before `version --output json`.

The wrapper accepts only the pinned executable hash for the current OS/architecture. It resolves PATH/symlinks to an absolute path, requires trusted ownership and no group/other-writable executable or ancestors, and hashes before every run. Mismatch fails closed without execution. A newer CLI needs a reviewed manifest update, not a bypass flag.

Wrappers require Python 3.9+ and POSIX descriptor APIs (macOS/Linux). On Windows use the verified CLI directly and separately approved scheduling; these wrappers do not support Windows. Output paths must not contain symlinks: for example, use canonical `/private/tmp`, not `/tmp`, on macOS.

## One-Off Recording

```bash
TOKEN_STATS_BIN=/absolute/path/to/token-stats AI_TOKEN_AGENT=codex \
  AI_TOKEN_OUTPUT=summary ./scripts/record-token-usage.sh
```

The wrapper always runs offline `usage --refresh --output json`, never sync or authentication commands.

| Variable | Meaning/default |
| --- | --- |
| `TOKEN_STATS_BIN` | CLI path/command; legacy `AI_TOKEN_STATS_BIN` fallback; default `token-stats` |
| `AI_TOKEN_AGENT` | Supported selector; default **codex**, changed from old wrapper's `all` |
| `AI_TOKEN_DAY` | ISO date; default today |
| `AI_TOKEN_DATA_DIR` | Default `~/.local/data/cycling-health-cli/token-usage` |
| `AI_TOKEN_<SOURCE>_HOME` | Eight local overrides; use `DEEPSEEK`, `WORKBUDDY_AI`, etc. |
| `AI_TOKEN_OUTPUT` | `json` for interactive use, `summary`, or `quiet`; default `json` |
| `AI_TOKEN_STATUS_FILE` | Optional private minimal latest-status JSON |
| `AI_TOKEN_RUN_DIR` | Opt-in full per-run snapshots; **unset by default** |
| `AI_TOKEN_RETENTION_DAYS` | `0` disables pruning; explicit `1..3650` with snapshot directory enables it |
| `TZ` | Chosen timezone; otherwise system local |

Summary contains only status, day, agent, record time, total tokens, and warning count. Scheduled failure records failure/time, not raw stderr. Read the private daily report or run an authorized diagnostic to inspect warnings. Full CLI output is not saved to operational logs.

## Preview And Consent

```bash
./scripts/install-launchd-token-recorder.sh --agent codex --interval 1800 \
  --bin /absolute/path/to/token-stats --timezone Asia/Shanghai
```

Preview verifies hashes and prints a plan without executing the CLI, creating directories/plists, or changing launchd. Show it to the user: source overrides, paths, hash, timezone, snapshots/retention, and immediate-start choice. Installation requires authorization for those choices.

Repeat with `--confirm` only after authorization. Minimum interval is 60 seconds, default 1,800. Registration enables periodic execution and login persistence but uses `RunAtLoad=false`. `--start-now` explicitly requests immediate execution. Without it, launchd can still run the task at its next scheduled interval.

Installation writes an owned `0600` plist and a private versioned runtime under `~/.local/state/token-stats-skill/<label>/<generation>/`. The helper and manifest are copied, so checkout edits do not silently alter installed code. The plist uses absolute Python/CLI paths, Python isolated mode, restricted PATH, and umask `077`. stdout/stderr go to `/dev/null`; minimal status goes to `~/Library/Logs/ai-token-ayalysis/<label>.status.json`.

All eight local `--*-home` flags are persisted. `--timezone` persists an explicit IANA timezone. Arbitrary shell environment variables, credentials, and proxies are not copied into the task. Source selection is not an OS-level access sandbox.

## Upgrade And Permissions

Legacy label `com.baijian.ai-token-ayalysis` and daily store are preserved. Existing jobs require `--replace` and `--confirm`. The installer rejects unrelated plists, conflicting loaded jobs, traversal, output symlinks, foreign-owned files, and hardlinked outputs.

Directories must be `0700`, files `0600`. Explain dedicated paths before adding `--repair-permissions` to an authorized install/replacement. It tightens only owned selected output directories and recognized daily/snapshot/status/legacy log files, never recursively changes the home directory or source logs. Symlinks/hardlinks are not repaired. Other agent namespaces are not recursively migrated; repair each intended scope separately.

Old snapshots are not enabled implicitly. Passing `--run-dir "$HOME/.local/state/ai-token-ayalysis/runs"` includes that directory in explicit permission repair and also enables future snapshots. No retention means no deletion. To preserve old history without new snapshots, migrate its permissions separately with approved scoped operations instead of enabling it in the schedule.

The installer locks label operations, rechecks the plist, and attempts to restore previous registration on replacement failure. Prepared private files can remain after failure. An inability to restore launchd is an error, not a successful installation.

## Status, Stop, And Uninstall

Use the same custom label when applicable:

```bash
./scripts/install-launchd-token-recorder.sh --action status
./scripts/install-launchd-token-recorder.sh --action stop
# Repeat with --confirm only after user authorization.
./scripts/install-launchd-token-recorder.sh --action stop --confirm

./scripts/install-launchd-token-recorder.sh --action uninstall
# After separate authorization to remove the task:
./scripts/install-launchd-token-recorder.sh --action uninstall --confirm
```

Status inspects registration; read the private status file for collection success/time. Stop unloads but preserves the plist, which can register at login. Uninstall unloads and removes only the owned plist. Both retain reports, snapshots, runtime generations, status, and the coordination lock. History/runtime removal is a separate scoped request.

## Snapshots And Retention

Snapshots copy cumulative daily reports and can expose session paths. Enable only for needed intra-day history. Use `--run-dir PATH --retention-days N` or matching environment variables. Retention defaults to disabled.

Pruning applies only to private, owned, single-link files matching `token-stats-<agent>-<day>-<uuid>.json` and older than N days by mtime. It never prunes daily reports, legacy snapshots, arbitrary files, source logs, or Trae caches. It runs only after a successful collection/snapshot. Approve retention as deletion, not merely a storage setting. No blanket cleanup is provided.

Recording refreshes only today. Backfill missed days and previous-day final events explicitly. Snapshots are cumulative; negative differences can be corrections/coverage changes, not negative token events.

## Residual Risks

- CLI signing/provenance and independently auditable releases need separate CLI release-pipeline work. An opaque-binary finding cannot be resolved simply through wording or checksums.
- Permissions protect against accidental broad access and unsafe targets, not root, same-user compromise, a replaced interpreter, all ACL configurations, or races between checks and CLI execution. Use a dedicated OS account/container for stronger isolation.
- The binary still reads sensitive agent stores. Offline command selection is not a network sandbox. Authorized Trae sync intentionally sends credentials to its official service.
- Local edits do not clear published audit results. Re-scan the actual next published artifact and distinguish scanner findings from verified behavior.
