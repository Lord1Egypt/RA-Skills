# TeamClaw validation checklist

## Startup checks

After startup, always give the user:

```bash
curl http://127.0.0.1:9527/api/v1/health
```

Expected shape:

```json
{"status":"ok","mode":"controller", ...}
```

Also point them to:

```text
http://127.0.0.1:9527/ui
```

## First smoke-test task

Recommend a tiny requirement before any large SDLC workflow:

```text
Create a minimal static site in the workspace with README.md, index.html, and style.css.
```

This checks controller intake, task routing, worker execution, workspace writes, and UI visibility with minimal risk.

## Timeout guidance

For real model runs:

- TeamClaw: `taskTimeoutMs = 1800000`
- OpenClaw: `agents.defaults.timeoutSeconds >= 2400`

If OpenClaw times out first, users often think TeamClaw is broken when the real issue is the inner agent deadline.

## Common failure checks

### localRoles or process

- confirm the chosen model already works in plain OpenClaw
- confirm `agents.defaults.workspace` points to a writable path

### distributed worker

- confirm `controllerUrl` is reachable from the worker machine
- confirm the worker role matches the intended role

### Docker

- confirm `workerProvisioningControllerUrl` is reachable from containers
- confirm the controller can access Docker
- confirm the runtime image is `ghcr.io/topcheer/teamclaw-openclaw:latest`

### Kubernetes

- confirm pods can reach `workerProvisioningControllerUrl`
- confirm the controller environment has `kubectl`
- confirm any workspace PVC actually exists

## Done criteria

Treat the install as successful only when:

1. controller health is `ok`
2. expected workers appear in the UI or status view
3. the smoke-test task completes
4. files appear in the workspace
