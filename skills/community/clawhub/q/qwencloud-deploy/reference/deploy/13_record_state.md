# Record State (Step 13)

Calls `scripts/record_state.py` to write deployment results into the `.qwencloud-deploy` state file.

---

## Invocation

```bash
PASSWORD="$ECS_PWD" [DB_PASSWORD="$DB_PWD"] \
 python3 scripts/record_state.py \
    --stack-id "$STACK_ID" \
    --stack-name "$STACK_NAME" \
    --region "$REGION" \
    --topology single \
    --app-type systemd --runtime none \
    --app-name "$APP_NAME" \
    --nginx-mode static+app \
    --outputs-json '{"PublicIp":"47.x.x.x","EcsInstanceIds":"i-xxx"}' \
    --artifact-bucket "$BUCKET" \
    --artifact-urls-json "$(cat /tmp/qwencloud-artifacts.json)" \
    [--with-rds --db-engine mysql] \
    [--static-dir dist] [--app-dir app]
```

> **For docker deployments, also pass** `--app-mode docker-image|docker-compose`,
> `--app-image-name <image:tag>` (docker-image mode), and `--app-port <port>`.
> Once these fields are in the state file, `update_app.sh` can correctly
> `docker load` / `docker compose up` on hot update; if missing they default to
> `docker-image` + `<APP_NAME>:latest` + port 8080.

---

## Password Handling

- `PASSWORD` env var → written to `.qwencloud-deploy.local` (permissions 0600)
- `DB_PASSWORD` env var → same file (when RDS is included)
- **Never pass passwords via CLI arguments** (avoids `ps` exposure)
- **Never output passwords to chat**

---

## outputs-json Format

Extract from `GetStack` Outputs and serialize as flat JSON:

```json
{
  "PublicIp": "47.x.x.x",
  "EcsInstanceIds": "i-bp1xxx",
  "SecurityGroupId": "sg-bp1xxx",
  "EipAllocationId": "eip-bp1xxx",
  "DbInstanceId": "rm-xxx",
  "DbConnectionAddress": "rm-xxx.mysql.rds.aliyuncs.com",
  "DbPort": "3306",
  "DbAccount": "appuser",
  "Domain": "app.example.com",
  "CertPath": "/etc/qwencloud/certbot/config/live/app.example.com/fullchain.pem"
}
```

---

## Output Files

| File | Contents | Security |
|------|----------|----------|
| `.qwencloud-deploy` | Full deployment state (no passwords, but includes `current_artifact_urls` OSS **signed URLs**) | Permissions 0600, auto-added to `.gitignore`; signed URLs act as download credentials while valid, so **do not commit to git / share** |
| `.qwencloud-deploy.local` | Contains ECS/RDS passwords | Auto-added to `.gitignore`, permissions 0600 |

> ⚠️ `current_artifact_urls`' `static_url` / `app_url` are OSS pre-signed download links; anyone holding them can download the artifacts until they expire. The state file is therefore written 0600 and added to `.gitignore`, and must not be committed or shared.

> 🔐 The script auto-adds the state file and password sidecar to `.gitignore`: `.qwencloud-deploy`,
> `.qwencloud-deploy.local`. It also scans the current directory and adds only the host AI-agent
> workspaces that **actually exist** (`.claude/`, `.qoder/`, `.cursor/`, `.windsurf/`, `.codex/`,
> `.gemini/`, `.continue/`, `.roo/`, `.cline/`, `.trae/`, `.aider`), since those may store approved
> commands/history containing AK/SK, passwords, or signed URLs.

---

## Key State File Fields

- `version`: 1
- `stack_id` / `stack_name` / `region_id`
- `app_type` / `nginx_mode` / `topology`
- `app_mode` / `app_image_name` / `app_port` (docker deployments only, used by hot update)
- `outputs.public_ip` / `outputs.ecs_instance_ids`
- `artifact_bucket`
- `current_artifact_urls`
- `created_at` / `updated_at`

---

## Full State File Schema

```json
{
  "version": 1,
  "deploy_mode": "full-stack",
  "region_id": "ap-southeast-1",
  "topology": "single",
  "app_type": "systemd", "runtime": "none",
  "static_dir": "dist",
  "app_dir": "app",
  "nginx_mode": "static+app",
  "app_mode": null,
  "app_image_name": null,
  "app_port": null,
  "stack_id": "xxx",
  "stack_name": "qwencloud-myapp-202607291700",
  "created_at": "2026-07-29T09:00:00Z",
  "updated_at": null,
  "tags": [{"Key": "from", "Value": "qwencloud"}],
  "outputs": {
    "public_ip": "47.x.x.x",
    "ecs_instance_ids": ["i-bp1xxx"],
    "security_group_id": null,
    "eip_allocation_id": null,
    "db_instance_id": null,
    "db_connection_address": null,
    "db_port": null,
    "db_account": null,
    "domain": null,
    "cert_path": null
  },
  "artifact_bucket": "qwencloud-deploy-tmp-abc123",
  "current_artifact_urls": {
    "static_url": "https://...",
    "app_url": "https://..."
  },
  "db_engine": null,
  "notes": ""
}
```

### .local File Format

```json
{
  "stack_id": "xxx",
  "warning": "This file contains passwords — do not commit to version control",
  "ecs_password": "...",
  "db_password": "..."
}
```

Permissions 0600, auto-appended to `.gitignore`.

---

## outputs-json Field Mapping

The script accepts both key styles (ROS API original format and lowercase):

| ROS Original Key | Lowercase Key | Purpose |
|-----------------|---------------|---------|
| `PublicIp` | `public_ip` | Public IP |
| `EcsInstanceIds` | `ecs_instance_ids` | ECS instance ID (comma-separated or array) |
| `SecurityGroupId` | `security_group_id` | ECS security group ID (ingress rule checks) |
| `EipAllocationId` | `eip_allocation_id` | EIP allocation ID (EIP status query / re-bind) |
| `DbInstanceId` | `db_instance_id` | RDS instance ID |
| `DbConnectionAddress` | `db_connection_address` | RDS internal address |
| `DbPort` | `db_port` | RDS port |
| `DbAccount` | `db_account` | RDS account |
| `Domain` | `domain` | Bound domain (empty when HTTPS not set up) |
| `CertPath` | `cert_path` | Certificate fullchain path on the ECS |

---

After state is written, proceed to step 14 and append an `event=deploy` line to
`app_timeline.jsonl`; see `reference/deploy/14_app_timeline.md`.
