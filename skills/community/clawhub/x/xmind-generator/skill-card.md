## Description:

Generate XMind mind map files (.xmind) from Markdown outlines or plain text descriptions.

This skill is ready for commercial/non-commercial use.

## Publisher:

[geoion](https://clawhub.ai/user/geoion)

### License/Terms of Use:

ISC

## Use Case:

Developers and agents use this skill to turn Markdown outlines or structured plain text into XMind mind map files for planning, visualization, and export workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill installs an npm dependency chain before first use.

Mitigation: Review dependency versions before installation and pin or update the xmind dependency chain when maintaining the package.

Risk: The generator writes .xmind files to a user-selected output path.

Mitigation: Review the output path before running the command so generated files are written only to intended workspace locations.

## Reference(s):


## Skill Output:

**Output Type(s):** [Files, Markdown, Shell commands, Guidance]

**Output Format:** [Markdown guidance with shell commands that generate .xmind files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces a workspace .xmind file at the requested output path.]

## Skill Version(s):

1.0.3 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
