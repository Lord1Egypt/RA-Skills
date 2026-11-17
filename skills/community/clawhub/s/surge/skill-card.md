## Description:

Blazing fast TUI download manager with multi-connection, queue management, server mode, multiple mirrors, and a terminal interface.

This skill is ready for commercial/non-commercial use.

## Publisher:

[kexu9](https://clawhub.ai/user/kexu9)

### License/Terms of Use:


## Use Case:

Developers and external users use this skill to install and operate Surge for fast single-file, batch, TUI, or headless download workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Downloads can write files to user-selected output paths.

Mitigation: Use trusted URLs and choose writable, expected output directories before starting downloads.

Risk: Server or remote-token mode can leave a download service running.

Mitigation: Start server mode only when intended, protect remote tokens, and stop the service when it is no longer needed.

Risk: The skill depends on an external Surge binary and distribution channels.

Mitigation: Install Surge only from trusted channels and prefer pinned releases or verified binaries.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/kexu9/skills/surge)
- [Surge project homepage](https://github.com/surge-downloader/Surge)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown with inline bash code blocks and concise command guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Guidance may include download URLs, output directories, queue operations, and optional server or remote-token mode.]

## Skill Version(s):

1.1.0 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
