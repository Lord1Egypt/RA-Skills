# Security Boundary

This skill package is intended for trusted Windows hosts that already run a local VisPatrol environment.

## Credential source

- The script reads a single local runtime file: %TEMP%/vpup.json.
- That file provides the VisPatrol service address, service ports, and a locally stored session token.
- The skill does not prompt for or collect a username or password.

## Approval boundary

- The skill must not be enabled until the operator explicitly approves local vpup.json access.
- SKILL.md declares this requirement through skills.entries.vispatrol-alarm-query.config.userApprovedVpupAccess.
- Each end-user run must also be preceded by a clear notice that vpup.json will be read for the current query.

## Allowed use

- Read alarm records.
- Read latest snapshot images associated with returned alarms.
- Save snapshot files only to ~/.openclaw/workspace/tmp_files/ or a user-specified snapshot output directory.

## Disallowed use

- Account access or identity management.
- Device control.
- Configuration mutation.
- Arbitrary directory traversal or unrelated file access.
- Reuse of the session token for operations outside scripts/alarm_query.py alarm and snapshot queries.

## Review notes

- The Windows TEMP directory lookup and host MAC lookup exist only to locate and decode the local VisPatrol runtime configuration already present on the same trusted machine.
- This package is intentionally scoped to Windows in SKILL.md metadata to avoid advertising unsupported or broader host access.