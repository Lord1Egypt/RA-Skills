## Description:

Weibo (微博) write operations via DrissionPage and Chrome CDP for posting, deleting, reposting, commenting, and liking on weibo.com.

This skill is ready for commercial/non-commercial use.

## Publisher:

[sunwz1115](https://clawhub.ai/user/sunwz1115)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to operate an authenticated Weibo account through Chrome CDP for publishing posts, deleting posts, reposting, commenting, liking, and checking post counts.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The Chrome debug profile can contain broad session data and the open CDP browser is sensitive while running.

Mitigation: Use a dedicated Chrome profile for Weibo, keep it separate from the primary browser profile, and close the CDP browser when the task is complete.

Risk: The delete_all action can remove many Weibo posts from the authenticated account.

Mitigation: Require explicit confirmation before delete_all and verify the target account before executing deletion commands.

Risk: Unpinned Python dependencies can change behavior between installations.

Mitigation: Install in an isolated Python environment and pin reviewed dependency versions before operational use.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/sunwz1115/skills/weibo-ops)
- [Weibo](https://weibo.com)

## Skill Output:

**Output Type(s):** [Shell commands, Guidance, Code]

**Output Format:** [Markdown with inline bash commands and concise operational guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires an authenticated Chrome profile and a Chrome CDP session on port 19334.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
