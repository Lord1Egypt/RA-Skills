## Description:

Sui Sec helps agents dry-run Sui CLI transaction commands and compare simulation results against user intent before signing or execution.

This skill is ready for commercial/non-commercial use.

## Publisher:

[k66inthesky](https://clawhub.ai/user/k66inthesky)

### License/Terms of Use:

MIT

## Use Case:

Developers and external users working with Sui transactions use this skill to collect transaction intent, run Sui dry-runs, and review whether simulated effects match the requested action. Security evidence indicates it should be treated as a limited dry-run helper, not an authoritative transaction approval gate.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Unsafe transactions could be labeled safe because security evidence says the broad protection claims are backed by only a narrow spending check.

Mitigation: Use the skill only as a dry-run helper and independently review recipients, asset movements, object ownership changes, call targets, and simulation output before signing.

Risk: Automated support is limited, and some Sui command paths require manual comparison against user intent.

Mitigation: For unsupported or manual paths, perform item-by-item intent comparison and avoid automatic execution based solely on the skill output.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/k66inthesky/skills/suisec)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Markdown guidance with inline shell commands and review tables]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires the local sui CLI and python3; automated findings should be reviewed before signing or executing transactions.]

## Skill Version(s):

1.0.1 (source: server release metadata; artifact/package.json reports 1.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
