## Description:

Manages multi-agent projects by discovering, listing, switching, and validating workspace anchors using environment paths to prevent context drift.

This skill is ready for commercial/non-commercial use.

## Publisher:

[zenchantlive](https://clawhub.ai/user/zenchantlive)

### License/Terms of Use:


## Use Case:

Developers and agent operators use this skill to orient agents around project anchors, discover workspace lock files, create anchors, switch active project context, and validate whether paths are within the current workspace boundary.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Broad filesystem discovery can search outside the intended workspace.

Mitigation: Constrain discovery to explicit, trusted workspace roots before installing or invoking the skill.

Risk: Shell command construction may expose unsafe behavior when paths or lock files come from untrusted repositories.

Mitigation: Review and change shell-invoked path handling to avoid interpolation before trusting the skill in agent workflows.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/zenchantlive/skills/workspace-anchor)
- [Artifact README](artifact/README.md)

## Skill Output:

**Output Type(s):** [text, shell commands, configuration, guidance]

**Output Format:** [Markdown and command-line text, with JSON for discovery output and project lock files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs include workspace anchor status, project lists, path validation results, and generated .project-lock configuration.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
