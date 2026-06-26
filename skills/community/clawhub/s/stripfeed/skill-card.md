## Description: <br>
Fetch URLs as clean, AI-ready Markdown with token counts and caching. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[AtlasOpenclaw](https://clawhub.ai/user/AtlasOpenclaw) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and agents use StripFeed to fetch public web pages, articles, or documentation as cleaner Markdown for LLM context, with optional JSON metadata, token counts, caching controls, and batch requests. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Target URLs and fetched page content are sent to StripFeed's external service, and the server evidence notes a privacy disclosure gap. <br>
Mitigation: Avoid internal systems, private documentation, authenticated pages, signed URLs, URLs containing tokens, and regulated data unless approved and the provider's retention and caching behavior is understood. <br>


## Reference(s): <br>
- [StripFeed homepage](https://www.stripfeed.dev) <br>
- [StripFeed fetch API](https://www.stripfeed.dev/api/v1/fetch?url=URL_HERE) <br>
- [StripFeed batch API](https://www.stripfeed.dev/api/v1/batch) <br>


## Skill Output: <br>
**Output Type(s):** [Markdown, Text, JSON, Shell commands, Guidance] <br>
**Output Format:** [Markdown or JSON returned from the StripFeed API, with curl examples and request guidance.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires STRIPFEED_API_KEY; responses can include token counts, cache status, selectors, truncation status, and batch result metadata.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
