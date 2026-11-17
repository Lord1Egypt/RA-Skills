## Description:

Guides agents to scrape website content through the r.jina.ai service, including examples for protected pages.

This skill is ready for commercial/non-commercial use.

## Publisher:

[itonlyforfun-ai](https://clawhub.ai/user/itonlyforfun-ai)

### License/Terms of Use:


## Use Case:

Developers and agents use this skill to retrieve web page content as Markdown through r.jina.ai for public pages they are authorized to access.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Target URLs are sent through r.jina.ai and could expose tokens, private query parameters, internal hostnames, authenticated content, or confidential targets.

Mitigation: Use only public pages you are authorized to scrape, and avoid sensitive, authenticated, internal, or confidential URLs.

Risk: The skill encourages broad protection bypassing and can be misused against sites with access controls or anti-automation protections.

Mitigation: Review intended targets before use and restrict scraping to authorized, policy-compliant pages.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/itonlyforfun-ai/skills/web-scraper-jina)
- [Publisher profile](https://clawhub.ai/user/itonlyforfun-ai)
- [r.jina.ai endpoint](https://r.jina.ai/)

## Skill Output:

**Output Type(s):** [Guidance, Markdown, Code, Shell commands]

**Output Format:** [Markdown guidance with curl and Python examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The target URL is sent to r.jina.ai.]

## Skill Version(s):

1.0.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
