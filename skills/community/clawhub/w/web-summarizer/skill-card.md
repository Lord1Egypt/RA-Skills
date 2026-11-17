## Description:

Summarize any web page by URL or by pasting text, returning a concise structured summary with key points, entities, and action items.

This skill is ready for commercial/non-commercial use.

## Publisher:

[terrycarter1985](https://clawhub.ai/user/terrycarter1985)

### License/Terms of Use:

MIT-0

## Use Case:

External users, employees, and developers use this skill to turn a URL or pasted text into a quick digest with a TL;DR, key takeaways, named entities, and action items.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Broad prompts such as "what's this about" may activate summarization when the user's intent is ambiguous.

Mitigation: Confirm or preserve the user's intended task when a URL or pasted text could reasonably require something other than summarization.

Risk: URL fetching can be incomplete when a site restricts access through paywalls, robots.txt, or site terms.

Mitigation: State access limits clearly and summarize only the content that is available to the agent.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/terrycarter1985/skills/web-summarizer)

## Skill Output:

**Output Type(s):** [Text, Markdown, Guidance]

**Output Format:** [Concise structured Markdown summary with a TL;DR, bullet points, named entities, and action items.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Summaries depend on the accessible source content and may be limited by paywalls, robots.txt, or site terms.]

## Skill Version(s):

1.0.0 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
