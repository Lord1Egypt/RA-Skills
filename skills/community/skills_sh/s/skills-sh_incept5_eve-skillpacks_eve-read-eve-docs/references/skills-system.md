# Skills System

## Use When
- You need to install, update, or reason about skill availability and resolution order.
- You need pack structure or SKILL discovery conventions across org projects.
- You need to control which skills are loaded for agents, CI, or repo clones.

## Load Next
- `references/agents-teams.md` for team/agent workflows that consume skills.
- `references/overview.md` for environment context and architecture assumptions.
- `references/cli.md` for install and resolve commands.

## Ask If Missing
- Confirm whether installation is local, repository-scoped, or organization-scoped.
- Confirm preferred source (`skills.txt` local path vs remote URL).
- Confirm whether you are using pack lockfile mode via `x-eve.packs`.

Eve Horizon has a public split between **developer skills** and **runtime
skills**. Skills follow the OpenSkills SKILL.md format -- YAML frontmatter for
metadata, imperative instructions in the body, and optional bundled resources --
but they are sourced and materialized differently.

- **Developer skills** live in root `skills.txt` and are refreshed with
  `eve skills install`. They target local coding agents (Claude Code, Codex,
  Gemini CLI, Pi) working on the repo.
- **Runtime skills** live in `.eve/manifest.yaml` (`x-eve.packs`), are pinned by
  `.eve/packs.lock.yaml`, and are materialized for Eve jobs by
  `eve skills materialize`. They are what runtime agents see inside jobs.

Runtime materialization writes canonical skills to `.agents/skills/` (plural)
and bridges harness-specific layouts (`.claude/skills`, `.pi/skills`) by
symlink. The singular `.agent/skills` path is no longer used anywhere -- all
code, hooks, and docs canonicalized on `.agents/skills/`.

## SKILL.md Format

```yaml
---
name: my-skill          # Required. Hyphen-case identifier.
description: One-line summary of what this skill does
---
```

Write the body in imperative form ("Check the config", not "You should check").
Keep SKILL.md under 5,000 words. Move detailed content to `references/`.

Progressive disclosure layers:
- **Metadata** (name, description) -- always available for discovery
- **Body** (SKILL.md instructions) -- loaded when the skill is invoked
- **Resources** (`references/`, `scripts/`, `assets/`) -- loaded on demand

| Resource dir | Purpose | Loaded |
|--------------|---------|--------|
| `references/` | Detailed documentation, guides | On demand |
| `scripts/` | Executable utilities | Never (executed via CLI) |
| `assets/` | Templates, images, configs | Never (used by scripts) |

## Pack Structure

Skills are grouped into **packs** -- directories of related skills. The public
eve-skillpacks repo ships three packs:

```
eve-skillpacks/
├── eve-work/                  # Productive work patterns
│   ├── README.md
│   ├── eve-orchestration/     # Parallel decomposition, job relations
│   ├── eve-job-lifecycle/     # Job states, completion, failure
│   ├── eve-job-debugging/     # Diagnosing stuck/failed jobs
│   ├── eve-read-eve-docs/     # Platform reference lookup
│   └── eve-skill-distillation/
├── eve-se/                    # Platform-specific engineering
│   ├── README.md
│   ├── eve-manifest-authoring/
│   ├── eve-deploy-debugging/
│   ├── eve-pipelines-workflows/
│   └── ...                    # auth, bootstrap, CLI, troubleshooting
├── eve-design/                # Architecture & design thinking
│   ├── README.md
│   └── eve-agent-native-design/
└── ARCHITECTURE.md
```

Each pack includes a `README.md` covering purpose, skills, audience, and
installation instructions.

## Installing and Materializing Skills

### Developer Path: `skills.txt` + `eve skills install`

Use this for local coding agents working on the repo. One source per line;
blank lines and `#` comments are ignored. Always prefix local paths with `./`,
`../`, `/`, or `~` to distinguish from `org/repo`.

```txt
./skillpacks/my-pack/*                   # All skills in a local pack
./skillpacks/my-pack/specific-skill      # One specific skill
https://github.com/eve-horizon/eve-skillpacks  # Remote source
```

```bash
eve skills install              # Read skills.txt, install via the upstream skills CLI
eve skills install <source>     # Ad-hoc install of a single source
```

This is the compatibility path. It shells out to the `skills` binary per
skill per agent, so it is fine for occasional dev refresh but not for
clone-time or runtime startup.

### Runtime Path: `x-eve.packs` + `eve skills materialize`

Declare runtime packs in `.eve/manifest.yaml` for reproducible, lockfile-based
materialization that runs without `skills add` subprocesses:

```yaml
x-eve:
  install_agents: [claude-code, codex, gemini-cli, pi]   # default for all four
  packs:
    - source: ./skillpacks/my-pack
    - source: eve-horizon/eve-skillpacks
      ref: 0123456789abcdef0123456789abcdef01234567       # pinned 40-char SHA
```

```bash
eve packs status                          # Show current pack state
eve packs resolve --dry-run               # Preview resolution
eve agents sync                           # Resolve and write packs.lock.yaml
eve skills materialize manifest           # Fast-path materialize runtime skills
eve skills materialize manifest --skill-mode software-engineering
eve skills materialize manifest --runtime # Runtime-only: vendored, no fetch
eve skills materialize skills.txt         # Fast-path for local skills.txt entries
```

Flags on `materialize`:

| Flag | Purpose |
|------|---------|
| `--skill-mode <name>` | Manifest skill mode to resolve (default: `runtime`) |
| `--mode symlink\|copy` | Filesystem mode (default: `symlink`) |
| `--agents a,b` | Comma-separated agent override |
| `--runtime` | Consume vendored externals from `.eve/materialized-skills/` only |

The lockfile `.eve/packs.lock.yaml` pins exact versions. External pack content
is vendored into `.eve/materialized-skills/<source-id>/<install-name>/` so
runtime startup stays filesystem-only with no network or `skills` subprocess.

To migrate runtime entries off `skills.txt`, run `eve migrate skills-to-packs`,
review the output, merge it into `.eve/manifest.yaml`, and keep only repo-local
developer skills in `skills.txt`. See `references/manifest.md` for the full
`x-eve.packs` schema and pack lockfile format.

### Skill Modes

`x-eve.skill_modes` declares named runtime selection policies that jobs can opt
into:

```yaml
x-eve:
  skill_modes:
    runtime:
      pack_set: runtime
    software-engineering:
      pack_set: runtime
      include_skills_txt: true        # add dev skills.txt to the materializer
      extra_packs:
        - source: ./private-eve-dev-skills/eve-dev
```

A job (or `effectiveInvocation.data.skill_mode`) selects a mode. Default for
both agent-runtime and worker is `runtime`. `software-engineering` is explicit
opt-in for repo-focused jobs that need dev skills alongside runtime skills.

### Multiple Sparse Agent Packs

`eve project sync` (and `eve agents sync`) supports multiple sparse agent
packs, each contributing only a subset of files. The pack resolver auto-detects
"simple pack" layouts -- packs that ship `agents.yaml`, `teams.yaml`, or
`chat.yaml` at the pack root without an `eve/pack.yaml` descriptor -- so two or
more sparse packs can coexist in `x-eve.packs` and merge cleanly into the
project's resolved agent/team/chat config.

## Glob Pattern Syntax

| Pattern | Meaning | Example |
|---------|---------|---------|
| `./path/*` | All direct child skills | `./skillpacks/my-pack/*` |
| `./path/**` | All nested skills recursively | `./skillpacks/**` |
| `./path/skill` | Single specific skill | `./skillpacks/my-pack/my-skill` |

The installer expands globs, finds directories containing `SKILL.md`, and
installs each. The directory name becomes the skill identifier.

## Runtime Materialization Flow

Both agent-runtime and worker now materialize runtime skills **before**
`.eve/hooks/on-clone.sh` runs, via `materializeWorkspaceSkills()` from
`@eve/shared`. The hook can assume runtime skills are already present, so it
no longer needs to call `eve skills install`.

Per-job flow:

1. Workspace is cloned (or reused).
2. Runtime resolves the selected `skill_mode` (default `runtime`).
3. Manifest packs are materialized into `.agents/skills/<install-name>/` --
   local sources via symlink, vendored externals from
   `.eve/materialized-skills/`.
4. Claude-family harnesses get `.claude/skills` -> `../.agents/skills`. Pi
   gets `.pi/skills`. Codex reads from `.agents/skills/` directly.
5. `.eve/hooks/on-clone.sh`, `on-acquire.sh`, etc. run.
6. Harness launches with skills already in place.

Worker software-engineering jobs may explicitly request
`skill_mode: software-engineering` to also pick up `skills.txt` dev skills via
the same fast-path materializer.

Install targets (`.agents/skills/`, `.claude/skills/`, `.pi/skills/`) are
always gitignored. Tracked sources live under repo-local pack paths (listed in
`skills.txt`), resolved from `.eve/packs.lock.yaml`, or vendored under
`.eve/materialized-skills/`.

## Skill Resolution and Loading

When `skill read <name>` is invoked, OpenSkills searches (first match wins):

1. `./.agents/skills/` (project universal -- canonical, used by codex, gemini-cli, pi)
2. `~/.agents/skills/` (global universal)
3. `./.claude/skills/` (project Claude-specific -- symlink to `.agents/skills` after materialize)
4. `~/.claude/skills/` (global Claude-specific)

Project skills shadow global skills with the same name. Output includes the
skill body and a base directory for resolving bundled resources.

`.agents/skills/` (plural) is the single canonical universal path. The legacy
singular `.agent/skills/` was a typo in the worker image and shared docs and
is no longer used; everything has been canonicalized on the plural form.

## Naming Conventions

- Use **hyphen-case**: `my-skill`, not `mySkill` or `my_skill`
- Prefix domain-specific skills to avoid collisions: `eve-`, `team-`
- The directory name is the skill identifier -- choose it carefully

## Creating a Custom Skill Pack

**1. Create the pack and README:**

```bash
mkdir -p skillpacks/my-pack
# Write README.md with purpose, skills, audience, install instructions
```

**2. Add skills:**

```bash
mkdir -p skillpacks/my-pack/my-skill
cat > skillpacks/my-pack/my-skill/SKILL.md << 'EOF'
---
name: my-skill
description: Handles X when user asks about Y
---
# My Skill

## When to Use
Load this skill when working on X.

## Instructions
To accomplish X:
1. Check configuration in `config/`
2. Apply patterns from references/patterns.md
3. Validate the output
EOF
```

**3. Register and install:**

For skills.txt, add `./skillpacks/my-pack/*`. For AgentPacks, add under
`x-eve.packs` and run `eve agents sync`.

**4. Commit:** Track pack sources and manifest. Never commit install targets.

## Best Practices

**Authoring:** Write in imperative form. Include a "When to Use" section so
agents self-select. Keep the body focused; push detail to `references/`.

**Organization:** Group by domain, not team. Keep packs cohesive. Always
include a README.

**Distribution:** Project-specific skills go in-repo (`skillpacks/`). Team
skills live in a shared Git repo. Personal skills install to `~/.agents/skills/`.

**Version control:** Commit pack sources and manifests. Gitignore install
targets (`.agents/skills/`, `.claude/skills/`).

## Examples

**Personal pack** -- `skills.txt`:
```txt
./skillpacks/personal/*
```

**Team pack via Git** -- `skills.txt`:
```txt
git@github.com:your-org/team-skills
```

**Mixed installation** -- `skills.txt`:
```txt
./skillpacks/my-pack/*                     # Local pack (all skills)
./skillpacks/another-pack/special-skill    # Single skill from another pack
https://github.com/eve-horizon/eve-skillpacks  # Remote packs
```
