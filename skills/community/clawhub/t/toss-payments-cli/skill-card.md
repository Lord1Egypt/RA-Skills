## Description:

Command-line skill for retrieving Toss Payments payment details and performing full or partial payment cancellations with payment keys.

This skill is ready for commercial/non-commercial use.

## Publisher:

[chloepark85](https://clawhub.ai/user/chloepark85)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators use this skill to run Toss Payments API workflows from a command line, including payment lookup and full or partial cancellation. It is intended for environments where the operator is authorized to use a Toss Payments secret key.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill requires a Toss Payments secret key, which can authorize real payment operations if exposed or misused.

Mitigation: Keep TOSS_SECRET_KEY private, use least-privileged operational environments, and avoid sharing command output or shell history that may contain secrets.

Risk: Cancel-payment commands can trigger real full or partial payment cancellations.

Mitigation: Confirm the payment key, cancellation reason, amount, and target environment before running cancellation commands.

Risk: An incorrect TOSS_BASE_URL could send payment requests to an unintended endpoint.

Mitigation: Verify that TOSS_BASE_URL points to the legitimate Toss Payments API before use, or leave it unset to use the documented default.

## Reference(s):

- [Toss Payments Core API](https://docs.tosspayments.com/reference#tag/Payments)
- [ClawHub Skill Page](https://clawhub.ai/chloepark85/skills/toss-payments-cli)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [None]

## Skill Version(s):

0.1.0 (source: server release metadata and artifact frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
