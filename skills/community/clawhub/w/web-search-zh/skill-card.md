## Description:

Searches the public web through the AISA API and returns structured titles, links, and summaries for agents that need online lookup or recent sources.

This skill is ready for commercial/non-commercial use.

## Publisher:

[aisadocs](https://clawhub.ai/user/aisadocs)

### License/Terms of Use:

MIT-0

## Use Case:

External users and agents use this skill to retrieve public internet search results, links, and summaries for current web research. The bundled CLI also exposes URL extraction, academic search, multi-source search, and AI synthesis modes that reviewers should consider when approving deployment.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: User queries, supplied URLs, and aggregated search results are sent to AISA endpoints.

Mitigation: Use the skill only for public-internet research and avoid submitting secrets, credentials, private URLs, or confidential business data.

Risk: The shipped CLI exposes URL extraction and AI synthesis modes that are broader than the public web-search description.

Mitigation: Review available CLI subcommands before deployment and restrict agent use to the intended search mode when narrower behavior is required.

Risk: Search summaries and AI synthesis can be incomplete, stale, or misleading.

Mitigation: Require source review and citation checks before acting on returned results.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/aisadocs/skills/web-search-zh)
- [AISA Website](https://aisa.one)
- [AISA API Base URL](https://api.aisa.one/apis/v1)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Markdown or terminal text with structured result titles, links, summaries, citations, and status messages.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires python3 and AISA_API_KEY; sends user queries, supplied URLs, and search results to AISA API endpoints.]

## Skill Version(s):

1.0.0 (source: release metadata and skill frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
