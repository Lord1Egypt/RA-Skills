## Description:

Manage a put.io account from the command line using the unofficial kaput CLI for transfers, file search, and transfer status checks.

This skill is ready for commercial/non-commercial use.

## Publisher:

[baanish](https://clawhub.ai/user/baanish)

### License/Terms of Use:


## Use Case:

Developers and external put.io users use this skill to install and authenticate the kaput CLI, add transfer URLs or magnets, search files, list transfers, and check transfer status.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The kaput CLI dependency is unofficial and installed without a pinned version.

Mitigation: Install only after reviewing and trusting the CLI, and prefer a reviewed pinned version when available.

Risk: The CLI stores a local put.io account token and status commands may reveal account details.

Mitigation: Treat the token file and account/status output as sensitive, avoid sharing logs, and do not run the CLI with sudo or root.

## Reference(s):

- [put.io device-code login](https://put.io/link)
- [ClawHub skill page](https://clawhub.ai/baanish/skills/putio)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Markdown with shell commands and command output summaries]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include put.io transfer, file, and account status output from the kaput CLI.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
