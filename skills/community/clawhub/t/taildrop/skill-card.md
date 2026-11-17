## Description:

Download files from Tailscale Taildrop inbox to local storage. Use when user wants to retrieve files sent via Tailscale or mentions Taildrop.

This skill is ready for commercial/non-commercial use.

## Publisher:

[cortexuvula](https://clawhub.ai/user/cortexuvula)

### License/Terms of Use:


## Use Case:

Developers, engineers, and Tailscale users use this skill to retrieve files sent through Taildrop on Linux systems where Taildrop files are not automatically saved.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: A malicious or unexpected destination path can cause unintended local command execution in the bundled shell script.

Mitigation: Review before installing, use only trusted literal destination paths, and remove eval-based command execution before use.

Risk: The overwrite mode can replace existing local files in the destination directory.

Mitigation: Use the default skip mode or rename mode unless replacing files is intentional.

## Reference(s):

- [Taildrop skill page](https://clawhub.ai/cortexuvula/skills/taildrop)

## Skill Output:

**Output Type(s):** [Markdown, Shell commands, Guidance, Files]

**Output Format:** [Markdown with inline bash commands and local file download behavior]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Downloads Taildrop files to a local directory and supports skip, overwrite, rename, and loop modes.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
