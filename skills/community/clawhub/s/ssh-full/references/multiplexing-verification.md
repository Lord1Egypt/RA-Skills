# Multiplexing Verification

Procedure to confirm that ControlMaster multiplexing is working correctly.

## Quick Checklist (6 steps)

### 1. Does the local socket exist?

```bash
ls -la /tmp/ssh-mux-<user>@<hostname>:<port>
# Ex: /tmp/ssh-mux-root@10.0.0.5:22
```

**Expected:** UNIX socket (`srw-------`) with the first connection's timestamp.

### 2. Does the socket timestamp stay unchanged across subsequent commands?

```bash
stat -c '%Y' /tmp/ssh-mux-<user>@<host>:<port>  # before
ssh-run.sh --host <host> --user <user> --vault-key <key> -- 'date'
stat -c '%Y' /tmp/ssh-mux-<user>@<host>:<port>  # after — same value!
```

**Expected:** same epoch timestamp before and after.

### 3. Only 1 mux process for the host?

```bash
ps aux | grep "[s]sh.*mux.*<host>"
```

**Expected:** exactly 1 process `ssh: /tmp/ssh-mux-... [mux]`.

### 4. Are TCP connections on the server consistent?

```bash
ssh-run.sh --host <host> --user <user> --vault-key id-rsa -- 'ss -tn sport = :22'
```

**Expected:** the number of ESTABLISHED connections to the Hermes IP does not increase with each command.

### 5. Does auth.log have only 1 Accepted per window?

```bash
ssh-run.sh --host <host> --user <user> --vault-key <key> \
           --sudo --sudo-pass-vault <name> \
           -- 'sudo grep "sshd.*Accepted.*<user>" /var/log/auth.log | tail -5'
```

**Expected:** only 1 `Accepted publickey` entry for the entire batch of commands within the ControlPersist window.

### 6. Is the JSON output clean (no vault pollution)?

```bash
result=$(ssh-run.sh --host <host> --user <user> --vault-key id-rsa -- 'hostname' 2>/dev/null)
echo "$result" | python3 -c "import sys,json; d=json.load(sys.stdin); print('OK:', d['stdout'].strip())"
```

**Expected:** successful parse, no "Retrieving SSH key..." messages in stdout.

## Signs that multiplexing is NOT active

| Symptom | Likely cause |
|---------|-------------|
| Socket does not exist after command | `ssh-agent` is not running → Python backend (no ControlMaster) |
| Multiple sockets with different timestamps | Different `--user` across calls → each user@host combination creates its own socket |
| Socket exists but timestamp changes per command | `ControlPersist` expired between calls (>180s) |
| `Permission denied (publickey)` | Wrong `--user` (local user instead of remote) |

## Quick diagnostic command

```bash
# Close old socket, test 3 commands, verify
ssh -o ControlPath=/tmp/ssh-mux-<user>@%h:%p -O exit <user>@<host> 2>/dev/null || true

TS1=$(bash ssh-run.sh --host <host> --user <user> --vault-key <key> --control-persist 180 -- 'hostname' 2>/dev/null | python3 -c "import sys,json; print(json.load(sys.stdin)['stdout'].strip())")
S1=$(stat -c '%Y' /tmp/ssh-mux-<user>@<host>:<port> 2>/dev/null)

TS2=$(bash ssh-run.sh --host <host> --user <user> --vault-key <key> -- 'date' 2>/dev/null | python3 -c "import sys,json; print(json.load(sys.stdin)['stdout'].strip())")
S2=$(stat -c '%Y' /tmp/ssh-mux-<user>@<host>:<port> 2>/dev/null)

TS3=$(bash ssh-run.sh --host <host> --user <user> --vault-key <key> -- 'whoami' 2>/dev/null | python3 -c "import sys,json; print(json.load(sys.stdin)['stdout'].strip())")
S3=$(stat -c '%Y' /tmp/ssh-mux-<user>@<host>:<port> 2>/dev/null)

echo "Socket epochs: $S1 $S2 $S3"
echo "Multiplexing: $([ "$S1" == "$S2" ] && [ "$S2" == "$S3" ] && echo '✅ ACTIVE' || echo '❌ FAILED')"
echo "Mux PID: $(ps aux | grep '[s]sh.*mux.*<host>' | awk '{print $2}')"
```
