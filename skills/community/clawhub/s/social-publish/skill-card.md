## Description:

Helps agents guide authorized, user-visible video publishing across Douyin, Kuaishou, Bilibili, Xiaohongshu, and WeChat Channels.

This skill is ready for commercial/non-commercial use.

## Publisher:

[hitjcl](https://clawhub.ai/user/hitjcl)

### License/Terms of Use:

MIT-0

## Use Case:

Content operators, marketers, and creators use this skill to prepare and guide video publishing workflows across multiple Chinese social video platforms while keeping account login and final publishing actions under user control.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can guide actions in logged-in social media accounts.

Mitigation: Use only accounts the user is comfortable controlling through the browser, require manual confirmation for every publish action, and review account activity after use.

Risk: Helper output may include curl or wget download commands for user-supplied URLs.

Mitigation: Prefer browser downloads, and run terminal download commands only after confirming the URL, filename, quoting, and source trustworthiness.

Risk: Platform publishing rules, upload limits, and account controls may change outside the skill.

Mitigation: Check each target platform's current creator workflow and rules before publishing, especially for production or brand accounts.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/hitjcl/skills/social-publish)
- [Skill instructions](artifact/SKILL.md)
- [Security notes](artifact/SECURITY.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with optional JSON from helper scripts and quoted shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires user-controlled browser sessions for platform account actions; helper scripts perform local validation or produce instructions rather than publishing directly.]

## Skill Version(s):

2.0.0 (source: server release metadata and artifact/skill.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
