## Description:

When users have long-form content ready to publish on Xiaohongshu, automatically completes the entire process: login detection, long content segmentation optimization, AI-generated images, content filling, AI-generated tags, tag activation, original content declaration, and publishing.

This skill is ready for commercial/non-commercial use.

## Publisher:

[openlark](https://clawhub.ai/user/openlark)

### License/Terms of Use:

MIT-0

## Use Case:

External creators and operators use this skill to prepare and publish existing long-form Xiaohongshu content through the creator platform. It helps segment long content, prepare a title and description, add tags, declare original content, and publish after login.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can publish public Xiaohongshu content under the user's logged-in account without a clear final approval step.

Mitigation: Require user review and explicit approval of the title, body, generated description, tags, images, original-content declaration, and final publish action before posting.

Risk: The skill operates through the user's logged-in Xiaohongshu creator session.

Mitigation: Install and run it only when the user is comfortable allowing an agent to use that session for public posting, and keep session access limited to the intended account.

Risk: Generated images and original-content declarations can create copyright, attribution, or authenticity risk if accepted without review.

Mitigation: Confirm image rights, content provenance, platform compliance, and original-content claims before allowing the publish step.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/openlark/skills/xiaohongshu-longpost-auto)
- [Xiaohongshu Creator Platform](https://creator.xiaohongshu.com/)
- [Xiaohongshu Publishing Page](https://creator.xiaohongshu.com/publish/publish)
- [Xiaohongshu Community Guidelines](https://www.xiaohongshu.com/community_guidelines)
- [Xiaohongshu Long-Form Post Guide](https://creator.xiaohongshu.com/help)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Guidance]

**Output Format:** [Markdown with browser automation steps and inline JavaScript snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs may include generated post descriptions, tags, formatting guidance, image guidance, and browser actions for a logged-in Xiaohongshu creator session.]

## Skill Version(s):

1.0.2 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
