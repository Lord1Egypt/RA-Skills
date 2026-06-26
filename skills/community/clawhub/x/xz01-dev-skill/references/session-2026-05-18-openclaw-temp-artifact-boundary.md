# Session 2026-05-18 — OpenClaw Temporary Artifact Boundary

## Trigger

During an xz01 live-site detail-page validation run, an independent test worker correctly saved screenshots under `/www/wwwroot/www.900az.com/test-artifacts/...` and copied WebUI media under `/root/.hermes/workspace/xz01-artifacts/...`, but also created a temporary capture script under `/root/.openclaw/workspace/`.

The script was not business code and was removed immediately, but it still violated the xz01 read-only boundary.

## Rule

`/root/.openclaw/` and every subdirectory are read-only learning material for Hermes xz01 work. This includes temporary helper scripts, browser capture scripts, manifests, generated reports, screenshots, logs, scratch files, lock files, downloaded assets, and any validation artifacts.

Do not write any temporary or generated file under `/root/.openclaw`, even if the file will be deleted later.

## Correct Artifact Locations

- Test-side artifacts for the live site: `/www/wwwroot/www.900az.com/test-artifacts/...`
- WebUI-shareable copies: `/root/.hermes/workspace/xz01-artifacts/...`
- Temporary scripts/scratch files for Hermes-native runs: `/tmp/...` or `/root/.hermes/workspace/xz01-artifacts/...`
- Verified packages: `/root/.hermes/workspace/xz01/...`

## Prompting Guidance

Every xz01 dev/test delegation that may create scripts, screenshots, manifests, reports, or other generated files must explicitly say:

```text
Do not create temporary scripts or artifacts under /root/.openclaw. Use /tmp, /www/wwwroot/www.900az.com/test-artifacts, or /root/.hermes/workspace/xz01-artifacts instead.
```

## Verification

Before final reporting, check for unexpected newly-created files under the active `/root/.openclaw/workspace` when a worker had file-write permissions. If found, remove only the accidental temporary artifact and report the boundary correction.
