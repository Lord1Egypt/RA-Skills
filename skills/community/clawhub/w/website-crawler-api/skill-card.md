## Description:

Helps agents map website URLs, crawl sites, and batch-extract pages into Markdown or other text formats through Scavio.

This skill is ready for commercial/non-commercial use.

## Publisher:

[scavio-ai](https://clawhub.ai/user/scavio-ai)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and other agents use this skill to discover site URLs or turn documentation, blogs, and other authorized web pages into content for knowledge bases and retrieval workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Target URLs and extracted page content are sent through Scavio's API.

Mitigation: Use only authorized, non-private URLs and confirm the user is comfortable sending this content to Scavio.

Risk: Larger crawl and batch jobs can consume paid API credits.

Mitigation: Scope jobs to needed pages and confirm the maximum credit cost before large runs.

Risk: Exposing the Scavio API key can allow unauthorized use.

Mitigation: Keep SCAVIO_API_KEY in a secret store or environment variable and out of source control.

## Reference(s):

- [ClawHub skill release](https://clawhub.ai/scavio-ai/skills/website-crawler-api)
- [Scavio Website Crawler API](https://scavio.dev/website-crawler-api?utm_source=agent-skills&utm_medium=skill&utm_campaign=website-crawler-api)
- [Map API documentation](https://scavio.dev/docs/extract-map?utm_source=agent-skills&utm_medium=skill&utm_campaign=website-crawler-api)
- [Crawl API documentation](https://scavio.dev/docs/extract-crawl?utm_source=agent-skills&utm_medium=skill&utm_campaign=website-crawler-api)
- [Batch API documentation](https://scavio.dev/docs/extract-batch?utm_source=agent-skills&utm_medium=skill&utm_campaign=website-crawler-api)

## Skill Output:

**Output Type(s):** [Guidance, Markdown, Shell commands, Code]

**Output Format:** [Markdown with URL lists, code blocks, and JSON response examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Source URLs can accompany extracted page content.]

## Skill Version(s):

1.0.0 (source: frontmatter and ClawHub release)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
