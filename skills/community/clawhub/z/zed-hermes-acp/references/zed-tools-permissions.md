# Zed Tools, Permissions & Sandboxing — Hermes (External Agent) Reference

> Distilled from Zed docs: `tools.md`, `tool-permissions.md`, `sandboxing.md`.
> **Linux-only.** macOS/Windows dropped. Section refs like `(tools.md)` point back to source pages.
> Audience: Hermes wired into Zed as an **External Agent** via `agent_servers` in `~/.config/zed/settings.json`.

## 0. The one rule that matters for Hermes
- Sandboxing applies **only to Zed Agent**. It does **NOT** sandbox Zed itself, language servers, extensions, tasks, normal terminal tabs, **External Agents**, or Terminal Threads. `(sandboxing.md)`
- Therefore an External Agent like Hermes runs **outside** Zed's OS sandbox. Tool **permissions** still gate what Hermes can do; **OS sandboxing** does not wrap Hermes invocations.
- `tool_permissions` restrict the agent's *ability to run* a tool action in the first place. Sandboxing restricts what a *running* action can touch. For Hermes, only the former applies. `(sandboxing.md)`

## 1. Built-in Zed tools (what the Agent Panel offers)
Tool availability is set by **Agent Profiles**; permission behavior by **tool_permissions**. `(tools.md)`

| Group | Tools |
|---|---|
| Read & Search | `diagnostics`, `fetch`, `find_path`, `grep`, `list_directory`, `read_file` |
| Web | `search_web` (Zed Pro + Zed provider only) |
| Edit | `copy_path`, `create_directory`, `delete_path`, `edit_file`, `move_path`, `write_file` |
| Shell | `terminal` (new shell per call; can opt into OS sandbox) |
| Other | `skill`, `spawn_agent` (subagents inherit parent's tools) |

- `fetch` is **not** run inside the terminal OS sandbox → terminal sandbox network grants (`allow_hosts`, `allow_all_hosts`) **do not apply** to `fetch`. `(tools.md)`
- Custom tools beyond these come from **MCP servers** (`mcp::<server>:<tool>`). `(tools.md)`

## 2. Tool permissions — what they govern
Controlled by `agent.tool_permissions.default` (Zed >= v0.224.0; older used `agent.always_allow_tool_actions` bool). `(tool-permissions.md)`

### 2.1 Permission-gated tools & match input
| Tool | Matched input |
|---|---|
| `terminal` | shell command string |
| `edit_file`, `write_file` | file path |
| `delete_path` | path being deleted |
| `move_path`, `copy_path` | source **and** dest paths |
| `create_directory` | directory path |
| `fetch` | URL |
| `search_web` | search query |
| `skill` | absolute path to `SKILL.md` |
| MCP tools | `mcp:<server>:<tool>` (e.g. `mcp:github:create_issue`) |

- User-invoked `/skill-name` slash commands don't re-prompt; model-invoked `skill` does. `(tool-permissions.md)`
- To block model invocation entirely: `disable-model-invocation: true` in the skill's `SKILL.md`. `(tool-permissions.md)`

### 2.2 Rule precedence (highest -> lowest)
1. **Built-in security rules** — hardcoded, non-overridable (terminal only; e.g. `rm -rf /`, `rm -rf ~`, `rm -rf $HOME`, `rm -rf .`, `rm -rf ..`, any flag combo, case-insensitive, checked per sub-command). `(tool-permissions.md)`
2. `always_deny` — blocks immediately, top priority.
3. `always_confirm` — prompts even when global `default: "allow"`.
4. `always_allow` — auto-approves (unless deny/confirm also match).
5. Tool-specific `default` (e.g. `tools.terminal.default`).
6. Global `default` (`tool_permissions.default`; `"confirm"` is the default). `(tool-permissions.md)`

### 2.3 Options & matching
- `default`: `"confirm"` | `"allow"` | `"deny"`.
- Patterns: **Rust regex**, case-insensitive by default (`case_sensitive: false`).
- `terminal` parsing: chained commands (`a && b`) are split; each sub-command checked against patterns. All major shells supported. `(tool-permissions.md)`
- UI prompt choices: Allow/Deny once; "Always for <input>" sets tool-level default or adds an `always_allow`/`always_deny` pattern (MCP tools: tool-level only). `(tool-permissions.md)`

### 2.4 Decision rule — should Hermes' action auto-run?
```
IF matches built-in security rule (terminal)  -> BLOCK (unavoidable)
ELSE IF matches always_deny                   -> BLOCK
ELSE IF matches always_confirm                -> PROMPT
ELSE IF matches always_allow                  -> RUN
ELSE IF tool-specific default set             -> use it
ELSE                                          -> use global default (confirm)
```

## 3. Sandboxing — Zed Agent only, NOT External Agents
Mechanism: OS-level (not instruction-following) restrictions on `terminal` and `fetch` tools. `(sandboxing.md)`

### 3.1 What the sandbox limits
| Tool | Limits |
|---|---|
| `terminal` | FS writes + outbound network for agent-run commands; Git metadata protected |
| `fetch` | which hosts can be reached |

- Still governed by `tool_permissions`, Agent Profiles, project trust. `(sandboxing.md)`
- **External Agents are explicitly excluded** from sandboxing. `(sandboxing.md)`

### 3.2 Linux specifics (`bwrap`)
- Requires runnable, **non-setuid** `bwrap` on `$PATH`. Zed **refuses setuid-root `bwrap`**. `(sandboxing.md#linux)`
- Uses unprivileged user namespaces (no extra privilege from setuid). Test: `bwrap --ro-bind / / -- echo "working"`. `(sandboxing.md#linux)`
- Ubuntu >=23.10: unprivileged user namespaces restricted by AppArmor; may need `bwrap-userns-restrict` profile. `(sandboxing.md#installing-bubblewrap-ubuntu)`
- If `bwrap` unavailable/can't create sandbox -> Zed runs command **without** OS sandbox + shows a warning. `(sandboxing.md#linux)`
- `/tmp` is a fresh tmpfs per call; cleared between calls. On unrestricted write grant, `/tmp` becomes the real host `/tmp`. `(sandboxing.md#linux)`

### 3.3 Default sandbox access (Zed Agent; for reference)
- Reads: most FS, incl. protected Git metadata.
- Writes: inside open project dirs, **except** Git metadata (`.git`, worktree metadata, refs, index, hooks, local config — never writable while sandboxed, even with broad grants).
- Temp: writable `$TMPDIR`/`$TMP`/`$TEMP`.
- Other writes & outbound network: **blocked** unless you approve a broader sandbox request.
- Local IPC Unix sockets: blocked (prevents escape via session bus / container daemon). `(sandboxing.md#default-access)`

### 3.4 Sandbox approval prompts (Zed Agent)
Can request: specific hosts / all hosts / specific write paths / unrestricted FS writes (except Git metadata) / run **unsandboxed**.
- Grant scope: one action | rest of thread (thread-only memory) | always (saved to `agent.sandbox_permissions`). `(sandboxing.md#approval-prompts)`
- Prefer narrow grants (`network_hosts`, `write_paths`) over `allow_all_hosts` / `allow_fs_write_all` / `allow_unsandboxed`. `(sandboxing.md#persistent-sandbox-permissions)`
- Git metadata writes are **never** grantable while sandboxed. `(sandboxing.md#git-metadata)`

### 3.5 `sandbox_permissions` keys (Zed Agent)
| Key | Effect |
|---|---|
| `network_hosts` | allowlisted hosts (exact or leading-`*.` wildcard) |
| `allow_all_hosts` | any host |
| `write_paths` | absolute dir subtrees writable w/o prompt |
| `allow_fs_write_all` | write anywhere except Git metadata |
| `allow_unsandboxed` | disable sandbox for Zed Agent terminal (fetch unrestricted) |

## 4. Side channels Hermes (outside sandbox) should note
Sandboxing is **one layer** in defense-in-depth; not a substitute for good practice. `(sandboxing.md#trust)`
- Language servers (e.g. Rust proc macros), built-in git client, regular terminal all run **outside** the sandbox.
- Agent can add a malicious proc macro (run by `rust-analyzer` outside sandbox), poison a `Makefile` (runs outside sandbox on `make`), or create a submodule whose Git metadata it controls (executed outside sandbox on `git`). `(sandboxing.md#trust)`
- Mitigations: disable code-executing language servers; use a Git-status shell prompt that doesn't run repo-defined programs; review diffs before `git commit`. `(sandboxing.md#trust)`

## 5. Quick config shapes (Linux, External Agent context)
- **Hermes-relevant**: tool_permissions still gate Hermes; tune `tools.terminal`/`edit_file`/`write_file`/`delete_path`/`fetch` rules. Sandboxing does not wrap Hermes.
- Global auto-approve (most tools, except deny/confirm/built-ins/settings dirs):
  ```json
  { "agent": { "tool_permissions": { "default": "allow" } } }
  ```
- Protect sensitive files via `edit_file`/`write_file` `always_deny` patterns (`.env`, `secrets?/`, `\.(pem|key)$`). `(tool-permissions.md)`
- Enable Linux sandbox for **Zed Agent** (not Hermes): install non-setuid `bwrap` (`sudo apt install bubblewrap` + AppArmor profile on Ubuntu). `(sandboxing.md#installing-bubblewrap)`
