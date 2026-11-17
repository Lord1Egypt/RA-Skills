## Description:

Extracts article content from URLs as clean Markdown, using Scrapling first with fast-to-stealth fallback and Jina Reader as an alternate path for simple pages.

This skill is ready for commercial/non-commercial use.

## Publisher:

[haanya168](https://clawhub.ai/user/haanya168)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent users use this skill to fetch readable article content from public web pages, including WeChat articles, blogs, news posts, and documentation pages. It is useful when an agent needs URL content converted into Markdown for reading, summarization, or downstream processing.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can fetch arbitrary URLs from the agent environment.

Mitigation: Use it only for URLs the user is authorized to access, and avoid private, internal, authenticated, signed, or token-bearing URLs unless exposure has been reviewed.

Risk: The fallback path may send URLs to a third-party reader service.

Mitigation: Disable or require explicit confirmation before using the Jina Reader fallback for sensitive URLs.

Risk: Runtime behavior depends on installed Python packages.

Mitigation: Install in a virtual environment and pin dependency versions before deployment.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/haanya168/skills/web-content-fetcher-hanya)
- [Python](https://www.python.org/)

## Skill Output:

**Output Type(s):** [markdown, text, json, guidance]

**Output Format:** [Markdown by default; JSON with URL, mode, selector, content length, and content when JSON output is requested.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Default output is capped at 30000 characters unless the caller supplies a different max_chars value.]

## Skill Version(s):

0.0.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
