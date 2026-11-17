## Description:

Sets up SearchDock CLI and read-only Google Search Console access, selects a verified property, and checks the connection.

This skill is ready for commercial/non-commercial use.

## Publisher:

[xplormityai](https://clawhub.ai/user/xplormityai)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and other Search Console users can install SearchDock, connect their Google account with read-only access, select a verified property, and confirm the connection.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: An unpinned installation command may retrieve changed third-party packages.

Mitigation: Verify the npm packages and repository source before installing; prefer a reviewed, pinned version.

Risk: OAuth client files, tokens, and private Search Console reports may be exposed during setup.

Mitigation: Request only the local client-file path; do not print, share, or commit credentials, tokens, or reports.

Risk: Installing skills or changing MCP configuration may affect other agent setups.

Mitigation: Prefer project-scoped installation and preserve existing skills, servers, and account settings.

## Reference(s):

- [SearchDock Google setup guide](https://github.com/xplormityai/searchdock-cli/blob/main/docs/google-setup.md)

## Skill Output:

**Output Type(s):** [Shell commands, Configuration instructions, Guidance]

**Output Format:** [Markdown with inline shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Reports installation, tool discovery, and Google connection status separately.]

## Skill Version(s):

1.0.0 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
