## Description:

Priority live web search for real-time information

This skill is ready for commercial/non-commercial use.

## Publisher:

[ytthuan](https://clawhub.ai/user/ytthuan)

### License/Terms of Use:


## Use Case:

External users and developers use this skill to have an agent look up recent information on a topic, prioritize current authoritative sources, summarize findings, and disclose when live search is unavailable or incomplete.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Search queries can disclose sensitive topics to the web search provider.

Mitigation: Avoid highly sensitive private details in search prompts unless that data sharing is acceptable.

Risk: Live search results may be incomplete, outdated, or unavailable if the host model does not support the required web search tool.

Mitigation: Prefer recent authoritative sources, clearly summarize uncertainty, and disclose fallback behavior when live search is unsupported.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/ytthuan/skills/super-websearch-realtime)

## Skill Output:

**Output Type(s):** [Text, Markdown, Guidance]

**Output Format:** [Natural-language response, typically Markdown]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include summarized current-source findings when the host agent supports live web search.]

## Skill Version(s):

1.0.0 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
