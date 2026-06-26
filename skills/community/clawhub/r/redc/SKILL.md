---
name: redc
description: Red team infrastructure multi-cloud automated deployment tool. Deploy, manage, and monitor cloud instances across Alibaba Cloud, AWS, Tencent Cloud, Volcengine, Huawei Cloud, and more via MCP. Credentials are read from environment variables — only configure the single provider you intend to use. Always inspect templates before applying.
version: 1.0.3
metadata:
  openclaw:
    requires:
      env:
        - ALICLOUD_ACCESS_KEY
        - ALICLOUD_SECRET_KEY
      bins:
        - redc
        - terraform
    emoji: "🔴"
    homepage: https://github.com/wgpsec/redc
    os:
      - macos
      - linux
      - windows
---

# RedC — Red Team Infrastructure Multi-Cloud Automated Deployment

RedC is an open-source red team infrastructure multi-cloud automated deployment tool. It uses Terraform under the hood to manage cloud resources across 6+ cloud providers.

**GitHub**: https://github.com/wgpsec/redc
**Template Registry**: https://redc.wgpsec.org

## Security & Credentials

### Credential Model

RedC reads cloud provider credentials from **environment variables** or a local **config.yaml** file managed by the `redc` CLI. Credentials are only passed to Terraform, which communicates directly with cloud provider APIs over HTTPS. No credentials are sent to the redc project, the template registry, or any third-party service.

**The metadata declares `ALICLOUD_ACCESS_KEY` and `ALICLOUD_SECRET_KEY` as the example required env vars** because Alibaba Cloud is the most commonly used provider. However, **you should substitute these with the credentials for whichever single provider you actually use.** The full list of provider-specific env vars that RedC/Terraform may read:

| Provider | Environment Variables | Notes |
|----------|----------------------|-------|
| Alibaba Cloud | `ALICLOUD_ACCESS_KEY`, `ALICLOUD_SECRET_KEY`, `ALICLOUD_REGION` | Declared in metadata |
| AWS | `AWS_ACCESS_KEY_ID`, `AWS_SECRET_ACCESS_KEY`, `AWS_DEFAULT_REGION` | Set only if using AWS |
| Tencent Cloud | `TENCENTCLOUD_SECRET_ID`, `TENCENTCLOUD_SECRET_KEY` | Set only if using Tencent |
| Volcengine | `VOLCENGINE_ACCESS_KEY`, `VOLCENGINE_SECRET_KEY` | Set only if using Volcengine |
| Huawei Cloud | `HW_ACCESS_KEY`, `HW_SECRET_KEY` | Set only if using Huawei |
| Azure | `ARM_CLIENT_ID`, `ARM_CLIENT_SECRET`, `ARM_TENANT_ID`, `ARM_SUBSCRIPTION_ID` | Set only if using Azure |

**You do NOT need to set all of these.** Only configure the env vars for the **single provider** you intend to deploy to. RedC will not attempt to read or use credentials for providers you are not deploying to.

### Credential Best Practices

- Use **scoped, short-lived credentials** with minimal permissions (e.g., only ECS/EC2 create/delete, no IAM/billing access).
- Test in **isolated/throwaway cloud accounts** to avoid impacting production resources.
- Do **NOT** paste long-lived root/owner keys into chat — configure them via `redc` CLI or environment variables before using this skill.
- Prefer scoped **IAM roles** or **temporary security tokens** (e.g., AWS STS AssumeRole) over static AK/SK pairs.

### Binary Verification

- Download `redc` only from official GitHub releases: https://github.com/wgpsec/redc/releases — verify SHA256 checksums listed in each release.
- Download `terraform` only from HashiCorp: https://developer.hashicorp.com/terraform/downloads — verify PGP signatures.

### Template Safety — IMPORTANT

Templates define the actual cloud infrastructure that will be created. They may contain:
- `remote-exec` provisioners that run arbitrary scripts on created instances
- `user_data` / `cloud-init` scripts that execute on instance boot
- Security group rules that open network ports (e.g., 0.0.0.0/0 ingress)
- `local-exec` provisioners that run commands on your local machine

**Before applying any template, you MUST:**

1. **Inspect the template source** — Run `get_template_info` to view the template's `main.tf`, `variables.tf`, and other files. Read them to understand what resources will be created.
2. **Use `plan_case` first** — This runs `terraform plan` to show a preview of all resources that will be created, modified, or destroyed. Review the plan output before proceeding to `start_case`.
3. **Audit registry templates** — The official template repository is fully open-source at https://github.com/wgpsec/redc-template. Compare pulled templates against the source to ensure they have not been tampered with.
4. **Do NOT blindly apply** — Never run `start_case` without first reviewing the plan. This skill will always use `plan_case` before `start_case` to give you a chance to review.

### MCP Server Exposure

- The built-in MCP server defaults to `stdio` transport (local only, no network exposure).
- The `sse` mode binds to a configurable address — always restrict it to `127.0.0.1` and do not expose it to untrusted networks.

## When to Use This Skill

Use this skill when the user wants to:
- Deploy cloud infrastructure (ECS, EC2, CVM, proxy pools, C2 servers, etc.)
- Manage running cloud instances (start, stop, destroy)
- Execute commands on remote servers via SSH
- Check cloud account balances and billing
- Estimate deployment costs
- Schedule automated start/stop for cloud resources
- Manage multi-cloud provider profiles and credentials
- Use redc-compose for multi-service orchestrated deployments

## Supported Cloud Providers

| Provider | Template Prefix | Description |
|----------|----------------|-------------|
| Alibaba Cloud (阿里云) | `aliyun/` | ECS, proxy, VPC, etc. |
| AWS | `aws/` | EC2, proxy, etc. |
| Tencent Cloud (腾讯云) | `tencent/` | CVM, lighthouse, etc. |
| Volcengine (火山引擎) | `volcengine/` | ECS, etc. |
| Huawei Cloud (华为云) | `huaweicloud/` | ECS, etc. |
| Azure | `azure/` | VM, etc. |

## Architecture

RedC has two modes:
1. **CLI mode** (`redc` binary) — command-line operations
2. **GUI mode** (`redc-gui`) — desktop application with built-in MCP server

The MCP server exposes all tools below. It can run in `stdio` or `sse` mode.

---

## Tools

### 1. list_templates

List all available redc templates/images installed locally.

**Command:**
```bash
redc list
```

**MCP Tool:** `list_templates`

Returns template names, descriptions, versions, and supported providers.

---

### 2. search_templates

Search for templates in the official registry by keywords.

**Command:**
```bash
redc search <query>
```

**MCP Tool:** `search_templates`
- `query` (string, required): Search query (e.g., "aliyun", "proxy", "ecs")
- `registry_url` (string, optional): Registry base URL (default: https://redc.wgpsec.org)

---

### 3. pull_template

Download a template from the registry.

**Command:**
```bash
redc pull <template_name>
```

**MCP Tool:** `pull_template`
- `template_name` (string, required): Template name (e.g., "aliyun/ecs" or "aliyun/ecs:1.0.1")
- `registry_url` (string, optional): Registry base URL
- `force` (boolean, optional): Force re-download even if template exists

---

### 4. list_cases

List all cases (scenes/deployments) in the current project with their status.

**Command:**
```bash
redc ps
```

**MCP Tool:** `list_cases`

Returns case ID, name, status (created/running/stopped/error/terminated), template type, and creation time.

**Status values:**
- `created` — case planned but not yet applied
- `running` — infrastructure is live
- `stopped` — infrastructure destroyed, state preserved
- `error` — deployment failed
- `terminated` — spot instance was reclaimed

---

### 5. plan_case

Plan a new case from a template (preview resources without creating them).

**Command:**
```bash
redc plan <template_name> [--name <case_name>] [--var key=value ...]
```

**MCP Tool:** `plan_case`
- `template_name` (string, required): Template name (e.g., "aliyun/ecs")
- `case_name` (string, optional): Case name (auto-generated if not provided)
- `vars` (string, optional): Environment variables for the template

---

### 6. start_case

Start (apply) a case — creates the cloud infrastructure.

**Command:**
```bash
redc up <case_id>
```

**MCP Tool:** `start_case`
- `case_id` (string, required): Case ID to start

---

### 7. stop_case

Stop (destroy) a case — tears down the cloud infrastructure.

**Command:**
```bash
redc down <case_id>
```

**MCP Tool:** `stop_case`
- `case_id` (string, required): Case ID to stop

---

### 8. kill_case

Remove a case completely (destroy infrastructure + delete all local state).

**Command:**
```bash
redc rm <case_id>
```

**MCP Tool:** `kill_case`
- `case_id` (string, required): Case ID to remove

---

### 9. get_case_status

Get detailed status of a specific case.

**MCP Tool:** `get_case_status`
- `case_id` (string, required): Case ID to check

---

### 10. get_case_outputs

Get terraform outputs for a case (IP addresses, passwords, instance IDs, etc.).

**MCP Tool:** `get_case_outputs`
- `case_id` (string, required): Case ID to get outputs

---

### 11. exec_command

Execute a command on a remote server via SSH.

**MCP Tool:** `exec_command`
- `case_id` (string, required): Case ID
- `command` (string, required): Shell command to execute

---

### 12. get_ssh_info

Get SSH connection information for a case (host, port, user, password/key).

**MCP Tool:** `get_ssh_info`
- `case_id` (string, required): Case ID

---

### 13. upload_file

Upload a local file to a remote case server via SCP/SFTP.

**MCP Tool:** `upload_file`
- `case_id` (string, required): Case ID
- `local_path` (string, required): Local file path
- `remote_path` (string, required): Remote destination path

---

### 14. download_file

Download a file from a remote case server to local machine.

**MCP Tool:** `download_file`
- `case_id` (string, required): Case ID
- `remote_path` (string, required): Remote file path
- `local_path` (string, required): Local destination path

---

### 15. get_template_info

Get detailed information about a locally installed template (metadata, variables, files).

**MCP Tool:** `get_template_info`
- `template_name` (string, required): Template name (e.g., "aliyun/ecs")

---

### 16. delete_template

Delete a locally installed template.

**MCP Tool:** `delete_template`
- `template_name` (string, required): Template name to delete

---

### 17. get_config

Get current redc configuration (project path, proxy settings, etc.).

**MCP Tool:** `get_config`

---

### 18. validate_config

Validate cloud provider configuration (check if credentials, region, instance type are valid).

**MCP Tool:** `validate_config`
- `provider` (string, required): Cloud provider name (e.g., "aliyun", "aws", "tencentcloud")
- `region` (string, optional): Region ID (e.g., "cn-hangzhou")
- `instance_type` (string, optional): Instance type (e.g., "ecs.t6-c1m1.large")

---

### 19. get_cost_estimate

Estimate deployment cost for a template (hourly and monthly cost breakdown by resource).

**MCP Tool:** `get_cost_estimate`
- `template_name` (string, required): Template name

---

### 20. get_balances

Query cloud account balances for configured providers.

**MCP Tool:** `get_balances`
- `providers` (string, optional): Comma-separated provider names (e.g., "aliyun,aws"). Empty = all providers.

---

### 21. get_resource_summary

Get a summary of cloud resources across all configured providers (instance counts, running status, etc.).

**MCP Tool:** `get_resource_summary`

---

### 22. get_predicted_monthly_cost

Get predicted total monthly cost based on currently running resources.

**MCP Tool:** `get_predicted_monthly_cost`

---

### 23. get_bills

Get cloud billing information for configured providers.

**MCP Tool:** `get_bills`
- `providers` (string, optional): Comma-separated provider names. Empty = all.

---

### 24. get_total_runtime

Get total runtime of all running cases.

**MCP Tool:** `get_total_runtime`

---

### 25. compose_preview

Preview a redc-compose deployment: list services, dependencies, providers, and replicas without deploying.

**MCP Tool:** `compose_preview`
- `file` (string, optional): Compose file path (default: redc-compose.yaml)
- `profiles` (string, optional): Comma-separated profiles (e.g., "prod,attack")

---

### 26. compose_up

Start a redc-compose deployment (deploys all services in dependency order).

**MCP Tool:** `compose_up`
- `file` (string, optional): Compose file path
- `profiles` (string, optional): Comma-separated profiles

---

### 27. compose_down

Destroy a redc-compose deployment (destroys all services in reverse dependency order).

**MCP Tool:** `compose_down`
- `file` (string, optional): Compose file path
- `profiles` (string, optional): Comma-separated profiles

---

### 28. list_deployments

List all custom deployments in the current project.

**MCP Tool:** `list_deployments`

---

### 29. start_deployment

Start a custom deployment by ID.

**MCP Tool:** `start_deployment`
- `deployment_id` (string, required): Custom deployment ID

---

### 30. stop_deployment

Stop a custom deployment by ID.

**MCP Tool:** `stop_deployment`
- `deployment_id` (string, required): Custom deployment ID

---

### 31. list_projects

List all redc projects.

**MCP Tool:** `list_projects`

---

### 32. switch_project

Switch to a different redc project.

**MCP Tool:** `switch_project`
- `project_name` (string, required): Project name to switch to

---

### 33. list_profiles

List all cloud provider profiles (credential sets).

**MCP Tool:** `list_profiles`

---

### 34. get_active_profile

Get the currently active cloud provider profile.

**MCP Tool:** `get_active_profile`

---

### 35. set_active_profile

Switch the active cloud provider profile.

**MCP Tool:** `set_active_profile`
- `profile_id` (string, required): Profile ID to activate

---

### 36. schedule_task

Schedule a future task for a case (start or stop at a specific time).

**MCP Tool:** `schedule_task`
- `case_id` (string, required): Case ID
- `case_name` (string, required): Case name
- `action` (string, required): Action to perform ("start" or "stop")
- `scheduled_at` (string, required): Time in RFC3339 format (e.g., "2025-01-15T10:30:00Z")

---

### 37. list_scheduled_tasks

List all pending scheduled tasks.

**MCP Tool:** `list_scheduled_tasks`

---

### 38. cancel_scheduled_task

Cancel a pending scheduled task.

**MCP Tool:** `cancel_scheduled_task`
- `task_id` (string, required): Task ID to cancel

---

## Common Workflows

### Deploy a proxy pool

```bash
# 1. Pull the template
redc pull aliyun/proxy

# 2. Plan the case (preview)
redc plan aliyun/proxy --var node=5 --var port=8388 --var password=MySecurePass

# 3. Start it
redc up <case_id>

# 4. Check outputs (IPs, passwords)
redc output <case_id>
```

### Check running infrastructure

```bash
# List all cases
redc ps

# Get cost summary
# (via MCP) get_predicted_monthly_cost, get_balances
```

### Orchestrated multi-service deployment

```yaml
# redc-compose.yaml
services:
  proxy:
    template: aliyun/proxy
    variables:
      node: 3
      port: 8388
  c2:
    template: aws/ec2
    depends_on:
      - proxy
```

```bash
redc compose up
redc compose down
```

## Summary

| Action | CLI Command | MCP Tool |
|--------|-------------|----------|
| List templates | `redc list` | `list_templates` |
| Search registry | `redc search <q>` | `search_templates` |
| Pull template | `redc pull <name>` | `pull_template` |
| List cases | `redc ps` | `list_cases` |
| Plan case | `redc plan <tmpl>` | `plan_case` |
| Start case | `redc up <id>` | `start_case` |
| Stop case | `redc down <id>` | `stop_case` |
| Remove case | `redc rm <id>` | `kill_case` |
| Get outputs | `redc output <id>` | `get_case_outputs` |
| SSH exec | — | `exec_command` |
| Cost estimate | — | `get_cost_estimate` |
| Account balance | — | `get_balances` |
| Compose up | `redc compose up` | `compose_up` |
| Compose down | `redc compose down` | `compose_down` |
| Schedule task | — | `schedule_task` |
