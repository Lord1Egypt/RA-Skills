# Zed AI Features — Hermes-as-External-Agent Reference

Scope: distilled from Zed's AI docs (overview, quick-start, llm-providers,
parallel-agents, inline-assistant). Linux only. Focus: what APPLIES to Hermes
(a custom ACP **External Agent**) vs what does NOT.

## 1. Three agent paths (overview.md, quick-start.md)
| Path | Runner | Config owner | Applies to Hermes? |
|------|---------|--------------|--------------------|
| **Zed Agent** | Zed-native | Zed (LLM Providers, profiles, Skills, Instructions, MCP) | No — separate agent |
| **External Agents** (ACP) | Your own process over stdio JSON-RPC | The agent (Hermes owns runtime/auth/models/tools) | **Yes — this is Hermes** |
| **Terminal Threads** | CLI/TUI in a terminal-backed thread | The CLI owns auth/config | No — different path |

- Hermes registers under `agent_servers` in `~/.config/zed/settings.json`; Zed auto-detects, no restart.
- Threads Sidebar organizes all thread types together; each runs its own agent, context, history.

## 2. What applies vs does NOT (decision table)
| Zed AI capability | Hermes thread? | Why |
|-------------------|---------------|-----|
| Agent Panel, chat, tool calls, file diffs | **Yes** | Core ACP External Agent UX |
| Parallel / multiple threads (Threads Sidebar) | **Yes** | Each thread independent; mix Zed Agent + External Agent |
| MCP servers (forwarded over ACP) | **Maybe** | Zed MCP may forward; Hermes also reads its own native MCP |
| Thread import from External Agent | **Yes** | Zed detects existing Hermes threads; import via Thread History toolbar (some agents like Cursor/Gemini CLI unsupported) |
| Worktree isolation per thread | **Yes** | Zed-level Git feature; `create_worktree` hook sets `ZED_WORKTREE_ROOT`, `ZED_MAIN_GIT_WORKTREE` |
| Model/provider config (LLM Providers) | **No** | Hermes owns models/auth; Zed providers do NOT configure External Agents (llm-providers.md) |
| Zed-hosted models, API keys, subscriptions, gateways, local models | **No** | All Hermes-side; Zed keys live in system keychain, never passed to Hermes |
| Zed Agent profiles / Zed Skills / Instructions | **No** | Hermes uses its own profiles, skills, instructions |
| Inline Assistant generations | **No** | External Agents run in agent threads but are NOT available for Inline Assistant (inline-assistant.md) |
| Edit Prediction | **No** | Own provider setup (`edit_predictions`); not an External Agent feature |
| Git commit generation (model-backed) | **No** | Powered by Zed-configured models, not Hermes |
| Thread summaries (model-backed) | **No** | Same as above |

## 3. Model access — NOT Hermes's concern
- LLM Providers (zed-hosted / API access / subscription / gateway / local) configure the **Zed Agent and model-backed features only** (llm-providers.md).
- External Agents and Terminal Threads "usually own their own model access, auth, and configuration."
- Anthropic-/OpenAI-compatible setup lives under Use API Access — irrelevant to Hermes threads.

## 4. Threads Sidebar & Parallel Agents (applies — parallel-agents.md)
- **Open**: `ctrl-alt-j` (Linux). Focus without toggle: `ctrl-alt-;`. Search: `ctrl-f` when focused.
- **Layout**: title-bar menu *Panel Layout > Agentic* (or `workspace: use agentic layout`); restore with *Classic*.
- **Switch threads**: click in sidebar, or `ctrl-tab` / `Shift+ctrl-tab` to cycle recent threads (works from Agent Panel too).
- **Thread History**: `ctrl-g` or clock icon. Archive (hover archive icon / `Shift+Backspace`), restore, or permanently delete (trash — unrecoverable). Fuzzy search on titles.
- **Multiple projects**: *Add Project* button (open-folder icon) in bottom bar → recent / Add Local Folders / Add Remote Folder. Multi-root folder projects let one thread read/write across folders.
- **New thread in a project**: hover project header `+`, or `agents sidebar: new thread in group`.
- **Thread types**: Zed Agent thread (Zed settings/profiles/tools/MCP) · External Agent thread (**ACP + Hermes native config**) · Terminal Thread (CLI owns auth).
- **Worktree isolation**: start a thread in a new Git worktree for isolated checkout; detached HEAD by default. Moving a finished thread to history saves/restores its worktree.

## 5. Inline Assistant & Edit Prediction — does NOT apply (inline-assistant.md)
- Inline Assistant (`ctrl-enter` in editors/channel notes/terminal panel) transforms a selection in place using **Zed-configured LLM providers** (zed-hosted, API keys, gateways, local, subscriptions).
- **External Agents are explicitly NOT available for Inline Assistant generations.**
- Context (`@`-mention files/dirs/threads/instructions/symbols, paste images, `@thread`) — Zed-side; not Hermes.
- Parallel generations (multiple cursors, `inline_alternatives` multi-model) — Zed model config; N/A to Hermes.
- Edit Prediction = automatic, context-inferred completions (vs prompt-driven Inline Assistant); separate `edit_predictions` provider; N/A to Hermes.

## 6. Disabling AI (quick-start.md)
- Settings Editor `zed: open settings` → *Disable AI*, or settings.json `"disable_ai": true`.
- Disables **all** AI features: Threads Sidebar, Agent Panel, Edit Prediction, Inline Assistant. Hermes threads stop too.

## 7. Config entry points (quick-start.md)
- LLM providers / External Agents / MCP: **Agent Settings** (`agent: open settings`).
- Tool permissions / edit prediction / disable AI: Settings Editor (`zed: open settings`).
- Advanced JSON: settings file (`zed: open settings file`) → `~/.config/zed/settings.json` on Linux.

---
*Source pages: overview, quick-start, llm-providers, parallel-agents, inline-assistant. Cross-ref: `references/zed-external-agents.md` for Hermes registry/auth/import depth.*
