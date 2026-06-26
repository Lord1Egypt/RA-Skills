---
name: groove-admin-install
description: "Install groove backends, companions, and AGENTS.md bootstrap. Run once per repo."
license: MIT
allowed-tools: Read Write Edit Glob Grep Bash(git:*) Bash(beans:*) Bash(gh:*) Bash(linear:*) Bash(npx:*) Bash(mkdir:*) AskUserQuestion
metadata:
  author: andreadellacorte
---

<!-- groove:managed — do not edit; changes will be overwritten by groove update -->

# groove-admin-install

## Outcome

All groove backends are installed in dependency order, **companion skills and groove skill symlinks are present** (first install is not complete without them), AGENTS.md contains the session bootstrap, and the repo is ready for use.

## Acceptance Criteria

- Task and memory backends installed (or clearly reported if a step failed)
- **Companion skills installed** (find-skills, agent-browser, pdf-to-markdown) — required; verify each `SKILL.md` exists after step 4
- **Platform symlinks** — `.claude/skills/groove*` and `.cursor/skills/groove*` point at `.agents/skills/groove*` — required on every install run
- User sees a summary of what was installed, including ✓/✗ for companions and symlinks

## Steps

Run in order:

1. If `.groove/index.md` does not exist, run `/groove-admin-config --defaults` to create it with all defaults (no prompts)
2. Run `/groove-utilities-task-install` — installs the configured task backend (e.g. beans)
3. Run `/groove-utilities-memory-install` — creates memory directories
4. **Install companion skills (mandatory — do not skip):** On first install and every later run, ensure these exist under `.agents/skills/`. If `SKILL.md` is missing, run the matching `npx skills add` command; on transient failure, retry once, then report failure (install is **not** complete until all three succeed).
   - **find-skills** (downloaded): `test -f .agents/skills/find-skills/SKILL.md` or `npx skills add https://github.com/vercel-labs/skills --skill find-skills`
   - **agent-browser** (downloaded): `test -f .agents/skills/agent-browser/SKILL.md` or `npx skills add https://github.com/vercel-labs/agent-browser --skill agent-browser`
   - **pdf-to-markdown** (embedded): `test -f .agents/skills/pdf-to-markdown/SKILL.md` or `npx skills add andreadellacorte/groove --skill pdf-to-markdown`
   - Afterward, verify: `test -f` each of the three `SKILL.md` paths — if any missing, stop and report install incomplete (do not claim success).
   - Report each as installed / already-present / failed
5. **Sync platform skill directories via symlinks (mandatory — do not skip):** Groove skills must be linked into each editor’s skills tree so `groove-*` commands resolve.
   - Create parent dirs if missing: `mkdir -p .claude/skills .cursor/skills` (Claude Code expects `.claude/skills/`; Cursor expects `.cursor/skills/`)
   - For each directory in `.agents/skills/` that starts with `groove`:
     - Create `.claude/skills/<name>` as a symlink → `../../.agents/skills/<name>`
     - Create `.cursor/skills/<name>` as a symlink → `../../.agents/skills/<name>`
   - Run: `mkdir -p .claude/skills .cursor/skills && for skill in .agents/skills/groove*; do name=$(basename "$skill"); ln -sfn "../../.agents/skills/$name" ".claude/skills/$name"; ln -sfn "../../.agents/skills/$name" ".cursor/skills/$name"; done`
   - Note: use `ln -sfn` (no-dereference) — `ln -sf` on an existing directory symlink follows the symlink and creates a nested symlink inside the target directory
   - Verify: at least one `groove-*` name exists under `.agents/skills/` and matching symlinks exist under `.claude/skills/` and `.cursor/skills/`
   - Report: "✓ platform symlinks updated (.claude/skills/, .cursor/skills/)" or report failure
6. Scaffold hooks and cache directories:
   - Create `.groove/hooks/` if it does not exist
   - Create `.groove/.cache/` if it does not exist (with a `.gitkeep`)
   - If `.groove/hooks/start.md` does not exist, create it with:
     ```markdown
     # Hook: Session Start

     Runs automatically at the end of `/groove-daily-start`.
     Add items to `## Actions` to automate session-start tasks.

     ## Actions

     <!-- Add actions here, one per line. Examples:
     - Run `git fetch --all` to refresh remote refs
     - Print "Good morning — groove is ready"
     -->
     ```
   - If `.groove/hooks/end.md` does not exist, create it with:
     ```markdown
     # Hook: Session End

     Runs automatically at the end of `/groove-daily-end`.
     Add items to `## Actions` to automate session-end tasks.

     ## Actions

     <!-- Add actions here, one per line. Examples:
     - Run `git push` to push today's commits
     - Print "Session closed — see you tomorrow"
     -->
     ```
   - Report hooks: created / already-present
7. Apply git strategy — write `.groove/.gitignore` from `git.*` sub-keys in `.groove/index.md` (see `/groove-admin-config` for rules)

## Constraints

- Read `.groove/index.md` for `tasks.backend` and `git.*` config before running
- If `.groove/index.md` does not exist, `/groove-admin-config` is run first (step 1) to create it
- Dependency order for backends must be respected: task → memory → companions
- Each step reports installed / already-present / failed
- `AGENTS.md` update is additive per section — preserve all other content
- If task or memory install fails, report it clearly and continue — user may still need companions + symlinks
- **Steps 4–5 (companion skills + symlinks) are required for a successful install:** do not report "install complete" until both steps succeeded. This is intentional: first-time bootstrap must leave skills discoverable in Cursor and Claude Code.
- Companion skills (find-skills, agent-browser, pdf-to-markdown) are hardcoded here, not read from any config file
- Report a final summary (include platform symlinks line):
  ```
  ✓ task backend (beans)
  ✓ memory backend — memory dirs ready
  ✓ companion: find-skills
  ✓ companion: agent-browser
  ✓ companion: pdf-to-markdown
  ✓ platform symlinks (.claude/skills/, .cursor/skills/)
  ✓ hooks: .groove/hooks/ ready
  ```
