## Description:

WenHub provides a three-court AI agent collaboration governance framework for task assignment, task grading, quality control, standardized reporting, knowledge reuse, security controls, and violation handling.

This skill is ready for commercial/non-commercial use.

## Publisher:

[18505298102](https://clawhub.ai/user/18505298102)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, team leads, and agent operators use this skill to structure multi-agent work into planning, execution, and independent quality review workflows. It is intended for teams that need repeatable governance rules, reporting templates, task grading, and security review practices for agent-assisted work.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may shape persistent workspace-level agent governance by asking users to add SOUL.md, AGENTS.md, IDENTITY.md, or .wenhub rule files.

Mitigation: Review the full contents of every proposed instruction or rule file, keep backups of existing instruction files, and install only changes that match the intended governance model.

Risk: The server security verdict is suspicious because the skill directs users toward remote templates for persistent agent instruction files.

Mitigation: Avoid installing mutable website templates unless the publisher provides versioned releases with hashes or signatures.

## Reference(s):

- [WenHub website](https://wenhub.huawen-inc.com)
- [WenHub ClawHub release](https://clawhub.ai/18505298102/skills/wenhub)
- [Three-court collaboration protocol](references/three-courts.md)
- [Task grading and execution controls](references/task-grading.md)
- [Quality scoring system](references/quality-system.md)
- [Reporting and communication standards](references/reporting.md)
- [Security rules](references/security-rules.md)
- [Violation handling system](references/violation-system.md)
- [Karpathy coding principles](references/karpathy-rules.md)

## Skill Output:

**Output Type(s):** [text, markdown, configuration, guidance]

**Output Format:** [Markdown guidance, structured checklists, reporting templates, and workspace governance configuration recommendations]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May recommend persistent workspace instruction files and governance rules that should be reviewed before installation.]

## Skill Version(s):

1.5.0 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
