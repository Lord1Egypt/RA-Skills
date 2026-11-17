## Description:

Generates Xiaohongshu-style post drafts with a title, body, hashtags, cover prompt, and posting strategy, with SkillPay billing before generation.

This skill is ready for commercial/non-commercial use.

## Publisher:

[arthuronai](https://clawhub.ai/user/arthuronai)

### License/Terms of Use:

MIT

## Use Case:

Content creators and marketers use this skill to draft Xiaohongshu post packages from a topic, including copy, hashtags, a cover prompt, and posting guidance.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Billing requests can be redirected to an arbitrary endpoint while carrying the SkillPay credential and part of the user topic.

Mitigation: Use only trusted installations, remove or strictly allowlist SKILLPAY_ENDPOINT to the official HTTPS SkillPay endpoint before use, and protect SKILLPAY_KEY.

Risk: The skill sends user topics to OpenAI, Datamuse, and SkillPay.

Mitigation: Do not submit sensitive topics unless those third-party transfers are acceptable for the deployment.

Risk: Dependencies are declared with version ranges and no lockfile is included.

Mitigation: Use pinned dependencies and a reviewed lockfile for production deployments.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/arthuronai/skills/xhs-viral-post)
- [ClawHub publisher profile](https://clawhub.ai/user/arthuronai)

## Skill Output:

**Output Type(s):** [text, guidance]

**Output Format:** [JSON object with title, content, hashtags, coverPrompt, and strategy fields.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires OPENAI_API_KEY and SKILLPAY_KEY; billing succeeds before generation; the topic is sent to external APIs.]

## Skill Version(s):

1.0.2 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
