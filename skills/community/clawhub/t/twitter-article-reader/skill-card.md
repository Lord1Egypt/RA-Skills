## Description:

Extracts readable markdown content from Twitter/X articles and tweets through r.jina.ai for user-provided Twitter/X URLs.

This skill is ready for commercial/non-commercial use.

## Publisher:

[showjim](https://clawhub.ai/user/showjim)

### License/Terms of Use:

MIT-0

## Use Case:

External users and agents use this skill to read Twitter/X articles or tweets as clean markdown when direct access is blocked or inconvenient.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Twitter/X URLs are fetched through r.jina.ai, so a third-party relay may receive the URL and normal request metadata.

Mitigation: Avoid using the skill for private, access-controlled, or sensitive Twitter/X links unless that relay exposure is acceptable.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/showjim/skills/twitter-article-reader)
- [Publisher profile](https://clawhub.ai/user/showjim)

## Skill Output:

**Output Type(s):** [text, markdown, guidance]

**Output Format:** [Markdown text]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May preserve tweet images as markdown image links.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
