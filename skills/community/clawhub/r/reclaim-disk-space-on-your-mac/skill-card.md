## Description:

Guides users through freeing macOS disk space by removing user cache files with a Terminal command.

This skill is ready for commercial/non-commercial use.

## Publisher:

[olegmayami45-boop](https://clawhub.ai/user/olegmayami45-boop)

### License/Terms of Use:


## Use Case:

Mac users and support agents use this skill to explain a quick cache cleanup workflow for reclaiming disk space when downloads, installs, or file transfers are blocked by low storage.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill asks users to run a broad force-delete command against macOS user cache files, which can remove app state or offline resources if run casually.

Mitigation: Prefer macOS storage tools or inspect cache sizes first, quit affected apps, avoid entering an admin password for this cleanup, and review the command before execution.

## Reference(s):


## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Markdown with an inline bash command]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes a cache-removal command that should be reviewed before execution.]

## Skill Version(s):

1.0.1 (source: server release metadata, created 2026-02-05)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
