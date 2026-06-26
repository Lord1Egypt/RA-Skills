# Security Remediation Playbook

**Purpose**: Safe, step-by-step procedures for fixing security issues found by the scanner. All fixes are **configuration-file edits only** — this playbook never instructs the AI agent to run system commands, open network connections, or execute subprocesses.

> **Operator note**: Where a step requires restarting services, running shell
> commands, or verifying network state, it is marked with the label
> **[OPERATOR]** to indicate the human administrator should perform it
> outside of this skill.

## Golden Rules

### Rule 1: Never Brick Remote Deployments

**Before ANY config change:**
1. Create a copy of `~/.openclaw/config.json` (e.g. add a `.backup.<timestamp>` suffix)
2. Confirm you have an alternative way to access the host (SSH, console, secondary channel)
3. Test the restore procedure
4. Schedule a maintenance window
5. Prepare a rollback plan

### Rule 2: Stage High-Risk Changes

```
Phase 1: Preparation (Day 1)
├─ Copy current config as backup
├─ Document current state
├─ Verify alternative access
└─ Notify stakeholders

Phase 2: Staging (Day 2-3)
├─ Apply config change to test environment
├─ Verify functionality
├─ Test rollback
└─ Get approval

Phase 3: Production (Day 4)
├─ Apply config change during maintenance window
├─ Monitor closely (24-48h)
├─ Keep rollback ready
└─ Document changes

Phase 4: Verification (Day 5-7)
├─ Verify security improvement
├─ Check for side effects
├─ Update documentation
└─ Close change ticket
```

### Rule 3: Always Have Rollback

Every fix has a rollback: restore the backed-up `config.json` and **[OPERATOR]** restart the gateway.

---

## Common Fixes

### Fix 1: Restrict Telegram Group Policy

**Risk Level**: CRITICAL  
**Risk of Fix**: LOW (won't break 1:1 chats)

**Current (Unsafe)**:
```json
{
  "channels": {
    "telegram": {
      "groupPolicy": "allow"
    }
  }
}
```

**Target (Safe)**:
```json
{
  "channels": {
    "telegram": {
      "groupPolicy": "allowlist",
      "allowedGroups": ["group-id-1", "group-id-2"]
    }
  }
}
```

**Procedure**:
1. Back up `~/.openclaw/config.json`
2. Edit `channels.telegram.groupPolicy` from `"allow"` to `"allowlist"`
3. Add known group IDs to `channels.telegram.allowedGroups`
4. Validate the JSON is well-formed
5. **[OPERATOR]** Restart the gateway and send a test message from an allowed group

**Rollback**: Restore the backed-up `config.json` and **[OPERATOR]** restart the gateway.

---

### Fix 2: Bind Gateway to Localhost

**Risk Level**: CRITICAL  
**Risk of Fix**: HIGH (will break remote access if not careful)

> **STAGED ROLLOUT REQUIRED** — verify alternative access before applying.

**Current (Unsafe)**:
```json
{
  "gateway": {
    "host": "0.0.0.0",
    "port": 18789
  }
}
```

**Target (Safe)**:
```json
{
  "gateway": {
    "host": "127.0.0.1",
    "port": 18789
  }
}
```

**Procedure**:
1. **[OPERATOR]** Confirm SSH or console access to the host works independently of the gateway
2. Back up `~/.openclaw/config.json`
3. **[OPERATOR]** (Optional, safer first step) Configure host-level firewall rules to restrict port 18789 before changing the bind address
4. Edit `gateway.host` from `"0.0.0.0"` to `"127.0.0.1"`
5. Validate the JSON is well-formed
6. **[OPERATOR]** Restart the gateway during a maintenance window
7. **[OPERATOR]** Verify the service is reachable locally and blocked remotely

**Rollback**: Restore the backed-up `config.json` and **[OPERATOR]** restart the gateway.

---

### Fix 3: Restrict Tool Execution

**Risk Level**: CRITICAL  
**Risk of Fix**: MEDIUM (may break workflows)

**Current (Unsafe)**:
```json
{
  "tools": {
    "exec": {
      "policy": "allow"
    }
  }
}
```

**Target (Safe)**:
```json
{
  "tools": {
    "exec": {
      "policy": "allowlist",
      "allowedCommands": [
        "openclaw status",
        "openclaw gateway restart",
        "git status",
        "ls",
        "cat",
        "grep"
      ]
    }
  }
}
```

**Procedure**:
1. **[OPERATOR]** Review recent logs to identify which commands are actually used
2. Build the `allowedCommands` list from observed usage
3. Back up `~/.openclaw/config.json`
4. Edit `tools.exec.policy` from `"allow"` to `"allowlist"` and add the `allowedCommands` array
5. Validate the JSON is well-formed
6. **[OPERATOR]** Restart the gateway
7. **[OPERATOR]** Monitor logs for denied commands and add missing ones to the allowlist as needed

**Rollback**: Restore the backed-up `config.json` and **[OPERATOR]** restart the gateway.

---

### Fix 4: Enable Web Authentication

**Risk Level**: CRITICAL  
**Risk of Fix**: LOW (won't break, just requires login)

**Current (Unsafe)**:
```json
{
  "channels": {
    "web": {
      "enabled": true,
      "authentication": {
        "enabled": false
      }
    }
  }
}
```

**Target (Safe)**:
```json
{
  "channels": {
    "web": {
      "enabled": true,
      "authentication": {
        "enabled": true,
        "provider": "password",
        "users": [
          {
            "username": "admin",
            "passwordHash": "<bcrypt-hash>"
          }
        ]
      }
    }
  }
}
```

**Procedure**:
1. **[OPERATOR]** Generate a bcrypt password hash (e.g. using `python3 -c "import bcrypt; ..."` or an equivalent tool)
2. Back up `~/.openclaw/config.json`
3. Set `channels.web.authentication.enabled` to `true` and add the `users` array with the hashed password
4. Validate the JSON is well-formed
5. **[OPERATOR]** Restart the gateway and verify the web UI now requires login

**Rollback**: Restore the backed-up `config.json` and **[OPERATOR]** restart the gateway.

---

### Fix 5: Enable TLS for Gateway

**Risk Level**: HIGH  
**Risk of Fix**: MEDIUM (requires certificate provisioning)

**Current (Unsafe)**:
```json
{
  "gateway": {
    "port": 18789
  }
}
```

**Target (Safe)**:
```json
{
  "gateway": {
    "port": 18789,
    "tls": {
      "enabled": true,
      "certFile": "/path/to/cert.pem",
      "keyFile": "/path/to/key.pem"
    }
  }
}
```

**Procedure**:
1. **[OPERATOR]** Obtain a TLS certificate and key (e.g. via Let's Encrypt or your CA)
2. Back up `~/.openclaw/config.json`
3. Add the `gateway.tls` section with `enabled: true` and the certificate/key paths
4. Validate the JSON is well-formed
5. **[OPERATOR]** Restart the gateway and verify HTTPS connectivity

**Rollback**: Remove the `gateway.tls` section (or set `enabled: false`) and **[OPERATOR]** restart the gateway.

---

## Emergency Procedures

### When a Fix Goes Wrong

**Symptoms**: Gateway won't start, can't connect remotely, constant restarts, error loops.

**Recovery**:
1. **[OPERATOR]** Access the host via SSH or console
2. Restore the backed-up `config.json`
3. **[OPERATOR]** Restart the gateway
4. **[OPERATOR]** If still broken, try `openclaw --recovery-mode` (starts with minimal config)

### Post-Mortem Template

```markdown
# Security Fix Incident Report

**Date**: YYYY-MM-DD
**Fix Attempted**: [Description]
**Outcome**: [Success/Partial/Failure]

## Timeline
- HH:MM: Started fix
- HH:MM: Issue detected
- HH:MM: Rollback initiated
- HH:MM: Service restored

## Root Cause
[What went wrong]

## Lessons Learned
1. [Lesson 1]
2. [Lesson 2]

## Action Items
- [ ] Update playbook
- [ ] Improve testing
- [ ] Add monitoring
- [ ] Training needed
```

---

## Monitoring After Fixes

### Verify Security Improvement

1. Re-run this security scanner to confirm findings are resolved
2. **[OPERATOR]** Check gateway logs for errors
3. **[OPERATOR]** Verify expected functionality still works (send test messages, etc.)

### Alert Configuration

Consider adding to your config:
```json
{
  "alerts": {
    "afterFix": {
      "enabled": true,
      "duration": "48h",
      "events": [
        "gateway_restart",
        "config_change",
        "auth_failure",
        "tool_denied"
      ],
      "notify": ["admin-channel"]
    }
  }
}
```

---

## Checklists

### Pre-Fix Checklist
- [ ] Config backup created and verified
- [ ] Alternative access confirmed (SSH / console)
- [ ] Rollback plan documented
- [ ] Maintenance window scheduled (if high-risk)
- [ ] Stakeholders notified

### Post-Fix Checklist
- [ ] Service running normally
- [ ] Security improvement verified (re-run scanner)
- [ ] No functionality broken
- [ ] Documentation updated
- [ ] Backup of new config created

---

**Version**: 1.0.4  
**Last Updated**: 2026-03-12  
**Next Review**: 2026-06-12
