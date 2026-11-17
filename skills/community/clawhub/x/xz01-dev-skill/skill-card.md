## Description:

Coordinates Hermes and Claude Code workflows for OpenClaw/xz01 template development, validation, role separation, read-only corpus handling, dual-end navigation and pagination checks, visual QA, and packaging gates.

This skill is ready for commercial/non-commercial use.

## Publisher:

[amd5](https://clawhub.ai/user/amd5)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators use this skill to coordinate xz01/OpenClaw template work with separated main, dev, test, and rule roles. It helps preserve read-only source boundaries while producing verified template changes, validation reports, shell commands, configuration guidance, and packaging handoffs.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Live-site deployment and runtime-clearing actions can affect production systems.

Mitigation: Require explicit confirmation gates before live deploys and runtime clears, and keep backups before replacing production theme files.

Risk: Automatic publishing can release skill changes without fresh approval.

Mitigation: Require a human approval gate before registry publishing and verify version, description, and changelog alignment before release.

Risk: Lanhu MCP usage depends on external Docker service setup and credentials.

Mitigation: Pin and review the Lanhu MCP dependency, protect credential files, and validate the service health before use.

Risk: Deletion or cleanup scripts could remove unintended files if paths are too broad.

Mitigation: Restrict deletion scripts to fixed allowlisted paths and review each destructive command before execution.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/amd5/skills/xz01-dev-skill)
- [xz01 Template Factory Architecture Notes](references/xz01-template-factory-architecture.md)
- [Hermes native xz01 live deployment and validation notes](references/hermes-native-xz01-live-deploy-validation.md)
- [Lanhu MCP installation for xz01 workflow](references/lanhu-mcp-installation.md)
- [xz01 dual-end list pagination rule](references/session-2026-05-18-dual-end-list-pagination.md)
- [Pagination data-volume validation correction](references/session-2026-05-18-pagination-data-volume-validation.md)
- [Dual-end top navigation dynamic menu rule](references/session-2026-05-18-dual-end-nav-dynamic-menu.md)
- [OpenClaw temporary artifact boundary](references/session-2026-05-18-openclaw-temp-artifact-boundary.md)
- [Full-page visual QA correction](references/session-2026-05-18-fullpage-visual-qa-correction.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance with inline code blocks, shell commands, checklists, and handoff notes]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include role-specific boundaries, validation gates, file path constraints, and packaging criteria.]

## Skill Version(s):

1.0.44 (source: SKILL.md frontmatter, artifact/skill.json, artifact/_meta.json, evidence release)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
