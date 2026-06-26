---
name: skill-port
description: Audit and port AI agent skills, Claude Code skills/plugins, Codex skills/plugins, Gemini CLI skills/extensions, slash commands, agents, hooks, policies, MCP-backed plugins, and similar skill repositories across target agents. Use when asked to assess portability, generate a compatibility/security report, stage a port under target-agent naming, or adapt agent-specific skills/plugins for another runtime.
license: Apache-2.0
metadata:
  author: Yaniv Daniel
  homepage: https://github.com/yand/skill-port
---

# Skill Port

Use this skill to audit or port agent skills and plugin ecosystems. It supports Claude Code, Codex, Gemini CLI, and Agent Skills-compatible sources and targets through an adapter-based workflow.

## Operating Modes

- **audit-only**: inspect the source and produce a deterministic compatibility/security report. Do not create ported files.
- **port**: inspect the source, stage target-agent files, and produce the same report.
- **case-study**: analyze a large ecosystem and recommend what to port, split, ignore, or keep as dependency notes.

Default to `audit-only` when the user's request is unclear or security-sensitive. In audit-only mode, be decisive: recommend a concrete port scope, target layout, command mapping plan, and next port command without creating files.

## Safety Rules

- Do not install a source skill/plugin as part of auditing or porting.
- Do not run source scripts, package managers, install lifecycle hooks, or plugin commands unless the user explicitly asks after reviewing the audit.
- Do not write into global or project agent install directories unless the user explicitly asks.
- Stage output under target-agent naming:
  - Single skill: `skills/<target-agent>/<skill-name>/`
  - Multi-skill/plugin source: `ports/<source-name>/<target-agent>/`
- Treat installation as a separate final step using the target agent's normal installer.
- Preserve warnings, legal disclaimers, human-review requirements, and safety limits from the source.

## Workflow

1. **Identify source and target**
   - Determine source path or URL, source agent/ecosystem, target agent, and requested mode.
   - If the target agent is not specified, infer it from the active runtime. When running in Codex, use `codex`.
   - For remote URLs, clone/fetch only after user approval or explicit execution request; otherwise document the needed command.
   - For expensive scans, ask the user to run focused commands and share output.

2. **Run inventory**
   - Prefer `scripts/audit_skill.py` for deterministic local inspection.
   - If the source is large, run it on the narrowest useful directory first.
   - Read source-specific references only as needed:
     - Portability model: `references/portability-model.md`
     - Claude sources: `references/source-claude.md`
     - Codex sources: `references/source-codex.md`
     - Gemini sources: `references/source-gemini.md`
     - Codex targets: `references/target-codex.md`
     - Claude targets: `references/target-claude.md`
     - Gemini targets: `references/target-gemini.md`
     - Large ecosystems: `references/ecosystem-porting.md`
     - Location policy: `references/locations.md`
     - Security review: `references/security.md`

3. **Classify artifacts**
   - First classify by layer: project instructions, skills, commands, agents, plugins, MCP/tools, hooks, assets/scripts.
   - Portable: agent-neutral `SKILL.md`, references, examples, assets, templates.
   - Needs adaptation: slash commands, agent prompts, Claude wording, target-specific frontmatter.
   - Dependency-bound: MCP configs, external APIs, subscriptions, app connectors, credentials.
   - Unsupported: lifecycle hooks, automatic plugin installation, Cowork dispatch, managed-agent orchestration, policy engines, and target-specific extension behavior unless a target equivalent is available.
   - Mark each mapped item as `direct`, `translated`, `partial`, `unsupported`, or `manual`.

4. **Port only when requested**
   - Create target-agent skill folders in the staging location.
   - Rewrite frontmatter for the target agent.
   - Convert slash-command intent into trigger text or workflow sections.
   - Create dependency and unsupported-feature notes for MCPs, provider credentials, app connectors, lifecycle hooks, and orchestration behavior.
   - Keep unsupported features in dependency notes or a compatibility report; do not pretend they work.

5. **Report**
   - Follow `references/report-schema.md`.
   - Include target compatibility, recommended scope, proposed target layout, auto-port candidates, dependency-bound items, unsupported items, security findings, output paths, install commands, and remaining manual steps.

## Useful Commands

```bash
python3 scripts/audit_skill.py <source-path> --target-agent codex
python3 scripts/audit_skill.py <source-path> --target-agent codex --format markdown
python3 scripts/audit_skill.py <source-path> --target-agent claude --format markdown
python3 scripts/audit_skill.py <source-path> --target-agent gemini --format markdown
python3 scripts/audit_skill.py <source-path> --target-agent codex --output report.json
```

## Output Standard

For every audit or port, state:

- Source inspected and target agent.
- Whether files were created and where.
- Compatibility summary.
- Layer summary and conversion status summary.
- Recommended scope and proposed target layout.
- Automatic work that can be done in port mode.
- Security findings that affect installation or trust.
- Manual setup still required, limited to credentials, MCP servers, app connectors, provisioning, regulated human review, or target-agent installation.
