## Description:

Que Yin monitors local resource status, schedules tasks, and generates load reports for balancing multi-task workloads.

This skill is ready for commercial/non-commercial use.

## Publisher:

[lt8899789](https://clawhub.ai/user/lt8899789)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators use this skill to inspect local CPU and memory status, assign simple task scheduling priority, and produce load reports with resource recommendations.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Running status or report commands can reveal basic local system resource details such as CPU, memory, platform, uptime, and timestamps.

Mitigation: Use only in environments where exposing basic local resource information is acceptable.

Risk: Documentation and generated recommendations are primarily Chinese-language.

Mitigation: Install only where Chinese-language documentation and output can be reviewed accurately.

Risk: Scheduling and load-report values are simple local heuristics and may include simulated queue or peak-load estimates.

Mitigation: Treat scheduling decisions and recommendations as operational guidance that should be reviewed before acting on them.

## Reference(s):

- [Que Yin ClawHub skill page](https://clawhub.ai/lt8899789/skills/que-yin)

## Skill Output:

**Output Type(s):** [text, JSON, shell commands, guidance]

**Output Format:** [JSON objects and command-line text]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Chinese-language documentation and recommendations; status output can include local CPU, memory, platform, uptime, and timestamp details.]

## Skill Version(s):

1.0.35 (source: SKILL.md frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
