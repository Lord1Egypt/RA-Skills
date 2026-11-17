## Description:

Search for Israel Rail train schedules using the railil CLI. Find routes between stations with fuzzy search, filter by date/time, and output in various formats (JSON, Markdown, Table).

This skill is ready for commercial/non-commercial use.

## Publisher:

[lirantal](https://clawhub.ai/user/lirantal)

### License/Terms of Use:


## Use Case:

External users and developers use this skill to install and run the railil CLI for Israel Rail route searches, including fuzzy station matching and date/time filtering.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Installing the railil npm package globally changes the agent environment by adding the railil executable.

Mitigation: Confirm the package source and install only in an environment where a global railil binary is acceptable.

Risk: Travel results depend on train-schedule data returned through the CLI and may change after retrieval.

Mitigation: Use the results as planning assistance and verify critical travel details before acting.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/lirantal/skills/skill-railil)
- [ClawHub Publisher Profile](https://clawhub.ai/user/lirantal)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration instructions, Guidance]

**Output Format:** [Markdown with inline bash commands and CLI output-format guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The underlying railil CLI can emit text, JSON, table, or Markdown output.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
