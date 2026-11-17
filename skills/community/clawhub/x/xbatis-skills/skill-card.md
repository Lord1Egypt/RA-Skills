## Description:

Guides agents working in xbatis-based Java projects to implement, refactor, review, and troubleshoot ORM, mapper, QueryChain, VO mapping, pagination, multi-tenancy, logic delete, optimistic locking, SQL template, and XML fallback decisions.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ai-010](https://clawhub.ai/user/ai-010)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to make agents follow xbatis-native patterns when generating, modifying, or reviewing Java persistence code for Spring Boot, Solon, and related xbatis projects.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill directs agents to use live xbatis GitHub or Gitee sources during xbatis tasks, which can introduce supply-chain drift or unreviewed code into generated guidance.

Mitigation: Require confirmation before repository downloads and prefer pinned releases or user-provided local source snapshots.

Risk: Setup examples include weak database credentials.

Mitigation: Replace sample credentials with environment variables or a dedicated least-privileged local account before generating project configuration.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/ai-010/skills/xbatis-skills)
- [Server-resolved Source Repository](https://github.com/xbatis/xbatis-skills)
- [Xbatis Framework Repository](https://github.com/xbatis/xbatis)
- [Xbatis Spring Boot Starter Repository](https://github.com/xbatis/xbatis-spring-boot-parent)
- [Xbatis Solon Plugin Repository](https://github.com/xbatis/xbatis-solon-plugin)
- [Environment Setup](references/environment-setup.md)
- [Query Strategy](references/query-strategy.md)
- [Mapper Modes](references/mapper-modes.md)
- [Framework Features](references/framework-features.md)
- [Advanced SQL Decision](references/advanced-sql.md)
- [XML Boundaries](references/xml-boundaries.md)
- [Review Checklist](references/review-checklist.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown with inline code blocks and configuration snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs should prefer actionable xbatis-native implementation guidance and flag unverified APIs or package names for project confirmation.]

## Skill Version(s):

0.1.0 (source: ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
