## Description:

Fetches WeChat public account article links and returns the article as Markdown or text through a public third-party service, without requiring an API key.

This skill is ready for commercial/non-commercial use.

## Publisher:

[alexduming](https://clawhub.ai/user/alexduming)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to convert WeChat public account article URLs into Markdown or plain text for downstream reading, summarization, or archiving workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: WeChat article URLs are sent to the public down.mptext.top service.

Mitigation: Use only for public or non-sensitive links unless the user has reviewed and accepts that service's handling of request data.

Risk: Some articles may be blocked, truncated, or unavailable due to anti-scraping controls, repost restrictions, or temporary image links.

Mitigation: Check fetched output for completeness and retry with text format or save referenced images promptly when needed.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/alexduming/skills/wechat-article-fetcher-alexdu)
- [mptext.top public download service](https://down.mptext.top)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Code, Guidance]

**Output Format:** [Markdown or plain text returned from the public article download API, with optional shell or Python command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires a WeChat article URL and sends it to down.mptext.top; no API key is required.]

## Skill Version(s):

1.0.0 (source: release evidence and artifact metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
