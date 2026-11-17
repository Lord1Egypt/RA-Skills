## Description:

Orchestrate parallel codebase research. Spawns multiple researcher subagents to investigate different areas, then synthesizes findings into research.md.

This skill is ready for commercial/non-commercial use.

## Publisher:

[flip-in](https://clawhub.ai/user/flip-in)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to map an existing codebase by splitting a research question into parallel investigation areas and synthesizing the results into a local research.md report.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill reads project files and writes a local research.md report that may include repository metadata and file references.

Mitigation: Review the generated report before sharing it outside the workspace.

Risk: Running the skill in a directory with an existing research.md may overwrite or replace prior research notes.

Mitigation: Keep a backup or run the skill in a prepared workspace when the existing report must be preserved.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/flip-in/skills/test-research-delete)
- [Publisher profile](https://clawhub.ai/user/flip-in)

## Skill Output:

**Output Type(s):** [markdown, shell commands, guidance]

**Output Format:** [Markdown report with frontmatter and file:line references]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Writes or updates a local research.md file.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
