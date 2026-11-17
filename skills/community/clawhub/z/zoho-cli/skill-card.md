## Description:

Read, search, send, and manage Zoho Mail from the terminal with JSON output for scripting and agents.

This skill is ready for commercial/non-commercial use.

## Publisher:

[robsannaa](https://clawhub.ai/user/robsannaa)

### License/Terms of Use:


## Use Case:

Developers, operators, and agents use this skill to read, search, send, and manage Zoho Mail through the local zoho CLI. It is suited for scripted mail workflows where JSON or markdown command output can be consumed by automation.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill relies on an unpinned third-party Zoho Mail CLI that handles OAuth credentials and mail operations.

Mitigation: Review the upstream source and installation path before installing, and prefer a pinned release or commit with integrity verification.

Risk: OAuth access can allow reading, sending, downloading, moving, and deleting mail on the user's behalf.

Mitigation: Grant the minimum appropriate account access, protect local config and keyring material, and avoid exposing token storage to untrusted parties.

Risk: Permanent delete and folder delete operations can cause irreversible mail loss when automated incorrectly.

Mitigation: Avoid destructive mail or folder deletion through automation unless the exact affected items have been independently confirmed and recovery options are available.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/robsannaa/skills/zoho-cli)
- [Zoho CLI repository](https://github.com/robsannaa/zoho-cli)
- [Zoho CLI setup guide](https://github.com/robsannaa/zoho-cli#setup)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration instructions, Guidance]

**Output Format:** [Markdown with inline shell commands and JSON examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Guidance centers on a local authenticated CLI whose stdout is JSON by default and markdown when requested.]

## Skill Version(s):

0.1.4 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
