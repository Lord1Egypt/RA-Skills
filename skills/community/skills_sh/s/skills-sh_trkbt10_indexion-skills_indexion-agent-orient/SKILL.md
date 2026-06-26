---
name: indexion-agent-orient
description: Generate and use a pre-edit structure brief so coding agents learn likely owners, consumer surfaces, and unsafe edit locations before implementing.
---

# Agent Orientation Workflow

Use this skill before starting implementation in an unfamiliar or ambiguous part
of a codebase.

## Why

Coding agents often anchor on the path or noun in the user prompt and start
editing before they have learned the repository's ownership structure. `indexion
agent orient` builds an incremental orientation map across the selected
codebase, then renders a short, evidence-backed brief that can be pasted into
AGENTS.md, CLAUDE.md, a Claude slash command, a Codex skill, or a subagent prompt.

The rendered `--limit` is only a display limit. Owner inference must come from
the full prebuilt map, including code structure, package READMEs, and wiki pages
whose provenance is maintained by `wiki pages update`, `wiki pages ingest`, and
`plan reconcile`.

Owner profiles use package documentation and owner-specific wiki pages. Broad
wiki pages with multiple source roots are useful background, but they should not
be treated as proof that every referenced package owns the task.

## Pipeline

0. Verify the installed CLI has this workflow:

   ```bash
   indexion agent orient --help
   ```

   If this command is missing, update or rebuild indexion before continuing.
   Having an older `indexion` binary in PATH is not enough for this skill.

1. Generate the brief:

   ```bash
   indexion agent orient --task-file task.md --output=.indexion/cache/agent/orient.md .
   ```

   The first run writes `.indexion/cache/agent/orient-map.json`. Later runs
   refresh changed files and affected owner profiles only. Use `--no-update`
   when you intentionally want to query the saved map without refreshing it.
   This is the mode to use when a zero-knowledge agent needs an immediate
   owner guess from the latest prebuilt map.

   For short tasks:

   ```bash
   indexion agent orient --task "add a name/content drift audit" .
   ```

   If the user task is in a language or wording that does not appear in the
   repository's identifiers and README prose, keep the original task in your
   notes and pass a short codebase-vocabulary gloss to `--task`. The gloss
   should describe the objective, not the suspected owner. For example, say
   "detect drift between names and implementation contents" instead of naming a
   package you have not confirmed.

   Do not put supporting infrastructure constraints into the owner-inference
   `--task` gloss. Keep the original request, required tools, and implementation
   constraints in your notes or subagent prompt. The gloss is only the objective
   vocabulary used to query the prebuilt map, for example:

   ```bash
   indexion agent orient --no-update --task "name/content drift scoring and remediation planning" .
   ```

2. Read these sections before editing:

   - `Likely Implementation Owners`: core packages that should own domain
     behavior.
     Treat the first entry as the initial owner hypothesis unless follow-up
     evidence contradicts it.
   - `Knowledge Sources`: release notes, wiki pages, READMEs, or other
     documentation that matched the task. Use these as context; do not treat a
     documentation-only path as the place to implement domain behavior.
   - `Consumer Surfaces`: CLI, skills, docs, or adapters likely to call the core.
   - `Do Not Implement Here`: files to avoid as domain implementation targets.
   - `Required Preflight`: files the agent should read before patching.
   - `Orientation Map`: confirms the total file/owner/documentation corpus used
     before display truncation.

3. Confirm the owner with focused tools:

   ```bash
   indexion doc graph --format=text <likely-owner>
   indexion grep --semantic=name:<term> .
   indexion search "<task concept>" .
   ```

   Use the distinguishing terms from the brief and the user task, not only the
   broad infrastructure words. If search results drift toward supporting
   systems instead of the likely owner, refine the query with the name/content,
   drift, divergence, or domain-specific terms that actually define the task
   before changing the owner.

4. Gate implementation:

   - If the intended edit path appears in `Do Not Implement Here`, stop and
     explain the conflict.
   - If the intended owner is absent from `Likely Implementation Owners`, gather
     more evidence with `doc graph`, `grep`, `search`, or `explore`.
   - Keep CLI code thin unless the brief and follow-up evidence show it owns the
     behavior.

5. Use for zero-knowledge delegation:

   Give a subagent only the task and the generated orientation brief, then quiz
   it before assigning implementation work. It should immediately name the core
   implementation owner, one knowledge source, one unsafe edit location, and one
   preflight evidence path. Passing that quiz is the signal that the prebuilt map
   has transferred the right ownership assumptions.

## External Agent Mapping

- Claude Code: store stable guidance in `CLAUDE.md`, project commands in
  `.claude/commands/`, and project subagents in `.claude/agents/`.
- Codex: store stable guidance in AGENTS.md or skills, and paste the orientation
  brief into delegated task context.
- Multi-agent workflows: use the brief as the structured handoff payload so each
  isolated agent starts with the same repository-specific assumptions.
