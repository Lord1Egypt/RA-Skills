## Description:

Profile offline OpenClaw skill run samples to detect latency, CPU, and memory bottlenecks and compare sessions.

This skill is ready for commercial/non-commercial use.

## Publisher:

[mike007jd](https://clawhub.ai/user/mike007jd)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to analyze offline OpenClaw run samples, identify latency, CPU, and memory bottlenecks, export reports, and compare before-and-after profiling snapshots.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: HTML reports generated from attacker-controlled sample data may include active browser content.

Mitigation: Generate HTML reports only from trusted samples or open them in a constrained environment until dynamic values are escaped.

## Reference(s):

- [SkillPulse ClawHub Page](https://clawhub.ai/mike007jd/skills/skillpulse)
- [README.md](README.md)

## Skill Output:

**Output Type(s):** [text, JSON, HTML files, shell commands, guidance]

**Output Format:** [CLI text, JSON envelopes, and JSON or HTML report files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Reports depend on user-provided offline sample arrays with latencyMs, cpuMs, and memoryMb fields.]

## Skill Version(s):

1.0.0 (source: server release metadata and package.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
