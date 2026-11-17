#!/usr/bin/env bash
# Hot update: Cloud Assistant → ECS atomic swap. See reference/hotfix/update_app.md
# Env: APP_URL / STATIC_URL (at least one non-empty), PROJECT_ROOT (default .)
# stdout: JSON  Exit: 0=success 1=nothing 2=state error 3=exec failed
set -uo pipefail
ROOT="${PROJECT_ROOT:-.}"
STATE="$ROOT/.qwencloud-deploy"

[ -f "$STATE" ] || { echo "Cannot find $STATE, please complete initial deployment first" >&2; exit 2; }
EVAL=$(python3 - "$STATE" <<'PY'
import json, shlex, sys
path = sys.argv[1]
try:
    with open(path, encoding="utf-8") as f:
        d = json.load(f)
except Exception as e:
    sys.stderr.write(f"State file parse failed: {e}\n"); sys.exit(2)

def need(k):
    v = d.get(k)
    if not v:
        sys.stderr.write(f"State file missing field '{k}'\n"); sys.exit(2)
    return v

region = need("region_id")
outputs = d.get("outputs") or {}
ecs_raw = outputs.get("ecs_instance_ids") or []
if isinstance(ecs_raw, str):
    ecs_raw = [x.strip() for x in ecs_raw.split(",") if x.strip()]
if not ecs_raw:
    sys.stderr.write("State file missing outputs.ecs_instance_ids\n"); sys.exit(2)

app_type = d.get("app_type") or ""
runtime = d.get("runtime") or "none"
nginx_mode = d.get("nginx_mode") or ""
bucket = d.get("artifact_bucket") or ""
public_ip = outputs.get("public_ip") or ""
app_mode = d.get("app_mode") or "docker-image"
image_name = d.get("app_image_name") or "qwencloud-app:latest"
app_port = d.get("app_port") or ""
service_name = d.get("service_name") or "qwencloud-app"

vals = {
    "REGION": region,
    "ECS_IDS": " ".join(ecs_raw),
    "APP_TYPE": app_type,
    "RUNTIME": runtime,
    "NGINX_MODE": nginx_mode,
    "BUCKET": bucket,
    "PUBLIC_IP": public_ip,
    "APP_MODE": app_mode,
    "IMAGE_NAME": image_name,
    "APP_PORT": str(app_port),
    "SERVICE_NAME": service_name,
}
for k, v in vals.items():
    print(f"{k}={shlex.quote(str(v))}")
PY
) || { echo "[update] Failed to read state file" >&2; exit 2; }
eval "$EVAL"

APP_URL="${APP_URL:-}"
STATIC_URL="${STATIC_URL:-}"

if [ -z "$APP_URL" ] && [ -z "$STATIC_URL" ]; then
  echo "[update] Both APP_URL and STATIC_URL are empty, nothing to update" >&2
  exit 1
fi

# Generate the docker app hot-update fragment (executed on the ECS instance).
# Relies on caller-expanded variables: APP_MODE / IMAGE_NAME / APP_PORT / APP_URL.
# Mirrors the first-boot logic in templates/userdata/docker.sh:
#   docker-image   -> download tar.gz -> docker load -> restart systemd-managed $SERVICE_NAME container
#   docker-compose -> download tar.gz (compose.yml + context/image) -> docker compose up -d --build
gen_app_update_docker() {
  local port="${APP_PORT:-8080}"
  local s="
# === Phase 1: Download new artifact to staging (old container keeps running) ===
echo '[update] Download+verify new docker artifact'
STAGING_DIR=/opt/qwencloud.staging
rm -rf \"\$STAGING_DIR\"
mkdir -p \"\$STAGING_DIR\"
curl -fsSL '$APP_URL' -o \"\$STAGING_DIR/app.tar.gz\"
tar -tzf \"\$STAGING_DIR/app.tar.gz\" >/dev/null
tar -xzf \"\$STAGING_DIR/app.tar.gz\" -C \"\$STAGING_DIR\"
rm -f \"\$STAGING_DIR/app.tar.gz\"

APP_PORT='$port'
DB_ENV_OPT=''
[ -f /etc/qwencloud/db.env ] && DB_ENV_OPT='--env-file /etc/qwencloud/db.env'
"

  if [ "$APP_MODE" = "docker-compose" ]; then
    s+="
# === docker-compose mode: switch to new directory and rebuild ===
if ! docker compose version >/dev/null 2>&1; then
  mkdir -p /usr/local/lib/docker/cli-plugins
  curl -fsSL https://github.com/docker/compose/releases/latest/download/docker-compose-linux-x86_64 \\
    -o /usr/local/lib/docker/cli-plugins/docker-compose
  chmod +x /usr/local/lib/docker/cli-plugins/docker-compose
fi

# Keep the old directory for rollback; stop old compose, then atomically swap directory
echo '[update] Stop old compose service'
if [ -f /opt/qwencloud/docker-compose.yml ]; then
  (cd /opt/qwencloud && docker compose -f docker-compose.yml down) || true
fi
rm -rf /opt/qwencloud.prev
if [ -d /opt/qwencloud ]; then mv /opt/qwencloud /opt/qwencloud.prev; fi
mv \"\$STAGING_DIR\" /opt/qwencloud
cd /opt/qwencloud
# Keep .env perms in sync with db.env (0600): db.env holds the DB password, and a
# plain cp would land it as 0644, exposing the secret to other local users.
[ -f /etc/qwencloud/db.env ] && install -m 600 /etc/qwencloud/db.env ./.env
echo '[update] Start new compose service'
# Under set -e, a failed up would exit immediately and skip health check/rollback.
docker compose -f docker-compose.yml up -d --build || echo '[update] compose up returned non-zero, entering health check/rollback'
"
  else
    s+="
# === docker-image mode: docker load new image and restart container ===
cd \"\$STAGING_DIR\"
if [ ! -f image.tar ]; then
  echo '[update] image.tar not found in artifact, cannot docker load' >&2
  exit 1
fi
# Record old image ID for rollback
PREV_IMAGE_ID=\$(docker images -q '$IMAGE_NAME' 2>/dev/null | head -1)
echo \"\$PREV_IMAGE_ID\" > /opt/qwencloud.prev-image 2>/dev/null || true
echo '[update] docker load new image'
# docker load prints 'Loaded image: repo:tag'; use it to learn the new image tag/ID.
LOAD_OUT=\$(docker load -i image.tar)
echo \"\$LOAD_OUT\"
# The loaded image tag may differ from the fixed IMAGE_NAME ('$IMAGE_NAME') the
# systemd unit runs, so re-tag the freshly loaded image as IMAGE_NAME.
LOADED_REF=\$(echo \"\$LOAD_OUT\" | sed -n 's/^Loaded image: //p' | head -1)
if [ -z \"\$LOADED_REF\" ]; then
  LOADED_REF=\$(echo \"\$LOAD_OUT\" | sed -n 's/^Loaded image ID: //p' | head -1)
fi
if [ -n \"\$LOADED_REF\" ] && [ \"\$LOADED_REF\" != '$IMAGE_NAME' ]; then
  echo \"[update] retagging new image \$LOADED_REF as $IMAGE_NAME\"
  docker tag \"\$LOADED_REF\" '$IMAGE_NAME'
fi

# Match first-boot: systemd-managed $SERVICE_NAME container; ensure unit exists
if [ ! -f /etc/systemd/system/$SERVICE_NAME.service ]; then
  cat > /etc/systemd/system/$SERVICE_NAME.service <<UNIT
[Unit]
Description=qwencloud app container
After=docker.service
Requires=docker.service

[Service]
Restart=always
ExecStartPre=-/usr/bin/docker rm -f $SERVICE_NAME
ExecStart=/usr/bin/docker run --rm --name $SERVICE_NAME -p \${APP_PORT}:\${APP_PORT} \${DB_ENV_OPT} $IMAGE_NAME
ExecStop=/usr/bin/docker stop $SERVICE_NAME

[Install]
WantedBy=multi-user.target
UNIT
  systemctl daemon-reload
  systemctl enable $SERVICE_NAME
fi

# Move the current version aside to .prev (for rollback/debugging), then install the new artifact dir
rm -rf /opt/qwencloud.prev
if [ -d /opt/qwencloud ]; then mv /opt/qwencloud /opt/qwencloud.prev; fi
mv \"\$STAGING_DIR\" /opt/qwencloud
echo '[update] Restart container'
# Note: the script header is set -euxo pipefail. If systemctl restart fails and is
# not swallowed, the script exits immediately and the health check + rollback block
# below becomes unreachable; meanwhile ExecStartPre already did docker rm -f on the
# old container, so neither old nor new is running. Swallow with '|| echo' and let
# the following health check / rollback decide.
systemctl restart $SERVICE_NAME || echo '[update] systemctl restart returned non-zero, entering health check/rollback'
"
  fi

  # === Health check (common to docker) ===
  s+="
echo '[update] Health check...'
BASE_RESTARTS=\$(_restarts)
sleep 3
HEALTHY=0
for _i in \$(seq 1 15); do
  if _healthy \"\$BASE_RESTARTS\"; then
    HEALTHY=1
    break
  fi
  sleep 2
done
if [ \"\$HEALTHY\" -eq 0 ]; then
  echo '[update] Health check failed, rolling back to previous version'
  echo '[update] Failure diagnostics (service status + app logs):'; _diag || true
"
  if [ "$APP_MODE" = "docker-compose" ]; then
    s+="
  if [ -d /opt/qwencloud.prev ]; then
    (cd /opt/qwencloud && docker compose -f docker-compose.yml down) || true
    rm -rf /opt/qwencloud.failed
    mv /opt/qwencloud /opt/qwencloud.failed || true
    mv /opt/qwencloud.prev /opt/qwencloud
    (cd /opt/qwencloud && docker compose -f docker-compose.yml up -d --build) || true
    BASE_RESTARTS=\$(_restarts)
    for _i in \$(seq 1 15); do
      if _healthy \"\$BASE_RESTARTS\"; then
        echo '[update] Rollback succeeded, previous version restored (new artifact kept at /opt/qwencloud.failed for debugging)'
        exit 1
      fi
      sleep 2
    done
    echo '[update] Health check still failing after rollback, manual intervention required'
  else
    echo '[update] No backup available, cannot roll back automatically'
  fi
"
  else
    s+="
  PREV_IMAGE_ID=\$(cat /opt/qwencloud.prev-image 2>/dev/null || true)
  if [ -n \"\$PREV_IMAGE_ID\" ]; then
    echo '[update] Re-tagging image back to previous version'
    docker tag \"\$PREV_IMAGE_ID\" '$IMAGE_NAME' || true
    rm -rf /opt/qwencloud.failed
    if [ -d /opt/qwencloud ]; then mv /opt/qwencloud /opt/qwencloud.failed || true; fi
    if [ -d /opt/qwencloud.prev ]; then mv /opt/qwencloud.prev /opt/qwencloud; fi
    systemctl restart $SERVICE_NAME || echo '[update] rollback restart returned non-zero, continuing health check'
    BASE_RESTARTS=\$(_restarts)
    for _i in \$(seq 1 15); do
      if _healthy \"\$BASE_RESTARTS\"; then
        echo '[update] Rollback succeeded, previous version restored (new artifact kept at /opt/qwencloud.failed for debugging)'
        exit 1
      fi
      sleep 2
    done
    echo '[update] Health check still failing after rollback, manual intervention required'
  else
    echo '[update] No previous image available, cannot roll back automatically'
  fi
"
  fi
  s+="
  exit 1
fi
echo '[update] Health check passed'
"
  echo "$s"
}

gen_update_script() {
  local script="#!/bin/bash
set -euxo pipefail
exec >> /var/log/qwencloud-update.log 2>&1
echo \"[\$(date -u +%FT%TZ)] === qwencloud update start ===\"
"
  # Health probe depends on how the app is supervised: compose is managed by
  # docker compose (no systemd unit); everything else runs under systemd.
  if [ "$APP_TYPE" = "docker" ] && [ "$APP_MODE" = "docker-compose" ]; then
    script+="
_restarts() { (cd /opt/qwencloud && docker compose -f docker-compose.yml ps -aq 2>/dev/null | xargs -r docker inspect -f '{{.RestartCount}}' 2>/dev/null) | awk '{s+=\$1} END {print s+0}'; }
# Healthy: at least one container running, none restarting/exited, and no new restarts vs baseline.
_healthy() { [ \"\$(cd /opt/qwencloud && docker compose -f docker-compose.yml ps --status running -q 2>/dev/null | wc -l)\" -gt 0 ] && ! (cd /opt/qwencloud && docker compose -f docker-compose.yml ps -a --format '{{.State}}' 2>/dev/null | grep -qE 'restarting|exited') && [ \"\$(_restarts)\" -le \"\${1:-0}\" ]; }
_diag() { (cd /opt/qwencloud && docker compose -f docker-compose.yml ps -a; echo ---; docker compose -f docker-compose.yml logs --tail=50) 2>&1; }
"
  else
    local applog
    if [ "$APP_TYPE" = "docker" ]; then
      applog="journalctl -u $SERVICE_NAME --no-pager | tail -n 50"
    else
      applog="tail -n 50 /var/log/$SERVICE_NAME.log 2>/dev/null"
    fi
    script+="
_restarts() { systemctl show -p NRestarts --value $SERVICE_NAME 2>/dev/null || echo 0; }
# Healthy: service active and no new restarts vs baseline (rules out CrashLoop under Restart=always).
_healthy() { systemctl is-active --quiet $SERVICE_NAME && [ \"\$(_restarts)\" -le \"\${1:-0}\" ]; }
# App-layer verification: judge liveness by service status + app logs, no HTTP probe.
_diag() { systemctl status $SERVICE_NAME --no-pager 2>&1 | tail -n 20; echo ---; $applog; }
"
  fi

  # Dispatch app-artifact update by APP_TYPE: docker and systemd use different
  # atomic-swap mechanics.
  if [ -n "$APP_URL" ] && [ "$APP_TYPE" = "docker" ]; then
    script+="$(gen_app_update_docker)"
  elif [ -n "$APP_URL" ]; then
    script+="
# === Phase 1: Download new artifacts to staging (service keeps running) ===
echo '[update] Download+verify new artifacts'
STAGING_DIR=/opt/qwencloud.staging
rm -rf \"\$STAGING_DIR\"
mkdir -p \"\$STAGING_DIR\"
curl -fsSL '$APP_URL' -o \"\$STAGING_DIR/app.tar.gz\"
tar -tzf \"\$STAGING_DIR/app.tar.gz\" >/dev/null
tar -xzf \"\$STAGING_DIR/app.tar.gz\" -C \"\$STAGING_DIR\"
rm -f \"\$STAGING_DIR/app.tar.gz\"
"

    # Warm dependencies in staging while the service is still running,
    # so the Phase 2 downtime window stays as short as possible.
    case "$RUNTIME" in
      python)
        script+="
cd \"\$STAGING_DIR\"
if [ -f requirements.txt ]; then
  echo '[update] Pre-downloading Python dependencies (service unaffected)'
  mkdir -p /tmp/qwencloud-pip-cache
  python3 -m pip download -d /tmp/qwencloud-pip-cache -r requirements.txt
  echo '[update] Python dependencies pre-downloaded'
fi
"
        ;;
      node)
        script+="
cd \"\$STAGING_DIR\"
if [ -f package.json ]; then
  echo '[update] Pre-installing Node dependencies (staging, service unaffected)'
  rm -rf node_modules
  yarn install --production
  echo '[update] Node dependencies installed'
fi
"
        ;;
    esac

    script+="
# === Phase 2: Atomic swap ===
echo '[update] Stop service'
systemctl stop $SERVICE_NAME || true
echo '[update] Atomic replacement'
# Keep the old version for rollback instead of deleting it; drop any stale backup first.
rm -rf /opt/qwencloud.prev
if [ -d /opt/qwencloud ]; then mv /opt/qwencloud /opt/qwencloud.prev; fi
mv \"\$STAGING_DIR\" /opt/qwencloud
"

    # Python deps must land in the new directory after the swap but before start;
    # install offline from the Phase 1 cache so no network is needed here.
    case "$RUNTIME" in
      python)
        script+="
cd /opt/qwencloud
if [ -f requirements.txt ] && [ -d /tmp/qwencloud-pip-cache ]; then
  echo '[update] Offline installing Python dependencies (using pre-downloaded cache)'
  python3 -m pip install --no-cache-dir --no-index --find-links /tmp/qwencloud-pip-cache -r requirements.txt
  rm -rf /tmp/qwencloud-pip-cache
fi
"
        ;;
    esac

    script+="
echo '[update] Start service'
# Under set -e, a failed restart would exit and skip health check + rollback.
systemctl restart $SERVICE_NAME || echo '[update] systemctl restart returned non-zero, entering health check/rollback'

# === Health check ===
echo '[update] Health check...'
BASE_RESTARTS=\$(_restarts)
sleep 3
HEALTHY=0
for _i in \$(seq 1 15); do
  if _healthy \"\$BASE_RESTARTS\"; then
    HEALTHY=1
    break
  fi
  sleep 2
done
if [ \"\$HEALTHY\" -eq 0 ]; then
  echo '[update] Health check failed, rolling back to previous version'
  echo '[update] Failure diagnostics (service status + app logs):'; _diag || true
  if [ -d /opt/qwencloud.prev ]; then
    systemctl stop $SERVICE_NAME || true
    rm -rf /opt/qwencloud.failed
    mv /opt/qwencloud /opt/qwencloud.failed || true
    mv /opt/qwencloud.prev /opt/qwencloud
    systemctl restart $SERVICE_NAME || echo '[update] rollback restart returned non-zero, continuing health check'
    BASE_RESTARTS=\$(_restarts)
    for _i in \$(seq 1 15); do
      if _healthy \"\$BASE_RESTARTS\"; then
        echo '[update] Rollback succeeded, previous version restored (new artifact kept at /opt/qwencloud.failed for debugging)'
        exit 1
      fi
      sleep 2
    done
    echo '[update] Health check still failing after rollback, manual intervention required'
  else
    echo '[update] No backup available, cannot roll back automatically'
  fi
  exit 1
fi
echo '[update] Health check passed'
"
  fi

  if [ -n "$STATIC_URL" ]; then
    script+="
# === Static update (zero downtime) ===
echo '[update] Download static artifacts'
STATIC_STAGING=/var/www/static.staging
rm -rf \"\$STATIC_STAGING\"
mkdir -p \"\$STATIC_STAGING\"
curl -fsSL '$STATIC_URL' -o /tmp/static.tar.gz
tar -tzf /tmp/static.tar.gz >/dev/null
tar -xzf /tmp/static.tar.gz -C \"\$STATIC_STAGING\" --strip-components=0
rm -f /tmp/static.tar.gz
rm -rf /var/www/static
mv \"\$STATIC_STAGING\" /var/www/static
nginx -t && systemctl reload nginx
echo '[update] Static update complete'
"
  fi

  script+="
rm -rf /opt/qwencloud.staging /var/www/static.staging /tmp/qwencloud-pip-cache 2>/dev/null || true
echo \"[\$(date -u +%FT%TZ)] === qwencloud update complete ===\"
"
  echo "$script"
}

UPDATE_SCRIPT=$(gen_update_script)

run_on_instance() {
  local instance_id="$1"
  echo "[update] Sending update command to $instance_id ..." >&2

  local out
  out=$(PAGER=cat aliyun ecs RunCommand \
    --RegionId "$REGION" \
    --InstanceId.1 "$instance_id" \
    --Type RunShellScript \
    --CommandContent "$UPDATE_SCRIPT" \
    --Timeout 300 2>&1)
  local code=$?
  if [ $code -ne 0 ]; then
    echo "[update] RunCommand failed: $out" >&2
    return 3
  fi

  local invoke_id
  invoke_id=$(echo "$out" | python3 -c "import json,sys;print(json.load(sys.stdin).get('InvokeId',''))" 2>/dev/null)
  if [ -z "$invoke_id" ]; then
    echo "[update] Cannot parse InvokeId: $out" >&2
    return 3
  fi
  echo "[update] InvokeId=${invoke_id}, waiting for execution..." >&2

  local deadline=$(( $(date +%s) + 300 ))
  local status=""
  local wait=2

  while [ $(date +%s) -lt $deadline ]; do
    local inv_out
    inv_out=$(PAGER=cat aliyun ecs DescribeInvocations \
      --RegionId "$REGION" \
      --InvokeId "$invoke_id" 2>&1) || { sleep "$wait"; continue; }

    status=$(echo "$inv_out" | python3 -c "
import json, sys
try:
    d = json.load(sys.stdin)
    invs = d.get('Invocations', {}).get('Invocation', [])
    if invs:
        instances = invs[0].get('InvokeInstances', {}).get('InvokeInstance', [])
        if instances:
            print(instances[0].get('InvocationStatus', ''))
except: pass
" 2>/dev/null)

    case "$status" in
      Finished|Success)
        echo "[update] $instance_id update complete" >&2

        local result_out
        result_out=$(PAGER=cat aliyun ecs DescribeInvocationResults \
          --RegionId "$REGION" \
          --InvokeId "$invoke_id" 2>&1)
        local output_b64
        output_b64=$(echo "$result_out" | python3 -c "
import json, sys
try:
    d = json.load(sys.stdin)
    items = d.get('Invocation', {}).get('InvocationResults', {}).get('InvocationResult', [])
    if items: print(items[0].get('Output', ''))
except: pass
" 2>/dev/null)
        if [ -n "$output_b64" ]; then
          echo "[update] === Remote output ===" >&2
          echo "$output_b64" | base64 -d 2>/dev/null >&2 || true
          echo "[update] === End remote output ===" >&2
        fi
        echo "$invoke_id"
        return 0
        ;;
      Failed)
        echo "[update] $instance_id execution failed" >&2

        local err_out
        err_out=$(PAGER=cat aliyun ecs DescribeInvocationResults \
          --RegionId "$REGION" \
          --InvokeId "$invoke_id" 2>&1)
        local err_b64
        err_b64=$(echo "$err_out" | python3 -c "
import json, sys
try:
    d = json.load(sys.stdin)
    items = d.get('Invocation', {}).get('InvocationResults', {}).get('InvocationResult', [])
    if items: print(items[0].get('Output', ''))
except: pass
" 2>/dev/null)
        if [ -n "$err_b64" ]; then
          echo "[update] === Error output ===" >&2
          echo "$err_b64" | base64 -d 2>/dev/null >&2 || true
        fi
        return 3
        ;;
      *)
        echo "[update] $(date -u +%H:%M:%S) $instance_id status=$status" >&2
        ;;
    esac
    sleep "$wait"; [ "$wait" -lt 10 ] && wait=$((wait + 2))
  done

  echo "[update] $instance_id execution timed out (5 minutes)" >&2
  return 3
}

UPDATED_INSTANCES=()
INVOKE_IDS=()
FAILED=0

IFS=' ' read -r -a ECS_ARRAY <<< "$ECS_IDS"
ecs="${ECS_ARRAY[0]}"
invoke_id=$(run_on_instance "$ecs") || FAILED=1
if [ $FAILED -eq 0 ]; then
  UPDATED_INSTANCES+=("$ecs")
  INVOKE_IDS+=("$invoke_id")
fi

if [ $FAILED -ne 0 ]; then
  echo "[update] Update failed" >&2
  exit 3
fi

python3 - "$STATE" "$APP_URL" "$STATIC_URL" <<'PY'
import json, os, sys
from datetime import datetime, timezone

path, new_app, new_static = sys.argv[1:4]
with open(path, encoding="utf-8") as f:
    state = json.load(f)

# Record the artifact URLs being replaced, to support manual rollback / history.
prev = state.get("current_artifact_urls") or {}

state["current_artifact_urls"] = {}
if new_app:
    state["current_artifact_urls"]["app_url"] = new_app
if new_static:
    state["current_artifact_urls"]["static_url"] = new_static

state["updated_at"] = datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")
if prev:
    state["previous_artifact_urls"] = prev
else:
    state.pop("previous_artifact_urls", None)

with open(path, "w", encoding="utf-8") as f:
    json.dump(state, f, ensure_ascii=False, indent=2)
# State file holds signed URLs (current_artifact_urls); keep 0600 so other local
# users cannot read it.
os.chmod(path, 0o600)
sys.stderr.write(f"[update] State file updated with updated_at\n")
PY

python3 - "${UPDATED_INSTANCES[@]}" -- "${INVOKE_IDS[@]}" <<'PY'
import json, sys
args = sys.argv[1:]
sep = args.index("--")
instances = args[:sep]
invoke_ids = args[sep+1:]
print(json.dumps({
    "status": "success",
    "updated_instances": instances,
    "invoke_ids": invoke_ids,
}, ensure_ascii=False))
PY
