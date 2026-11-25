## Description:

Writes a field service troubleshooting guide with ordered diagnostic steps, safety limits and escalation triggers for US technicians.

This skill is ready for commercial/non-commercial use.

## Publisher:

[rapidworker1](https://clawhub.ai/user/rapidworker1)

### License/Terms of Use:

MIT-0

## Use Case:

US field service managers, repair shop owners, and support leads use the skill to structure troubleshooting briefs with ordered checks, safety limits, and escalation points. The bundled script currently produces a brief-validation report rather than the troubleshooting guide described in the skill summary.

### Deployment Geography for Use:

United States

## Known Risks and Mitigations:

Risk: The security assessment flags a mismatch between the promised troubleshooting guide and the script's brief-validation report; it also says some references were unresolved, leaving evidence incomplete.

Mitigation: Confirm the intended output and tool scope with the publisher, then review the generated report before relying on it as a troubleshooting guide.

## Reference(s):

- [Troubleshooting US rules](artifact/references/troubleshooting-us-rules.md)
- [ClawHub skill release](https://clawhub.ai/rapidworker1/skills/troubleshooting-guide-writer)

## Skill Output:

**Output Type(s):** [Guidance, Markdown, Configuration]

**Output Format:** [YAML troubleshooting brief template and Markdown brief-validation report]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The bundled script checks field completeness and character limits; it does not generate the troubleshooting guide described by the skill summary.]

## Skill Version(s):

1.0.7 (source: artifact/SKILL.md frontmatter, release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
