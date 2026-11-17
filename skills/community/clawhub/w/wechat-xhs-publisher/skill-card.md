## Description:

Wechat Xhs Publisher helps an agent rewrite trending news into WeChat Official Account articles, generate supporting images, check the publishing IP, and publish to WeChat and Xiaohongshu.

This skill is ready for commercial/non-commercial use.

## Publisher:

[achievejia](https://clawhub.ai/user/achievejia)

### License/Terms of Use:

MIT-0

## Use Case:

External content operators and social media publishers use this skill to turn news material into platform-ready WeChat and Xiaohongshu posts. The workflow covers article drafting, image planning, IP checking, and final posting steps.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The workflow can give an agent authority to publish public WeChat and Xiaohongshu content.

Mitigation: Require explicit human review and approval before any post is published or saved as a platform draft.

Risk: The publishing command template uses unpinned tooling through npx -y.

Mitigation: Pin or preinstall the required Bun and publishing tools before use.

Risk: Drafts, images, account details, and platform credentials may be exposed to external publishing or image services.

Mitigation: Run the skill only with the specific account and content needed for the post, and avoid unnecessary sensitive drafts or credentials.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/achievejia/skills/wechat-xhs-publisher)
- [Publisher profile](https://clawhub.ai/user/achievejia)
- [IP38 IP lookup](https://www.ip38.com/)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown with inline shell commands and publishing parameters]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May create article markdown, image files, publishing reports, and platform API call instructions.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
