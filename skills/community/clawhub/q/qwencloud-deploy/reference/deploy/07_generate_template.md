# Generate Template (Step 7)

Calls `scripts/generate_template.py` to assemble the ROS template and UserData script.

---

## Invocation

### Without RDS

```bash
python3 scripts/generate_template.py \
  --topology single \
  --app-type systemd --runtime none \
  --app-port 8080 \
  --app-name "$APP_NAME" \
  --start-command "./server" \
  --nginx-mode static+app \
  --output /tmp/qwencloud-template.yaml \
  --userdata-output /tmp/qwencloud-userdata.sh
```

### With RDS

```bash
DB_PASSWORD='<strong-pwd>' python3 scripts/generate_template.py \
  --topology single \
  --app-type systemd --runtime none \
  --app-port 8080 \
  --app-name "$APP_NAME" \
  --start-command "./server" \
  --nginx-mode proxy \
  --with-rds \
  --output /tmp/qwencloud-template.yaml \
  --userdata-output /tmp/qwencloud-userdata.sh
```

> This step produces a template with placeholder artifact URLs for step-9 validation and pricing.
> Real artifact URLs are filled in at step 10, which re-runs this script with `--artifacts-json`.

---

## Parameters

| Parameter | Description |
|-----------|-------------|
| `--topology` | Fixed `single` (single instance) |
| `--app-type` | `docker` / `systemd` / `static-only` |
| `--app-port` | App listen port |
| `--app-name` | Service name (systemd unit / container name / log file name / default image tag); must match `^[a-z][a-z0-9-]{0,30}$` |
| `--runtime` | Runtime install (systemd only): `none` (default) / `java` / `node` / `python`.<br>Only these three languages plus statically compiled ones (`none`) use systemd; every other language uses `--app-type docker`, see `03_analyze_project.md` |
| `--start-command` | Full start command (relative to `/opt/qwencloud`) |
| `--nginx-mode` | `static+app` / `proxy` / `static` |
| `--artifacts-json` | Path to `upload_artifacts.py` output JSON (or `-` for stdin) |
| `--with-rds` | Uses `*_rds.yaml` template variant |

---

## Key Behaviors

| Behavior | Description |
|----------|-------------|
| Template skeleton | Reads `templates/ros_single.yaml` or `ros_single_rds.yaml` |
| UserData injection | Assembled from `templates/userdata/*.sh` based on app_type |
| Without RDS | Template written as-is; UserData to separate file, passed as ROS Parameter |
| With RDS | UserData base64-encoded and inlined at `__USERDATA_BODY__` in template |
| DB_PASSWORD | Must be passed via environment variable (never CLI arg — avoids `ps` exposure) |

---

## UserData Assembly Details

Template reads fragments from `templates/userdata/*.sh`, combining them based on nginx_mode and app_type.

### nginx Fragment Selection

| nginx_mode | Fragment File | Placeholders |
|------------|--------------|--------------|
| `static+app` | `nginx_static_proxy.sh` | `__STATIC_ARTIFACT_URL__`, `__APP_PORT__` |
| `proxy` | `nginx_proxy.sh` | `__APP_PORT__` |
| `static` | `nginx_static.sh` | `__STATIC_ARTIFACT_URL__` |

### App Fragment Selection

| app_type | Fragment File | Placeholders |
|----------|--------------|--------------|
| `docker` | `docker.sh` | `__APP_ARTIFACT_URL__`, `__APP_MODE__`, `__APP_PORT__`, `__APP_IMAGE_NAME__` |
| `systemd` | `systemd.sh` | `__APP_ARTIFACT_URL__`, `__APP_RUNTIME__`, `__START_COMMAND__`, `__APP_PORT__` |
| `static-only` | No app fragment | — |

### Runtime Mapping

| `--runtime` arg | `__APP_RUNTIME__` value | Description |
|-----------------|-------------------------|-------------|
| `none` (default) | `none` | No runtime install (static binary, or runtime already exists) |
| `java` | `java` | Install JDK 17 |
| `node` | `node` | Install Node.js + npm + yarn |
| `python` | `python` | Install Python3 + pip |

---

## UserData Inline Mechanism (with RDS)

1. Assembled UserData body is **base64 encoded**
2. Injected at `__USERDATA_BODY__` placeholder in template
3. At runtime ECS first writes `db.env` (RDS variables substituted by Fn::Sub), then decodes + sources main script
4. Fn::Sub never touches shell variables, avoiding unreliable `${!VAR}` issues

`--userdata-output` with `--with-rds` only writes a placeholder reference file.
