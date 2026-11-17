## Description:

Performs web searches through a local SearXNG-backed command and returns raw search results for a given query.

This skill is ready for commercial/non-commercial use.

## Publisher:

[netobasilio](https://clawhub.ai/user/netobasilio)

### License/Terms of Use:


## Use Case:

Developers and agents use this skill to retrieve up-to-date web search results from a controlled local SearXNG setup. It is suited for workflows that need search results without relying on paid search APIs.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill delegates user-provided searches to a host command and configured local SearXNG service.

Mitigation: Install it only where /usr/local/bin/websearch and the SearXNG instance are trusted and controlled.

Risk: Search results may contain untrusted or misleading web content.

Mitigation: Review returned results before using them for decisions, generated code, or downstream actions.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/netobasilio/skills/websearch)

## Skill Output:

**Output Type(s):** [text]

**Output Format:** [String; raw SearXNG results as JSON or text depending on local configuration]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires a trusted executable at /usr/local/bin/websearch and an accessible SearXNG instance.]

## Skill Version(s):

1.0.0 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
