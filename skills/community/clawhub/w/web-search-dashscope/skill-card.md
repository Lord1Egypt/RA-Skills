## Description:

Provides real-time internet search through the Serper API, returning Google Search-based results for OpenClaw users.

This skill is ready for commercial/non-commercial use.

## Publisher:

[tom859174-sketch](https://clawhub.ai/user/tom859174-sketch)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and OpenClaw users use this skill to retrieve current web search results, weather, news, market information, and technical-documentation links from Serper-backed Google Search results.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The artifact includes a hardcoded Serper API key and directs users to edit source code for credentials.

Mitigation: Remove and rotate the packaged key, then load credentials from an environment variable or secret store before deployment.

Risk: Search queries are sent to the Serper service.

Mitigation: Disclose the third-party search provider to users and avoid submitting confidential queries unless that use is approved.

Risk: The security verdict is suspicious even though the behavior is ordinary web search.

Mitigation: Review and scan the skill before installing or running it in an agent environment.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/tom859174-sketch/skills/web-search-dashscope)
- [Serper](https://serper.dev/)
- [Serper API key documentation](https://serper.dev/api-key)
- [Serper Google Search endpoint](https://google.serper.dev/search)

## Skill Output:

**Output Type(s):** [text, JSON, shell commands, configuration]

**Output Format:** [JSON-RPC-style JSON containing text search results]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Search result count is clamped from 1 to 10.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
