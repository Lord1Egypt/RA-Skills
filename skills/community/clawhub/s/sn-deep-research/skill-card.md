## Description:

Coordinates multi-agent deep research workflows that plan, gather cross-source evidence, review findings, and produce report-style deliverables for research, due diligence, competitive analysis, trend analysis, and fact-checking.

This skill is ready for commercial/non-commercial use.

## Publisher:

[sensenova-skills](https://clawhub.ai/user/sensenova-skills)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill when a request requires deeper research than a simple answer. It selects a workflow mode, delegates scouting, planning, research, review, and writing roles, validates intermediate artifacts, and produces cited research deliverables.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill starts a local-network-accessible workbench that can expose files, editing actions, and agent-session access beyond normal expectations.

Mitigation: Install only where that exposure is acceptable; prefer loopback-only use, avoid broad environment secrets, and avoid shared networks or sensitive workspaces until authentication, path containment, and narrower agent-credential handling are added.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/sensenova-skills/skills/sn-deep-research)
- [ClawHub publisher profile](https://clawhub.ai/user/sensenova-skills)
- [Skill source](artifact/SKILL.md)
- [Plan schema](artifact/schemas/plan.schema.md)
- [Evidence schema](artifact/schemas/evidence.schema.md)
- [Outline schema](artifact/schemas/outline.schema.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, JSON, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown research reports with JSON intermediate artifacts and shell commands for workspace and workbench setup.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Creates a run-specific report directory with request, briefing, plan, evidence, outline, sections, stitched report, report, and citations artifacts depending on the selected workflow mode.]

## Skill Version(s):

2026.9.11 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
