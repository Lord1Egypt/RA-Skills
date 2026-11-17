## Description:

Shared memory governance for multi-agent OpenClaw workspaces with tiered memory, learnings capture, promotion review, lifecycle management, self-maintaining reports, cross-skill collaboration, and bilingual ClawHub-friendly docs.

This skill is ready for commercial/non-commercial use.

## Publisher:

[zqh2333](https://clawhub.ai/user/zqh2333)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent operators use this skill to govern shared workspace memory across long-running OpenClaw sessions, including learnings capture, promotion review, health checks, maintenance reports, and cross-skill collaboration.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can create persistent scheduled OpenClaw jobs with read and command-execution access.

Mitigation: Use only in a trusted workspace and inspect, modify, or disable scheduled jobs after setup.

Risk: The skill includes guidance around a private secrets memory file.

Mitigation: Do not store real credentials in memory/private-secrets.md; use an approved secret manager for live credentials.

Risk: Some bundled scripts use a hardcoded workspace path and default schedule timezone.

Mitigation: Change the workspace path and timezone before running the scripts outside the original environment.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/zqh2333/skills/shared-memory-os)
- [Governance Guide](references/governance-guide.md)
- [Pattern Harvesting](references/pattern-harvesting.md)
- [Archive Strategy](references/archive-strategy.md)
- [Learnings Entry Template](references/learnings-template.md)
- [Health Check Guide](references/health-check.md)
- [Self-Improving Loop](references/self-improving-loop.md)
- [Health Score Model](references/health-score-model.md)
- [Migration Guide](references/migration-guide.md)
- [Policy Profiles](references/policy-profiles.md)
- [Workspace Profiles](references/workspace-profiles.md)
- [Cross-Skill Collaboration](references/cross-skill-collaboration.md)
- [Multi-Agent Governance](references/multi-agent-governance.md)
- [Periodic Memory Maintenance Day](references/maintenance-day.md)
- [Chinese Guide](references/zh-cn-guide.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell commands, JavaScript script entrypoints, and generated Markdown or JSON report files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May create or update workspace memory files, scheduled maintenance jobs, and shared-memory reports when its scripts are run.]

## Skill Version(s):

1.7.2 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
