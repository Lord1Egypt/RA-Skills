# Zed Agent Paths — Reference for Hermes ACP

> Distilled from Zed docs: `zed-agent.md`, `terminal-threads.md`. Linux focus; macOS/Windows steps omitted.
> Companion to `zed-external-agents.md`; Hermes is an **External Agent**.

## 1. Three Paths at a Glance

| Path | What it is | Owns auth/model/tools | Integration |
|------|-----------|----------------------|-------------|
| **Zed Agent** | Zed-native agent in Agent Panel + Threads Sidebar | Zed (LLM Providers, Profiles, Skills, MCP) | Built-in, no ACP |
| **External Agent** (e.g. Hermes) | Separate process exposed to Zed over ACP, rendered as a thread | The agent (own auth, model, tools, instructions) | ACP via `agent_servers` |
| **Terminal Thread** | A CLI/TUI run in a terminal, organized as a thread | The CLI/TUI (shell env + own config files) | Terminal-backed, not ACP |

Sources: `zed-agent.md#other-agent-paths`, `terminal-threads.md#what-the-cli-owns`.

## 2. Zed Agent — Native Path

- Runs in the Agent Panel and Threads Sidebar (`parallel-agents.md#threads-sidebar`).
- Model access via configured LLM Providers.
- Source-of-truth table (what configures each capability):
  - Model access -> LLM Providers (`llm-providers.md`)
  - Panel workflow -> Agent Panel (`agent-panel.md`)
  - Tool availability -> Agent Profiles (`agent-profiles.md`)
  - Tool approval -> Tool Permissions (`tool-permissions.md`)
  - Built-in tools -> Tools (`tools.md`)
  - External tools -> MCP (`mcp.md`)
  - Reusable task instructions -> Skills (`skills.md`)
  - Always-on instructions -> Instructions (`instructions.md`)
- Use it to: read/search project, edit files, run terminal commands, use Zed-managed MCP, follow Agent Profiles, use Zed Skills/Instructions, show changes in Zed's review UI.
- Source: `zed-agent.md#what-zed-agent-uses`.

## 3. External Agent — ACP Path (Hermes)

- Integrates through ACP; renders as an agent thread (like Zed Agent, not a terminal).
- The agent typically owns its own auth, model, tool, and native instruction configuration.
- Hermes wiring (Linux): run `hermes acp` as an ACP server, register it in `~/.config/zed/settings.json` under `agent_servers`.
- Zed Agent profiles, tool permissions, Skills, and MCP settings do NOT auto-apply — the agent brings its own.
- Contrast with Terminal Threads: External Agents use ACP and render as agent threads; Terminal Threads run the native CLI inside a terminal.
- Sources: `zed-agent.md#other-agent-paths`, `terminal-threads.md` (intro).

## 4. Terminal Threads — CLI/TUI Path

- Terminal-backed threads in the Threads Sidebar; open via the new-thread menu -> **Terminal** (Agent Panel agent selector or `+` icon).
- **Zed owns**: the thread surface, grouping by project, switching/organizing the terminal session alongside other threads.
- **The CLI owns**: authentication, model/provider config, subscriptions/API keys, tool config, skills/instruction files, MCP config.
- Zed Agent profiles/permissions/Skills/MCP do NOT auto-apply.
- Open as many as you like; each gets its own sidebar entry.
- Auto-run a CLI via the `agent.terminal_init_command` setting (command sent to the shell on thread creation and on reopen of saved threads); configurable in Settings UI -> AI -> "Terminal Thread Init Command".
- Titles auto-update from the running process; custom name via the title/pencil icon.
- Closed, not archived — no Thread History; hover the `x` or select and press the keybinding.
- Credentials come from the terminal session + CLI; Zed does NOT copy LLM-provider API keys into Terminal Threads. Remote projects read the remote shell env/config.
- Sources: `terminal-threads.md#what-zed-owns`, `#what-the-cli-owns`, `#opening-a-terminal-thread`, `#terminal-thread-init-command`, `#closing-terminal-threads`, `#credentials-and-remote-projects`.

## 5. Notifications (Shared Surface)

- A terminal/CLI bell while unfocused -> Zed pop-up + optional sound (same as agent-done).
- Settings: `agent.notify_when_agent_waiting`, `agent.play_sound_when_agent_done`.
- Source: `terminal-threads.md#terminal-thread-notifications`.

## 6. Decision Rule — Which Path?

Ask in order:

1. Want Zed-native models + Zed Skills/MCP + review UI, no external setup? -> **Zed Agent**.
2. Have/want a CLI or TUI agent with no ACP integration, and the CLI should own auth/config/subscription? -> **Terminal Thread**.
3. Want an ACP-integrated external agent that brings its own auth/model/tools (e.g. Hermes via `hermes acp`)? -> **External Agent** via `agent_servers` in `~/.config/zed/settings.json`.

Quick map:

| Need | Path |
|------|------|
| Use Zed's models + Zed Skills/MCP, see diffs in review UI | Zed Agent |
| Run a CLI/TUI (e.g. Claude Code, Codex, OpenCode) natively | Terminal Thread |
| Plug in Hermes (or any ACP agent) as a first-class thread | External Agent |

Sources: `terminal-threads.md#when-to-use-terminal-threads`, `zed-agent.md#other-agent-paths`.

## 7. Linux-Specific Notes

- All settings live in `~/.config/zed/settings.json` (or custom `XDG_CONFIG_HOME`).
- Skip upstream macOS/Windows sections (WSL passthrough, etc.) — not applicable.
- For Hermes: ensure `hermes acp` is reachable and registered under `agent_servers`; it then renders as a normal agent thread, distinct from any Terminal Thread.
