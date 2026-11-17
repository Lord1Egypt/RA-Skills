## Description:

Tools for fetching and extracting cleaned text, metadata, and links from single or multiple web pages with format options and link filtering.

This skill is ready for commercial/non-commercial use.

## Publisher:

[paulgnz](https://clawhub.ai/user/paulgnz)

### License/Terms of Use:


## Use Case:

Developers and agents use this skill to fetch web pages, extract readable page content, collect metadata, discover links, and compare content from multiple URLs during research or data-gathering workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can make unrestricted outbound requests.

Mitigation: Run it only in trusted network environments and consider destination allowlists, private-address blocking, and redirect validation before broad use.

Risk: The skill can forward user-supplied headers to arbitrary targets.

Mitigation: Do not pass Authorization, Cookie, API key, or internal service headers through the scraping tools.

Risk: Large or streaming responses can increase runtime and resource exposure.

Mitigation: Keep response size limits in place and add streaming response limits where the runtime supports them.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/paulgnz/skills/xpr-web-scraping)

## Skill Output:

**Output Type(s):** [text, markdown, html, metadata, links]

**Output Format:** [JSON tool responses containing extracted content, page metadata, resolved links, status fields, and errors when a request fails.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Single-page responses are limited to 5MB, multi-page scraping accepts up to 10 URLs, and link extraction returns up to 200 links.]

## Skill Version(s):

0.2.11 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
