## Description:

Summarize any web page by URL into a concise structured brief.

This skill is ready for commercial/non-commercial use.

## Publisher:

[terrycarter1985](https://clawhub.ai/user/terrycarter1985)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to summarize one or more web pages from URLs into concise structured briefs for quick review or comparison.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The bundled script returns an empty summary skeleton, so relying on the script alone may produce incomplete output.

Mitigation: Have the agent retrieve and inspect the target page content with its web tools before presenting a summary, and verify that key points and overview fields are populated.

Risk: Summarizing private or internal URLs can expose sensitive content to the agent workflow.

Mitigation: Use only URLs the user intends the agent to retrieve and process, and avoid private or sensitive links unless that handling is approved.

## Reference(s):


## Skill Output:

**Output Type(s):** [text, markdown, shell commands]

**Output Format:** [Markdown summary with optional JSON skeleton output from summarize_url.py]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Each URL summary is expected to include a title, source URL, key points, and a brief overview; batch requests may be aggregated in a comparison table.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
