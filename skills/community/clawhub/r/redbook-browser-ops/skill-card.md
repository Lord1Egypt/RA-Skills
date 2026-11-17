## Description:

Publish and manage Xiaohongshu (RED/Xiaohongshu) content via browser automation with confirm-before-publish safety, including image posts and no-image longform notes on creator.xiaohongshu.com.

This skill is ready for commercial/non-commercial use.

## Publisher:

[yikailucas](https://clawhub.ai/user/yikailucas)

### License/Terms of Use:


## Use Case:

External creators and operators use this skill to draft, publish, reply, and review visible metrics in a logged-in Xiaohongshu creator account. It is intended for browser-based creator workflows where publishing requires explicit confirmation.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill operates in a user's logged-in Xiaohongshu creator account and can affect public content.

Mitigation: Install only for intended creator-account operations, review post and reply content before use, and preserve the explicit publish-confirmation requirement.

Risk: Login, CAPTCHA, SMS, or platform risk controls may block automation.

Mitigation: Pause for the user to complete required platform checks and do not use the skill to bypass platform controls.

Risk: Creator-site UI changes may prevent the agent from finding expected controls or completing a publish flow.

Mitigation: Refresh the browser snapshot, use the nearest equivalent visible control, keep content as a draft when publishing is unavailable, and report any manual step clearly.

## Reference(s):

- [Xiaohongshu Creator Center](https://creator.xiaohongshu.com)
- [Post Templates](references/post-templates.md)
- [Redbook Browser Ops on ClawHub](https://clawhub.ai/yikailucas/skills/redbook-browser-ops)

## Skill Output:

**Output Type(s):** [Text, Markdown, Guidance]

**Output Format:** [Markdown status summary with account, title, mode, result, details, and next step]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include draft, publish, reply, or metrics action status.]

## Skill Version(s):

0.1.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
