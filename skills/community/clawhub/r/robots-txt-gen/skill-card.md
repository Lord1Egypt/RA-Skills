## Description:

Generate, validate, and analyze robots.txt files for websites, including platform presets, URL allow/block tests, and crawl directive audits.

This skill is ready for commercial/non-commercial use.

## Publisher:

[johnnywang2001](https://clawhub.ai/user/johnnywang2001)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, site operators, and SEO practitioners use this skill to create robots.txt files, validate local or remote robots.txt syntax, test crawler access for specific URL paths, and apply presets for common web platforms.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Remote robots.txt validation can fetch arbitrary URLs from the agent environment without network or response-size limits.

Mitigation: Prefer local file validation for untrusted inputs; when remote validation is needed, run in a network-restricted sandbox and avoid URLs that could reach internal services or cloud metadata endpoints.

## Reference(s):


## Skill Output:

**Output Type(s):** [text, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell commands and robots.txt/plain-text output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May write generated robots.txt content to a file when the output option is used; remote validation can make outbound HTTP requests.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
