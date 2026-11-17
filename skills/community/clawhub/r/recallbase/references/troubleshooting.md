# Troubleshooting

Read this file when the CLI is unavailable, results are empty or incomplete, imports fail, or browser-extension capture is unhealthy.

## CLI and source coverage

1. Run `rb --version` to confirm which local release is active.
2. Run `rb sources --json` and inspect health, counts, import times, and diagnostics.
3. Run `rb import --json` when known local sources have not been imported. It skips unchanged sources; use `rb import --force --json` only when a full re-import is required. `today` and non-empty `search` queries normally refresh known default sources automatically; explicit database paths, explicit roots, and `--no-refresh` suppress that refresh.
4. Retry the narrow query. Stop when results are available or the source status identifies the missing coverage.

If `rb` is not installed, report that prerequisite. Install it only within the user's authorization; the standard package command is `npm install -g recallbase`.

## Browser capture

Use the read-only check first:

```bash
rb extension verify-host --json
```

If setup is missing or stale and the user wants it repaired, run:

```bash
rb extension install-host --json
```

Installation changes per-user browser native-host configuration. It supports Chrome, Chrome for Testing on macOS/Linux, Edge, and Firefox. `RECALLBASE_CHROME_EXTENSION_ID` adds one exact alternate Chromium ID; `RECALLBASE_FIREFOX_EXTENSION_ID` replaces the default Firefox ID for alternate builds.

## Safe diagnostics

Use structured error codes, short messages, and actionable hints. Keep user-facing diagnostics free of local database paths, secrets, raw DOM, API payloads, headers, cookies, tokens, full URL queries, clipboard contents, and conversation text.
