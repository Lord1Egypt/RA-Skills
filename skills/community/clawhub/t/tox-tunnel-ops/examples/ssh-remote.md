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
  rules_file: ~/.config/toxtunnel/server/rules.yaml
```

> **`rules_file` must be an absolute path.** ToxTunnel expands `~` and nothing
> else, then hands the string to the rules loader, so a relative path resolves
> against the **daemon's working directory** — not this config's directory.
> Starting the daemon from anywhere else dies with
> `Failed to load rules file: Rules file not found: rules.yaml`. Verified on
> v0.4.12.


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
      local_address: 127.0.0.1
      remote_host: 127.0.0.1
      remote_port: 22
```

> ### ⚠️ `local_port: 2222` binds `0.0.0.0` without `local_address` (pre-v0.5.0)
>
> On v0.4.12 and older `ForwardRule` has no bind-address field and the client calls
> `TcpListener(io, 2222)`, which binds `asio::ip::tcp::v4()`. Verified on
> v0.4.12: `ss` shows `0.0.0.0:2222` and the port answers on the machine's LAN
> address. On **v0.4.13+** set `local_address: 127.0.0.1` (the config above
> does). On v0.4.12 and older there is no bind key at all, and `local_host` is
> not one on any version — it is silently ignored (`config check --strict` flags
> it as unknown) and the port still binds everything.
>
> So on any shared network, every host that can reach your laptop can reach the
> remote sshd through this port. Mitigate with one of:
>
> ```bash
> # Linux (nftables)
> sudo nft add rule inet filter input tcp dport 2222 iif != lo drop
> # Linux (ufw)
> sudo ufw deny in to any port 2222
> # macOS: add to /etc/pf.conf, then sudo pfctl -f /etc/pf.conf
> #   block in proto tcp to any port 2222
> ```
>
> ```powershell
> New-NetFirewallRule -DisplayName "block toxtunnel 2222" -Direction Inbound `
>   -LocalPort 2222 -Protocol TCP -Action Block
> ```
>
> Or skip the static forward and use a loopback-only SOCKS5 listener
> (`client.socks5`), whose `listen` address *is* validated to be loopback.

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
>
> **Latency caveat:** each `ssh` invocation starts a fresh toxtunnel process
> that must (re)establish the Tox friend link before any byte flows — ~10 s on
> a LAN, but **minutes** when the peers only reach each other through a Tox TCP
> relay. `ssh` gives up long before that and exits with no error text. If the
> first attempt dies silently, either retry (the server now knows the friend,
> so it is faster) or use a long-lived `forwards:` client instead — a resident
> client keeps the friend link warm and `ssh -p 2222 …` connects instantly.

Instead of port forwarding, you can use pipe mode directly:

```bash
ssh -o ProxyCommand="toxtunnel -m client --server-id <TOX_ID> -d ~/.config/toxtunnel/ssh-proxy --pipe 127.0.0.1:22" user@remote
```

Add to `~/.ssh/config` for convenience:

```
Host remote-via-tox
    HostName remote
    User your-user
    ProxyCommand toxtunnel -m client --server-id <TOX_ID> -d ~/.config/toxtunnel/ssh-proxy --pipe 127.0.0.1:22
```

Then simply: `ssh remote-via-tox`

> ### ⚠️ Give the ProxyCommand its own `-d` data directory
>
> Since **v0.4.11** a daemon takes an **exclusive lock** on its `data_dir`
> (`<data_dir>/toxtunnel.lock`, plus a `toxtunnel.pid`). Two processes cannot
> share one. So a ProxyCommand using the default `~/.config/toxtunnel` fails
> with exit 1 and
>
> ```text
> data directory <dir> is already in use by toxtunnel pid <N>. Two daemons cannot
> share one data_dir: they would share the Tox identity, the inspect socket and
> known_servers.yaml.
> ```
>
> whenever a resident client is already running — and **two concurrent `ssh`
> invocations collide with each other** for the same reason, so the second one
> dies. `ssh` surfaces this as a connection failure with little explanation.
>
> Hence the `-d ~/.config/toxtunnel/ssh-proxy` above. But note the consequence:
>
> - **A separate data directory means a separate Tox identity**, so this
>   ProxyCommand has a different public key from your resident client. The
>   server's `rules.yaml` needs a second `friend:` entry for it, or every tunnel
>   is default-denied.
> - It still does not make concurrent `ssh` runs work — they would share
>   `ssh-proxy` and collide. For parallel sessions, use one data dir per session
>   (each needing its own rules entry), or use SSH's own multiplexing
>   (`ControlMaster auto` / `ControlPersist`) so only the first connection starts
>   a toxtunnel at all.
>
> **If that bookkeeping is not worth it, prefer the resident `forwards:` client
> above.** One identity, one rules entry, no lock contention, and the friend link
> stays warm so `ssh -p 2222 …` connects immediately instead of re-establishing
> the Tox link per invocation.

> **Tip:** if you connect to the same server frequently, register an alias once
> and use it in place of the 76-char Tox ID:
>
> ```bash
> # Stop the client daemon first — the registry is single-writer across
> # processes, so a running daemon will clobber this edit on its next update.
> toxtunnel servers add remote-host <FULL_76_CHAR_TOX_ID>
> # then in ~/.ssh/config:
> #   ProxyCommand toxtunnel -m client --server-id remote-host -d ~/.config/toxtunnel/ssh-proxy --pipe 127.0.0.1:22
> ```
>
> Aliases live in `<data_dir>/known_servers.yaml`, so register the alias in the
> **same** data directory the ProxyCommand uses — a `-d ssh-proxy` client cannot
> see an alias added to the default directory.

## Verification

```bash
bash scripts/verify.sh 2222 ssh client.yaml
```

Run this from the skill root (the script lives at `scripts/verify.sh`).
Passing the client config lets it read `friends_online` from the running
daemon instead of guessing from a local TCP accept.

**Judge it by the exit code:** `0` = the remote service answered through the
tunnel, `2` = local checks passed but end-to-end was **not** proven (do not
report this as working), `1` = a check failed.
