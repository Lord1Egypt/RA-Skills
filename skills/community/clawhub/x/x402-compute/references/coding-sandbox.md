# Coding sandbox from anywhere

A **Coding sandbox** is an Agent Pod running a coding agent (Claude Code, Codex, OpenCode or Pi) on
its own private computer. Its pod `agent_id` is `coding`. It sleeps after 15 idle minutes and wakes
when you use it.

You can use it from your own terminal, from scripts, and from any OpenAI client:

| You want to | Use |
|-------------|-----|
| A full shell in the sandbox, from your terminal | `singularity sandbox connect` |
| Real SSH: `ssh`, `scp`, `sftp`, port forwarding, VS Code / Cursor Remote-SSH | `singularity sandbox ssh-config`, then `ssh sgl-<name>` |
| Run one command, read or write a file | `singularity sandbox exec / files / get / put`, or the REST routes below |
| Talk to the sandbox's coding agent from any app | an OpenAI-compatible key: `singularity sandbox key` |

Everything below uses the compute API at `https://compute.x402layer.cc`.

---

## Auth

- **A compute API key** (`x402c_...`) from Settings > API keys, sent as `X-API-Key`. It needs
  Compute "Extend, resize, destroy" (`compute:write`) and the Agent Pods permission "Read and write pod files, install skills, create and restore backups"
  (**`pods:control:write`**).
- **Or a Solana keypair** (wallet signature, same scheme as the rest of the compute API).
- Keys made from a Google, GitHub or X login can use the terminal, SSH and the OpenAI-compatible keys.
  `exec` and files need a key from a wallet login.

---

## CLI (available from CLI 0.5.0)

```bash
npm i -g @singularity-layer/cli
export SGL_API_KEY=x402c_...

singularity sandbox list                    # your Coding sandboxes
singularity sandbox status                  # state, harness, awake hours this month
singularity sandbox connect                 # a full shell here. Type ~. at the start of a line to leave
singularity sandbox exec -- npm test        # one command; exits with its exit code (--timeout 1..300)
singularity sandbox files                   # list the workspace
singularity sandbox get src/app.ts          # print a file (or: get src/app.ts ./app.ts to save it)
singularity sandbox put ./notes.md          # upload a text file (up to 100 KB)
singularity sandbox wake                    # or: sleep
singularity sandbox key --name my-app       # OpenAI-compatible key for the sandbox's coding agent
singularity sandbox keys                    # list those keys
singularity sandbox revoke-key <key-id>
```

- With more than one sandbox, name it: its id, the start of the id, or its name
  (`singularity sandbox connect 99a7`, or `--sandbox <it>`). Leave it out if you have only one.
- `connect` needs Node 22 or newer. `~~` sends a single `~`.
- `--keypair <path>` signs with a Solana keypair instead of a key. `--json` for scripts.

---

## SSH, VS Code and Cursor (available from CLI 0.6.0)

```bash
singularity sandbox ssh-config 99a7         # key + a Host entry in ~/.ssh/config; prints the name, e.g. sgl-my-sandbox
ssh sgl-my-sandbox                          # a shell as the sandbox user
scp ./data.csv sgl-my-sandbox:workspace/    # copy files in or out
ssh -L 3000:localhost:3000 sgl-my-sandbox   # the sandbox's port 3000 on your machine
singularity sandbox ssh 99a7 -- -L 3000:localhost:3000   # the same without any config
```

- There is no SSH port to dial. The CLI is ssh's ProxyCommand: it asks for a single-use 60-second
  ticket bound to your public key (`POST /pods/<id>/coding/ssh` with `{"public_key": "ssh-ed25519 ..."}`)
  and carries the SSH stream over the same WebSocket path as the terminal. The sandbox starts an SSH
  server for that one connection, which accepts only that key. No passwords; agent and X11
  forwarding are off; you log in as the sandbox user (never root).
- VS Code or Cursor: install **Remote - SSH**, then **Connect to Host** and pick the name. The first
  connection can take a minute while the sandbox wakes: set `"remote.SSH.connectTimeout": 60`.
- `ssh-config` makes `~/.singularity/ssh/id_ed25519` (the private half stays on your computer) and
  saves the API key it ran with to `~/.singularity/credentials.json` (mode 600) so editors, which
  start ssh without your shell's environment, can connect. `--no-save-key` skips that; `--remove`
  takes the entry out again.
- An open connection keeps the sandbox awake (awake hours count as usual); it sleeps after you disconnect.
- A sandbox made before SSH existed gets it the first time you connect (about a minute, once).

---

## Terminal over WebSocket

The same path the browser terminal uses: a single-use ticket and a WebSocket relayed through the
sandbox's own outbound connection. No open port.

```bash
curl -s -X POST "https://compute.x402layer.cc/pods/$POD/coding/terminal" -H "X-API-Key: $SGL_API_KEY"
# -> { "ticket": "...", "ttl_seconds": 60, "path": "/pods/screen/<ticket>" }
```

Then open `wss://compute.x402layer.cc<path>`:

- The ticket works **once**, within **60 seconds**.
- Send a **text** frame `{"cols": 120, "rows": 40}` to set or change the terminal size.
- **Binary** frames you send are keystrokes. **Binary** frames you receive are terminal output.
- Close code **4006** means the terminal was closed after 10 idle minutes.

---

## Run a command and work with files

The general Agent Pods sandbox routes work for a Coding sandbox. A sleeping sandbox wakes for them.

```bash
# Run one command (timeout_seconds 1 to 300, default 60)
curl -s -X POST "https://compute.x402layer.cc/pods/v1/pods/$POD/exec" \
  -H "X-API-Key: $SGL_API_KEY" -H 'content-type: application/json' \
  -d '{"command":"npm test","timeout_seconds":120}'
# -> { "exec": { "exit_code": 0, "stdout": "...", "stderr": "", "timed_out": false, "truncated": false } }

# List the workspace
curl -s "https://compute.x402layer.cc/pods/v1/pods/$POD/files" -H "X-API-Key: $SGL_API_KEY"

# Read one file
curl -s "https://compute.x402layer.cc/pods/v1/pods/$POD/files?path=src/app.ts" -H "X-API-Key: $SGL_API_KEY"

# Write a text file (up to 256 KB per file, 128 KB per request)
curl -s -X PUT "https://compute.x402layer.cc/pods/v1/pods/$POD/files" \
  -H "X-API-Key: $SGL_API_KEY" -H 'content-type: application/json' \
  -d '{"path":"notes.md","content":"hello"}'
```

Limits and response details: `references/agent-pods-api.md` (Sandbox).

---

## OpenAI-compatible address for the coding agent

Mint a key (needs `pods:control:write`). The secret is shown **once**:

```bash
curl -s -X POST "https://compute.x402layer.cc/pods/v1/pods/$POD/keys" \
  -H "X-API-Key: $SGL_API_KEY" -H 'content-type: application/json' -d '{"name":"my-app"}'
# -> { "key": { "id": "...", "secret": "sk-sglpod-int-..." },
#      "endpoint": { "base_url": "https://compute.x402layer.cc/pods/<id>/v1", "model": "agent-pod" } }
```

(Signed in on the dashboard, `POST /pods/<id>/api-keys` does the same.)

Then point any OpenAI client at the base URL with model **`agent-pod`**:

```bash
curl -s "https://compute.x402layer.cc/pods/$POD/v1/chat/completions" \
  -H "Authorization: Bearer $POD_KEY" -H 'content-type: application/json' \
  -d '{"model":"agent-pod","stream":true,"messages":[{"role":"user","content":"Run the tests and fix what fails"}]}'
```

- `GET /v1/models` and `POST /v1/chat/completions`. Streaming works: `"stream": true` returns
  `chat.completion.chunk` events ending with `data: [DONE]`.
- **Each request is one turn of the sandbox's coding agent.** It can edit files and run commands
  in the sandbox, so treat the key like a password. Revoke with
  `DELETE /pods/v1/pods/<id>/keys/<keyId>`.
- At most 1000 requests per key per day.
- Billing: OpenCode or Pi on Singularity Layer models bills the owner's credits. Claude Code runs
  only on the owner's own Claude login or Anthropic key.
