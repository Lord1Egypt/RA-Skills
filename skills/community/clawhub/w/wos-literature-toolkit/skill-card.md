## Description:

WOS Literature Toolkit helps agents launch a local Web UI for Web of Science literature searches, Excel export, and multi-channel PDF batch downloads.

This skill is ready for commercial/non-commercial use.

## Publisher:

[grizzlyccc](https://clawhub.ai/user/grizzlyccc)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, research staff, and academic users can use this skill to guide Web of Science search crawling, export results to Excel, and batch-download PDFs through a local browser workflow. Use requires authorized WOS access and download rights.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The workflow stores WOS login cookies.

Mitigation: Use only with authorized WOS access, understand where cookies are stored, and remove saved cookies when they are no longer needed.

Risk: The PDF download flow includes Sci-Hub, which may be unacceptable under some legal, network, or institutional rules.

Mitigation: Confirm download rights before use and prefer authorized publisher or open-access channels when Sci-Hub is not allowed.

Risk: The skill installs and runs browser automation and web-request dependencies.

Mitigation: Install dependencies in an isolated environment and review the skill carefully before installing.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/grizzlyccc/skills/wos-literature-toolkit)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell commands and configuration notes]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Guides a local Web UI workflow that may produce Excel exports and downloaded PDF files.]

## Skill Version(s):

1.1.2 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
