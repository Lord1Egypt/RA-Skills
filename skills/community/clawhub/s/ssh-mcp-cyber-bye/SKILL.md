---
name: ssh-mcp-cyber-bye
description: Manage persistent SSH connections, execute async non-blocking commands, handle concurrent bulk executions across fleets, and manage SSH keys and client assignments.
version: 2.0.0
metadata:
  openclaw:
    emoji: "🔑"
    requires:
      bins:
        - node
      mcp:
        - ssh_server_status
        - ssh_stream_info
        - ssh_tool_search
        - ssh_conn
        - ssh_exec
        - ssh_shell
        - ssh_sftp
        - ssh_file
        - ssh_key
        - ssh_bulk_exec
        - ssh_bulk_audit
        - ssh_bulk_conn
        - ssh_client
---

# SSH Connection & Execution Management Skill

> [!IMPORTANT]
> **Dependency Warning:**
> This skill requires the `ssh_mcp` server to be running and registered with the Model Context Protocol (MCP) host. It enables secure, persistent, non-blocking execution across remote Linux servers.

This skill equips the agent to manage remote SSH connection lifecycles, perform system updates, troubleshoot connectivity, and execute commands in bulk across server fleets.

---

## Guidelines for the Agent

### 1. Connection Discovery & Diagnostics
- Use `ssh_conn` (action `list`) to view all saved connection configurations.
- Use `ssh_conn` (action `test`) to check remote host reachability before saving a new target connection.
- Use `ssh_conn` (action `save`) to store connections in the SQLite database to avoid hardcoding auth credentials or private keys in scripts.

### 2. Session Lifecycle Management
- To run commands, first call `ssh_exec` (action `open`) with the target connection ID. This establishes a persistent SSH connection and returns a `sessionId`.
- Re-use active sessions across multiple command runs instead of repeatedly opening new connections. Monitor active sessions using `ssh_exec` (action `list`).
- Always finalize your work by calling `ssh_exec` (action `close`) with the `sessionId` to release resources and prevent orphan connections on remote hosts.

### 3. Non-Blocking Execution Protocol
- Execute commands using `ssh_exec` (action `run`) on an open `sessionId`. This returns a `commandId` immediately and does not block the agent's execution.
- Monitor the execution state using `ssh_exec` (action `status`) with the `commandId`.
- Retrieve command output logs using `ssh_exec` (action `logs`). Since remote commands can produce long outputs, always use appropriate log filters:
  - `grep`: Filter output lines matching a regex or substring.
  - `head` / `tail`: Limit the number of lines returned.
  - `fromLine` / `toLine`: Fetch specific line ranges.
  - `stream`: Target `stdout`, `stderr`, or `both`.

### 4. Asynchronous Bulk Execution
- When executing the same command across a client's server fleet, use `ssh_bulk_exec` or `ssh_bulk_audit` instead of sequentially looping.
- **Dynamic Session Reuse & Auto-Cleanup**: 
  - If a connection already has an active session, `ssh_bulk_exec` will automatically reuse it.
  - If no session exists, it creates a transient session, executes the command, and automatically cleans up (closes) the session once execution finishes.
- **Log Aggregation**:
  - Track bulk execution progress by passing `bulkExecId` to `ssh_exec` (action `status` or `logs`).
  - Retrieve aggregated log output for all targets under the bulk ID, or filter for a specific target by specifying the `connectionId`, `name`, or `host`.

### 5. Multi-Client Organization
- Use `ssh_client` (action `list`) to inspect current client groups.
- Assign or remove connections under specific client ownerships using `ssh_client` with action `assign` or `remove`. This keeps server fleets clean and traceable by client context.

### 6. SSH Key Management
- Link stored private keys to connections using `ssh_key` (action `link`).
- Never store plaintext private keys directly inside connection files. Use `ssh_key` (action `add`) to import the private key content securely, and link it to the target connections.

---

## Tool Call Examples

### 1. Key & Connection Management

**Add an SSH Private Key:**
```json
{
  "name": "ssh_key",
  "arguments": {
    "op": "add",
    "keyName": "prod-deploy-key",
    "privateKey": "-----BEGIN OPENSSH PRIVATE KEY-----\nb3BlbnNzaC1rZXktdjEAAAAABG5vbmUAAAAEbm9uZQAAAAAAAAABAAAAMwAAAAtzc2gtZW\n..."
  }
}
```

**Save a New Connection with a Linked Key:**
```json
{
  "name": "ssh_conn",
  "arguments": {
    "op": "save",
    "name": "production-app-server",
    "host": "192.168.1.50",
    "port": 22,
    "username": "ubuntu",
    "client": "AcmeCorp"
  }
}
```
*Tip: After saving, link the key using:*
```json
{
  "name": "ssh_key",
  "arguments": {
    "op": "link",
    "keyName": "prod-deploy-key",
    "connectionId": "uuid-of-production-app-server"
  }
}
```

---

### 2. Connection Lifecycle & Non-Blocking Execution

**Open Session:**
```json
{
  "name": "ssh_exec",
  "arguments": {
    "op": "open",
    "connectionId": "uuid-of-production-app-server"
  }
}
```
*Returns:* `Session ID: 9f8e7d6c-5b4a-3f2e-1d0c-9b8a7f6e5d4c`

**Run a Command Asynchronously:**
```json
{
  "name": "ssh_exec",
  "arguments": {
    "op": "run",
    "sessionId": "9f8e7d6c-5b4a-3f2e-1d0c-9b8a7f6e5d4c",
    "command": "apt-get update && apt-get upgrade -y"
  }
}
```
*Returns:* `Command ID: a1b2c3d4-e5f6-7a8b-9c0d-1e2f3a4b5c6d`

**Check Status & Fetch Filtered Logs:**
```json
{
  "name": "ssh_exec",
  "arguments": {
    "op": "status",
    "commandId": "a1b2c3d4-e5f6-7a8b-9c0d-1e2f3a4b5c6d"
  }
}
```
```json
{
  "name": "ssh_exec",
  "arguments": {
    "op": "logs",
    "commandId": "a1b2c3d4-e5f6-7a8b-9c0d-1e2f3a4b5c6d",
    "tail": 50,
    "grep": "error"
  }
}
```

**Disconnect Session:**
```json
{
  "name": "ssh_exec",
  "arguments": {
    "op": "close",
    "sessionId": "9f8e7d6c-5b4a-3f2e-1d0c-9b8a7f6e5d4c"
  }
}
```

---

### 3. Bulk Execution & Fleet Audits

**Execute Command Across Multiple Targets (Async):**
```json
{
  "name": "ssh_bulk_exec",
  "arguments": {
    "commands": ["systemctl restart nginx", "systemctl status nginx"],
    "connectionIds": ["server-uuid-1", "server-uuid-2", "server-uuid-3"],
    "concurrency": 5
  }
}
```
*Returns:* `bulkExecId: e8d7c6b5-a4f3-9e2d-8c1b-7a0f9e8d7c6b`

**Monitor Bulk Status:**
```json
{
  "name": "ssh_exec",
  "arguments": {
    "op": "status",
    "bulkExecId": "e8d7c6b5-a4f3-9e2d-8c1b-7a0f9e8d7c6b"
  }
}
```

**Fetch Aggregated Logs for the Bulk Run:**
```json
{
  "name": "ssh_exec",
  "arguments": {
    "op": "logs",
    "bulkExecId": "e8d7c6b5-a4f3-9e2d-8c1b-7a0f9e8d7c6b",
    "tail": 20
  }
}
```

**Fetch Logs for a Specific Target in a Bulk Run:**
```json
{
  "name": "ssh_exec",
  "arguments": {
    "op": "logs",
    "bulkExecId": "e8d7c6b5-a4f3-9e2d-8c1b-7a0f9e8d7c6b",
    "connectionId": "server-uuid-1",
    "tail": 20
  }
}
```

**Run Bulk Security Audit (Synchronous):**
```json
{
  "name": "ssh_bulk_audit",
  "arguments": {
    "op": "security",
    "client": "AcmeCorp",
    "concurrency": 3
  }
}
```

---

## Execution Flow Examples

### Flow 1: Persistent Single-Server Command Lifecycle

```mermaid
sequenceDiagram
    participant LLM as OpenClaw Agent
    participant MCP as SSH MCP Server
    participant Host as Target Linux Server

    LLM->>MCP: ssh_exec(op="open", connectionId="web-server-uuid")
    MCP->>Host: SSH Handshake & Connect
    Host-->>MCP: Handshake Success
    MCP-->>LLM: sessionId="9f8e7d6c..."

    Note over LLM, Host: Run multiple sequential tasks on the same persistent session
    LLM->>MCP: ssh_exec(op="run", sessionId="9f8e7d6c...", command=["apt-get update", "apt-get upgrade -y"])
    MCP-->>LLM: commandId="cmd-12345" (returns immediately)

    MCP->>Host: Execute "apt-get update"
    Host-->>MCP: stdout/stderr logs stream
    Note right of MCP: Stream logs to SQLite
    MCP->>Host: Execute "apt-get upgrade -y"
    Host-->>MCP: stdout/stderr logs stream

    LLM->>MCP: ssh_exec(op="status", commandId="cmd-12345")
    MCP-->>LLM: Status: running / completed / failed

    LLM->>MCP: ssh_exec(op="logs", commandId="cmd-12345", tail=20)
    MCP-->>LLM: [stdout] ... Completed successfully!

    LLM->>MCP: ssh_exec(op="close", sessionId="9f8e7d6c...")
    MCP->>Host: Close Connection
    MCP-->>LLM: Success
```

---

### Flow 2: Asynchronous Bulk Execution with Transient Sessions

```mermaid
sequenceDiagram
    participant LLM as OpenClaw Agent
    participant MCP as SSH MCP Server
    participant Srv1 as Server 1 (No active session)
    participant Srv2 as Server 2 (Active session exists)

    LLM->>MCP: ssh_bulk_exec(commands=["docker ps"], connectionIds=["srv1-id", "srv2-id"])
    MCP-->>LLM: bulkExecId="bulk-abc-123", status="running"

    par Server 1 Execution
        Note over MCP, Srv1: No active session → Create transient session
        MCP->>Srv1: Open Dynamic Connection
        MCP->>Srv1: Execute "docker ps"
        Srv1-->>MCP: Command Completed
        Note over MCP, Srv1: Auto-disconnect transient session
        MCP->>Srv1: Disconnect Session
    and Server 2 Execution
        Note over MCP, Srv2: Active session found → Re-use it
        MCP->>Srv2: Execute "docker ps" on existing channel
        Srv2-->>MCP: Command Completed
        Note over MCP, Srv2: Keep session open for future reuse
    end

    Note over LLM, MCP: Monitor bulk run progress and logs
    LLM->>MCP: ssh_exec(op="status", bulkExecId="bulk-abc-123")
    MCP-->>LLM: targets: [Srv1: completed, Srv2: completed]

    LLM->>MCP: ssh_exec(op="logs", bulkExecId="bulk-abc-123", tail=10)
    MCP-->>LLM: Aggregated logs JSON output for all servers
```

---

## Edge Cases and Failure Handling

1. **Connection Timeouts & Failures**:
   - If `ssh_exec` (action `open`) fails, check connection credentials, firewall rules, and key links. Use `ssh_conn` (action `test`) to run diagnostics.
   
2. **Channel Concurrency Limitations**:
   - If the remote server enforces strict session channel limits (`MaxSessions`), concurrent executions may fail to open channels. The SSH MCP server implements a self-healing queue that detects channel failures, decreases concurrency, and retries tasks with an exponential backoff.
   
3. **Exit Code Evaluation**:
   - Always verify the command exit code in the status output. Exit code `0` indicates success. A non-zero exit code or `null` indicates failure or premature termination.
   
4. **Transient Dynamic Connection Isolation**:
   - If a bulk execution fails on a specific server in the fleet, the failure will remain isolated to that connection. Other fleet members will execute successfully. The failed target status will be saved with an error code and stored under the bulk ID log history for easy debugging.
