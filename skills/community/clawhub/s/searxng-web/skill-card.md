## Description:

Proxies search queries to a local SearXNG instance and returns JSON-formatted search results with titles, URLs, snippets, and sources.

This skill is ready for commercial/non-commercial use.

## Publisher:

[zomgirprogrammer](https://clawhub.ai/user/zomgirprogrammer)

### License/Terms of Use:


## Use Case:

Agents and developers use this skill to run web searches through a trusted local SearXNG service and receive normalized result metadata for downstream tasks.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Search queries are visible to the local SearXNG service at host.docker.internal:8081.

Mitigation: Install only when that SearXNG service is controlled and trusted, and avoid sending secrets or highly sensitive text.

Risk: The security evidence notes documentation and hardening gaps, including missing request timeouts and size limits.

Mitigation: Add request timeouts, response size limits, and clearer operational documentation before broad deployment.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/zomgirprogrammer/skills/searxng-web)
- [Publisher profile](https://clawhub.ai/user/zomgirprogrammer)

## Skill Output:

**Output Type(s):** [Text, JSON]

**Output Format:** [JSON object containing query, count, and normalized search results]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Result count is clamped from 1 to 10.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
