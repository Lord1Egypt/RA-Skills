## Description:

Use this skill for XCrawl scrape tasks, including single-URL fetch, format selection, sync or async execution, and JSON extraction with prompt or json_schema.

This skill is ready for commercial/non-commercial use.

## Publisher:

[wykings](https://clawhub.ai/user/wykings)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to perform single-page XCrawl scraping, choose response formats, run synchronous or asynchronous requests, and request JSON extraction from web content.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can send scrape targets, supplied headers, cookies, prompts, and extracted content to XCrawl.

Mitigation: Use it only for approved public or permitted pages, avoid private or regulated content unless authorized, and review request payloads before execution.

Risk: The skill depends on a local XCrawl API key file.

Mitigation: Protect ~/.xcrawl/config.json, limit access to the API key, and rotate the key if exposure is suspected.

Risk: The scanner notes broader Write/Edit permissions than the workflow explains.

Mitigation: Review requested permissions before use and grant only the permissions needed for the specific scrape task.

## Reference(s):

- [XCrawl homepage](https://www.xcrawl.com/)
- [XCrawl dashboard](https://dash.xcrawl.com/)
- [XCrawl API base](https://run.xcrawl.com)
- [ClawHub skill page](https://clawhub.ai/wykings/skills/xcrawl-scrape)
- [Publisher profile](https://clawhub.ai/user/wykings)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown with JSON and shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Returns endpoint and mode details, request payloads, raw XCrawl API responses, and error details when requests fail.]

## Skill Version(s):

1.0.2 (source: release evidence and skill metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
