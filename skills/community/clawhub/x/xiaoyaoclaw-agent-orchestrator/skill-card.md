## Description:

Coordinates multi-agent work by breaking tasks into subtasks, dispatching them, tracking progress, and combining attributed results with bounded retries.

This skill is ready for commercial/non-commercial use.

## Publisher:

[dtsola](https://clawhub.ai/user/dtsola)

### License/Terms of Use:

MIT

## Use Case:

OpenClaw users and developers use this skill to delegate multi-agent tasks, monitor execution, and deliver sourced summaries. It checks the required coordination settings and asks before changing configuration.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The configuration loader may read credential-bearing sections even though scanners found no credential output or external transmission.

Mitigation: Review the configuration read path and limit access to the minimum configuration needed for coordination before use.

Risk: Scan coverage was partial: some SKILL.md references could not be resolved, and the QR image was not analyzed by static scanners.

Mitigation: Review the unresolved references and inspect the QR image before relying on the release.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/dtsola/skills/xiaoyaoclaw-agent-orchestrator)
- [Project documentation](https://github.com/dtsola/xiaoyaoclaw-agent-orchestrator)
- [Agent-to-agent configuration guide](references/agent_to_agent.md)
- [sessions_send reference](references/sessions_send.md)
- [Configuration patch safety guide](references/config_patch.md)

## Skill Output:

**Output Type(s):** [Markdown, Text, Guidance]

**Output Format:** [Markdown task prompts, progress summaries, and sourced aggregation reports]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Retries failed tasks up to three times by default; report files go to a user-selected location after confirmation.]

## Skill Version(s):

1.0.7 (source: server-resolved release)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
