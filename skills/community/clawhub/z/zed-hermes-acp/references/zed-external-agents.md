# Zed External Agents (ACP)

Distilled from `zed.dev/docs/ai/external-agents.md` and `agents.md`. Load when
wiring any non-registry ACP agent into Zed, or when you need the exact
Zed↔agent boundary rules (what Zed controls vs what the agent owns).

## What an External Agent is
- An agent that integrates with Zed through the **Agent Client Protocol (ACP)**.
- Zed hosts the thread in the **Agent Panel** + **Threads Sidebar**; the
  External Agent owns its own runtime, auth, model selection, tools, and
  native configuration.
- Contrast with **Terminal Threads** (run a CLI/TUI directly in a
  terminal-backed thread) and **Zed Agent** (Zed-native).
- Zed does **not** charge for External Agents. Billing, legal terms,
  retention, and data handling are between you and the agent provider.

## Three agent paths (`agents.md`)
| Path | Runs in | Uses | Best when |
| --- | --- | --- | --- |
| Zed Agent | Agent Panel / Sidebar | Zed LLM providers, native tools, skills, instructions, MCP | you want Zed's native agent integration |
| External Agents | Agent Panel / Sidebar | ACP process + own auth/config | Claude, Codex, OpenCode, Copilot, Cursor, Pi, **Hermes**, or another ACP agent |
| Terminal Threads | Sidebar + terminal | native CLI/TUI auth/config | you want the tool's command-line experience in Zed |

## Install from the ACP Registry
- Open with `zed: acp registry`, or Agent Settings (`agent: open settings`) →
  **External Agents** → Add Agent → **Install from Registry**.
- After install the agent appears in the new-thread menu (Agent Panel /
  Threads Sidebar).
- Common curated agents: Claude, Codex, OpenCode, Copilot, Cursor, Pi Coding
  Agent, Gemini CLI, Poolside. (Poolside also supports `pool acp setup
  --editor zed`, which writes `~/.config/zed/settings.json`.)

## Custom Agents (the Hermes path)
- Use when developing an ACP-compatible agent or one not in the registry.
- Agent Settings → External Agents → Add Agent → **Add Custom Agent**. Zed
  opens your settings file with an `agent_servers` entry.
- Shape (verbatim from docs):
  ```json
  {
    "agent_servers": {
      "my-agent": {
        "type": "custom",
        "command": "node",
        "args": ["~/projects/agent/index.js", "--acp"],
        "env": {}
      }
    }
  }
  ```
- Registry-installed agents also accept per-agent settings under
  `agent_servers.`.
- Hermes is configured identically with `command: "hermes"`, `args: ["acp"]`
  (see SKILL.md Procedure). Zed auto-detects the settings change — no restart.

## Configuration Boundaries (Zed ↔ agent)
| Capability | Behavior in External Agent threads |
| --- | --- |
| Model / provider config | usually owned by the External Agent |
| Auth / API keys / subscriptions | usually owned by the External Agent |
| Zed Agent profiles | do **NOT** apply |
| Zed Skills | do **NOT** apply as Zed Skills |
| Native agent skills / instructions | depends on the agent |
| Zed MCP servers | may be forwarded over ACP |
| Native MCP config | may also be read by the agent |
| Tool permissions | Zed ACP / tool-forwarding perms may apply; native perms depend on agent |

## Per-agent auth examples
- **Claude Agent**: own auth/billing; run `/login` in the thread. `CLAUDE.md`
  may be read directly. A Zed Anthropic key does **not** configure Claude Agent.
- **Codex**: own auth; ChatGPT login / Codex / OpenAI / Codex-native; native
  login flow.
- **Gemini CLI**: own auth; reads `GEMINI_API_KEY` / `GOOGLE_AI_API_KEY` if
  present, else Zed passes its Google AI key as `GEMINI_API_KEY`.
- **OpenCode / Copilot / Cursor / Pi / Poolside**: each owns its own
  auth/model/subscription.

## Remote Projects
- Agents may read credentials locally, remotely, or via their own sign-in.
- Zed LLM provider keys in the local keychain ≠ an External Agent's
  credentials. Check the agent's setup path for SSH / dev containers.

## Importing Threads
- Threads Sidebar (`ctrl-alt-j` / `cmd-alt-j`) → clock icon → **Import
  Threads** → pick agents.
- Zed connects over ACP and adds sessions not already in history. Entries are
  archived; open one to restore and continue. Sessions without a working
  directory are skipped; re-import is safe (existing threads skipped).

## MCP
- Zed-configured MCP servers **may be forwarded** to External Agents over ACP.
- Agents may also read their own native MCP config. If an MCP tool is missing
  in the agent, check **both** Zed's MCP config and the agent's native config.

## Debugging
- `dev: open acp logs` (command palette) inspects messages between Zed and an
  External Agent. Include these logs when reporting ACP issues.
