# Create Stack (Step 11)

Calls `scripts/create_stack.sh` to create the ROS stack. This document covers invocation, parameter rules, and retry safety.

---

## Invocation

The params file holds plaintext passwords: create it with `umask 077` (mode 600) and delete it
right after the stack is created.

```bash
umask 077 && cat > /tmp/qwencloud-params.json <<'JSON'
... params JSON (see below) ...
JSON
APP_NAME="$APP_NAME" APP_DESC="$APP_DESC" \
  [TIMEOUT_MIN=40] \
  bash scripts/create_stack.sh "$REGION" "$TEMPLATE_URL" "$STACK_NAME" /tmp/qwencloud-params.json
rm -f /tmp/qwencloud-params.json
```

> The ROS CLI receives passwords as command-line arguments, visible via `ps` while the process
> runs — a CLI limitation. Restricting the params file's permissions and deleting it after use
> reduces residual exposure on disk.

---

## Parameter File Format

Agent generates a JSON file (e.g. `/tmp/qwencloud-params.json`) containing all ROS template parameters:

```json
[
  {"key": "AppName", "value": "myapp"},
  {"key": "InstanceType", "value": "<type selected in step 6>"},
  {"key": "Password", "value": "<Agent-generated strong password>"},
  {"key": "SystemDiskSize", "value": "40"},
  {"key": "AppPort", "value": "8080"},
  {"key": "ZoneId", "value": "ap-southeast-1a"},
  {"key": "UserDataScript", "value": "<userdata script content>"}
]
```

With RDS, omit `UserDataScript` and add:
- `DbInstanceClass` (= step-5 `DB_INSTANCE_CLASS`), `DbInstanceStorage` (GiB), `DbName`,
  `DbAccount`, `DbPassword`

> `DbInstanceClass`/`DbInstanceStorage` values come from the user's step-5 selection —
> the stack must be created with the class the user chose.

---

## Stack Name Rule

Format: `qwencloud-${APP_NAME}-$(date +%Y%m%d%H%M)`

> ⚠️ **Generate once only**. On retry, reuse the same stack name — the script auto-checks whether the server already has a stack with that name.

---

## Password Rules

- ≥12 characters
- Special characters limited to `!@%^*+=_-` (`& # $ | ;` break `db.env` shell sourcing)
- ECS and RDS passwords generated separately
- Passwords are **never shown in chat**

---

## Retry Safety (built into script)

1. Before creating, `ListStacks` checks for same-name stack
2. Found CREATE_IN_PROGRESS/COMPLETE → reuse its StackId
3. Found CREATE_FAILED → DeleteStack first to free the name, then create
4. CLI timeout → sleep 3s then query server; if created, reuse
5. On success, immediately writes provisional state file `.qwencloud-deploy` (`provisional: true`)

---

## Timeout Settings

| Scenario | TIMEOUT_MIN |
|----------|-------------|
| No RDS   | 15 (default; ECS+EIP is usually ready in 2-5 min) |
| With RDS | 40 (RDS instance creation takes ~10-30 min) |

> This is the **ROS-side** `TimeoutInMinutes`; once it elapses ROS marks the stack failed.
> Keep it below step 12's `wait_and_probe.py --max-wait` (default 1200s=20min, pass 2700s=45min with RDS),
> otherwise ROS has already failed the stack while the client keeps waiting.

---

## Tags (auto-applied by script)

- `from=qwencloud`
- `qwencloud-appName=$APP_NAME`
- `qwencloud-appDesc=$APP_DESC`

---

## Parameter Building Logic (internal to script)

The script reads parameters from the JSON file and converts each to `--Parameters.N.ParameterKey / ParameterValue` CLI args.
Agent only needs to ensure the JSON file format is correct — no need to handle CLI arg assembly.

### CreateStack CLI Args (auto-assembled by script)

```
--RegionId $REGION
--StackName $STACK_NAME
--TemplateURL $TEMPLATE_URL
--DisableRollback false
--TimeoutInMinutes $TIMEOUT
--Tags.1.Key from         --Tags.1.Value qwencloud
--Tags.2.Key qwencloud-appName  --Tags.2.Value $APP_NAME
--Tags.3.Key qwencloud-appDesc  --Tags.3.Value $APP_DESC
--Parameters.1.ParameterKey ...  --Parameters.1.ParameterValue ...
```

> ⚠️ `DisableRollback` must be `false` (auto-rollback on creation failure).

---

## Provisional State File (orphan prevention)

After successful creation, immediately writes `.qwencloud-deploy` (`provisional: true`):
- Even if subsequent steps are interrupted, `delete_stack.sh` can locate and clean up the stack
- `record_state.py` (step 13) overwrites this provisional file with complete state
