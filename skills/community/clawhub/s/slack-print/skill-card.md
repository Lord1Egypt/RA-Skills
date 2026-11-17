## Description:

Print files uploaded to a Slack channel with smart matching for file count, filename filters, file type, and recent upload time.

This skill is ready for commercial/non-commercial use.

## Publisher:

[caigang78](https://clawhub.ai/user/caigang78)

### License/Terms of Use:


## Use Case:

External users and employees use this skill to print recently uploaded Slack files or direct text content through a local printer. It is intended for Slack-to-printer workflows where the agent maps a user's request to printer commands and filtering parameters.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Core Slack download and argument parsing behavior depends on shared helper scripts that were not included in the artifact.

Mitigation: Install only with a trusted local shared helper directory and verify those helpers before use.

Risk: The skill can print Slack files and text to local printers, which may expose sensitive content if used on shared printers or broad Slack channels.

Mitigation: Use a dedicated printer, a minimally scoped Slack token, and explicit user confirmation before printing.

Risk: The skill includes printer administration commands such as queue inspection and canceling jobs.

Mitigation: Gate printer administration actions behind explicit confirmation and avoid granting this skill unnecessary printer control in shared environments.

## Reference(s):


## Skill Output:

**Output Type(s):** [shell commands, configuration, text, guidance]

**Output Format:** [Markdown guidance with inline bash commands and shell output text]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses environment variables such as PRINTER, LIMIT, NAME_PREFIX, NAME_CONTAINS, MINUTES, and FILE_TYPE to control file selection and printing.]

## Skill Version(s):

1.0.0 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
