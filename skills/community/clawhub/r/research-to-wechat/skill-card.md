## Description:

Turns topics, notes, articles, URLs, or transcripts into sourced WeChat-ready articles with research notes, Markdown, HTML, visuals, and optional draft delivery or cross-platform copies.

This skill is ready for commercial/non-commercial use.

## Publisher:

[clarezoe](https://clawhub.ai/user/clarezoe)

### License/Terms of Use:

MIT

## Use Case:

Writers, creators, and content teams use this skill to research source material, draft WeChat articles, prepare images and HTML, and optionally save drafts or adapt copy for other platforms.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Manual installation can execute a downloaded shell script.

Mitigation: Install through ClawHub instead of using the curl-to-bash command.

Risk: Networked draft saves, image uploads, rewrite review, and cross-platform delivery may expose article material or use account credentials beyond the intended scope.

Mitigation: Confirm the exact text, source material, images, credentials, and destination platforms before enabling these steps; review drafts before delivery.

Risk: Author configuration can append promotional calls to action to drafts.

Mitigation: Review or disable EXTEND.md CTA settings if promotional content is unwanted.

## Reference(s):

- [ClawHub skill release](https://clawhub.ai/clarezoe/skills/research-to-wechat)
- [Declared project homepage](https://github.com/Fei2-Labs/skill-genie)
- [Execution contract](references/execution-contract.md)
- [WeChat delivery compatibility](references/wechat-compat.md)

## Skill Output:

**Output Type(s):** [Markdown, HTML, JSON, Images]

**Output Format:** [Article and research files, WeChat-ready HTML, manifest JSON, and cover and inline image assets]

**Output Parameters:** [One article workspace per run]

**Other Properties Related to Output:** [Optional WeChat draft save and platform-specific copy; draft delivery requires account credentials and read-back verification.]

## Skill Version(s):

0.7.2 (source: release metadata, skill frontmatter, CHANGELOG)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
