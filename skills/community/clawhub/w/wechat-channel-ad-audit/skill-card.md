## Description:

Assesses WeChat Channel creators for advertising partnerships using recent posts and engagement data.

This skill is ready for commercial/non-commercial use.

## Publisher:

[dunkong](https://clawhub.ai/user/dunkong)

### License/Terms of Use:

MIT-0

## Use Case:

Marketing teams and advertisers use this skill to assess a WeChat Channel creator before a paid placement, comparing recent content, posting frequency, and engagement stability.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Creator and video identifiers are sent to a third-party API.

Mitigation: Use only when sharing those identifiers with api.we-media.cn is acceptable.

Risk: API requests may incur charges and require a local API key.

Mitigation: Keep the key out of chat and reports; review estimated costs before approving paid requests.

Risk: Reports and checkpoint files persist locally.

Mitigation: Choose output paths deliberately and manage saved files according to your retention needs.

## Reference(s):

- [ClawHub skill release](https://clawhub.ai/dunkong/skills/wechat-channel-ad-audit)
- [We-Media API guide](https://api.we-media.cn/client/ai-guide)
- [We-Media product documentation](https://api.we-media.cn/client/products)

## Skill Output:

**Output Type(s):** [Analysis, Guidance, Files]

**Output Format:** [Markdown summary and local JSON report; optional Excel export]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes supporting observations and actual API spending; results may be partial.]

## Skill Version(s):

1.4.2 (source: ClawHub release metadata and skill frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
