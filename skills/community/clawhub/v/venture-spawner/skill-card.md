## Description:

Venture Spawner turns orchestrator job postings into configured sub-agent tasks, passing context, enforcing timeouts and concurrency limits, and tracking completion.

This skill is ready for commercial/non-commercial use.

## Publisher:

[dodge1218](https://clawhub.ai/user/dodge1218)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators use this skill to convert scoped job postings into bounded sub-agent work, monitor completion, and keep an orchestrator job board current.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Autonomous sub-agents may modify repositories, push commits, or perform SSH-related work.

Mitigation: Run the skill only in controlled workspaces with protected branches and require explicit approval before pushes or remote commands.

Risk: Job board context may include sensitive business or personal files.

Mitigation: Use trusted JOB_BOARD.md authors, limit credentials, and review sensitive-data handling before spawning agents.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/dodge1218/skills/venture-spawner)

## Skill Output:

**Output Type(s):** [markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown updates and structured task instructions]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Updates JOB_BOARD.md with job status, agent session keys, artifact links, and completion time.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
