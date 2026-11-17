## Description:

Search people and companies, inspect contact intelligence, and review company signals in RocketReach - funding, growth, size, and tech stack.

This skill is ready for commercial/non-commercial use.

## Publisher:

[hith3sh](https://clawhub.ai/user/hith3sh)

### License/Terms of Use:

MIT-0

## Use Case:

External users, sales teams, recruiters, and business researchers use this skill to look up decision-maker contact information, research company profiles, and build prospect lists through RocketReach via ClawLink.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill depends on a third-party ClawLink plugin and hosted credential flow.

Mitigation: Confirm trust in the ClawLink plugin and hosted credential flow before installation or account connection.

Risk: RocketReach lookups can reveal personal contact data.

Mitigation: Confirm each lookup target with the user and avoid storing or logging personal data without explicit consent.

Risk: RocketReach lookups can consume account credits, especially during bulk searches.

Mitigation: Check account context and confirm before running bulk or credit-consuming lookups.

## Reference(s):

- [RocketReach API](https://rocketreach.co/api)
- [ClawLink Docs](https://docs.claw-link.dev/openclaw)
- [ClawLink Verification](https://claw-link.dev/verify)
- [ClawHub Skill Page](https://clawhub.ai/hith3sh/skills/rocketreach-contact-intel)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown with inline shell commands and JSON tool-call examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses ClawLink-authenticated RocketReach read operations; lookup results may include personal contact data and account-credit consumption.]

## Skill Version(s):

1.0.5 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
