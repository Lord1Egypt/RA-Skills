## Description:

Web search via Tavily API with built-in monthly usage tracking and quota management for agents that need sourced search results.

This skill is ready for commercial/non-commercial use.

## Publisher:

[neverland83](https://clawhub.ai/user/neverland83)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to run Tavily-backed web searches, return Markdown or JSON results, and track monthly search usage against a configurable quota.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Search queries and the Tavily API key are sent to Tavily.

Mitigation: Keep sensitive or private content out of search queries and protect the Tavily API key.

Risk: The local usage counter may not match Tavily service-side usage in every situation.

Mitigation: Review the local usage counter and Tavily account usage when quota tracking matters.

## Reference(s):

- [Tavily Metered Search on ClawHub](https://clawhub.ai/neverland83/skills/tavily-metered-search)
- [Tavily](https://tavily.com)

## Skill Output:

**Output Type(s):** [text, markdown, json, configuration]

**Output Format:** [Markdown search results or JSON objects]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Can include an optional short answer and monthly usage warnings; max results is capped at 10.]

## Skill Version(s):

1.0.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
