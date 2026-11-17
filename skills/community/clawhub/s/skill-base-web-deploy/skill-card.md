## Description:

Skill Base server deployment guide for starting the Skill Base server with npx or Docker, configuring ports and data directories, and planning SQLite database backups.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ginuim](https://clawhub.ai/user/ginuim)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators use this skill when deploying or operating the Skill Base platform server, including npm and Docker startup, host and port settings, persistent data directories, and database backup planning.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The guide includes examples that can expose the initial administrator setup page on all network interfaces.

Mitigation: Initialize the first administrator while bound to 127.0.0.1 or behind trusted access controls, and avoid broadly publishing port 8000 until setup is complete.

Risk: The npm quick-start command can run an unpinned skill-base package.

Mitigation: Use a reviewed, pinned skill-base version before installing or sharing deployment instructions with operators.

Risk: The Skill Base data directory contains the SQLite database and skill artifacts.

Mitigation: Keep the data directory access-restricted and backed up during low write activity or off-peak windows.

## Reference(s):


## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline bash code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes deployment commands, configuration flags, backup notes, and troubleshooting guidance.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
