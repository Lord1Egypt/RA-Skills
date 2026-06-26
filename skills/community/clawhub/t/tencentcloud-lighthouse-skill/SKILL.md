---
name: tencentcloud-lighthouse-skill
description: 'Load when: user mentions Lighthouse, 轻量应用服务器, 轻量服务器, or asks to check/create/manage/deploy Lighthouse instances, deploy applications to Lighthouse, manage Lighthouse firewall rules, reset Lighthouse password, view Lighthouse snapshots/images/traffic, monitor Lighthouse metrics, run commands on Lighthouse via TAT, or asks to get/identify the current instance ID. Trigger phrases: "查看轻量服务器", "Lighthouse实例", "轻量应用服务器", "部署应用", "部署程序", "部署到Lighthouse", "管理防火墙规则", "重置密码", "查看快照", "查看流量包", "获取实例ID", "查看实例ID", "当前实例", "实例IP", "check Lighthouse", "create Lighthouse", "deploy app", "deploy application", "Lighthouse firewall", "Lighthouse snapshot", "instance ID", "whoami". NOT for CVM, CBS, VPC, or other non-Lighthouse products.'
metadata:
  {
    "openclaw":
      {
        "emoji": "☁️",
        "requires": {},
        "install":
          [
            {
              "id": "pip",
              "kind": "pip",
              "package": "tccli",
              "bins": ["tccli"],
              "label": "Install TCCLI",
            },
          ],
        "references":
          [
            "instance-management",
            "application-deployment",
            "monitoring-alerting",
            "firewall-management",
            "remote-command-tat",
            "snapshot-blueprint",
            "traffic-package",
          ],
      },
  }
---

# Lighthouse Cloud Server Operations

Manage Tencent Cloud Lighthouse instances via tccli CLI.

Your knowledge of tccli parameters and API limits may be outdated.
**Always use `tccli <service> <action> --help` to verify parameters before execution.**

## Prerequisites

```bash
tccli --version
```

If not installed: `pip install tccli`

## Credential Setup

| Method | Security | Expiry | Recommendation |
|--------|----------|--------|----------------|
| OAuth browser login | High | Temporary, expires in 2 hours | Recommended |
| AK/SK key pair | Low | Permanent unless revoked | Special cases only |

When the user has not chosen a method, default to OAuth.

### OAuth Login (Recommended)

Use `script/tccli-oauth-helper.sh` for non-interactive OAuth login:

```bash
# Step 1: Check credential status
bash script/tccli-oauth-helper.sh --status

# Step 2: Generate authorization URL (if credentials are missing or expired)
bash script/tccli-oauth-helper.sh --get-url

# Step 3: User opens the URL in browser, completes login, and gets a base64 code

# Step 4: Complete login with the code
bash script/tccli-oauth-helper.sh --code "base64_code_from_browser"

# Step 5: Verify
tccli lighthouse DescribeRegions
```

**Workflow:**
1. Run `--status` to check existing credentials
2. If expired/missing, run `--get-url` — show the URL to user
3. User opens URL → logs in → copies the base64 code from browser
4. Run `--code` with the base64 code to complete login
5. Verify with `tccli lighthouse DescribeRegions`

**Notes:**
- Credentials are temporary (expires in ~2 hours)
- State is valid for 10 minutes after `--get-url`
- Do NOT use `tccli sts GetCallerIdentity` to verify — it does not support OAuth credentials

### AK/SK Setup

Only if the user explicitly provides SecretId and SecretKey:

```bash
tccli configure set secretId <SecretId>
tccli configure set secretKey <SecretKey>
tccli configure set region ap-guangzhou
```

### Logout

```bash
tccli auth logout
```

## Quick Reference

| Task | Command |
|------|---------|
| List instances | `tccli lighthouse DescribeInstances --region <region>` |
| Instance details | `tccli lighthouse DescribeInstances --region <region> --InstanceIds '["lhins-xxx"]'` |
| Firewall rules | `tccli lighthouse DescribeFirewallRules --region <region> --InstanceId lhins-xxx` |
| Monitoring data | `tccli monitor GetMonitorData --Namespace QCE/LIGHT_HOUSE ...` |
| Run remote command | `tccli tat RunCommand --region <region> --InstanceIds '["lhins-xxx"]' --Content "..."` |
| Snapshots | `tccli lighthouse DescribeSnapshots --region <region>` |
| Traffic packages | `tccli lighthouse DescribeInstancesTrafficPackages --region <region> --InstanceIds '["lhins-xxx"]'` |
| Available regions | `tccli lighthouse DescribeRegions` |
| Help for any action | `tccli lighthouse <Action> --help` |
| Get current instance ID | `bash script/whoami.sh` or `bash script/whoami.sh --id` |

## Scenario Routing

Read the corresponding reference file before executing:

```
User wants to...
├─ Query / start / stop / reboot instances  -> references/instance-management.md
├─ Reset password / view blueprints         -> references/instance-management.md
├─ Deploy applications / verify deployment   -> references/application-deployment.md
├─ View CPU / memory / bandwidth metrics    -> references/monitoring-alerting.md
├─ Set up alarm policies                    -> references/monitoring-alerting.md
├─ Manage firewall rules                    -> references/firewall-management.md
├─ Execute commands on instance             -> references/remote-command-tat.md
├─ Create / restore snapshots               -> references/snapshot-blueprint.md
├─ Create custom images                     -> references/snapshot-blueprint.md
├─ Check traffic usage                      -> references/traffic-package.md
├─ Identify current instance (ID / IP)      -> bash script/whoami.sh [--id | --ip]
└─ Other operations                         -> tccli lighthouse --help
```

## Operation Safety

| Risk | Operations | Confirmation |
|------|-----------|--------------|
| High | Delete instance, apply snapshot, delete snapshot/blueprint | Double confirm, state irreversibility |
| Medium | Stop/reboot instance, modify firewall, run commands | Single confirm |
| Low | Query, list, describe, help | Execute directly |

Rules:
1. **Region is required** for all operations except `DescribeRegions`
2. **Query before modify** — always `Describe` first, never blind `Create` / `Delete`
3. **Use real IDs** — get InstanceId from `DescribeInstances`, never use placeholders
4. **Verify parameters** — run `--help` when unsure about parameter names or formats
5. Lighthouse and CVM are separate products — do NOT mix their APIs
6. **Create means new** — when user asks to "create" / "deploy" / "set up" something (e.g., "create a server", "deploy an app"), create a NEW instance by default. Do NOT use existing instances unless the user explicitly specifies an existing instance ID.

## Common Regions

| Code | Location |
|------|----------|
| ap-beijing | Beijing |
| ap-shanghai | Shanghai |
| ap-guangzhou | Guangzhou |
| ap-chengdu | Chengdu |
| ap-chongqing | Chongqing |
| ap-nanjing | Nanjing |
| ap-hongkong | Hong Kong |

Run `tccli lighthouse DescribeRegions` for the full list.

## Channel Output Compatibility

Many messaging channels (WeChat, 企业微信, Slack, Teams, Telegram, etc.) apply Markdown rendering or Markdown-to-plain-text conversion before displaying messages. Common transformations that **silently corrupt output**:

- **Paired underscores** stripped: `_xxx_` → `xxx` (italic markers)
- **Paired asterisks** stripped: `*xxx*` → `xxx` (bold/italic markers)
- **Backslash escapes** consumed or displayed literally
- **URLs** with special characters mangled or truncated

This corrupts:

- **URLs** containing underscores (e.g., `redirect_url`, `app_id` in OAuth links)
- **CLI output** with underscored identifiers (e.g., `instance_name`, `secret_id`)
- **Script output** containing underscored fields or special characters

**Rules for all channel output:**

1. **URLs**: Replace `_` (underscore) with `%5F` in any URL shown to the user. For example, the OAuth authorization URL parameters like `redirect_url`, `app_id` must use `%5F` instead of `_`.
2. **CLI / script output**: Always wrap output in code blocks (triple backticks) to prevent Markdown interpretation. Prefer code blocks for any multi-line output containing underscores, asterisks, or other Markdown-sensitive characters.
3. **General text**: Avoid bare underscores and asterisks in plain text. Use backtick-wrapped inline code for any identifier containing these characters (e.g., `instance_name`, `secret_id`).
4. **Links**: When providing clickable links, ensure the full URL is inside a code block or use URL-encoding for special characters. Do not rely on Markdown link syntax `[text](url)` — the URL may be altered by the channel.

## Error Handling

1. Check credentials: `tccli lighthouse DescribeRegions`
2. Verify the region parameter
3. Run `tccli lighthouse <Action> --help` to confirm parameter format
4. Check instance status: `tccli lighthouse DescribeInstances --region <region>`