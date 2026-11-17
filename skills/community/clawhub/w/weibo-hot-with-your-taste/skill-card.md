## Description:

Fetches Weibo trending topics, filters them against a user's preferences, and guides an agent through setup, scheduled pushes, feedback capture, and preference refinement.

This skill is ready for commercial/non-commercial use.

## Publisher:

[zify9000](https://clawhub.ai/user/zify9000)

### License/Terms of Use:

MIT-0

## Use Case:

External users and agent operators use this skill to configure personalized Weibo hot-topic monitoring, receive Feishu updates, and provide feedback that improves future topic selection.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill asks the agent to install external GitHub code.

Mitigation: Review and pin the GitHub implementation before installation.

Risk: Scheduled background jobs may run unattended.

Mitigation: Avoid unattended no_agent schedules unless the exact command and removal process are understood.

Risk: LLM, Feishu, and Weibo credentials are stored locally.

Mitigation: Use dedicated low-privilege credentials and do not copy unrelated agent secrets into this skill.

Risk: Local preference and history files can be changed or deleted.

Mitigation: Review reset and state-changing workflows before running them.

## Reference(s):

- [Server-resolved GitHub provenance](https://github.com/zify9000/weibo-hot-with-your-taste)
- [ClawHub skill page](https://clawhub.ai/zify9000/skills/weibo-hot-with-your-taste)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown with inline shell commands and configuration guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces agent-facing workflows for credential setup, scheduled execution, feedback capture, preference tuning, and recovery from expired Weibo cookies.]

## Skill Version(s):

0.1.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
