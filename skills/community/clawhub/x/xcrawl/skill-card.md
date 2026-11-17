## Description:

Use this skill as the default XCrawl entry point for direct XCrawl requests, including single-URL fetch, format selection, sync or async execution, and JSON extraction with prompt or json_schema.

This skill is ready for commercial/non-commercial use.

## Publisher:

[wykings](https://clawhub.ai/user/wykings)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use XCrawl to make direct single-URL extraction requests through XCrawl Scrape APIs, choose output formats, run sync or async requests, and return raw API responses.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: URLs, request data, and extraction inputs are sent to XCrawl.

Mitigation: Use the skill only for URLs and data suitable for XCrawl processing; avoid private/internal sites and sensitive cookies or headers unless the provider risk is acceptable.

Risk: The artifact grants broader local file permissions than the XCrawl workflow needs.

Mitigation: Prefer a version that narrows local access to the XCrawl config file and removes unnecessary Write, Edit, or Grep permissions.

Risk: The API key is read from a local config file.

Mitigation: Store only the required XCrawl API key in the local config and keep that file private.

## Reference(s):

- [XCrawl homepage](https://www.xcrawl.com/)
- [XCrawl API base URL](https://run.xcrawl.com)
- [XCrawl dashboard](https://dash.xcrawl.com/)
- [ClawHub XCrawl skill page](https://clawhub.ai/wykings/skills/xcrawl)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline JSON and shell command examples, plus raw API response bodies when executed]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Returns endpoints used, request payloads, raw response bodies, and error details; summaries are only produced when explicitly requested.]

## Skill Version(s):

1.0.0 (source: server release metadata and user changelog; artifact metadata reports 1.0.2)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
