## Description:

Automatically extracts and displays titles, descriptions, and favicons for shared HTTP/HTTPS URLs so users can preview webpage content without visiting.

This skill is ready for commercial/non-commercial use.

## Publisher:

[kingfish1949101-wq](https://clawhub.ai/user/kingfish1949101-wq)

### License/Terms of Use:

MIT-0

## Use Case:

External users and agents use this skill to turn shared public HTTP/HTTPS links into concise preview cards with page title, description, favicon, domain, and a brief summary.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Fetching a URL can expose private, internal, token-bearing, or sensitive links to the host environment used for preview generation.

Mitigation: Use the skill only for public HTTP/HTTPS URLs unless the host environment blocks private-network, credential-bearing, and otherwise sensitive requests.

Risk: Preview content may be incomplete or misleading when a public page omits accurate metadata or changes after the preview is generated.

Mitigation: Treat generated previews as summaries and open trusted sources directly when accuracy matters.

## Reference(s):


## Skill Output:

**Output Type(s):** [Markdown, Text, Guidance]

**Output Format:** [Markdown preview card with a linked title, description, site/domain line, and brief summary]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Limits descriptions to about 200 characters and advises no more than 5 URL previews per minute.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
