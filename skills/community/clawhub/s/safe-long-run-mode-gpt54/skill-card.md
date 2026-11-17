## Description:

Operate long-running tasks safely when the environment is optimized for GPT-5.4 as the primary and often only model.

This skill is ready for commercial/non-commercial use.

## Publisher:

[bwiley1989](https://clawhub.ai/user/bwiley1989)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, engineers, and agent operators use this skill to plan long-running GPT-5.4 workflows with segmentation, checkpoints, resumable artifacts, and rate-limit-aware handling of external systems.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may cause an agent to batch work, create checkpoint artifacts, or delegate tasks more aggressively than intended.

Mitigation: Review the requested scope before use, especially when external services, project trackers, or subagents are involved.

Risk: Long-running workflows can be interrupted or lose context if progress is not recorded.

Mitigation: Use the skill's checkpoint and resume pattern so completed work, saved artifacts, blockers, and the next exact step are documented.

Risk: External APIs or hosted services may throttle requests during high-throughput work.

Mitigation: Batch requests, avoid rapid polling, serialize writes when needed, and respect retry windows.

## Reference(s):

- [GPT-5.4 Only Long-Run Checklist](references/checklist.md)
- [ClawHub Skill Page](https://clawhub.ai/bwiley1989/skills/safe-long-run-mode-gpt54)

## Skill Output:

**Output Type(s):** [guidance, markdown, configuration, shell commands]

**Output Format:** [Markdown guidance with checklists, operating procedures, and optional command recommendations]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The skill produces process guidance for long-running agent work; it does not execute code by itself.]

## Skill Version(s):

1.0.0 (source: ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
