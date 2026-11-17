## Description:

Fetch any URL as clean, AI-ready Markdown with token counts and caching. Strip ads, nav, scripts, and noise from web pages.

This skill is ready for commercial/non-commercial use.

## Publisher:

[atlasopenclaw](https://clawhub.ai/user/atlasopenclaw)

### License/Terms of Use:


## Use Case:

Developers and agents use StripFeed to fetch public web pages, articles, and documentation as cleaner Markdown with token counts for context planning.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Requested URLs and retrieved page content are processed by StripFeed's external API.

Mitigation: Avoid internal systems, signed links, secret-bearing query strings, authenticated private documents, and regulated data unless that disclosure is explicitly accepted.

Risk: Cached responses may be stale or retained longer than expected for time-sensitive content.

Mitigation: Use cache=false when freshness or retention matters.

## Reference(s):

- [StripFeed homepage](https://www.stripfeed.dev)
- [ClawHub StripFeed skill page](https://clawhub.ai/atlasopenclaw/skills/stripfeed)

## Skill Output:

**Output Type(s):** [markdown, text, json, shell commands, configuration, guidance]

**Output Format:** [Markdown, text, JSON, or HTML returned by the StripFeed API, with curl command examples in the skill instructions.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires STRIPFEED_API_KEY and curl; supports caching, token counts, optional max_tokens truncation, selectors, and batch requests depending on plan.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
