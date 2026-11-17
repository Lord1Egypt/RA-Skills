## Description:

SocialPost Auto helps generate, schedule, and run social media posting workflows for Xiaohongshu, Weibo, and Twitter/X, with optional auto-reply support.

This skill is ready for commercial/non-commercial use.

## Publisher:

[anson125chen](https://clawhub.ai/user/anson125chen)

### License/Terms of Use:

MIT-0

## Use Case:

External users and social media operators use this skill to draft platform-specific posts, schedule publication tasks, and manage basic automated reply workflows across supported social platforms.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can schedule unattended public social media posts and auto-replies using account credentials.

Mitigation: Review generated content before publication, test with non-public or low-risk accounts first, and enable scheduled or auto-reply behavior only when preview, logging, pause, and removal procedures are in place.

Risk: Platform credentials and cookies are required for posting workflows.

Mitigation: Store credentials with restrictive permissions, limit account privileges where possible, and rotate credentials if they may have been exposed.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/anson125chen/skills/socialpost-auto)
- [Publisher profile](https://clawhub.ai/user/anson125chen)
- [Project website](https://asmartglobal.com)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown with command examples and JSON configuration snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May create scheduled posting tasks and print task status when its helper script is run.]

## Skill Version(s):

1.0.0 (source: SKILL.md frontmatter, package.json, release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
