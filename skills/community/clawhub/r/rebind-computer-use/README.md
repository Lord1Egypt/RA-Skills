# rebind-computer-use — an OpenClaw skill

Give your OpenClaw agent a **real hardware keyboard and mouse**. Rebind presents
the OS with a genuine USB device (Teensy HID), so the agent can operate any
desktop GUI — including apps that reject synthetic input — with nothing installed
on the machine being controlled.

- **Skill:** `rebind-computer-use/SKILL.md` — teaches the agent when and how to
  drive the tools.
- **Tools:** the [`@rebind.gg/mcp-server`](https://www.npmjs.com/package/@rebind.gg/mcp-server)
  MCP server — `screenshot`, `zoom`, verified `click`, `type`, `key`, `scroll`,
  window control, `calibrate`.

Supported on **Windows and macOS**.

## Setup (once)

### 1. Start Rebind with Remote Access

The skill talks to a Rebind relay over `ws://127.0.0.1:19561`. In Rebind, load
and run the **Remote Access** script (`remote_access.lua`, protocol ≥ 1.1.0).
This is the single most common reason a first attempt fails — if the relay isn't
running, nothing works.

Verify it's reachable:

```sh
bunx @rebind.gg/mcp-server --selftest
# selftest OK: relay ws://127.0.0.1:19561, display 1 2560x1440
```

### 2. Windows only: turn off pointer acceleration

Windows ships **"Enhance pointer precision"** on by default. It warps the
relationship between mouse motion and pixels, so clicks drift. Turn it off:
*Settings → Bluetooth & devices → Mouse → Additional mouse settings → Pointer
Options → uncheck "Enhance pointer precision".* If you skip this, the agent will
warn on every screenshot that the mouse is uncalibrated and verify each click.

### 3. Install the skill and register the MCP server

```sh
openclaw skills install @usinput/rebind-computer-use
openclaw mcp add rebind --no-probe \
  --command bunx --arg @rebind.gg/mcp-server \
  --env REBIND_URL=ws://127.0.0.1:19561
openclaw config set skills.entries.rebind-computer-use.env.REBIND_URL ws://127.0.0.1:19561
```

The `config set` line matters: the skill's requirements gate reads OpenClaw's
own config, not the MCP server's env — without it the skill shows "needs setup"
and never loads. `--no-probe` lets you register before the relay is running;
the selftest in step 1 is the real check.

(If you set `AUTH_TOKEN` in the Remote Access script, also pass
`--env REBIND_TOKEN=<token>`. For the raw config form, see `mcp.example.json`.
Not using ClawHub? Run `./install.sh` from this directory instead — it does all
of the above and runs the selftest.)

### 4. Start a NEW OpenClaw session

OpenClaw snapshots its skills when a session starts. A skill installed
mid-session is **invisible until you start a new session** (or restart the
gateway). Do this before your first message, or the agent will tell you it can't
control the computer even though everything is installed.

## Use

Text your agent:

> "Take a screenshot and describe my screen."

Then anything GUI: browse a site, fill a form, operate a desktop app. The agent
batches deterministic steps into Luau scripts, verifies visually at checkpoints,
and confirms before anything irreversible or outbound (see the Safety section
of `SKILL.md`).

## Troubleshooting

| Symptom | Fix |
|---|---|
| Agent says it can't control the computer | You didn't start a new session after install (step 4). |
| `openclaw skills list` shows "needs setup" | The `config set ...env.REBIND_URL` line from step 3 is missing. |
| `selftest FAILED` / actions time out | Remote Access script isn't running in Rebind (step 1). |
| Clicks land slightly off (Windows) | "Enhance pointer precision" is on (step 2), or run the `calibrate` tool. |
| Small targets get mis-clicked | Ask the agent to `zoom` before clicking small text. |
