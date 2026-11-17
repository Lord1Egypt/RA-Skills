## Description:

AI-powered Twitter/X content generator for tweets, threads, and content strategies using the Sloan agent.

This skill is ready for commercial/non-commercial use.

## Publisher:

[icepopma](https://clawhub.ai/user/icepopma)

### License/Terms of Use:

MIT

## Use Case:

Content creators, marketers, and social media managers use this skill to generate tweets, multi-post threads, and short content strategies with configurable style, tone, hashtags, and emojis.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security evidence says the skill automatically contacts a payment service before generating content.

Mitigation: Require explicit user configuration and confirmation for paid charges, and use test mode before any paid run.

Risk: The security evidence reports an embedded merchant credential and recommends review before install.

Mitigation: Remove and rotate the embedded credential, require SKILLPAY_MERCHANT_KEY to be provided by the user, and review the payment flow before deployment.

Risk: The security guidance flags package version misalignment and non-HTTPS registry sources.

Mitigation: Align package, lockfile, and release versions, then regenerate dependency metadata from HTTPS registry sources before treating the release as low risk.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/icepopma/skills/twitter-content-generator)
- [SkillPay](https://skillpay.me)
- [Artifact-declared GitHub Support Link](https://github.com/icepopma/twitter-content-generator)

## Skill Output:

**Output Type(s):** [text, markdown, guidance]

**Output Format:** [CLI text containing generated tweet, thread, or content strategy content plus run metadata.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Normal runs process a 0.002 USDT payment before generation; test mode skips payment.]

## Skill Version(s):

1.0.9 (source: server release and SKILL.md frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
