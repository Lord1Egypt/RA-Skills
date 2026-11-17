## Description:

Deploy AI-generated static assets with StaticHub CLI. Use when a user wants to publish files with `statichub deploy <path>`, where `<path>` must be an explicit non-empty directory or a non-empty `.html` file.

This skill is ready for commercial/non-commercial use.

## Publisher:

[patrick0308](https://clawhub.ai/user/patrick0308)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to publish static HTML files or non-empty static asset directories through the StaticHub CLI. It helps agents validate deployment inputs, produce the appropriate deploy command, and report the resulting live URL and subdomain.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may lead an agent to run an unpinned remote shell installer for the StaticHub CLI.

Mitigation: Require explicit approval before local CLI installation; prefer a pinned release or package source and verify checksums or signatures where available.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/patrick0308/skills/statichub)
- [StaticHub CLI installer script](https://raw.githubusercontent.com/Patrick0308/statichub/main/scripts/install.sh)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Markdown with inline shell commands and deployment result text]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include repair commands when the requested deployment path is invalid.]

## Skill Version(s):

0.1.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
