## Description:

xt-webnovel-writing helps agents plan, draft, revise, diagnose, and persist Chinese webnovel projects through routed workflows for text analysis, story blueprinting, plot design, prose improvement, quality checks, and memory.

This skill is ready for commercial/non-commercial use.

## Publisher:

[xiaotiewinner](https://clawhub.ai/user/xiaotiewinner)

### License/Terms of Use:

MIT-0

## Use Case:

External writers and agent users use this skill to create and manage Chinese webnovel projects, including ideation, outlines, character work, chapter drafting, style revision, anti-AI-tell diagnostics, and continuity memory.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Project mode can create and update a broad local project tree.

Mitigation: Choose an explicit project_root before use and review every planned write or delete path before allowing persistence.

Risk: Weak path-containment guidance could allow unsafe paths when names, slugs, or index data are untrusted.

Mitigation: Use trusted project names and slugs, sanitize path-like inputs, and confirm writes stay under project_root and the documented subdirectories.

Risk: Strict global rules may affect unrelated agent sessions if copied broadly.

Mitigation: Apply the two-phase and persistence rules only to intended workspaces or projects unless broad behavior changes are desired.

## Reference(s):

- [ClawHub release page](https://clawhub.ai/xiaotiewinner/skills/xt-webnovel-writing)
- [Publisher profile](https://clawhub.ai/user/xiaotiewinner)
- [README](README.md)
- [Anti-AI-tell rules](references/anti-ai-tells.md)
- [OpenClaw two-phase enforcement](references/openclaw-enforcement-two-phase.md)
- [OpenClaw hook setup](references/openclaw-hooks-setup.md)
- [Webnovel memory directory schema](webnovel-memory/references/directory-schema.md)
- [Webnovel memory write protocol](webnovel-memory/references/write-protocol.md)
- [Webnovel writing manual source](https://zhuanlan.zhihu.com/p/467588933)
- [AgentSkills compatibility](https://agentskills.io)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Chinese Markdown with tables, code blocks, structured project files, and optional shell commands.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Project mode may create or update files under a user-selected project_root after verification; one-off writing can skip persistence when requested.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
