## Description:

知识星球助手 helps an agent log in to zsxq.com, navigate Knowledge Planet groups, view content, and publish posts when the user requests those actions.

This skill is ready for commercial/non-commercial use.

## Publisher:

[codeteenager](https://clawhub.ai/user/codeteenager)

### License/Terms of Use:

MIT-0

## Use Case:

External users use this skill to guide an agent through Knowledge Planet login, group navigation, content viewing, and post publishing workflows on zsxq.com.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can publish to a user's Knowledge Planet account without a clear final approval step.

Mitigation: Require the agent to show the final post content and receive explicit user approval immediately before publishing.

Risk: Login requires QR-code screenshots that may expose account access flow details.

Mitigation: Share login screenshots only with the requesting user and avoid retaining them after the login flow completes.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/codeteenager/skills/zsxq-helper)
- [Knowledge Planet Login](https://wx.zsxq.com/login)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, Configuration instructions]

**Output Format:** [Markdown with inline shell commands and browser-operation guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include instructions to show login screenshots and confirm final post content before publishing.]

## Skill Version(s):

1.1.0 (source: server release metadata and artifact version text)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
