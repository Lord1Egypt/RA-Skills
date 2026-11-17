## Description:

Web Search Instant uses the DuckDuckGo Instant Answer API to retrieve quick facts, definitions, calculations, conversions, abstracts, and related topics without requiring API credentials.

This skill is ready for commercial/non-commercial use.

## Publisher:

[86293073](https://clawhub.ai/user/86293073)

### License/Terms of Use:


## Use Case:

Developers, engineers, and agent users use this skill to run command-line web lookups for quick facts, definitions, calculations, conversions, and summaries when an instant answer is sufficient.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Search terms are sent to DuckDuckGo's Instant Answer API.

Mitigation: Do not use the skill for secrets, credentials, private internal project names, or sensitive personal data; narrow trigger rules where possible.

Risk: Instant answers may be incomplete, stale, or unavailable for recent news, real-time data, complex math, and some definitions.

Mitigation: Treat results as quick-lookups and verify important answers with the included source or full DuckDuckGo search link.

Risk: Fallback parsing without jq may mishandle some non-ASCII text and reduce output quality.

Mitigation: Install jq in environments where clean JSON parsing and character fidelity matter.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/86293073/skills/web-search-instant-1-1-0)
- [DuckDuckGo Instant Answer API documentation](https://duckduckgo.com/api)
- [DuckDuckGo Instant Answer API endpoint](https://api.duckduckgo.com/)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [CLI output in colored text, plain text, or Markdown]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes source URLs, fallback DuckDuckGo search URLs, and a configurable related-topic count.]

## Skill Version(s):

1.1.0 (source: artifact/_meta.json and CHANGELOG-v1.1.0.md; server release metadata reports 1.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
