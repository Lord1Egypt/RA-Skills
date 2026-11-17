## Description:

Automates daily Xiaohongshu content planning, 9-image post generation, slide rendering, browser-assisted publishing, and scheduled follow-up while leaving final publish confirmation to the user.

This skill is ready for commercial/non-commercial use.

## Publisher:

[gd269438407](https://clawhub.ai/user/gd269438407)

### License/Terms of Use:

MIT-0

## Use Case:

External creators and operators use this skill to build and run a daily Xiaohongshu content workflow. It helps generate topic digests, post copy, HTML slide pages, rendered image assets, and prefilled browser publishing sessions for user review.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Persistent Xiaohongshu sessions and cookies may expose the user's account if the .auth directory is synced, committed, or shared.

Mitigation: Treat .auth as secret material, keep it out of version control and cloud sync, use a dedicated low-privilege workspace/profile, and prefer owner-only permissions or avoiding raw cookie persistence.

Risk: Browser automation includes anti-detection flags, no-sandbox settings, and broad clipboard/notification permissions that increase installation and account-risk review needs.

Mitigation: Review the automation before installing and remove anti-detection flags, unnecessary clipboard permissions, and no-sandbox settings unless explicitly accepted for the environment.

Risk: Scheduled publishing workflows can repeatedly prepare content under the user's account without fresh context review.

Mitigation: Keep the final publish click manual and review generated text, images, timing, and platform-policy fit before publishing.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/gd269438407/skills/xhs-daily-publisher)
- [ClawHub publisher profile](https://clawhub.ai/user/gd269438407)
- [Xiaohongshu Creator Center](https://creator.xiaohongshu.com)
- [Xiaohongshu](https://www.xiaohongshu.com)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with generated project files, HTML templates, JPG image outputs, and shell commands.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires the user's Xiaohongshu account and local browser profile; the final publish action remains manual.]

## Skill Version(s):

0.1.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
