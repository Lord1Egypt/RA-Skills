## Description:

Publishes Zhihu column articles from a Linux VNC Chrome session by attaching to local Chrome remote debugging, filling a title and body, and optionally submitting the post.

This skill is ready for commercial/non-commercial use.

## Publisher:

[m-lemon](https://clawhub.ai/user/m-lemon)

### License/Terms of Use:

MIT-0

## Use Case:

External users and agents use this skill to draft or provide article content and publish it to a logged-in Zhihu column account from a Linux server with VNC and Chrome. It is intended for workflows where the user has authorized real posting from the saved browser profile.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can publish real Zhihu articles from a saved logged-in browser session without a fresh confirmation step.

Mitigation: Prefer preview or draft mode unless the user explicitly confirms the final title and body before submitting.

Risk: The Chrome debugging port and saved browser profile can expose an authenticated Zhihu session if mishandled.

Mitigation: Keep the debugging port bound locally, use a dedicated Zhihu automation profile, and require VNC login only for that profile.

Risk: Setup may download chromedriver and install Python dependencies that affect the runtime environment.

Mitigation: Review downloaded dependencies before setup and prefer user-local installs instead of sudo or system-wide driver installation when possible.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/m-lemon/skills/zhihu-publish-attach)
- [Linux server + VNC setup](artifact/references/linux-vnc-setup.md)
- [Chrome for Testing](https://googlechromelabs.github.io/chrome-for-testing/)
- [Zhihu Creator](https://www.zhihu.com/creator)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration]

**Output Format:** [Markdown or plain text article content, shell command execution, and JSON status from the publish script]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May create a temporary body file and screenshots; publish status includes fields such as ok, published, url, screenshot, and error.]

## Skill Version(s):

0.0.3 (source: ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
