## Description:

Workbuddy Smart Learning helps an agent record feedback and behavioral signals, identify recurring task patterns, and distill reusable templates and avoidance rules.

This skill is ready for commercial/non-commercial use.

## Publisher:

[wwenie](https://clawhub.ai/user/wwenie)

### License/Terms of Use:

MIT-0

## Use Case:

Agents and developers use this skill to run a local learning loop that captures task feedback, tracks execution signals, detects repeated work patterns, and recommends reusable templates or corrective rules.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill records feedback, task history, tool use, and derived patterns in local memory.

Mitigation: Use it only in workspaces where behavioral history can be stored, and provide users a way to inspect, disable, or delete .workbuddy/memory data.

Risk: The security review notes that the skill can read or write an unexpected hard-coded workspace path.

Mitigation: Require an explicit workspace path before use and remove the hard-coded default path from runtime commands.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/wwenie/skills/workbuddy-smart-learning)
- [Publisher profile](https://clawhub.ai/user/wwenie)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown reports, CLI text output, JSON memory records, and YAML template files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Stores local learning data under .workbuddy/memory and produces pattern, alert, feedback, signal, profiler, and distillation reports.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
