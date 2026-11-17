## Description:

Deploy a local TODO web app that reads and writes a Markdown TODO.md file.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jwhowa](https://clawhub.ai/user/jwhowa)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and OpenClaw users use this skill to deploy a local web UI for viewing, toggling, and archiving tasks stored in TODO.md from devices on a trusted LAN.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The web app exposes readable and writable TODO data on the LAN without authentication.

Mitigation: Run it only on a trusted network or bind it to localhost, and add authentication before broader LAN use.

Risk: Persistent launchd startup can keep the service available after setup.

Mitigation: Prefer manual startup until the launchd plist and service behavior have been reviewed.

Risk: Rendered TODO content may include unsafe formatting if task text comes from other tools or people.

Mitigation: Fix HTML escaping for formatted task text before using shared or untrusted TODO content.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/jwhowa/skills/todo-webapp)
- [Preview Screenshot](https://i.imgur.com/noOCejM.jpeg)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, Configuration]

**Output Format:** [Markdown with inline shell commands and configuration steps]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces setup and operation guidance for a local Node.js TODO web app that reads and writes TODO.md and TODO-done.md.]

## Skill Version(s):

1.0.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
