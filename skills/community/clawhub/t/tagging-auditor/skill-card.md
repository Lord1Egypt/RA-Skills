## Description:

Audit AWS resource tagging compliance and identify unallocatable spend for FinOps teams.

This skill is ready for commercial/non-commercial use.

## Publisher:

[anmolnagpal](https://clawhub.ai/user/anmolnagpal)

### License/Terms of Use:


## Use Case:

FinOps teams and cloud engineers use this skill to review user-provided AWS resource and cost exports, score tag compliance, identify unallocatable spend, and draft remediation guidance.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: AWS cost and resource exports can reveal internal infrastructure, resource inventory, and spend patterns.

Mitigation: Use sanitized exports where appropriate and avoid sharing credentials, access keys, secret keys, or unnecessary sensitive account details.

Risk: Generated AWS Config rules, SCP snippets, and remediation commands could affect account governance if applied without review.

Mitigation: Review generated rules, policies, and commands with the responsible cloud or security owner before applying them in an AWS account.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/anmolnagpal/skills/tagging-auditor)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown report with tables, JSON snippets, policy snippets, and shell command blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Analyzes user-provided AWS exports and descriptions; does not access AWS accounts directly.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
