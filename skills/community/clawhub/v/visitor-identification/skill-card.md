## Description:

Helps teams identify companies visiting their website and the pages they view using consent-gated Snitcher tracking and Cargo models.

This skill is ready for commercial/non-commercial use.

## Publisher:

[cargo-ai](https://clawhub.ai/user/cargo-ai)

### License/Terms of Use:

MIT-0

## Use Case:

Marketing, sales development, and engineering teams use this skill to add consent-gated, company-level website visitor identification and review company visits and page activity in Cargo. It does not identify named individuals.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Visitor tracking may conflict with privacy expectations or organizational requirements.

Mitigation: Confirm permission to use Cargo and Snitcher, publish a reviewed privacy disclosure, and verify the tracker loads only after visitor consent.

Risk: Identified companies incur per-company charges that rise with traffic.

Mitigation: Check the live per-company price and available credits, then obtain explicit approval before deployment.

## Reference(s):

- [ClawHub skill listing](https://clawhub.ai/cargo-ai/skills/visitor-identification)
- [Cargo skills homepage (listed in release metadata)](https://github.com/getcargohq/gtm-skills)
- [Consent and site setup](artifact/references/consent.md)
- [Visitor data and limitations](artifact/references/data.md)
- [Snitcher cookie consent documentation](https://docs.snitcher.com/product/tracker/cookie-consent)

## Skill Output:

**Output Type(s):** [Guidance, Code, Shell commands, Configuration instructions]

**Output Format:** [Markdown with code and shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Adapted site consent gate and Cargo visitor models require operator review before deployment.]

## Skill Version(s):

0.1.2 (source: release metadata and skill frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
