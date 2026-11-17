## Description:

AI-powered semantic lead prospecting that discovers, qualifies, and enriches high-intent business opportunities from public web communities, forums, Reddit, and other public discussions.

This skill is ready for commercial/non-commercial use.

## Publisher:

[simplysemantics](https://clawhub.ai/user/simplysemantics)

### License/Terms of Use:

MIT

## Use Case:

External developers, sales teams, SaaS companies, consultants, agencies, and AI builders use this skill to turn public discussion signals into prioritized lead records for review, outreach planning, enrichment, or agent handoff.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Prospecting criteria are sent to Simply Semantics and discovered public lead records are stored in the user's account.

Mitigation: Use the skill only for criteria and account data acceptable for Simply Semantics processing and storage.

Risk: Lead exports or outreach may be subject to source community terms, privacy requirements, and applicable outreach rules.

Mitigation: Review community terms and applicable privacy or outreach rules before exporting, contacting, or automating follow-up with leads.

Risk: New accounts may return mock test data when no real search strategy is selected.

Mitigation: Set strategy to brave or llm for real searches and check is_mock or search_strategy before treating results as real leads.

## Reference(s):

- [Semantic Prospect product page](https://www.simplysemantics.com/semantic-prospect.html)
- [Semantic Prospect ClawHub listing](https://clawhub.ai/simplysemantics/skills/semantic-prospect)
- [Semantic Prospect API endpoint](https://dashboard.simplysemantics.com/sp/mcp/forum-leads-api)

## Skill Output:

**Output Type(s):** [text, markdown, API calls, configuration, guidance]

**Output Format:** [Markdown summary with structured lead records from JSON API responses]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires SIMPLY_SEMANTICS_API_KEY; real lead searches should explicitly set strategy to brave or llm.]

## Skill Version(s):

1.0.1 (source: server release metadata and artifact/clawhub.json; artifact/SKILL.md and artifact/CHANGELOG.txt list 1.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
