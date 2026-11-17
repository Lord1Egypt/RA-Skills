# Hot Update

Calls `scripts/update_app.sh` to atomically replace application code on ECS via Cloud Assistant.

Below, `<service_name>` = the `service_name` field in the state file (read automatically by
`update_app.sh`); falls back to `qwencloud-app` when missing.

---

## Invocation

```bash
APP_URL="$APP_URL" STATIC_URL="$STATIC_URL" \
  bash scripts/update_app.sh
```

Environment variable `PROJECT_ROOT` (default `.`) points to the directory containing `.qwencloud-deploy`.

---

## Prerequisites

- `.qwencloud-deploy` state file exists
- New artifacts uploaded via `upload_artifacts.py`
- At least one of `APP_URL` or `STATIC_URL` is non-empty

---

## Execution Flow (logic executed on ECS)

The script dispatches app-update logic by `app_type` in the state file (`docker` / `systemd`).
**Docker deployments must take the docker branch** so the running container is actually
replaced.

### App Update · systemd (minimal downtime window)

1. **Phase 1: Preparation** (service keeps running)
   - Downloads new artifacts to `/opt/qwencloud.staging`
   - Integrity check (`tar -tzf`)
   - Pre-installs dependencies (Python: pip download; Node: yarn install)

2. **Phase 2: Atomic Swap** (downtime window)
   - `systemctl stop <service_name>`
   - `rm -rf /opt/qwencloud && mv staging → /opt/qwencloud`
   - Offline dependency install (using Phase 1 pre-downloaded cache)
   - `systemctl restart <service_name>`
   - Health check: service status + app logs (no HTTP probe), auto-rollback on failure

### App Update · docker

Uses state fields: `app_mode` (`docker-image` / `docker-compose`),
`app_image_name` (image name:tag), `app_port` (health check / port mapping).

- **docker-image mode**
  1. Download tar.gz to `/opt/qwencloud.staging`, verify, extract `image.tar`
  2. Record old image ID (for rollback) → `docker load -i image.tar`
  3. Ensure systemd unit `<service_name>.service` exists → atomic dir swap → `systemctl restart <service_name>`
  4. On health-check failure → `docker tag` rollback to old image and restart (new artifact kept at `/opt/qwencloud.failed`)
- **docker-compose mode**
  1. Download tar.gz (contains `docker-compose.yml` + context/image) to staging
  2. `docker compose down` old service → atomic dir swap → `docker compose up -d --build`
  3. On health-check failure → restore old dir and `docker compose up -d --build`

### Static Update (zero downtime)

1. Download to `/var/www/static.staging`
2. Integrity check
3. `rm -rf /var/www/static && mv staging`
4. `nginx -t && systemctl reload nginx`

---

## Output

stdout JSON:
```json
{"status": "success", "updated_instances": ["i-xxx"], "invoke_ids": ["t-xxx"]}
```

---

## Append application dossier

After a successful update, append an `event=hotfix` line to `app_timeline.jsonl`:

```bash
python3 scripts/append_timeline.py --skill qwencloud-deploy --event hotfix \
  --summary "Hot update done: app artifact replaced, service status verified" \
  --data-json '{"artifact":"app+static","verification":"passed"}'
```

---

## Key Mechanisms

| Mechanism | Description |
|-----------|-------------|
| Cloud Assistant | Delivered via `RunCommand`, no SSH needed, port 22 not required |
| Polling | `DescribeInvocations` waits up to 5 minutes |
| State file update | On success, auto-writes `updated_at` and `current_artifact_urls` |
| Dependency pre-install | Python/Node pre-installed in staging dir, minimizes downtime |

---

## Exit Codes

| Code | Meaning |
|------|---------|
| 0 | Success |
| 1 | Nothing to update |
| 2 | State file error |
| 3 | RunCommand execution failed |
