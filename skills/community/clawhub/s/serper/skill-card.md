## Description:

Serper lets an agent run Google searches through the Serper API and enrich results with extracted full-page content.

This skill is ready for commercial/non-commercial use.

## Publisher:

[nesdeq](https://clawhub.ai/user/nesdeq)

### License/Terms of Use:

MIT

## Use Case:

External developers and agent operators use this skill to answer current or research questions by retrieving Google Search and Google News results with extracted page text.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill automatically fetches search-result pages, which can reach destinations the agent did not explicitly vet.

Mitigation: Review before installing on machines with private network, local admin panel, cloud metadata, or sensitive intranet access; use a restricted network environment where possible.

Risk: Search queries and requests are sent to an external Serper API service.

Mitigation: Avoid sensitive search queries and keep the Serper API key in a private skill-local environment file.

Risk: Dependency behavior can change if runtime packages are installed without pinning.

Mitigation: Prefer pinned dependencies and scan the skill before deployment.

## Reference(s):

- [Serper API](https://serper.dev)
- [ClawHub skill page](https://clawhub.ai/nesdeq/skills/serper)
- [README](README.md)

## Skill Output:

**Output Type(s):** [text, JSON, shell commands, guidance]

**Output Format:** [Streamed JSON array with search metadata, result URLs, source labels, dates when available, and extracted page content.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires SERPER_API_KEY or SERP_API_KEY; default mode returns 5 web results and current mode combines recent web and news results.]

## Skill Version(s):

3.0.2 (source: server release metadata; artifact metadata reports 3.0.1)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
