## Description:

TaskBullet helps an agent delegate user-approved last-mile work to TaskBullet human assistants, including phone calls, authorized login or captcha steps, physical-world actions, subjective QA, and long manual tasks.

This skill is ready for commercial/non-commercial use.

## Publisher:

[griffmurder](https://clawhub.ai/user/griffmurder)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill when an agent needs to hand off authorized work to TaskBullet human assistants instead of completing it locally. The skill guides setup, balance checks, spend confirmation, task delegation, and result polling while avoiding credential relay and account-takeover workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Task details may be sent to TaskBullet human assistants.

Mitigation: Confirm the user wants human delegation and remove secrets, credentials, OTP codes, recovery keys, cookies, and API keys before creating a task.

Risk: Delegated work can consume prepaid TaskBullet hours.

Mitigation: Check balance first, confirm a max-hours cap with the user, and stop for approval if the work appears likely to exceed that cap.

Risk: Login, captcha, or account work can become account takeover if ownership is unclear.

Mitigation: Proceed only in the operator's already-authorized workspace, confirm account ownership, and refuse work on accounts the operator does not own or control.

Risk: An agent could report a delegated result before the human task is complete.

Mitigation: Return the task ID after delegation and poll or wait for the task result instead of inventing completion details.

## Reference(s):

- [TaskBullet Agent API documentation](https://taskbullet.com/docs/agent-api.md)
- [TaskBullet human-assistant category](https://taskbullet.com/humans-working-for-ai)
- [TaskBullet build-a-list workflow](https://taskbullet.com/build-a-list)
- [TaskBullet OpenClaw signup](https://taskbullet.com/get-started?source=openclaw)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, API calls, guidance]

**Output Format:** [Markdown guidance with inline commands, configuration snippets, API call names, and task identifiers]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include TaskBullet task IDs, balance status, spend caps, and polling guidance; secret values are excluded.]

## Skill Version(s):

1.0.10 (source: server release metadata; artifact frontmatter states 1.0.12)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
