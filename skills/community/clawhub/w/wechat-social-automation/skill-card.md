## Description:

Automates WeChat Official Account and Moments workflows, including content publishing, scheduled posts, interaction analysis, and follower management.

This skill is ready for commercial/non-commercial use.

## Publisher:

[daimingvip-a11y](https://clawhub.ai/user/daimingvip-a11y)

### License/Terms of Use:

MIT-0

## Use Case:

Social media operators and developers can use this skill to guide agents through WeChat Official Account and Moments publishing, scheduling, analytics, and follower-management tasks.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Sensitive WeChat credentials could be exposed if users place a real AppSecret in TOOLS.md or another shared project file.

Mitigation: Use protected environment injection or a secrets manager, and rotate any credential already stored in a shared file.

Risk: Publishing, scheduling, fan management, and profiling actions can be public or privacy-impacting.

Mitigation: Require explicit confirmation and compliance review before carrying out posting, scheduling, follower management, or profiling requests.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/daimingvip-a11y/skills/wechat-social-automation)
- [ClawHub publisher profile](https://clawhub.ai/user/daimingvip-a11y)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance with prompt examples and shell or configuration snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May require WeChat credentials; the reviewed artifact contains documentation only.]

## Skill Version(s):

0.1.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
