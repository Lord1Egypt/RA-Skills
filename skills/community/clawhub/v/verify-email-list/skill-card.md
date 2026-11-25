## Description:

Verifies email addresses in a list using Cargo's workspace Verify email tool, with Waterfall as a fallback.

This skill is ready for commercial/non-commercial use.

## Publisher:

[cargo-ai](https://clawhub.ai/user/cargo-ai)

### License/Terms of Use:

MIT-0

## Use Case:

Marketing, sales development, and revenue operations teams use this skill to check email list deliverability before sending. It returns per-address status and safety information to help identify addresses that need review.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: ClawScan marks the skill suspicious because scanners report actions beyond email verification, including installing an unpinned skill collection and changing GitHub account state; scan coverage is partial.

Mitigation: Review those instructions and remove or clearly justify them before use; only run installation or GitHub account actions when intended and approved.

Risk: The security guidance says the skill does not explain when email addresses are sent to external providers.

Mitigation: Clarify the data flow and obtain appropriate approval before sending an email list to a verification provider.

## Reference(s):

- [ClawHub release](https://clawhub.ai/cargo-ai/skills/verify-email-list)
- [Cargo GTM skills project](https://github.com/getcargohq/gtm-skills)
- [Outreach activation recipe](https://github.com/getcargohq/cargo-skills/blob/main/cargo-gtm/recipes/outreach-activation.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Guidance]

**Output Format:** [Markdown with per-address deliverability results and shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes email status and a safety flag for each address, plus a summary of counts and estimated credit cost.]

## Skill Version(s):

1.1.0 (source: frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
