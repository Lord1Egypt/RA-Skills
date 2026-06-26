# Context-Aware Permission Management

**Purpose**: Implement flexible, scenario-based permission switching for OpenClaw to achieve least-privilege security while maintaining usability.

> **Scope**: This reference documents **configuration patterns** only. It does
> not instruct the AI agent to run shell commands or access the network.
> Steps requiring service restarts or CLI interaction are marked **[OPERATOR]**.

## Problem Statement

Traditional permission models face a dilemma:
- **Too restrictive**: Users can't complete legitimate tasks
- **Too permissive**: Security vulnerabilities, potential abuse

**Solution**: Context-aware permissions that adapt based on:
- User identity and role
- Channel type (1:1 vs group)
- Time of day
- Location/network
- Task sensitivity

## Permission Levels

### Level 1: Restricted (Default)
```json
{
  "context": "default",
  "tools": {
    "exec": { "policy": "deny" },
    "fs": { "workspaceOnly": true },
    "enabled": ["read", "search", "web_fetch"]
  }
}
```

**Use cases**: Unknown users, group chats, untrusted channels.

### Level 2: Standard
```json
{
  "context": "trusted_user",
  "tools": {
    "exec": { "policy": "allowlist", "allowedCommands": ["ls", "cat", "grep"] },
    "fs": { "workspaceOnly": true },
    "enabled": ["read", "search", "web_fetch", "write", "edit"]
  }
}
```

**Use cases**: Known users (owner, admins), 1:1 chats, trusted channels.

### Level 3: Elevated
```json
{
  "context": "admin_maintenance",
  "tools": {
    "exec": { "policy": "allowlist", "allowedCommands": ["systemctl", "docker", "git"] },
    "fs": { "workspaceOnly": false, "allowedPaths": ["/var/log", "/etc/openclaw"] },
    "enabled": ["*"]
  },
  "timeLimit": "30m",
  "requireApproval": true
}
```

**Use cases**: System maintenance, debugging, emergency fixes. **Time-limited, requires approval.**

### Level 4: Emergency
```json
{
  "context": "emergency",
  "tools": {
    "exec": { "policy": "allow" },
    "fs": { "workspaceOnly": false }
  },
  "timeLimit": "10m",
  "requireApproval": true,
  "auditLevel": "full",
  "notifyOnUse": true
}
```

**Use cases**: Critical incidents, system recovery. **Strictly time-limited, full audit logging, immediate notification.**

## Implementation Patterns

### Pattern 1: User-Based Contexts

```json
{
  "contexts": {
    "enabled": true,
    "rules": [
      {
        "name": "owner",
        "condition": { "userId": "6055210169" },
        "permissionLevel": "standard"
      },
      {
        "name": "admin",
        "condition": { "roleId": "admin" },
        "permissionLevel": "elevated"
      },
      {
        "name": "unknown",
        "condition": { "userId": "*" },
        "permissionLevel": "restricted"
      }
    ]
  }
}
```

### Pattern 2: Channel-Based Contexts

```json
{
  "contexts": {
    "rules": [
      {
        "name": "private_chat",
        "condition": { "chatType": "direct" },
        "permissionLevel": "standard"
      },
      {
        "name": "group_chat",
        "condition": { "chatType": "group" },
        "permissionLevel": "restricted"
      },
      {
        "name": "admin_channel",
        "condition": { "channelId": "admin-telegram-id" },
        "permissionLevel": "elevated"
      }
    ]
  }
}
```

### Pattern 3: Time-Based Contexts

```json
{
  "contexts": {
    "rules": [
      {
        "name": "business_hours",
        "condition": {
          "timeRange": "09:00-18:00",
          "timezone": "Asia/Shanghai"
        },
        "permissionLevel": "standard"
      },
      {
        "name": "after_hours",
        "condition": {
          "timeRange": "18:00-09:00"
        },
        "permissionLevel": "restricted"
      },
      {
        "name": "maintenance_window",
        "condition": {
          "scheduled": true,
          "timeRange": "02:00-04:00"
        },
        "permissionLevel": "elevated"
      }
    ]
  }
}
```

### Pattern 4: Network-Based Contexts

```json
{
  "contexts": {
    "rules": [
      {
        "name": "trusted_network",
        "condition": {
          "network": "192.168.3.0/24"
        },
        "permissionLevel": "standard"
      },
      {
        "name": "public_network",
        "condition": {
          "network": "*"
        },
        "permissionLevel": "restricted"
      }
    ]
  }
}
```

## Lifecycle Management

### Permission Request Flow

```
┌─────────────┐
│   User      │
│  Request    │
└──────┬──────┘
       │
       ▼
┌─────────────────┐
│ Context Engine  │
│ - Check user    │
│ - Check channel │
│ - Check time    │
│ - Check network │
└──────┬──────────┘
       │
       ▼
┌─────────────────┐
│ Permission      │
│ Level Assigned  │
└──────┬──────────┘
       │
       ▼
┌─────────────────┐     ┌──────────────┐
│ Restricted?     │────►│ Auto-approve │
└──────┬──────────┘     └──────────────┘
       │
       ▼
┌─────────────────┐     ┌──────────────┐
│ Elevated?       │────►│ Require MFA  │
└──────┬──────────┘     │ Time limit   │
       │                └──────────────┘
       ▼
┌─────────────────┐     ┌──────────────┐
│ Emergency?      │────►│ Require      │
└──────┬──────────┘     │ Approval +   │
                        │ Full Audit   │
                        └──────────────┘
```

### Time-Limited Permissions

**[OPERATOR]** Use the OpenClaw CLI to request elevated access:

```
openclaw contexts request --level elevated --duration 30m --reason "Debugging deployment issue"
```

Expected output:
```
✅ Elevated permissions granted
⏰ Expires: 2026-03-08 14:30:00
📋 Reason: Debugging deployment issue
🔔 Notification sent to admins
```

After the time limit expires, the system automatically reverts to the previous level.

### Approval Workflow

```json
{
  "approval": {
    "required": true,
    "approvers": ["user:admin1", "user:admin2"],
    "quorum": 1,
    "timeout": "15m",
    "notification": {
      "channel": "telegram",
      "chatId": "admin-chat-id"
    }
  }
}
```

## Audit Logging

### Log All Permission Changes

```json
{
  "audit": {
    "enabled": true,
    "logLevel": "info",
    "events": [
      "permission_granted",
      "permission_denied",
      "permission_expired",
      "context_switched",
      "elevated_access_used"
    ],
    "retention": "90d",
    "format": "json"
  }
}
```

### Example Log Entry

```json
{
  "timestamp": "2026-03-08T13:45:00Z",
  "event": "permission_granted",
  "user": "6055210169",
  "context": "elevated",
  "previousLevel": "standard",
  "newLevel": "elevated",
  "reason": "Debugging deployment issue",
  "approvedBy": "admin1",
  "expiresAt": "2026-03-08T14:15:00Z",
  "ipAddress": "192.168.3.100"
}
```

## Quick Switch Profiles

**[OPERATOR]** These profiles are switched via the OpenClaw CLI (`openclaw contexts switch <profile>`), not by this skill.

```yaml
profiles:
  restricted:
    description: "Safe mode for public/untrusted scenarios"
    tools:
      exec: deny
      fs: workspace-only
    channels:
      groups: deny
      unknown-users: deny

  standard:
    description: "Normal operation for trusted users"
    tools:
      exec: allowlist
      fs: workspace-only
    channels:
      groups: allowlist
      unknown-users: deny

  elevated:
    description: "Admin tasks, time-limited"
    tools:
      exec: allowlist-extended
      fs: selective-paths
    time-limit: 30m
    requires: approval

  emergency:
    description: "Critical incidents only"
    tools:
      exec: allow
      fs: full
    time-limit: 10m
    requires: 2-approvals, full-audit
```

## Best Practices

### DO
- Default to restricted permissions
- Use time-limited elevated access
- Require approval for sensitive operations
- Log all permission changes
- Regularly audit permission usage
- Implement least-privilege per context

### DON'T
- Grant permanent elevated permissions
- Share elevated access credentials
- Skip approval workflows
- Disable audit logging
- Use emergency mode for routine tasks
- Forget to revoke temporary permissions

## Rollback Procedures

### If Permissions Lock You Out

1. **[OPERATOR]** Access the host via SSH or console
2. Restore `~/.openclaw/config.json` from the backup copy
3. **[OPERATOR]** Restart the gateway

Alternatively, to reset only the context engine, remove the `"contexts"` key from `config.json`:

**Before**:
```json
{
  "contexts": { "enabled": true, "rules": [ ... ] },
  "gateway": { ... }
}
```

**After**:
```json
{
  "gateway": { ... }
}
```

Then **[OPERATOR]** restart the gateway. This disables context-aware permissions and reverts to defaults.

## Monitoring & Alerts

### Alert on Suspicious Activity

```json
{
  "alerts": {
    "rules": [
      {
        "name": "elevated_after_hours",
        "condition": {
          "context": "elevated",
          "timeRange": "22:00-06:00"
        },
        "action": "notify_admin"
      },
      {
        "name": "multiple_denials",
        "condition": {
          "event": "permission_denied",
          "count": 5,
          "window": "5m"
        },
        "action": "notify_admin"
      },
      {
        "name": "emergency_used",
        "condition": {
          "context": "emergency"
        },
        "action": "notify_all_admins"
      }
    ]
  }
}
```

## References

- OpenClaw Security Scanner: `../SKILL.md`
- Remediation Playbook: `remediation-playbook.md`

---

**Version**: 1.0.4  
**Last Updated**: 2026-03-12
