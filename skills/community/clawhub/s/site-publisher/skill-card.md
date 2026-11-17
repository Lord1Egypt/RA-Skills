## Description:

Serve and package static websites for preview and deployment. Use when you need to preview a static site, serve HTML files locally, or package a site for sharing/deployment.

This skill is ready for commercial/non-commercial use.

## Publisher:

[147258xuan](https://clawhub.ai/user/147258xuan)

### License/Terms of Use:

MIT-0

## Use Case:

Developers use this skill to preview a static website over HTTP and package its files for sharing or deployment.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The server can expose unrelated local files, and crafted packaging paths can execute commands.

Mitigation: Prefer a patched version that confines reads to the website directory, binds explicitly to localhost, and invokes tar without a shell. Until fixed, avoid exposing the server or supplying untrusted packaging paths.

Risk: The standalone packaging command produces a folder rather than a ZIP archive.

Mitigation: Inspect the packaged folder contents before sharing.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/147258xuan/skills/site-publisher)

## Skill Output:

**Output Type(s):** [Shell commands, Code, Guidance]

**Output Format:** [Markdown instructions with shell examples and JavaScript API snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [None]

## Skill Version(s):

1.0.0 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
