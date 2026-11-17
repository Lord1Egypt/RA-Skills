## Description:

Manage Synology Calendar events and todos via API. Supports calendars, events, todos, and contacts. Based on official Calendar API Guide (v5).

This skill is ready for commercial/non-commercial use.

## Publisher:

[fpengziyang](https://clawhub.ai/user/fpengziyang)

### License/Terms of Use:


## Use Case:

Developers and operators use this skill to manage Synology Calendar calendars, events, tasks, and contacts through the Synology Calendar API.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Credentials may be sent over plain HTTP if the default Synology URL pattern is used.

Mitigation: Configure the Synology URL with HTTPS and use the skill only on trusted networks.

Risk: Calendar events and tasks can be created, completed, deleted, or otherwise changed.

Mitigation: Use a dedicated low-privilege Synology account and review target calendar IDs, event IDs, and delete commands before execution.

Risk: Supplying a password on the command line can expose it through shell history or process listings.

Mitigation: Prefer environment variables or a secret manager, and avoid passing passwords directly as command-line arguments.

## Reference(s):

- [Official Synology Calendar API Guide](https://global.download.synology.com/download/Document/Software/DeveloperGuide/Package/Calendar/All/enu/Calendar_API_Guide_enu.pdf)
- [Synology Calendar Office Suite API](https://office-suite-api.synology.com/Synology-Calendar/v1)
- [Synology Calendar API Reference](https://office-suite-api.synology.com/Calendar/v1)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown with inline Python and shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May guide or generate Synology Calendar API calls when configured with user-provided credentials.]

## Skill Version(s):

1.0.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
