## Description:

Orchestrate growth loops across the skill portfolio by connecting usage, feedback, improvement, and adoption into self-reinforcing cycles.

This skill is ready for commercial/non-commercial use.

## Publisher:

[harrylabsj](https://clawhub.ai/user/harrylabsj)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, skill maintainers, and portfolio operators use this skill to design growth loops, analyze adoption funnels, draft referral or engagement plans, and generate simulated metric reports for planning.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Local scripts can overwrite writable files when users pass broad or unintended output paths.

Mitigation: Run the scripts from a dedicated workspace and choose explicit output paths that do not point at important project files.

Risk: Generated reports and metrics are simulated and may be mistaken for live analytics.

Mitigation: Label generated metrics as mock data and validate any recommendations against real usage data before business decisions.

Risk: Some generated growth advice promotes public-by-default publishing patterns.

Mitigation: Require explicit user opt-in and a privacy review before publishing skill outputs or user-generated content.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/harrylabsj/skills/skills-orchestrator)
- [Skill documentation](artifact/SKILL.md)
- [README](artifact/README.md)
- [Sample loop analysis](artifact/data/LOOP-ANALYSIS-20260313.md)
- [Sample loop design](artifact/data/LOOP-DESIGN-test-skill-20260313.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, JSON, Shell commands, Guidance]

**Output Format:** [Markdown reports, JSON metrics, and inline shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Simulated metrics only; script outputs are local files and console text.]

## Skill Version(s):

1.0.1 (source: server release metadata; artifact _meta.json reports 1.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
