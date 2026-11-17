# Zed Skills, MCP & Instructions — Reference for the Hermes ACP skill

Scope: Linux only (`~/.config/zed/...`, `~/.agents/skills/`). Hermes runs in Zed as an **External Agent** over ACP. Distills Zed's `ai/mcp`, `ai/skills`, `ai/instructions` docs into a structural reference. macOS/Windows paths dropped. NO invented commands/paths.

## 0. Core boundary (read first)

Zed exposes three agent paths; Hermes is the External Agent one:

| Path | Nature | Skills | MCP | Instructions |
|------|--------|--------|-----|--------------|
| Zed Agent | Zed-native | Native Zed Skills | Zed-configured directly | Zed AGENTS.md loader |
| External Agents (Hermes) | ACP process you own | **No — Hermes uses its own** | **Zed may forward over ACP; Hermes also reads native config** | "Not generally used" / "depends on agent" |
| Terminal Threads | Raw CLI/TUI | Own native | Own native | Own native |

Rule of thumb: Zed Skills and Zed's instruction loader **do not** govern Hermes threads. Hermes brings its own skills, MCP config, and instructions.

## 1. Zed Skills — what they are (and why they don't touch Hermes)

- Reusable, on-demand instruction packages: a folder with `SKILL.md` (YAML frontmatter + Markdown body).
- Agent sees a catalog (name + description) and loads one on demand, or you invoke by name.
- Two scopes:
  - Global: `~/.agents/skills/` (every project)
  - Project-local: `<worktree>/.agents/skills/` (current project only)
- Flat layout only; nesting is not discovered. Project-local loads only from **trusted worktrees**.
- Name collision: project-local overrides global.
- Invocation: autonomous (catalog match) or manual slash `/<name>` / `@<name>` mention.
- `disable-model-invocation: true` hides from catalog but keeps the slash command.
- Frontmatter: `name` (a-z/0-9/-, 1–64 chars, no leading/trailing/double hyphen), `description` (≤1024 bytes), optional `disable-model-invocation`.
- Body ≤500 lines; push detail to `references/`, scripts to `scripts/` (progressive disclosure).

**CRITICAL for Hermes:** Zed docs state Skills apply to the Zed Agent; External Agents "may have their own native skills, prompts, or instruction systems." Configure those in the External Agent. → Zed Skills do **not** load into Hermes threads.

## 2. Hermes skills (counterpart)

- Hermes owns its skills independently (`~/.hermes/skills/...`). Zed Skills, Zed profiles, and Zed's skill loader are irrelevant to a Hermes ACP thread.
- Do not expect a `~/.agents/skills/` skill to surface inside Hermes.

## 3. MCP in Zed

Supported: **Tools** and **Prompts** (plus `notifications/tools/list_changed` auto-reload). Not yet: Discovery / Sampling / Elicitation.

### Install (two routes)
- As Extensions: Settings → AI → MCP Servers → Add Server → Install from Extensions (e.g. Context7, GitHub, Puppeteer).
- As Custom Servers: same panel → Add Server → Add Local / Add Remote. Writes to `context_servers` in settings (`zed: open settings file`):
  - Local: `command` + `args` + optional `env`
  - Remote: `url` + optional `headers` (Bearer token); omit `Authorization` header → Zed triggers MCP OAuth flow.
- Health check: Settings → AI → MCP Servers indicator dot (green = "Server is active").

### Agent Path Support (MCP)
- Zed Agent: uses Zed-configured MCP directly.
- External Agents (Hermes): **Zed can forward configured MCP servers over ACP**; the agent may also read its own native MCP config.
- Terminal Threads: native CLIs/TUIs read their own MCP config.

### MCP forwarding to External Agents (Hermes) — key point
- MCP servers configured in Zed are forwarded to Hermes over ACP automatically.
- Hermes can *also* read its own native MCP config independently.
- Tool missing? Check **both** Zed `context_servers` and Hermes MCP config. To stop Hermes auto-starting globally-configured MCP in ACP, host sets `HERMES_ACP_SKIP_CONFIGURED_MCP=1` (host env, not user `.env`).
- Tool approval: Zed `agent.tool_permissions.default` (`confirm` default / `allow` / `deny`); per-tool key `mcp:<server>:<tool_name>` (e.g. `mcp:github:create_issue`); the `default` sub-key is the primary lever for MCP tools.

## 4. Instructions (AGENTS.md)

- Always-on context for the Zed Agent (persistent guidance every interaction). Skills are for reusable named workflows — pick Instructions for conventions / tone / constraints.
- Personal: `~/.config/zed/AGENTS.md` (applies to every project).
- Project: first match among `.rules`, `.cursorrules`, `.windsurfrules`, `.clinerules`, `.github/copilot-instructions.md`, `AGENT.md`, `AGENTS.md`, `CLAUDE.md`, `GEMINI.md`. Project overrides personal on conflict.

### Instruction File Support (Zed's view)
| File | Zed Agent | External Agents | Terminal Threads |
|------|-----------|-----------------|------------------|
| `~/.config/zed/AGENTS.md` | personal instructions | Not generally used | Not used unless CLI reads it |
| Project `AGENTS.md` | project instructions | Depends on the agent | Depends on the CLI |
| `CLAUDE.md` | compatible project | Claude reads natively | Claude Code CLI reads natively |
| `.github/copilot-instructions.md` | compatible project | Depends on the agent | Depends on the CLI |

**For Hermes:** External Agents "may read their own native instruction files directly. Do not assume Zed's instruction loader controls those agents." → Hermes reads its own config/instructions, not Zed's `AGENTS.md`, unless Hermes's CLI chooses to.

## 5. Decision rules

- Reusable task steps in Zed? → Zed Skill (won't reach Hermes).
- Always-on repo guidance in Zed? → `AGENTS.md` (won't reach Hermes).
- Tool available inside a Hermes thread? → configure in Zed `context_servers` (forwarded over ACP) **or** Hermes native MCP; verify in both.
- Want Hermes to behave a certain way? → configure in Hermes, not via Zed Skills/Instructions.

## 6. Source pages (Zed docs, distilled)
- `ai/mcp`, `ai/skills`, `ai/instructions` — macOS/Windows paths dropped.
