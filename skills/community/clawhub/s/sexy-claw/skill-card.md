## Description:

Sexy-Claw helps an agent search Xiaohongshu, Douyin, Bilibili, and YouTube for appearance-focused creator or video recommendations based on saved user preferences.

This skill is ready for commercial/non-commercial use.

## Publisher:

[deanzh0912](https://clawhub.ai/user/deanzh0912)

### License/Terms of Use:

MIT-0

## Use Case:

External users can use this skill to ask an agent for personalized social-media creator or video recommendations across Xiaohongshu, Douyin, Bilibili, and YouTube. The skill records preferences locally and uses platform search scripts to return ranked results.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill asks users to store raw social-media login cookies, which can expose account sessions if mishandled.

Mitigation: Use anonymous search or official scoped authentication where possible, and avoid placing real cookies in references/platform_cookies.json unless the package is fully trusted.

Risk: Crafted search text can run local commands through shell-based command construction in the bundled search scripts.

Mitigation: Review and fix shell=True command construction before installation or execution.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/deanzh0912/skills/sexy-claw)
- [platform_cookies.json](references/platform_cookies.json)
- [user_preference.json](references/user_preference.json)
- [Xiaohongshu](https://www.xiaohongshu.com)
- [Douyin](https://www.douyin.com)
- [Bilibili](https://www.bilibili.com)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, JSON]

**Output Format:** [Markdown guidance with shell commands and JSON search results]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May produce platform video links and local preference or cookie configuration updates.]

## Skill Version(s):

1.0.0 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
