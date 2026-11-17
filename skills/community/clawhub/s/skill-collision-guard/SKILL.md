---
name: skill-collision-guard
version: 0.1.1
description: Use only when the user explicitly asks to inspect or compare coding-agent skills before installation or invocation. The workflow uses bounded local discovery, optional read-only Git candidate retrieval, deterministic comparison of names, capabilities, policies, and behavior, and reversible session suppression; it reads SKILL.md files only, never executes candidate code or installs/removes skills, and leaves conflict decisions with the user.
compatibility: Requires Node.js 18 or newer. Git is used only when a user supplies a remote candidate. Local inspection reads declared skill roots or the supplied candidate path; optional remote inspection uses a temporary shallow clone and session suppression writes a small local state file.
allowed-tools:
  - "Bash(node {baseDir}/bin/skill-guard.js scan *)"
  - "Bash(node {baseDir}/bin/skill-guard.js check-install *)"
  - "Bash(node {baseDir}/bin/skill-guard.js compare *)"
  - "Bash(node {baseDir}/bin/skill-guard.js suppress *)"
  - "Bash(node {baseDir}/bin/skill-guard.js status *)"
  - "Bash(node {baseDir}/bin/skill-guard.js restore *)"
user-invocable: true
disable-model-invocation: true
metadata:
  openclaw:
    requires:
      bins:
        - node
        - git
    envVars:
      - name: SKILL_GUARD_STATE_DIR
        required: false
        description: Optional directory override for local session suppression state.
      - name: XDG_STATE_HOME
        required: false
        description: Optional platform state root used when SKILL_GUARD_STATE_DIR is unset.
      - name: LOCALAPPDATA
        required: false
        description: Optional Windows state root used when SKILL_GUARD_STATE_DIR is unset.
    config:
      stateDirs:
        - "$SKILL_GUARD_STATE_DIR/sessions"
        - "$XDG_STATE_HOME/skill-collision-guard/sessions"
        - "$LOCALAPPDATA/skill-collision-guard/sessions"
---

# Skill Collision Guard

This skill is a preflight and comparison workflow. The runtime is bundled next to this document; use `{baseDir}` rather than searching parent directories for executable files:

```bash
node {baseDir}/bin/skill-guard.js check-install <candidate> --agent <current-agent> --session <session-id>
```

The published bundle includes that entrypoint and its local `src/` modules; no parent-directory lookup or hidden runtime download is required.

The candidate can be a local skill/plugin path, a GitHub URL or `owner/repo`, or a locally configured `plugin@marketplace` reference. Use `scan` for the installed inventory and `compare` for a direct comparison.

## Access and Safety

- The detector reads `SKILL.md` text and metadata. It never executes code from a candidate and never installs, removes, renames, or edits an installed skill.
- Local discovery is bounded to the selected host's declared project, user, system, extension, and plugin-cache roots. Candidate traversal rejects symbolic links whose canonical target leaves the supplied candidate root.
- A remote check occurs only when the user supplies a Git-compatible reference. It invokes the declared `git` binary with `git clone --depth 1 --no-tags`, reads the staged `SKILL.md` files, and removes only the temporary clone after inspection. No candidate code is run and the workflow does not upload inspected file contents to a separate service.
- Suppression writes only skill names/paths and timestamps to the session state directory declared above, using private directory/file permissions where the platform supports them. `SessionEnd` removes only that session file; it does not delete a skill or its directory.
- The bundled CLI reports relationships and recommendations. It does not make an installation or removal decision. Exit status `2` requires the user to choose how to proceed; do not bypass it silently.
- English and Chinese phrases in the capability taxonomy are recognition signals so multilingual skill descriptions can be compared. They do not force a language or trigger unrelated tasks.

## Decisions

- `name-shadow`: two skills expose the same normalized name. Recommend keeping one.
- `capability-collision`: differently named skills provide the same capability. Compare their full instructions before choosing one.
- `capability-conflict`: the same capability is governed by incompatible roles or behavior. Ask which behavior applies.
- `capability-overlap`: related capability facets may coexist if their trigger boundaries are clear.
- `behavioral-interference`: a global write policy can alter a fixed workflow. Keep the fixed workflow authoritative and suppress the overlay while they overlap.
- `complementary`: the skills cover separate, useful passes. Keep both and run them separately.
- `policy-conflict`: their scopes overlap but their instructions disagree. Ask which policy applies to the current task.
- `probable-duplicate`: their goals and instructions substantially overlap. Recommend the narrower or better-maintained skill.
- `overlap`: both may trigger, but can coexist if their descriptions clearly separate their scopes.

Show the compared names, paths, descriptions, relationship type, score, evidence source, affected workflows, opposing policies, and recommendation. Treat curated and automatic results as evidence requiring semantic review, except exact same-name shadowing. For a consequential decision, read both `SKILL.md` files before advising which one to remove. Never remove, rename, or edit an installed skill without the user's approval.

## Session Suppression

Prefer reversible session suppression when the user only needs one skill temporarily:

```bash
node {baseDir}/bin/skill-guard.js suppress <name-or-path> --session <session-id>
node {baseDir}/bin/skill-guard.js restore <name-or-path> --session <session-id>
node {baseDir}/bin/skill-guard.js status --session <session-id>
```

With lifecycle hooks enabled, `/skill-guard suppress <name-or-path>` and `/skill-guard restore [name-or-path]` update the same session state. Suppression is an instruction-level session overlay: it does not move or delete files. The session-end hook removes the state file automatically.

If the host has no lifecycle hook support, keep the suppression instruction in the active conversation and use `status` before each skill invocation. State clearly that this is cooperative rather than host-enforced.

## Installed Inventory

Use `scan` to find cross-agent duplicates already present:

```bash
node {baseDir}/bin/skill-guard.js scan --agent <current-agent>
```

The `codex` scope includes both Codex-specific roots and portable `.agents/skills`. Do not treat a clean heuristic result as proof of semantic compatibility. Capability families are deliberately curated; if two unclassified skills affect the same high-risk workflow, compare their full instructions even when their score is below the warning threshold.
