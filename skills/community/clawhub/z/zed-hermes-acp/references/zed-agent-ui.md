# Zed Agent UI Reference — How Hermes (External Agent / ACP) Appears

Scope: Linux. Hermes runs as an ACP External Agent. This distills three Zed
pages ([agent-panel], [agent-settings], [agent-profiles]) into what matters for
an External Agent in the Agent Panel, Agent Settings, and Agent Profiles.

Keep in mind the single biggest rule: **Agent Profiles apply only to the Zed
Agent.** External Agents (Hermes) and Terminal Threads do NOT use Zed Agent
profiles unless their integration explicitly supports similar behavior
([agent-profiles]#agent-path-boundaries).

## 1. Surface map

| Surface | Open with | Where Hermes shows up |
| --- | --- | --- |
| Agent Panel | `agent: new thread` (Command Palette) or ✨ status-bar icon | In the "New Thread…" agent list; its own threads |
| Agent Settings | `agent: open settings` (→ AI page) | External Agents sub-page under **General** |
| Agent Profiles | Profile selector → `Configure`, or `agent: manage profiles` | **Not used by Hermes** (Zed-Agent-only) |

Other entry points: `zed: open settings` → AI sidebar; `zed: open settings file`
for raw JSON. Settings Editor has LLM Providers, External Agents, MCP Servers
each as its own sub-page under **General** ([agent-settings]).

## 2. Agent Panel

### Starting a Hermes thread
- Empty-state: click the **agent selector** (left) or the **+** icon (top-right)
to open "New Thread…".
- In that menu: pick **Zed Agent** or **any installed External Agent** (Hermes)
to start a thread with that agent ([agent-panel]#new-thread).
- `agent: new external agent thread` starts a thread with the specified
**External Agent id** ([agent-panel]#new-thread).
- Also startable from the Threads Sidebar, scoped per project
([agent-panel]#multiple-threads).

### Where Hermes lives once running
- **Threads Sidebar**: `ctrl-alt-j` — all threads grouped by project; click to
switch, `ctrl-tab` to cycle recent threads. Archive via hover or
`shift-backspace`.
- **Thread History**: all threads across projects, chronological; restorable.
- **Worktree picker** (title bar): isolate a thread in a Git worktree to avoid
file-edit collisions.

### Feature availability for External Agents (varies by integration)
> "Some Agent Panel features may not be available for every External Agent.
> Restoring threads from history, checkpoints, token usage display, and similar
> features depend on the agent integration." ([agent-panel]#overview)

| Feature | External Agent behavior |
| --- | --- |
| Restore from history / checkpoints | Depends on integration; may be absent |
| Token usage display | Near profile selector; may not surface for all agents |
| Auto / manual compaction (`/compact`) | Zed-Agent-only; not guaranteed for external |
| **Steering** (interrupt at next step) | **Not available** — Zed can't detect external turn boundaries ([agent-panel]#editing-messages) |
| Model selector (`ctrl-alt-/`) | For LLM providers; external agents are chosen as the agent, not the model |
| "No tools" label | Shown for models lacking tool support — not Hermes-specific |

### Things that DO work the same
- Edit/remove queued messages; immediate stop via Stop button.
- Context via `@` (files, dirs, symbols, threads, skills, URLs) and
`ctrl->` (selection as context).
- Right-click response → Copy / Open Thread as Markdown / scroll.
- Review Changes multi-buffer (`ctrl-shift-r`); `agent.single_file_review`
for inline diffs.
- Rate responses (thumbs up/down); warnings about data sent to Zed on rating.

## 3. Agent Settings

- The **External Agents** section configures **ACP-integrated agents**
([agent-settings]#external-agents).
- Open with `agent: open settings` → AI page; External Agents is a sub-page
under **General**.
- `Add Agent` offers: **Install from Registry** and **Add Custom Agent**.
  (Setup details / support boundaries: see [external-agents].)
- For settings not exposed in UI, `zed: open settings file` for direct JSON.

Related surfaces in the same AI page: **LLM Providers** (model providers) and
**MCP Servers** (`Add Local/Remote Server`, `Install from Extensions`; per-row
Configure/Uninstall/enable toggle) ([agent-settings]#mcp-servers).

### Settings that are Zed-Agent / model-backed (do NOT apply to Hermes)
`agent.inline_assistant_model`, `agent.commit_message_model`,
`agent.thread_summary_model`, `agent.compaction_model`, `agent.subagent_model`,
`agent.commit_message_instructions`, `agent.inline_alternatives`,
`agent.auto_compact`, `agent.model_parameters`, `agent.favorite_models`
([agent-settings]).

## 4. Agent Profiles — Hermes is NOT here

Agent profiles control **how the Zed Agent behaves**: default model + which
built-in/MCP tools are available. They do **not** govern allow/deny/confirm
that's Tool Permissions ([agent-profiles]).

- Built-in: `Write` (read/edit/run), `Ask` (read-only), `Minimal` (no project
tools).
- Configure: profile selector → `Configure`, or `agent: manage profiles`;
per-profile: create, fork, set default model, built-in tools, MCP tools, delete.
- Stored under `agent.profiles` in settings (example in [agent-profiles]#settings).
- **External Agents and Terminal Threads do not use Zed Agent profiles unless
their integration explicitly supports similar behavior**
([agent-profiles]#agent-path-boundaries).

Decision rule:
| You want to… | Use |
| --- | --- |
| Change Hermes tools/behavior | Hermes-side config or its ACP integration — not Agent Profiles |
| Gate a tool call (allow/deny/confirm) | Tool Permissions (profiles only toggle availability, not gating) |
| Pick which built-in/MCP tools a **Zed Agent** thread has | Agent Profiles |

## 5. Quick decision rules (External Agent lens)

- Need a Hermes thread? → "New Thread…" menu (pick Hermes) or
  `agent: new external agent thread <id>`.
- Configure Hermes? → Agent Settings → External Agents (ACP) sub-page.
- Tune Hermes tool policy? → NOT Agent Profiles; use Hermes/ACP integration +
  Tool Permissions. Profiles are Zed-Agent-only.
- Missing checkpoints / history-restore / token display? → Expected if the
  Hermes ACP integration doesn't surface them; availability varies by agent.
- Steering / auto-compaction not working? → Zed-Agent-only features.

---
Sources: [agent-panel]=agent-panel.md, [agent-settings]=agent-settings.md,
[agent-profiles]=agent-profiles.md, [external-agents]=external-agents.md.
Linux-only; macOS/Windows steps omitted. No verbatim reproduction beyond
quoted phrases.
