## Description:

webfetch helps agents fetch webpage content with the webfetch CLI and convert it to Markdown, plain text, or HTML.

This skill is ready for commercial/non-commercial use.

## Publisher:

[lyhue1991](https://clawhub.ai/user/lyhue1991)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to fetch static webpage content, save it to files, and convert it into Markdown, plain text, or raw HTML for downstream reading or processing.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: TLS certificate verification can be bypassed with `--insecure`, which may expose sensitive browsing or fetched content to interception.

Mitigation: Avoid `--insecure` for sensitive or trusted sites; use it only in reviewed environments where the certificate risk is understood.

Risk: The installation guidance recommends an unpinned global npm install.

Mitigation: Prefer a pinned, reviewed, project-local installation of the webfetch package before use.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/lyhue1991/skills/webfetch)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell command examples; fetched content may be Markdown, plain text, HTML, or saved files.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Static pages only; JavaScript rendering is not supported; documented response size limit is 5MB.]

## Skill Version(s):

0.1.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
