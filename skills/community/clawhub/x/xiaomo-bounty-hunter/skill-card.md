## Description:

Find legitimate GitHub bounties by filtering out farm/scam repositories, tracking competition, and monitoring payment history.

This skill is ready for commercial/non-commercial use.

## Publisher:

[xiaomomini](https://clawhub.ai/user/xiaomomini)

### License/Terms of Use:

MIT-0

## Use Case:

External developers use this skill to discover viable GitHub bounty opportunities, screen out likely farms or scams, compare competition, and check available payment-history signals before deciding whether to pursue an issue.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may use GitHub search tooling through an authenticated gh session to inspect public issues and repository activity.

Mitigation: Install only if that GitHub access posture is acceptable, and review proposed gh commands before execution.

Risk: Bounty legitimacy, competition, and payment history can be incomplete or outdated, especially for off-chain or token-based payments.

Mitigation: Verify issue status, maintainer activity, payment terms, and payment evidence directly before claiming or starting work.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/xiaomomini/skills/xiaomo-bounty-hunter)
- [Publisher Profile](https://clawhub.ai/user/xiaomomini)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with GitHub search queries and structured bounty summaries]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include repository and issue URLs, competition scores, payment-signal notes, filtered-count summaries, and suggested GitHub CLI search commands.]

## Skill Version(s):

1.0.0 (source: server release metadata and artifact metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
