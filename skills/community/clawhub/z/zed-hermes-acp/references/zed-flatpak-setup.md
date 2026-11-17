# Wiring Hermes into the Zed Flatpak (dev.zed.Zed)

Operational recipe for running Hermes as an ACP External Agent inside the Zed
Flatpak. Distilled from a live integration on Fedora (Zed 1.17.2, system
Flatpak, Hermes 0.20.6). Verified end-to-end.

## Settings path
- Flatpak: `~/.var/app/dev.zed.Zed/config/zed/settings.json`
- Native (contrast): `~/.config/zed/settings.json`

## No override needed
`dev.zed.Zed`'s manifest already grants `filesystems=home` (covers
`~/.local/bin` and `~/.hermes`) and `shared=network`. So:
- **Do NOT** add `flatpak override --filesystem=...` — redundant.
- The sandbox CAN see and exec the hermes launcher + venv python.

## command path (the critical gotcha)
Inside the sandbox, `command` MUST be the **absolute in-sandbox path**:
`~/.local/bin/hermes`
- Sandbox PATH is `/app/bin:/usr/bin` — host binaries (incl. bare `hermes`)
  are NOT on it. Bare `hermes` fails with "command not found".
- Host `$HOME/...` and in-sandbox `~/...` are the same
  (Flatpak bind-mounts $HOME); use `~/...` in `command` because it is
  resolved *inside* the sandbox.
- Do NOT use a `flatpak-spawn --host` wrapper — unnecessary; `home` grant
  already exposes the launcher.

## the agent_servers KEY is the agent id
The dict KEY under `agent_servers` is the id Zed registers and looks up — it
is NOT a free-form display name. If you start a thread and see
`Custom agent server 'hermes-agent' is not registered`, the configured key
does not match the id the thread references.

- Use the lowercase id `hermes-agent` (this is what the Agent Panel's
  new-thread menu selects and what saved/imported threads reference).
- A display-style key like `"Hermes"` (capital H) will NOT match and produces
  the "not registered" error even though the entry otherwise launches fine.
- Fix: rename the key to `hermes-agent` and reload settings (auto). Verify
  with a tolerant JSONC parse that the key is exactly `hermes-agent`.

## settings.json is JSONC
Zed's settings file is JSONC: `//` line comments + trailing commas. Hermes's
`write_file`/`patch` tools run **strict JSON validation** and will **REFUSE**
to write it (`JSONDecodeError` on the comments). Workarounds:
- Edit with a tolerant method on the host (the file is a normal file at
  `~/.var/app/.../settings.json`) — anchor-replace preserves structure:
  ```python
  p = "~/.var/app/dev.zed.Zed/config/zed/settings.json"
  s = open(p).read()
  old = '  "agent_servers": {\n    },\n'
  new = '''  "agent_servers": {
    "hermes-agent": {
      "type": "custom",
      "command": "~/.local/bin/hermes",
      "args": ["acp"],
      "env": {}
    }
  },\n'''
  assert old in s, "anchor not found"
  open(p, "w").write(s.replace(old, new, 1))
  ```
- Or parse-then-rewrite (loses Zed's comments, which is fine — Zed accepts
  plain JSON too): strip `//` comments + trailing commas, `json.loads`,
  modify, `json.dump` back.
- Never drive the edit through a JSON-only writer that chokes on comments or
  silently strips them.

## Pre-flight verification (no GUI needed)
Prove the exact spawn Zed will use works inside the sandbox before opening
Zed:
```bash
flatpak run --command=bash dev.zed.Zed -c '~/.local/bin/hermes acp --check'
# expect: "Hermes ACP check OK"
```
This validates: launcher resolves, venv python executes under the sandbox
glibc, and the `acp` extra is importable. (Network is already shared; an
"Could not resolve host" on a non-existent domain is a red herring, not a
sandbox block.)

## Other caveats
- Zed auto-reloads `settings.json` — no restart needed after saving.
- Projects outside `$HOME` (e.g. `/mnt`, `/srv`): the org.freedesktop.Sdk
  runtime also grants `host`, so Hermes can read them. Tighten only if you
  later drop that grant.
- The ACP subprocess is stdio-only — no D-Bus/session-bus grant required.
