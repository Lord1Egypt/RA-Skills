## Description:

Helps U.S. field-service teams draft safety-conscious troubleshooting guides with ordered checks, escalation triggers, parts limits, and repair-claim review.

This skill is ready for commercial/non-commercial use.

## Publisher:

[rapidworker1](https://clawhub.ai/user/rapidworker1)

### License/Terms of Use:

MIT-0

## Use Case:

Field-service managers, repair-shop owners, and support leads use this agent to prepare technician-facing troubleshooting guides from a unit model, symptoms, fault codes, and governing manuals. A qualified reviewer should verify each guide against the manufacturer's manual and approved service bulletins before use.

### Deployment Geography for Use:

United States

## Known Risks and Mitigations:

Risk: The helper's input-validation report could be mistaken for a completed service guide, or an unverified draft could contain unsafe or inaccurate instructions.

Mitigation: Treat the helper output as a completeness and length report, and have a qualified reviewer verify any service guide against the manufacturer's manual and approved service bulletins before use.

## Reference(s):

- [U.S. repair, safety, and warranty rules](references/troubleshooting-us-rules.md)
- [ClawHub skill release](https://clawhub.ai/rapidworker1/skills/troubleshooting-guide-writer)
- [Publisher homepage](https://github.com/rapidworker1)

## Skill Output:

**Output Type(s):** [Text, Markdown, Configuration]

**Output Format:** [Technician-facing troubleshooting-guide content, a YAML guide template, and a Markdown input-validation report.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Organizes fault paths, ordered checks, safety limits, escalation triggers, parts, and claim flags. The included helper reports field completeness and length; it does not generate the troubleshooting guide.]

## Skill Version(s):

1.0.6 (source: frontmatter, server release)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
