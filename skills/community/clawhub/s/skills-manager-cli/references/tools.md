# Tool ids for `skm --for` / `skm list --tool`

Pass these ids (or a unique prefix) to `--for` and `--tool`. Exact id wins
before prefix, so `trae` is Trae, not Trae CN.

`detected` means the tool's config directory exists on this machine.
`skm init` records that snapshot; later `skm` loads do not re-run full
detection for tools already in config. A tool installed after init may
still show `not installed` until the GUI redetects.

Project-local skills (workspace copies) are only defined for the tools
that have a `project_skills_dir` below. Other tools are global-hub only.

| id | Name | Home config dir | CLI | Project skills dir |
| --- | --- | --- | --- | --- |
| `claude-code` | Claude Code | `.claude` | `claude` | `.claude/skills` |
| `codex` | Codex | `.codex` | `codex` | `.agents/skills` |
| `deepseek-harness` | DeepSeek Harness | `.dsh` | `dsh` | `.dsh/skills` |
| `codebuddy` | CodeBuddy | `.codebuddy` | `codebuddy` | — |
| `opencode` | OpenCode | `.config/opencode` (alt `.opencode`) | `opencode` | `.opencode/skills` |
| `cursor` | Cursor | `.cursor` | `cursor` | `.cursor/skills` |
| `gemini` | Gemini CLI | `.gemini` | `gemini` | `.gemini/skills` |
| `antigravity` | Antigravity | `.antigravity` | `antigravity` | — |
| `windsurf` | Windsurf | `.windsurf` | `windsurf` | — |
| `trae` | Trae | `.trae` | `trae` | — |
| `droid` | Droid | `.factory` (alt `.droid`) | `droid` | — |
| `augment` | Augment | `.augment` | `augment` | — |
| `openclaw` | OpenClaw | `.openclaw` | `openclaw` | — |
| `cline` | Cline | `.cline` | `cline` | — |
| `vercel-skills` | Vercel Skills | `.agents` (alt `.vercel`, `.vercel-skills`) | `vercel` | `.agents/skills` |
| `commandcode` | CommandCode | `.commandcode` | `commandcode` | — |
| `continue` | Continue | `.continue` | `continue` | — |
| `crush` | Crush | `.config/crush` (alt `.crush`) | `crush` | — |
| `goose` | Goose | `.config/goose` (alt `.goose`) | `goose` | — |
| `iflow` | iFlow | `.iflow` | `iflow` | — |
| `junie` | Junie | `.junie` | `junie` | — |
| `kilo-code` | Kilo Code | `.kilocode` | `kilo` | — |
| `kiro` | Kiro | `.kiro` | `kiro` | — |
| `qoder` | Qoder | `.qoder` | `qoder` | — |
| `qwen-code` | Qwen Code | `.qwen` | `qwen` | — |
| `roo-code` | Roo Code | `.roo` | `roo` | — |
| `zencoder` | Zencoder | `.zencoder` | `zencoder` | — |
| `pi` | Pi | `.pi/agent` | `pi` | — |
| `trae-cn` | Trae CN | `.trae-cn` | `trae` | — |
| `hermes` | Hermes | `.hermes` | `hermes` | — |
| `workbuddy` | WorkBuddy | `.workbuddy` | `workbuddy` | — |
| `qoderwork-cn` | QoderWork CN | `.qoderworkcn` | `qoderworkcn` | — |

Custom tools from the GUI also appear in `skm doctor --json` / `skm list`
under whatever id the user gave them. Prefix-match those the same way.

## Prefix collisions to avoid

| Typed | Resolves to | Collision |
| --- | --- | --- |
| `trae` | `trae` (exact) | `trae-cn` exists; use `trae-cn` for Trae CN |
| `qoder` | `qoder` (exact) | `qoderwork-cn` exists; use `qoderwork-cn` |
| `claude` | `claude-code` | unique prefix |
| `code` | ambiguous | `codebuddy`, `codex`, `commandcode` |

When unsure, copy `id` from `skm doctor --json`.

## Windows linking

`enable` tries, in order: directory symlink (Developer Mode or elevated) →
directory junction (`mklink /J`, no admin) → tracked copy with
`.skills-manager-source.json`. A standard account is enough. Elevation
does not help a tool that is not detected — the tool's config directory
still has to exist.
