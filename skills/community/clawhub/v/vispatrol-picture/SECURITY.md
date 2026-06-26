# Security Boundary

This skill is a narrowly scoped VisPatrol integration for trusted Windows hosts that already run a local VisPatrol runtime.

## Local inputs and fixed host discovery

- The script reads exactly one local runtime file: %TEMP%/vpup.json.
- Under WSL compatibility, the script may run fixed literal commands only to resolve the Windows host TEMP directory:
	- cmd.exe /d /c echo %TEMP%
	- cmd.exe /d /c echo %TMP%
	- powershell.exe -NoProfile -Command [System.IO.Path]::GetTempPath()
- Those commands do not accept user-controlled arguments and are not used as general shell execution.
- The script may derive a machine identifier via uuid.getnode() and Windows getmac fallback only to decode the VisPatrol session token already stored on the same host in vpup.json.
- The machine identifier is not returned to the user, not written to disk, and not transmitted to unrelated services.

## Credential boundary

- The only credential handled by this skill is the local VisPatrol session token stored in %TEMP%/vpup.json.
- The skill does not prompt for or collect a username or password.
- The decrypted token remains in process memory for the current query only.
- The token must not be logged, written back to disk, exported to other files, or reused for anything outside read-only device status and snapshot queries.

## Network boundary

- Outbound requests are limited to the VisPatrol device, media, and related local service endpoints declared in the same vpup.json and used by scripts/picture_capture.py for read-only snapshot retrieval.
- The skill must not POST or forward vpup.json, the decrypted token, MAC-derived material, or snapshot data to unrelated domains, telemetry collectors, or public internet endpoints.

## Approval boundary

- The skill must not be enabled until the operator explicitly approves local vpup.json access in OpenClaw configuration.
- Each end-user run must also start with a clear notice that %TEMP%/vpup.json will be read for the current query.
- Any all-device capture requires a separate explicit confirmation for that run before snapshots are retrieved or forwarded.
- If the user does not approve that access or does not approve the all-device scope, the query must not run.

## Allowed use

- Read latest snapshot images for explicitly named devices from the local VisPatrol deployment.
- Read latest snapshot images for all currently configured devices only after separate explicit end-user confirmation for that run.
- Save snapshot files only to ~/.openclaw/workspace/tmp_files/ or a user-specified snapshot output directory.

## Disallowed use

- Account access or identity management.
- Device control.
- Configuration mutation.
- Arbitrary directory traversal or unrelated file access.
- Uploading local credentials or snapshots to non-VisPatrol endpoints.
- Broad all-device capture based on ambiguous or underspecified requests.
- Reusing the session token for operations outside scripts/picture_capture.py read-only snapshot queries.

## Reviewer note

The Windows TEMP lookup and machine-identifier lookup exist only because the current VisPatrol desktop runtime stores its local session material in %TEMP%/vpup.json and binds token decoding to the local host. This skill keeps that handling local, read-only, approval-gated, and separately confirms any all-device snapshot retrieval.