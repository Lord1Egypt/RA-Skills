# Host adapter: OpenClaw

**HR deployment note:** On OpenClaw, treat **`skill-hr` as the dedicated HR function** for your skill workforce—the same JD → match → recruit → handoff → performance / termination loop as in `SKILL.md`, with `.skill-hr/` registry and incidents as the **HR record** for assignments (host-agnostic paths; see `references/06-state-and-artifacts.md`).

## Source of truth (keep current with upstream)

Authoritative behavior and schema change with OpenClaw releases. Prefer these pages when anything below drifts:

- [Skills (loading, precedence, format, security)](https://docs.openclaw.ai/tools/skills)
- [Skills config (`openclaw.json`)](https://docs.openclaw.ai/tools/skills-config)
- [Creating skills](https://docs.openclaw.ai/tools/creating-skills)
- [ClawHub (install / browse)](https://docs.openclaw.ai/tools/clawhub) — registry: [clawhub.ai](https://clawhub.ai/)

## Main config file

Skill loader and install settings live under **`skills`** in:

`~/.openclaw/openclaw.json`

Agent-level **visibility** (allowlists) lives under **`agents.defaults.skills`** and **`agents.list[].skills`** (separate from *where* files sit on disk).

## Where skills load from (precedence)

When the **same skill name** exists in more than one place, **higher row wins** (workspace / agent paths beat shared and bundled copies):

| Precedence (high → low) | Typical meaning |
|-------------------------|-----------------|
| `<workspace>/skills/` | Per-agent workspace skills; `openclaw skills install` targets the active workspace `skills/` tree |
| `<workspace>/.agents/skills/` | Project-scoped agent skills for that workspace |
| `~/.agents/skills/` | Shared across workspaces for the user profile |
| `~/.openclaw/skills/` | Managed / local overrides visible to agents on this machine |
| Bundled skills | Shipped with the OpenClaw install |
| `skills.load.extraDirs` | Extra directories to scan (**lowest** precedence); each entry should be a folder whose **child directories** are individual skills (each child contains `SKILL.md`) |

Exact path spelling follows your OS and OpenClaw workspace layout; resolve real paths on the machine and record them in the incident the first time you recruit on that host.

Useful **`skills.load`** knobs (defaults may change—see [Skills config](https://docs.openclaw.ai/tools/skills-config)):

- `extraDirs` — additional skill roots
- `watch` / `watchDebounceMs` — refresh when `SKILL.md` changes (often picked up on the next agent turn)

## Installing `skill-hr`

1. Copy this repository folder **`packages/skill-hr/`** into a **skill root** as a directory named **`skill-hr`**, so `SKILL.md` resolves as **`skill-hr/SKILL.md`**, preserving **`references/`** and **`scripts/`**.

   **Common choices:**

   - **All agents on this machine:** `~/.openclaw/skills/skill-hr/`
   - **Current OpenClaw workspace only:** `<active-workspace>/skills/skill-hr/` (matches “workspace wins” precedence)
   - **Shared pack via config:** parent directory listed in `skills.load.extraDirs`, with `skill-hr` as a subfolder under that parent

2. If you use **agent skill allowlists**, add the skill key OpenClaw uses for this package. Default config keys match the skill **`name`** in frontmatter (`skill-hr`). Hyphenated names are supported; in JSON5 you can quote the key under `skills.entries` if needed.

3. **Reload:** start a **new** session (e.g. `/new` in chat) or **`openclaw gateway restart`** so the loader picks up the skill. Verify with:

   ```bash
   openclaw skills list
   ```

## Discovering the installed pool (P02)

- Prefer **`openclaw skills list`** for the effective snapshot on that session.
- For bench analysis, you may still enumerate skill directories under the roots above and read each **`SKILL.md`** frontmatter (`name`, `description`).
- Merge with **project** `.skill-hr/registry.json` when the workspace uses HR state in-repo.

## Format notes (OpenClaw ↔ this bundle)

OpenClaw documents **[AgentSkills](https://agentskills.io/)**-compatible folders with **`SKILL.md`** + YAML frontmatter. The embedded parser expects **single-line frontmatter keys**; keep `description` on **one line** (quoted if it contains `:`). If you add **`metadata.openclaw`**, upstream expects it as a **single-line JSON object** in frontmatter—see [Skills](https://docs.openclaw.ai/tools/skills).

Optional: use **`{baseDir}`** in instructions to mean the skill folder path (OpenClaw replaces it when building prompts).

## Recruitment and marketplace flows

- **From ClawHub / CLI:** prefer documented commands such as **`openclaw skills install …`** and **`openclaw skills update --all`** per [ClawHub](https://docs.openclaw.ai/tools/clawhub); installs into the **active workspace** `skills/` tree unless your setup differs.
- **From git:** cloning or copying into one of the skill roots above is fine; log **`source_url`** in `.skill-hr/registry.json`.
- **Safety:** treat third-party skills as untrusted; avoid silent **`curl | sh`**. Gateway-backed installs may run a **dangerous-code scanner**—still apply **`references/01-competency-model.md`** vetoes and user confirmation before risky steps.

## Sandbox and env

If the agent runs in a **sandbox**, host `process.env` may not apply to skill child processes. Per OpenClaw docs, use **`agents.defaults.sandbox.docker.env`** (or per-agent equivalents) or a custom image when a recruited skill needs env vars or binaries inside the container.

## Incident and registry paths

Use **workspace root** paths from **`references/06-state-and-artifacts.md`** so HR state can live in the repo (`.skill-hr/registry.json`, `.skill-hr/incidents/`) regardless of OpenClaw skill install location.

## Maintenance

When OpenClaw changes default paths or config keys, update this file in **one focused edit** and align any examples in **`references/prompts/P04-market-search-brief.md`** outputs for `host: openclaw`.
