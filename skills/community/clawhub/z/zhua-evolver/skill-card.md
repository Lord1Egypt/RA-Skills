## Description:

Zhua Evolver helps an agent analyze capability gaps, search for skills, run evolution workflows, coordinate helper roles, and record evolution progress.

This skill is ready for commercial/non-commercial use.

## Publisher:

[beipian261](https://clawhub.ai/user/beipian261)

### License/Terms of Use:

MIT-0

## Use Case:

External developers and agent operators use this skill to guide self-improvement workflows for the Zhua agent persona, including gap analysis, skill discovery, skill installation planning, helper-role orchestration, and evolution logging.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can direct an agent toward automatic installation of unreviewed skills.

Mitigation: Require explicit user approval before each installation, use trusted or pinned skill sources, and review visible diffs before applying changes.

Risk: The skill describes persistent identity or SOUL.md changes as part of evolution workflows.

Mitigation: Back up persistent identity files, show proposed changes before writing, and keep rollback controls available.

Risk: Security evidence rates the package as suspicious because approval and safety controls are not clear in the instructions.

Mitigation: Review the packaged scripts and instructions before deployment and restrict execution to supervised environments.

## Reference(s):

- [Reference Documentation for Zhua Evolver](references/api_reference.md)
- [ClawHub release page for zhua-evolver](https://clawhub.ai/beipian261/skills/zhua-evolver)
- [Publisher profile: beipian261](https://clawhub.ai/user/beipian261)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell command examples and optional JSON output from helper scripts]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May produce local evolution metrics, task assignments, installation plans, and log-ready summaries.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
