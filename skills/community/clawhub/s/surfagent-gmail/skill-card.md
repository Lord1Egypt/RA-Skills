## Description:

Gmail platform skill for SurfAgent, covering mailbox checks, mailbox triage, latest-thread opening, compose and reply task runners, tab hygiene, sent-message verification, proof rules, and when to use the Gmail adapter over raw browser control.

This skill is ready for commercial/non-commercial use.

## Publisher:

[surfagentapp](https://clawhub.ai/user/surfagentapp)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to guide agents through Gmail mailbox checks, triage, compose, reply, send verification, and recovery workflows in SurfAgent/browser sessions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Automating Gmail can expose mailbox contents or send messages from the active Gmail account.

Mitigation: Install only when Gmail automation is intended, grant access only in an account context suitable for automation, and review sensitive drafts before sending.

Risk: Gmail compose and send flows can appear successful before Gmail confirms the message was sent and rendered correctly.

Mitigation: Require compose proof, send confirmation, and Sent Mail or thread render verification before claiming task success.

## Reference(s):

- [SurfAgent homepage](https://surfagent.app)
- [ClawHub skill page](https://clawhub.ai/surfagentapp/skills/surfagent-gmail)

## Skill Output:

**Output Type(s):** [Guidance, Markdown, Text]

**Output Format:** [Markdown skill instructions]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Guidance covers Gmail browser workflows, task-runner selection, mailbox triage, compose and reply handling, and visible verification checks.]

## Skill Version(s):

1.3.0 (source: frontmatter, skill.json, release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
