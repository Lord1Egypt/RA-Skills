## Description:

Audits Agent Casino fairness by guiding cryptographic bet verification, randomness testing, RTP checks, and audit report generation.

This skill is ready for commercial/non-commercial use.

## Publisher:

[rollhub-dev](https://clawhub.ai/user/rollhub-dev)

### License/Terms of Use:


## Use Case:

External auditors, developers, and casino integrity reviewers use this skill to verify individual Agent Casino bets, run statistical checks over sampled betting data, and assemble fairness audit reports.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill encourages live betting and account registration.

Mitigation: Do not run betting or registration commands unless the operator understands the legal, account, privacy, and financial implications.

Risk: Audit reports may overstate independent verification.

Mitigation: Treat generated reports as weak evidence until each bet is independently verified from the raw commitment, server seed, client seed, nonce, and result data.

Risk: The artifact includes an exposed ClawHub publishing token.

Mitigation: Revoke the exposed token and remove it from artifacts and publication history before release.

## Reference(s):

- [Fairness Auditor Skill Page](https://clawhub.ai/rollhub-dev/skills/rollhub-auditor)
- [Agent Casino API](https://agent.rollhub.com/api/v1)
- [Cryptographic Verification](references/crypto-verification.md)
- [Statistical Tests for Fairness Auditing](references/statistical-tests.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell commands, code snippets, API examples, and generated text reports]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires an AGENT_CASINO_API_KEY for live API commands and may write local audit data and report files.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
