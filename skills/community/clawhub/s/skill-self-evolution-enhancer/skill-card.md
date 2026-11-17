## Description:

Enables an agent to add self-evolution scaffolding to other skills, including domain-specific learnings, error logs, feature requests, evolution rules, and a Review-Apply-Report workflow.

This skill is ready for commercial/non-commercial use.

## Publisher:

[zhaobudaoyuema](https://clawhub.ai/user/zhaobudaoyuema)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and skill maintainers use this skill to add persistent learning workflows to an existing skill. It analyzes a target skill, drafts domain-specific learning and error structures, and produces evolution guidance tailored to the target skill's language and use case.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill introduces persistent self-modifying behavior into other skills.

Mitigation: Use a dry run first, back up the target skill, and review every generated file before deployment.

Risk: Learning logs may accidentally retain secrets, raw user data, or sensitive corrections.

Mitigation: Avoid storing secrets or raw user data in .learnings and redact sensitive details before keeping entries.

Risk: Promoting learnings into durable rules can make incorrect or misleading guidance persist across future tasks.

Mitigation: Require explicit approval before promoting learnings into rules and periodically review superseded or contradicted entries.

## Reference(s):

- [Skill workflow](SKILL.md)
- [README](README.md)
- [Domain examples](references/domain-examples.md)
- [OpenClaw feedback integration](references/openclaw-feedback.md)
- [ClawHub release page](https://clawhub.ai/zhaobudaoyuema/skills/skill-self-evolution-enhancer)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance, generated Markdown files, and optional shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May create .learnings/ logs, EVOLUTION.md, and domain configuration drafts in a target skill after review.]

## Skill Version(s):

1.0.0 (source: server release metadata and artifact _meta.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
