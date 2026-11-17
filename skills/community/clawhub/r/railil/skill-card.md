## Description:

Search for Israel Rail train schedules using the railil CLI, including fuzzy station lookup, date and time filters, and text, JSON, table, or Markdown output.

This skill is ready for commercial/non-commercial use.

## Publisher:

[lirantal](https://clawhub.ai/user/lirantal)

### License/Terms of Use:


## Use Case:

External users and agents use this skill to query Israel Rail route schedules through the railil CLI and request results in human-readable or machine-readable formats.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill installs and runs a third-party npm CLI globally, and the release evidence notes the package is unpinned.

Mitigation: Review or pin the railil npm package version before installation, and run it as a normal user or in a sandbox when limiting exposure from third-party npm code matters.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/lirantal/skills/railil)
- [Skill homepage](https://github.com/lirantal/railil)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Guidance]

**Output Format:** [Markdown guidance with railil CLI commands and optional text, JSON, table, or Markdown command output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires the railil CLI binary, normally installed from the railil npm package.]

## Skill Version(s):

1.0.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
