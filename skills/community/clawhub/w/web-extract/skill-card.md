## Description:

Web Extract lets agents extract structured JSON, markdown, or raw HTML from individual pages, JavaScript-rendered pages, Google search results, URL maps, and recursive crawls through ZooData WebTools.

This skill is ready for commercial/non-commercial use.

## Publisher:

[apiclaw](https://clawhub.ai/user/apiclaw)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to collect structured page data, search-result content, URL inventories, and crawl results from the open web when downstream workflows need machine-readable fields instead of screenshots or prose-only fetches.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Requested URLs, search queries, crawl options, and the ZooData API key are sent to ZooData.

Mitigation: Use the skill only for data you are permitted to send to ZooData, prefer ZOODATA_API_KEY in the environment, and keep any ~/.zoodata/config.json file private.

Risk: Broad crawls, polling, and deep-scraped searches can consume paid credits.

Mitigation: Confirm crawl scope, result limits, polling intervals, and estimated credit use before submitting large jobs.

Risk: A successful API response can still contain a target site's error page or incomplete extraction.

Mitigation: Check response status metadata and validate extracted fields before relying on results.

## Reference(s):

- [Web Extract endpoint reference](references/reference.md)
- [ZooData API keys](https://zoodata.ai/en/api-keys)
- [ZooData pricing](https://zoodata.ai/en/pricing)
- [Skill homepage](https://github.com/SerendipityOneInc/ZooData-Skills)
- [ClawHub skill page](https://clawhub.ai/apiclaw/skills/web-extract)

## Skill Output:

**Output Type(s):** [JSON, Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [JSON-first CLI/API responses with optional Markdown or raw HTML page content]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires ZOODATA_API_KEY and may consume ZooData credits for API calls.]

## Skill Version(s):

0.2.4 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
