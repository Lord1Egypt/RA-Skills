# Preflight Checks

This file defines the shared preflight checks for `volcengine-landing-zone`.

## 1. Tool Checks

```bash
which terraform && terraform version
which ve && ve version
which python3 && python3 --version
```

- If `ve` is unavailable, prefer the latest installation instructions from the official README instead of maintaining fixed install steps inside this skill.
- Official README: <https://github.com/volcengine/volcengine-cli/blob/master/README.MD>

## 2. Credential and Provider Checks

```bash
ve sts GetCallerIdentity 2>&1
```

Core rules:

- A working `ve` CLI does **not** automatically mean the Terraform Provider is usable. They use **separate** credential sources.
- The `ve` CLI console login (`ve login`) stores only a `login-session` token in `~/.volcengine/config.json`; the credential fields required by the Terraform provider stay **empty**. The CLI exchanges the session for temporary credentials internally per request and never writes AK/SK to disk. **Therefore the agent cannot extract AK/SK/SessionToken from the `ve` profile, and the Terraform `volcenginecc` provider cannot reuse the console-login profile** (its profile mode expects explicit credential fields, which remain empty here).
- The `volcenginecc` provider needs its own credentials. If `terraform plan` reports `Either (AccessKey and SecretKey) or Profile must be provided`, treat it as **Terraform provider credentials not configured**, not a blueprint bug.
- **Guide the user to configure Terraform provider credentials themselves** before real execution, following the official provider docs: <https://github.com/volcengine/terraform-provider-volcenginecc>. The current blueprints declare `provider "volcenginecc" { region = var.region }` with no inline credentials, so the recommended path is **environment variables**:
  - `export VOLCENGINE_ACCESS_KEY=<ak>` / `export VOLCENGINE_SECRET_KEY=<sk>` / `export VOLCENGINE_REGION=<region>` (recommended; nothing written to disk).
  - Alternatively a profile holding real AK/SK referenced via `VOLCENGINE_PROFILE` (provider default `file_path` is `~/.volcengine`). Note this must be an AK/SK profile, **not** the console-login profile.
  - Static `access_key`/`secret_key` inside the `.tf` is officially discouraged (secret-leak risk) and should not be suggested.
- Before Terraform runs, confirm the current process can actually read valid `VOLCENGINE_ACCESS_KEY`, `VOLCENGINE_SECRET_KEY`, and `VOLCENGINE_REGION` (or an AK/SK profile). If not, stop and ask the user to complete the credential setup above; do not paste AK/SK on their behalf and do not create extra credential files.

If `ve sts GetCallerIdentity` fails:

- Prefer the `Console 登录 (login)` section in the official Volcengine CLI README.
- Console login docs: <https://github.com/volcengine/volcengine-cli/blob/master/README.MD#console-%E7%99%BB%E5%BD%95-login>
- The default profile name is `landingzone`.
- During consulting, design, or evaluation, only explain that a valid login state will be required before real execution. Do not start the login flow directly.
- Enter the login branch only after the user explicitly decides to continue with real execution.
- When a reusable existing profile is available, reuse it first. Re-login only if it is clearly expired, conflicting, or otherwise unusable.
- When a login is needed, the agent **runs it directly and non-interactively**: `ve login -p <selected_profile> -r <region>`. Do not hand this command back to the user to run manually. Use `--remote` only when the current environment cannot complete the local redirect flow.
- Within the same preflight run, once `selected_profile` is confirmed reusable or one successful login is completed, reuse it for later phases by default and do not trigger a second `ve login`.
- Later login checks should prefer read-only commands. Re-enter the login branch only when the profile is clearly missing, expired, invalid, or absent.

## 3. Execution Context Checks

> Path anchors: any `./skills/volcengine-landing-zone/...` and `./volcengine-landing-zone-workspace/...` path in this file or elsewhere resolves through the `Path Anchors` section in `SKILL.md` as `${SKILL_ROOT}/...` and `${WORKSPACE_ROOT}/...`. Do not depend on process cwd.

- Resolve `SKILL_ROOT` first, the install root that contains `SKILL.md`, and `WORKSPACE_ROOT`, the writable runtime root that defaults to `<current working directory>/volcengine-landing-zone-workspace/`.
- Confirm that the current working directory is correct and writable, or that the user explicitly provided a writable runtime root.
- Confirm that `./skills/volcengine-landing-zone/assets/blueprints/` exists and contains the blueprints required for this run.
- If the flow will enter `04-log`, confirm that `./skills/volcengine-landing-zone/assets/blueprints/landing-zone-setup/04-log/tos_activate.py` exists.
- The runtime root is always `./volcengine-landing-zone-workspace/`; create it automatically if it does not exist.
- Before real execution begins, sync the blueprints into `./volcengine-landing-zone-workspace/blueprints/`.
- Built-in blueprint sources inside the skill are read-only in the execution chain. See G3. Custom changes must land only in workspace execution copies.
- Runtime directories such as `account-factory/` and `account-factory/runs/` may be created automatically.

## 4. Path-Specific Extra Checks

- `Consulting and Solution Design`
  - Under G5, this path is read-only: explain concepts, ordering, value, and recommendations only. Do not start any real execution action such as preflight, login, blueprint sync, or writes.

- `Initial Landing Zone Setup`
  - Under G1, confirm that solution confirmation is already complete, meaning the solution document has been displayed and the user has confirmed it, before entering further preflight.
  - Run `ve organization DescribeOrganization` first. If the organization already exists, then run `ve organization ListOrganizationalUnits --body '{}'` to fetch the root OU.
  - If it returns `RecordNotExists` or a similar `organization not exists`, treat that as the normal initial state for a first-time setup and continue with `ve organization CreateOrganization --body '{}'`.
  - If `CreateOrganization` returns `NoPermissionOnVerificationError`, recognize it as missing enterprise real-name verification. Stop and guide the user to complete verification at <https://console.volcengine.com/user/authentication/detail/>.
  - When the organization already exists, automatically scan the standard OUs `Platform`, `Applications`, `SandBox`, plus `Dev`, `Staging`, and `Prod` under `Applications` before entering `01-organization`.
  - For any standard OU that is stably detected, inject the corresponding `existing_*_ou_id` before Terraform runs. Ask the user for OU IDs only if stable auto-detection fails.

- `Account Creation and Baseline Setup`
  - Before account creation, check that the minimum account-creation input is complete.
  - Before baseline creation, confirm that `account-factory/baseline/` can be created and written.
  - Before baseline apply, confirm that the target `*.baseline.json` exists and conforms to `references/account-factory/baseline.schema.json`.
  - When applying a baseline, pass `workspace_root` explicitly and confirm that it points at `./volcengine-landing-zone-workspace/`.
  - If the baseline includes `identity` capability, confirm that `ve cloudidentity GetServiceStatus` has already been checked. If the service is not enabled, run `EnableService` first.

- `Cross-account execution phases`
  - Do not block earlier global preflight steps just because `AssumeRole` is not yet available.
  - Check cross-account `AssumeRole` suitability only right before entering `04-log`, `05-network`, or a cross-account networking module inside baseline apply.
  - If the current `ve` login comes from the Volcengine primary account and the next step really needs cross-account `AssumeRole`, stop before that phase and tell the user to re-login with an IAM sub-user that has `STSAssumeRoleAccess`.

- `Failure Recovery`
  - Confirm the failure point, the latest execution artifacts, and the current resource state first.
  - If the issue involves `ConcurrentException`, partial success, or state drift, reconcile first and regenerate a plan later.

## 5. Failure Handling

- If any required check fails, stop real execution.
- Explain the problem first, then give a repair suggestion. After repair, restart from preflight.
- A missing directory is not automatically a failure. Treat it as a real blocker only when blueprints cannot be populated, the workspace cannot be created, the runtime root is not writable, or results cannot be written.
- `DescribeOrganization` or `ListOrganizationalUnits` returning `organization not exists` is not a failure for first-time setup. Treat it as blocking only when organization creation itself fails or the root OU still cannot be obtained afterward.
