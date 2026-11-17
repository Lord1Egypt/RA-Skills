## Description:

Use the Context Hub chub CLI to fetch current third-party SDK, API, and cloud-service documentation before writing, modifying, or reviewing integration code.

This skill is ready for commercial/non-commercial use.

## Publisher:

[kshern](https://clawhub.ai/user/kshern)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to look up current third-party SDK, API, and cloud-service documentation with the chub CLI before implementing, modifying, troubleshooting, or reviewing integration code.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The agent may use the chub CLI for documentation lookups and occasional local annotations.

Mitigation: Confirm that CLI-based documentation lookup and local annotation behavior are acceptable before installing or using the skill.

Risk: The skill includes a feedback command that can send documentation feedback externally when approved.

Mitigation: Avoid approving chub feedback submissions unless external feedback is intended.

## Reference(s):


## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline shell commands and code examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include CLI lookup commands, fetched documentation summaries, implementation guidance, and local annotation guidance.]

## Skill Version(s):

1.0.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
