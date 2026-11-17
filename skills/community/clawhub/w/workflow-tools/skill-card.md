## Description:

Work smarter with loop detection, parallel decisions, and file size analysis.

This skill is ready for commercial/non-commercial use.

## Publisher:

[leegitw](https://clawhub.ai/user/leegitw)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent operators use this skill to inspect workflow state, decide whether work should run serially or in parallel, analyze large files for context efficiency, and delegate subworkflows to installed ClawHub skills.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Path-based workflow scans can read any location the agent can access.

Mitigation: Run the skill in a constrained workspace and avoid pointing /wt loops or /wt mce at sensitive directories.

Risk: Subworkflow delegation can invoke other installed skills and expand the effective permission footprint.

Mitigation: Review installed skills before using /wt subworkflow and prefer environments where broad delegation is disabled or explicitly confirmed.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/leegitw/skills/workflow-tools)
- [Publisher profile](https://clawhub.ai/user/leegitw)
- [OpenClaw workflow tools configuration](.openclaw/workflow-tools.yaml)
- [Claude workflow tools configuration](.claude/workflow-tools.yaml)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown-style agent responses with command examples and workspace report files.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Writes analysis outputs under output/loops, output/parallel-decisions, output/mce-analysis, and output/subworkflows when used by an agent.]

## Skill Version(s):

1.5.1 (source: release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
