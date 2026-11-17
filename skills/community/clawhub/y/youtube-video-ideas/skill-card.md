## Description:

AI-powered YouTube video ideas generator. Generate viral video concepts, titles, and hooks.

This skill is ready for commercial/non-commercial use.

## Publisher:

[icepopma](https://clawhub.ai/user/icepopma)

### License/Terms of Use:

MIT

## Use Case:

External creators and content teams use this skill to generate YouTube video concepts, titles, hooks, SEO keywords, and optional content outlines for a supplied topic.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill performs paid billing by default through SkillPay.

Mitigation: Review the billing flow and price before normal use, and use test mode when validating behavior.

Risk: The package contains a public fallback merchant key.

Mitigation: Confirm the payment destination before use and set a controlled SKILLPAY_MERCHANT_KEY for deployments.

Risk: The security review reports supply-chain weaknesses.

Mitigation: Review the package manifest and lockfile before installation, and install only in controlled environments.

Risk: The skill sends the supplied topic text to a local OpenClaw agent.

Mitigation: Avoid entering sensitive topics unless the local agent configuration and data handling are acceptable.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/icepopma/skills/youtube-video-ideas)
- [Source Repository](https://github.com/icepopma/youtube-video-ideas)
- [Publisher Profile](https://clawhub.ai/user/icepopma)

## Skill Output:

**Output Type(s):** [text, markdown, guidance]

**Output Format:** [Markdown-like text printed to stdout]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs five video ideas and may include brief outlines when requested.]

## Skill Version(s):

1.1.2 (source: server release metadata and package.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
