## Description:

Rule Spec helps agents define, manage, and compile business rules as structured YAML data into LLM-ready prompts and agent-loadable SKILL.md files.

This skill is ready for commercial/non-commercial use.

## Publisher:

[pallaoro](https://clawhub.ai/user/pallaoro)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators use this skill to create, validate, update, and compile operational business rules, policies, guardrails, escalation rules, SLA requirements, and similar constraints for AI agents.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill uses an unpinned npm CLI through npx, so command behavior may change if the package changes.

Mitigation: Pin an exact reviewed rulespec package version before use and install only if the package and publisher are trusted.

Risk: Business rules and examples may contain sensitive operational or compliance information.

Mitigation: Run the skill in a least-privileged workspace and avoid sending sensitive rules or examples to untrusted model providers.

## Reference(s):

- [Rule Spec on ClawHub](https://clawhub.ai/pallaoro/skills/rulespec)
- [Clawnify](https://www.clawnify.com)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, Configuration, Markdown, Code]

**Output Format:** [Markdown guidance with shell, YAML, and TypeScript examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May help produce rulespec.yaml configuration and generated SKILL.md files; examples are excluded from emitted skill files by default unless requested.]

## Skill Version(s):

1.0.7 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
