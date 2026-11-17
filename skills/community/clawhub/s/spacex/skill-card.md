## Description:

CLI for AI agents to lookup SpaceX launches and rockets for their humans. No auth required.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jeffaf](https://clawhub.ai/user/jeffaf)

### License/Terms of Use:

MIT

## Use Case:

External users and agents use this skill to answer SpaceX launch, rocket, and crew questions through a CLI backed by the community SpaceX API.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The reviewed package does not include the executable implementation that the README tells agents to install.

Mitigation: Review the external repository before installation and pin the installation to a known commit.

## Reference(s):

- [SpaceX API](https://github.com/r-spacex/SpaceX-API)
- [SpaceX API Documentation](https://github.com/r-spacex/SpaceX-API/tree/master/docs)
- [SpaceX API v4 Base URL](https://api.spacexdata.com/v4)

## Skill Output:

**Output Type(s):** [Text, Shell commands, Guidance]

**Output Format:** [Markdown with inline shell commands and concise CLI output examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires bash, curl, and jq; uses unauthenticated community SpaceX API data that may lag real time.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
