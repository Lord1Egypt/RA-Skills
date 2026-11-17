## Description:

Provides OpenClaw agents with a local SearXNG search helper that queries a trusted localhost SearXNG instance and returns agent-friendly Markdown search results.

This skill is ready for commercial/non-commercial use.

## Publisher:

[upsurge911-lgtm](https://clawhub.ai/user/upsurge911-lgtm)

### License/Terms of Use:


## Use Case:

Developers and agent operators use this skill to run local SearXNG queries for market intelligence, technical research, real-time briefings, and data-sovereignty-sensitive searches, with results formatted for agent ingestion.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill depends on a local SearXNG service, so search privacy depends on how that service is deployed, logged, and configured.

Mitigation: Run it only against a trusted SearXNG instance bound to loopback or a trusted Docker network, and review enabled engines and logging before sensitive searches.

Risk: The documentation makes strong privacy claims that the security evidence characterizes as overclaiming.

Mitigation: Treat the skill as a local search helper rather than a complete privacy guarantee, and validate the SearXNG deployment against organizational data-handling requirements.

Risk: Default output appends Upsurge attribution, which may be inappropriate in some downstream agent reports.

Mitigation: Review generated Markdown before external use and adjust downstream formatting policies where attribution is not desired.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/upsurge911-lgtm/skills/upsurge-searxng)
- [Expected local SearXNG service](http://localhost:8080)
- [Expected SearXNG search endpoint](http://localhost:8080/search)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Markdown search results with result titles, source URLs, snippets, and an optional time-filter note]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires a trusted local SearXNG service at http://localhost:8080; defaults to English results with safe search enabled.]

## Skill Version(s):

1.4.0 (source: server release metadata and SKILL.md frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
