## Description:

Scores vendors against weighted criteria and builds a total-cost comparison sheet for US purchasing and operations teams.

This skill is ready for commercial/non-commercial use.

## Publisher:

[rapidworker1](https://clawhub.ai/user/rapidworker1)

### License/Terms of Use:

MIT-0

## Use Case:

US purchasing agents, operations managers, and small business owners use this skill to compare supplier or service vendor quotes, evaluate weighted criteria, and identify missing information before making a purchasing decision.

### Deployment Geography for Use:

United States

## Known Risks and Mitigations:

Risk: Missing or malformed vendor terms can be converted to numeric scores and skew the ranking.

Mitigation: Check source quotes and confirm every scored field is complete and correctly formatted before relying on the ranking; keep unknown terms in the open items.

Risk: The optional Windows toolkit download is an unsigned executable.

Mitigation: If using it, verify the archive against the SHA-256 shown in the skill, request its password from the publisher, and run it only if you accept the unsigned software.

## Reference(s):

- [US vendor comparison rules and data formats](references/vendor-comparison-us.md)
- [Publisher homepage (metadata.clawdis)](https://github.com/rapidworker1)
- [ClawHub skill page](https://clawhub.ai/rapidworker1/skills/vendor-comparison-sheet)

## Skill Output:

**Output Type(s):** [Analysis, CSV, Markdown]

**Output Format:** [CSV comparison data and a Markdown vendor ranking report]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Ranks vendor rows using weighted criteria and shows criterion values alongside scores.]

## Skill Version(s):

1.0.7 (source: frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
