## Description:

Crawl entire websites using the Scrapfly Crawler API with the Python SDK.

This skill is ready for commercial/non-commercial use.

## Publisher:

[scrapfly](https://clawhub.ai/user/scrapfly)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to configure Scrapfly crawler jobs for site-wide crawling, URL discovery, bulk content retrieval, structured extraction, and WARC/HAR archive downloads.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Crawls may reach sensitive, private, large, or unintended sites if scope settings are too broad.

Mitigation: Review crawl limits, include and exclude paths, external-link settings, and robots.txt handling before running crawler jobs.

Risk: The skill uses a third-party crawling service and requires a Scrapfly API key.

Mitigation: Install only when Scrapfly use is intended, run from a dedicated environment, and manage the API key through environment variables or equivalent secret handling.

Risk: Examples can download and save crawl archives or generated text files locally.

Mitigation: Confirm archive paths and output locations before running examples on sensitive sites or large crawls.

## Reference(s):

- [Scrapfly Crawler ClawHub page](https://clawhub.ai/scrapfly/skills/scrapfly-crawler)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration instructions, Guidance]

**Output Format:** [Markdown guidance with inline Python and bash examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires a Scrapfly API key; examples may call the Scrapfly API and write WARC/HAR archives or llms-full.txt when used.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
