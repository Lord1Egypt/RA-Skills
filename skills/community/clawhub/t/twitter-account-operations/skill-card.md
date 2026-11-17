## Description:

Guides scheduled posting, replies, monitoring, and recovery for an X account the operator owns or is authorized to run.

This skill is ready for commercial/non-commercial use.

## Publisher:

[alexbloch-ia](https://clawhub.ai/user/alexbloch-ia)

### License/Terms of Use:

MIT-0

## Use Case:

Account owners and authorized operators use this skill to plan posts, review notifications and public conversations, publish useful content, and track results through scheduled agent workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Scheduled actions may publish publicly from a logged-in account without adequate oversight.

Mitigation: Limit use to owned or explicitly authorized accounts; configure the account, schedule, retention, and human approval rules before enabling automation.

Risk: Sensitive or inaccurate posts and replies could mislead readers or harm reputations.

Mitigation: Require operator approval for health, legal, financial, political, client-result, named-person, and correction content; verify claims before publishing.

Risk: Platform challenges or rate limits could indicate that continued automation is unsafe.

Mitigation: Stop the run on CAPTCHA, verification challenges, account locks, or rate-limit notices and hand control to a human.

## Reference(s):

- [X / Twitter Account Operations on ClawHub](https://clawhub.ai/alexbloch-ia/skills/twitter-account-operations)
- [OpenClaw](https://openclaw.ai)

## Skill Output:

**Output Type(s):** [Guidance, Markdown, Configuration instructions, Shell commands]

**Output Format:** [Markdown guidance with YAML configuration and shell examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes posting and reply workflows, review checkpoints, and recovery procedures.]

## Skill Version(s):

1.1.0 (source: server-resolved release)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
