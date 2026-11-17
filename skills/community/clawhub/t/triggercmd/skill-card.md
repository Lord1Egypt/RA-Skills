## Description:

Control TRIGGERcmd computers remotely by listing and running commands via the TRIGGERcmd REST API.

This skill is ready for commercial/non-commercial use.

## Publisher:

[rvmey](https://clawhub.ai/user/rvmey)

### License/Terms of Use:


## Use Case:

External users and developers use this skill to inspect TRIGGERcmd commands available to their account and trigger selected commands on registered computers through the TRIGGERcmd REST API.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Remote commands can change files, launch programs, or affect systems connected to the user's TRIGGERcmd account.

Mitigation: Require clear user confirmation before triggering commands with side effects, and list available computers or commands when the target is ambiguous.

Risk: The TRIGGERcmd API token grants access to list and run commands for the account.

Mitigation: Prefer a temporary TRIGGERCMD_TOKEN, keep any token file permission-restricted, avoid printing token values, and rotate the token if it is exposed.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/rvmey/skills/triggercmd)
- [TRIGGERcmd](https://www.triggercmd.com)
- [TRIGGERcmd API base URL](https://www.triggercmd.com/api)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline bash commands and JSON API payload examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires curl, jq, and a user-provided TRIGGERCMD_TOKEN or private token file.]

## Skill Version(s):

1.0.4 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
