# SSH Remote Access via ToxTunnel

## Scenario

You have a remote machine (home server, office workstation) running SSH, and you want to access it from anywhere without exposing port 22 to the internet.

## Topology

```
Your Laptop (client)                 Remote Machine (server)
───────────────────                  ───────────────────────
ssh -p 2222 user@127.0.0.1          sshd listening on :22
        ↓                                    ↑
  toxtunnel client                    toxtunnel server
  local_port: 2222                    (accepts tunnel, connects to 127.0.0.1:22)
        ↓                                    ↑
        └──── Tox P2P encrypted tunnel ──────┘
```

## Server Config (on remote machine)

```yaml
mode: server
data_dir: ~/.config/toxtunnel/server
logging:
  level: info
tox:
  udp_enabled: true
  bootstrap_mode: auto
server:
  rules_file: rules.yaml
```

## Client Config (on your laptop)

```yaml
mode: client
data_dir: ~/.config/toxtunnel/client
logging:
  level: info
tox:
  udp_enabled: true
  bootstrap_mode: auto
client:
  server_id: <PASTE_SERVER_TOX_ID_HERE>
  forwards:
    - local_port: 2222
      remote_host: 127.0.0.1
      remote_port: 22
```

## Rules (minimal access — replace with your actual friend public key)

```yaml
rules:
  - friend: "AABBCCDD...your-64-char-hex-public-key-here...EEFF"
    allow:
      - host: "127.0.0.1"
        ports: [22]
```

Note: The `friend` field must be the client's 64-character hex public key (NOT the full 76-char Tox ID). You can find it in the client's startup log. If `rules_file` is unset, the server is default-deny and will refuse the friend request, so this rule is required.

## Steps

1. Start server: `toxtunnel -m server -c server.yaml`
2. Copy the Tox ID from server output
3. Paste it into client.yaml as `server_id`
4. Start client: `toxtunnel -m client -c client.yaml`
5. Wait for friend connection (typically 10-30 seconds)
6. Connect: `ssh -p 2222 user@127.0.0.1`

## Alternative: SSH ProxyCommand (pipe mode)

> **Note:** Pipe mode is POSIX only (macOS / Linux). It is **not supported on Windows**. On Windows, use the port forwarding approach above.

Instead of port forwarding, you can use pipe mode directly:

```bash
ssh -o ProxyCommand="toxtunnel -m client --server-id <TOX_ID> --pipe 127.0.0.1:22" user@remote
```

Add to `~/.ssh/config` for convenience:

```
Host remote-via-tox
    HostName remote
    User your-user
    ProxyCommand toxtunnel -m client --server-id <TOX_ID> --pipe 127.0.0.1:22
```

Then simply: `ssh remote-via-tox`

> **Tip:** if you connect to the same server frequently, register an alias once
> and use it in place of the 76-char Tox ID:
>
> ```bash
> toxtunnel servers add remote-host <FULL_76_CHAR_TOX_ID>
> # then in ~/.ssh/config:
> #   ProxyCommand toxtunnel -m client --server-id remote-host --pipe 127.0.0.1:22
> ```

## Verification

```bash
bash verify.sh 2222 ssh
```
