## Description:

Use this skill for XCrawl map tasks, including site URL discovery, regex filtering, scope estimation, and crawl planning before full-site crawling.

This skill is ready for commercial/non-commercial use.

## Publisher:

[wykings](https://clawhub.ai/user/wykings)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to discover URLs for authorized sites, apply regex filtering, estimate scope, and plan selective crawls through the XCrawl Map API.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill requests broad local file read, write, edit, and search permissions that are not needed for URL mapping.

Mitigation: Review permissions before installation and prefer a narrower version that reads only ~/.xcrawl/config.json and uses curl or node for requests.

Risk: URL mapping requests and the XCrawl API credential are sent to XCrawl's service.

Mitigation: Use the skill only for domains you are authorized to submit to XCrawl and keep the API key in the documented local config file.

Risk: URL discovery may be incomplete when the configured limit is reached.

Mitigation: Do not claim full site coverage when limit-bound responses are returned; preserve the raw response and reported counts for review.

## Reference(s):

- [XCrawl Homepage](https://www.xcrawl.com/)
- [XCrawl Map Skill Page](https://clawhub.ai/wykings/skills/xcrawl-map)

## Skill Output:

**Output Type(s):** [text, code, shell commands, configuration, guidance]

**Output Format:** [Markdown with JSON responses and inline bash or Node commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Returns the endpoint used, request payload, raw XCrawl Map API response body, and error details when a request fails.]

## Skill Version(s):

1.0.2 (source: server release evidence and skill metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
