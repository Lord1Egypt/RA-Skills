# Remote Command Execution (TAT)

Use Tencent Automation Tools (TAT) to run commands on Lighthouse instances remotely.

## Run a Command

```bash
tccli tat RunCommand --region ap-guangzhou \
  --InstanceIds '["lhins-xxxxxxxx"]' \
  --Content "uptime && df -h && free -m" \
  --Timeout 60
```

### Parameters

| Parameter | Required | Description |
|-----------|----------|-------------|
| InstanceIds | Yes | Target instance IDs |
| Content | Yes | Shell command content (base64 or plain text) |
| Timeout | No | Timeout in seconds (default 60) |
| CommandType | No | SHELL (default) or POWERSHELL |
| WorkingDirectory | No | Working directory for the command |
| Username | No | User to run the command as |

## Query Command Execution

```bash
# List commands
tccli tat DescribeCommands --region ap-guangzhou

# Query invocation status
tccli tat DescribeInvocations --region ap-guangzhou \
  --InvocationIds '["inv-xxxxxxxx"]'

# Query invocation task results (detailed output)
tccli tat DescribeInvocationTasks --region ap-guangzhou \
  --InvocationTaskIds '["invt-xxxxxxxx"]'
```

## Common Diagnostic Commands

```bash
# System overview
--Content "uptime && df -h && free -m && top -bn1 | head -20"

# Network check
--Content "ss -tlnp && ip addr show"

# Service status
--Content "systemctl list-units --type=service --state=running"

# Disk usage
--Content "df -h && du -sh /var/log/* | sort -rh | head -10"
```

## Workflow

1. Get InstanceId via `DescribeInstances`
2. Run command via `RunCommand` — returns an InvocationId
3. Check status via `DescribeInvocations` with the InvocationId
4. Get detailed output via `DescribeInvocationTasks`

> Commands execute asynchronously. Always check the invocation status before reporting results to the user.