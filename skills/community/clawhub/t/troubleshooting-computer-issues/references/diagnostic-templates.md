# Diagnostic Templates & Checklists

This document provides structured guidelines and commands for diagnosing computer issues at each difficulty level.

---

## 1. Difficulty-Specific Checklists

### 简单 (Simple)
- **Applicability**: Common installation errors, missing paths, syntax errors, well-known issues.
- **Workflow**:
  1. Extract keywords from the error message.
  2. Match against existing internal knowledge base or [common-solutions.md](common-solutions.md).
  3. Formulate direct, clear step-by-step instructions.
  4. Ask the user to verify by running the software/command.

### 中等 (Medium)
- **Applicability**: Unfamiliar library issues, configuration mismatches, version conflicts.
- **Workflow**:
  1. Search web resources (priority: official docs/repos → reputable developer blogs → stackoverflow).
  2. Enable deep thinking mode: analyze the context of the error.
  3. Avoid copy-pasting answers without understanding the underlying mechanism.
  4. Compare the failing case with a known working baseline/example if available.

### 困难 (Hard)
- **Applicability**: System-level permissions, network port conflicts, background service crashes, resource exhaustion.
- **Workflow**:
  1. Apply the **Medium** strategy.
  2. Determine the OS platform (Windows, macOS, Linux).
  3. Execute targeted diagnostic commands (see Section 2) to collect concrete system state.
  4. Run a minimal mock script/command to verify if the hypothesis holds before applying the fix.

### 极其困难 (Extreme)
- **Applicability**: Intermittent bugs, complex multi-component environment issues, deep-level system errors.
- **Workflow**:
  1. Apply the **Hard** strategy.
  2. Formulate multiple hypotheses.
  3. Subdivide the problem and allocate sub-tasks to parallel agents (see Section 3).
  4. Run iterations of hypotheses, test, verify, and log. Do not exceed 5 iterations without consulting the user.

---

## 2. Cross-Platform Diagnostic Command Reference

Always use the correct command based on the target OS:

| Diagnostic Goal | Windows (PowerShell) | macOS (Terminal) | Linux (Terminal) |
| :--- | :--- | :--- | :--- |
| **Port Occupancy** | `Get-NetTCPConnection -LocalPort <Port>` | `lsof -i :<Port>` | `ss -tlnp \| grep :<Port>` |
| **Process Check** | `Get-Process -Name <Name>` | `ps aux \| grep <Name>` | `ps aux \| grep <Name>` |
| **Environment PATH**| `$env:PATH -split ';'` | `echo $PATH \| tr ':' '\n'` | `echo $PATH \| tr ':' '\n'` |
| **Disk & Storage** | `Get-PSDrive -PSProvider FileSystem` | `df -h` | `df -h` |
| **DNS Resolution** | `Resolve-DnsName <Domain>` | `dig <Domain>` | `dig <Domain>` or `nslookup` |
| **Network Route** | `Test-NetConnection <Host> -Port <P>` | `nc -zv <Host> <Port>` | `nc -zv <Host> <Port>` |
| **System/App Logs** | `Get-EventLog -LogName System -Newest 20`| `log show --last 10m` | `journalctl -xe -n 50` |
| **File Permissions** | `Get-Acl <Path> \| Format-List` | `ls -la <Path>` | `ls -la <Path>` |

---

## 3. Subagent Task Delegation Template (Extreme Difficulty)

When delegating to subagents:
```json
{
  "Subagents": [
    {
      "TypeName": "research",
      "Role": "Log Analyst",
      "Prompt": "Analyze the following logs for stack traces, memory exhaustion signs, or timeout events. List the top 3 potential root causes: <Log Excerpt>"
    },
    {
      "TypeName": "research",
      "Role": "Environment Auditor",
      "Prompt": "Search GitHub issues and official documentation for version compatibility matrices between library A (v1.2) and runtime B (v20). Detail any known conflicts."
    }
  ]
}
```

---

## 4. Ask Clarification Checklist

To avoid dead ends and assumptions, ask the user these questions early if they are not provided:
1. **OS and Environment**: "What OS version, shell, and runtime/language versions are you using?"
2. **Context of Occurrence**: "Does this happen consistently on start, or only after specific actions?"
3. **Recent Changes**: "Did this work previously? If yes, what changed (e.g. system update, dependency upgrade, code modification)?"
4. **Permissions**: "Are you running this command with administrative / sudo privileges?"
