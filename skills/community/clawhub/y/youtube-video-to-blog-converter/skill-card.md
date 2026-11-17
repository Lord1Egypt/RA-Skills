## Description:

Converts YouTube transcripts into structured Markdown blog drafts, with reserved premium upgrade hooks for SEO optimization and multi-platform publishing formats.

This skill is ready for commercial/non-commercial use.

## Publisher:

[wingogx](https://clawhub.ai/user/wingogx)

### License/Terms of Use:


## Use Case:

External users and developers use this skill to turn a YouTube video title, transcript, and optional video URL into a structured blog draft. It supports a free blog-draft workflow while indicating that premium SEO, image suggestion, and multi-platform output features are reserved.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The release evidence flags under-disclosed payment and billing behavior in a transcript converter.

Mitigation: Review payment prompts and billing artifacts before installation, and do not allow the skill to initiate charges automatically.

Risk: Payment URL configuration may direct users to untrusted destinations if configured carelessly.

Mitigation: Restrict payment URL configuration to trusted HTTPS hosts and encoded parameters.

Risk: Users needing non-Chinese output may not get the expected language coverage.

Mitigation: Confirm language support before using the skill in workflows that require output outside the demonstrated Chinese draft format.

## Reference(s):

- [SkillPay API Contract](references/skillpay-api-contract.md)
- [ClawHub Skill Page](https://clawhub.ai/wingogx/skills/youtube-video-to-blog-converter)

## Skill Output:

**Output Type(s):** [markdown, code, shell commands, configuration, guidance]

**Output Format:** [JSON containing a Markdown blog draft and upgrade metadata]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires user_id, video_title, and transcript inputs; video_url and tier are optional.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
