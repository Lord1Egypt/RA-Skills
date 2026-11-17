## Description:

Manage application secrets with the Redshift CLI for decentralized, encrypted secret management built on Nostr.

This skill is ready for commercial/non-commercial use.

## Publisher:

[accolver](https://clawhub.ai/user/accolver)

### License/Terms of Use:


## Use Case:

Developers and engineers use this skill to operate the Redshift CLI for setting, retrieving, listing, deleting, uploading, downloading, and injecting application secrets across project environments.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Commands that show raw secret values, download secret files, upload secrets, delete secrets, or run processes with injected secrets can expose or alter sensitive data.

Mitigation: Review each Redshift command before execution, prefer redacted listing where possible, and treat downloaded files and injected environments as sensitive.

Risk: Running Redshift commands through `redshift run` can execute user commands with secret-bearing environment variables.

Mitigation: Only execute commands explicitly requested and confirmed by the user, and avoid constructing arbitrary commands.

Risk: Starting the Redshift web UI on a network-facing host can expose the interface beyond localhost.

Mitigation: Use the default localhost binding unless network exposure is intentional and reviewed.

## Reference(s):

- [Redshift homepage](https://redshiftapp.com)
- [Redshift source repository](https://github.com/accolver/redshift)
- [ClawHub skill page](https://clawhub.ai/accolver/skills/redshift)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline shell command examples and concise procedural guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include commands that operate on sensitive secret data and should be reviewed before execution.]

## Skill Version(s):

0.2.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
