## Description:

Generate WeChat comic articles and publish them to the WeChat Official Account draft box by executing local Python pipeline scripts.

This skill is ready for commercial/non-commercial use.

## Publisher:

[archibald80000-ai](https://clawhub.ai/user/archibald80000-ai)

### License/Terms of Use:

MIT-0

## Use Case:

External creators and operators use this skill to generate a short WeChat comic article series from a comic type, topic, and count, then optionally create a draft in the WeChat Official Account draft box.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can create real WeChat Official Account draft entries when credentials are configured.

Mitigation: Use a test account first, review generated HTML and article assets before publishing, and only run publish commands for explicitly intended tasks.

Risk: Model-provider credentials, WeChat credentials, and cached WeChat access tokens are sensitive.

Mitigation: Keep config.json, output files, logs, publish_result.json, and logs/wechat_access_token.json out of release packages and delete or protect local token caches after use.

Risk: Publishing from untrusted task directories or remote image URLs can introduce unsuitable or unexpected content.

Mitigation: Avoid publishing from untrusted task directories and inspect generated HTML, images, and draft metadata before creating a WeChat draft.

Risk: Generated articles include default publisher branding unless the operator changes the configuration.

Mitigation: Review and update defaults.publisher_name and defaults.publisher_tagline before production use.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/archibald80000-ai/skills/wechat-comic-factory)
- [Publisher profile](https://clawhub.ai/user/archibald80000-ai)
- [WeChat Official Account API endpoint](https://api.weixin.qq.com)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Files]

**Output Format:** [JSON status output with generated Markdown/HTML article assets and WeChat draft metadata.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Creates local task outputs and can create WeChat Official Account draft entries when valid provider and WeChat credentials are configured.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
