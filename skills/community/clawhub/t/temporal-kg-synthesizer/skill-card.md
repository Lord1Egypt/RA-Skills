## Description:

Actively parses daily session logs and unstructured memory files to extract entities, temporal data, and relationships into a structured Knowledge Graph.

This skill is ready for commercial/non-commercial use.

## Publisher:

[elmoorish](https://clawhub.ai/user/elmoorish)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and OpenClaw users use this skill to synthesize structured entity summaries from daily memory logs and support later entity or timeline queries.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill reads broad OpenClaw daily memory logs that may contain sensitive names, projects, or relationship context.

Mitigation: Install and run it only where that memory access is acceptable, and review the memory scope before enabling the skill.

Risk: Generated entity Markdown files can persist derived summaries under ~/.openclaw/workspace/memory/entities/.

Mitigation: Review generated entity files after execution and remove files that expose sensitive people, projects, or timelines.

Risk: The optional cron setup can keep synthesis running as a daily background task.

Mitigation: Run cron_setup.sh only when daily background processing is intended, and audit or remove the OpenClaw cron entry when it is no longer needed.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/elmoorish/skills/temporal-kg-synthesizer)
- [ClawHub publisher profile](https://clawhub.ai/user/elmoorish)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration]

**Output Format:** [Markdown status text plus generated Markdown entity files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May create persistent entity summaries under ~/.openclaw/workspace/memory/entities/.]

## Skill Version(s):

0.1.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
