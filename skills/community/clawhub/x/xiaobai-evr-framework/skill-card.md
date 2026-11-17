## Description:

EVR Framework guides agents through Execute-Verify-Report so they perform requested actions, independently verify results, and report evidence before claiming completion.

This skill is ready for commercial/non-commercial use.

## Publisher:

[aptratcn](https://clawhub.ai/user/aptratcn)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent users use this skill to make assistants execute tasks, verify results with independent checks, and report concrete evidence before claiming completion.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill encourages agents to take real actions and persist evidence or behavioral rules, which can be risky without clear user consent.

Mitigation: Require explicit user approval for destructive actions, external messages, scheduled jobs, credentialed operations, persistent memory updates, and WORK_RULES.md changes.

Risk: Verification-focused reporting can still include incorrect or misleading guidance if command results are misunderstood.

Mitigation: Review proposed actions and verification evidence before deployment, and scan the skill before use.

## Reference(s):


## Skill Output:

**Output Type(s):** [Guidance, Shell commands, Text]

**Output Format:** [Markdown guidance with inline shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include verification evidence and command output summaries.]

## Skill Version(s):

1.1.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
