## Description:

Publish notes (posts) to Xiaohongshu via the Creator Platform using browser automation with CDP.

This skill is ready for commercial/non-commercial use.

## Publisher:

[waao666](https://clawhub.ai/user/waao666)

### License/Terms of Use:


## Use Case:

External creators and agents use this skill to prepare and publish Xiaohongshu notes with images through an already logged-in Creator Platform browser session.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can publish to a real Xiaohongshu account from an already logged-in browser session.

Mitigation: Require an explicit manual confirmation immediately before any publish click.

Risk: The skill includes broad account-management and profile-fetching behavior.

Mitigation: Use only the publishing workflow unless broader account actions are clearly authorized.

Risk: Generated cover images with missing CJK fonts can render Chinese text incorrectly and contribute to publishing failures.

Mitigation: Verify generated images before upload and use a CJK-capable font such as DroidSansFallbackFull.ttf.

## Reference(s):

- [Xiaohongshu Creator Platform](https://creator.xiaohongshu.com)
- [Xiaohongshu Creator Publish Page](https://creator.xiaohongshu.com/publish/publish)
- [Xiaohongshu User Profile Page](https://www.xiaohongshu.com/user/profile/{userId})
- [ClawHub Skill Page](https://clawhub.ai/waao666/skills/xhs-publisher)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, Code, Configuration]

**Output Format:** [Markdown with inline code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes browser automation steps that can affect a real Xiaohongshu account.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
