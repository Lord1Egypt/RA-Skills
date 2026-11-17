---
name: zed-hermes-acp
description: "Connect Hermes Agent to Zed via the Agent Client Protocol."
version: 0.1.0
author: Hermes
platforms: [linux]
metadata:
  openclaw:
    os: [linux]
    homepage: https://github.com/mina-atef-00/agent-skills
  hermes:
    tags: [Zed, ACP, External Agents, IDE Integration, Hermes]
    related_skills: [hermes-agent, hermes-browsers, ai-coding-agents]
---

# Hermes in Zed via ACP

Wire Hermes Agent into the Zed editor as an ACP **External Agent**, so you get
Hermes's model/provider setup, memory, skills, and tools inside Zed's Agent
Panel — without Zed owning your credentials or config. This skill covers the
Zed-side wiring (External Agents, the `agent_servers` config, boundaries,
debugging) and the exact Hermes-side ACP launch config. It does NOT cover
Zed's native "Zed Agent", Terminal Threads, macOS/Windows paths, or general
Zed editing.

Dependency stance: requires Hermes installed with the `acp` extra
(`agent-client-protocol`), and Zed at/after the ACP External Agents release.
All Hermes credentials live in `~/.hermes/` as usual. Hermes-side ACP
internals (Buzz bridge, VS Code/JetBrains setup, the full approvals matrix,
`HERMES_ACP_SKIP_CONFIGURED_MCP`) live in the `hermes-agent` skill — load it
for those.

## When to Use
- "Add Hermes to Zed" / "use Hermes inside Zed"
- "Configure Zed external agent for Hermes" / "agent_servers hermes"
- "Hermes ACP not showing in Zed" / "Zed can't find hermes acp"
- "ACP external agent Zed config" / wiring any custom ACP agent into Zed

## Prerequisites
- Hermes installed and on your `PATH` (`command -v hermes`).
- ACP extra installed — invoke through the `terminal` tool:
  `cd ~/.hermes/hermes-agent && uv pip install -e '.[acp]'`
  This enables `hermes acp`, `hermes-acp`, and `python -m acp_adapter`.
- Hermes provider credentials configured (Zed does NOT supply them):
  `hermes model` (interactive), or set in `~/.hermes/.env` / `~/.hermes/config.yaml`.
- Zed installed. Linux settings path (native install):
  `~/.config/zed/settings.json`.
- **Zed as Flatpak** (`dev.zed.Zed`): settings live at
  `~/.var/app/dev.zed.Zed/config/zed/settings.json`, the file is **JSONC**
  (`//` comments + trailing commas), and the sandbox needs the **absolute
  in-sandbox `command` path** `~/.local/bin/hermes` (sandbox PATH
  has no host binaries). No `flatpak override` is needed — the manifest
  already grants `home` + `network`. Full recipe + JSONC edit workaround in
  `references/zed-flatpak-setup.md`. Zed auto-reloads settings (no restart).
- (Optional) ACP browser tools need Node + Chromium via
  `hermes acp --setup-browser` (see Pitfalls / `hermes-agent` skill).

## Zed ACP Concepts
Zed supports three agent paths: **Zed Agent** (Zed-native),
**External Agents** (ACP process you own), and **Terminal Threads** (raw
CLI/TUI). Hermes is an External Agent.

- External Agents run as a separate process, talking to Zed over **ACP** (stdio
  JSON-RPC). Zed hosts the thread UI; the agent owns runtime, auth, models,
  tools.
- Register a custom agent under `agent_servers` in Zed settings. Zed
  auto-detects the file change — no restart needed.
- **Configuration boundaries** (what Zed controls vs Hermes owns):
  - Model/provider config → owned by Hermes
  - Auth / API keys / subscriptions → owned by Hermes
  - Zed Agent profiles → do NOT apply to Hermes
  - Zed Skills → do NOT apply (Hermes uses its own skills)
  - Zed MCP servers → MAY be forwarded to Hermes over ACP
  - Native MCP config → Hermes may also read its own
  - Tool permissions → Zed ACP/tool-forwarding permissions may apply
- See `references/zed-external-agents.md` (load on demand —
  `skill_view(name='zed-hermes-acp', file_path='references/zed-external-agents.md')`)
  for registry install, common agents, per-agent auth, and thread import.

## How to Run
Canonical flow: install the Hermes ACP extra, confirm it launches, then add the
`hermes-agent` entry to Zed's `agent_servers` and start a thread. Local
commands run through the `terminal` tool. The Zed settings edit uses
`write_file`/`patch` for **native** installs, but a **tolerant JSONC-aware
edit** for the Flatpak (see `references/zed-flatpak-setup.md`) — Hermes's
JSON-only writers reject Zed's `//` comments.

## Quick Reference
- Install ACP extra: `cd ~/.hermes/hermes-agent && uv pip install -e '.[acp]'`
- Launch/check Hermes ACP: `hermes acp` · `hermes acp --version` · `hermes acp --check`
- Health: `hermes doctor` · `hermes status` · `hermes model`
- Optional browser tools: `hermes acp --setup-browser` (or `--yes`)
- Zed settings (native): `~/.config/zed/settings.json`
- Zed settings (Flatpak): `~/.var/app/dev.zed.Zed/config/zed/settings.json`
- Flatpak pre-flight (mimics Zed's spawn): `flatpak run --command=bash dev.zed.Zed -c '~/.local/bin/hermes acp --check'`
- Zed ACP debug: run `dev: open acp logs` from the command palette (`Ctrl+Shift+P`)
- Zed custom-agent config key: `agent_servers`
- Start thread: Agent Panel → new-thread menu → select **hermes-agent**

## Procedure
1. **Install the ACP extra** (one time), through the `terminal` tool:
   ```bash
   cd ~/.hermes/hermes-agent && uv pip install -e '.[acp]'
   ```
2. **Verify Hermes ACP launches** (stdout is reserved for ACP JSON-RPC; logs go
   to stderr):
   ```bash
   hermes acp --check
   ```
   Expect a clean check with no errors. If it errors, run `hermes doctor` and
   `hermes status`.
3. **Confirm credentials** for the provider you want Hermes to use in Zed:
   ```bash
   hermes model
   ```
4. **Add Hermes as a custom agent server in Zed.** Merge this block under
   `agent_servers` (the key is the label shown in Zed's new-thread menu — any
   name works):

   ```json
   {
     "agent_servers": {
       "hermes-agent": {
         "type": "custom",
         "command": "~/.local/bin/hermes",
         "args": ["acp"],
         "env": {}
       }
     }
   }
   ```

   - **Native install** (`~/.config/zed/settings.json`): edit with `read_file`
     + `write_file`/`patch` (plain JSON).
   - **Flatpak** (`~/.var/app/dev.zed.Zed/config/zed/settings.json`): the file
     is **JSONC** — Hermes's `write_file`/`patch` tools reject it (strict JSON
     validation fails on the `//` comments). Edit with a tolerant method
     instead (anchor-replace recipe in `references/zed-flatpak-setup.md`). The
     `command` MUST be the absolute in-sandbox path `~/.local/bin/hermes`
     — bare `hermes` is not on the sandbox PATH.
   Zed auto-detects the settings change — no restart required.
5. **Start a Hermes thread.** Open the Agent Panel, use the agent selector /
   new-thread menu, and pick **hermes-agent**. Zed connects over ACP; Hermes
   renders chat, tool activity, file diffs, terminal commands, approval
   prompts, and streamed thinking.
6. **(Optional) Approve tool calls.** On first runs Hermes raises permission
   requests in Zed. Choose:
   - `allow_once` — this one call only
   - `allow_session` — all matching calls this ACP session (recommended default)
   - `allow_always` — writes a permanent Hermes allowlist entry
   - `deny` — block this call
7. **(Optional) Enable browser tools.** ACP browser tools need the
   `agent-browser` npm package + Chromium, not in the Python wheel:
   ```bash
   hermes acp --setup-browser --yes
   ```
   Installs Node 26 into `~/.hermes/node/`, `npm install -g agent-browser
   @askjo/camofox-browser`, and Playwright Chromium (or uses a detected system
   Chrome/Chromium). Idempotent.

## Pitfalls
- **Zed can't find `hermes acp`** → verify `command -v hermes` and that the ACP
  extra installed (`hermes acp --version`). The host command must be `hermes`
  with args `["acp"]`.
- **ACP starts then errors** → `hermes acp --check`, `hermes doctor`,
  `hermes status`. Logs are on stderr; stdout must stay clean for JSON-RPC.
- **Missing credentials in Zed** → Zed does NOT pass its own keys to Hermes.
  Configure via `hermes model` or `~/.hermes/.env` first.
- **Zed Agent profiles / Zed Skills don't apply** to Hermes threads — Hermes
  uses its own profiles, skills, and MCP config. Don't expect Zed's skills or
  profiles to load.
- **Browser tools absent** until you run `--setup-browser`; the ACP toolset
  includes `browser_*` only after that bootstrap. Distinct from Hermes's own
  `browser` toolset / `use_gateway` config.
- **MCP not appearing** → Zed MCP servers may be forwarded over ACP, but Hermes
  also reads its own native MCP config. Check both. To stop Hermes from
  auto-starting globally configured MCP servers in ACP, the host can set
  `HERMES_ACP_SKIP_CONFIGURED_MCP=1` (host-set, not user `.env`).
- **ACP debug in Zed** → `dev: open acp logs` from the command palette shows
  Zed↔agent messages; include when reporting issues.
- **Linux settings path** — native: `~/.config/zed/settings.json`; Flatpak:
  `~/.var/app/dev.zed.Zed/config/zed/settings.json` (unless a custom
  `XDG_CONFIG_HOME`). Not the macOS/Windows paths.
- **Zed settings.json is JSONC** (Flatpak and native) — Hermes's `write_file`/
  `patch` tools do strict-JSON validation and **refuse to write it** (the `//`
  comments fail the check). Edit with a tolerant method (python anchor-replace;
  see `references/zed-flatpak-setup.md`). Never use a JSON-only writer that
  would strip Zed's comments.
- **Flatpak `command` must be an absolute in-sandbox path**
  (`~/.local/bin/hermes`), not bare `hermes` — the sandbox PATH is
  `/app/bin:/usr/bin` with no host binaries. No `flatpak override` is required
  (manifest already grants `home` + `network`).

## Verification
Pre-flight the exact spawn Zed will use — works without a display:
```bash
flatpak run --command=bash dev.zed.Zed -c '~/.local/bin/hermes acp --check'
# expect: "Hermes ACP check OK"
```
Then confirm registration and connection in Zed:
1. In Zed, open the command palette (`Ctrl+Shift+P`) and run `dev: open acp logs`.
2. Start a **hermes-agent** thread from the Agent Panel and send a message
   (e.g. "list files in the current directory").
3. The ACP logs show a successful `session/new` handshake with Hermes
   responding. If the thread appears and answers, the integration works.

## References (on demand)
Load any with `skill_view(name='zed-hermes-acp', file_path='references/<file>')`.
Linux-focused; macOS/Windows content was dropped during distillation.

- `references/zed-flatpak-setup.md` — **Flatpak path (dev.zed.Zed).** Verified recipe: settings at `~/.var/app/dev.zed.Zed/config/zed/settings.json`, no `flatpak override` needed (`home`+`network` already granted), `command` must be absolute in-sandbox `~/.local/bin/hermes`, the file is JSONC (Hermes's `write_file`/`patch` refuse it — use the python anchor-replace workaround), and the `flatpak run --command=bash dev.zed.Zed -c '... acp --check'` pre-flight. Load when the user runs Zed as a Flatpak.
- `references/zed-external-agents.md` — **Integration core.** ACP registry vs custom-agent install, the `agent_servers` JSON shape, the Zed↔agent boundary table, per-agent auth, thread import, MCP forwarding, and `dev: open acp logs` debugging. Load first when wiring or troubleshooting any custom ACP agent in Zed.
- `references/zed-agent-paths.md` — Contrasts Zed Agent (Zed-owned config) vs Terminal Threads (CLI-owned) vs Hermes-as-External-Agent (ACP, agent-owned via `agent_servers`), with a decision rule for which path to use. Load when choosing or explaining the agent path.
- `references/zed-agent-ui.md` — How Hermes (External Agent) appears in the Agent Panel, Agent Settings (External Agents sub-page), and why Agent Profiles do NOT apply; which panel features (checkpoints, history restore, token display, steering, compaction) do/don't apply. Load when configuring or troubleshooting the panel.
- `references/zed-tools-permissions.md` — Zed's built-in tools, the tool-permission model (precedence, match inputs, Rust-regex rules), and OS sandboxing. Key finding: Zed's sandbox excludes External Agents like Hermes, so Hermes is gated only by `tool_permissions`, not bwrap. Load when locking down or reasoning about what Hermes can do.
- `references/zed-mcp-skills-instructions.md` — MCP server install/config, MCP forwarding to External Agents over ACP, the hard line that Zed Skills ≠ Hermes skills (Zed Skills are Zed-Agent-only), and the AGENTS.md instruction model. Load when a Zed MCP tool, Zed Skill, or AGENTS.md isn't reaching Hermes.
- `references/zed-ai-features.md` — Overview/quick-start/LLM-providers/parallel-agents/inline-assistant distilled into an apply-vs-does-not-apply matrix for Hermes threads. Load when explaining feature coverage.
- `references/zed-ai-privacy.md` — Data boundary: Hermes (External Agent) owns its provider data, feedback, and training under its own terms; Zed's rating/Edit-Prediction opt-ins apply only to Zed-hosted features. Load when asked whether Zed retains Hermes-thread prompts/code.
- `references/zed-cli.md` — Zed CLI reference for script/agent integration: opening files/dirs, `line:col` syntax, window-control flags (`-n`, `-w`, `-a`, `-r`, `--wait`, `--diff`, `--user-data-dir`, `--zed`), stdin via `zed -`, URL handling, default-editor wiring, exit codes. Load when automating Zed from shell/agent scripts.

`hermes-agent` skill — Hermes-side ACP server internals (Buzz bridge, VS Code/JetBrains setup, the full approvals matrix, `HERMES_ACP_SKIP_CONFIGURED_MCP`). Load for anything beyond the Zed-side wiring.
