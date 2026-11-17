## Description:

Search patents owned or filed by one or more specified applicants within a defined technology topic. Use when an IP searcher or analyst needs an applicant-first, topic-constrained PatSnap strategy; evidence-backed assignee expansion; auditable PatSnap formulas; executed retrieval and deduplicated datasets; or a Markdown and Word retrieval report. Do not use for an unconstrained applicant portfolio dump, an applicant-free technology landscape, or downstream technical tagging after retrieval.

This skill is ready for commercial/non-commercial use.

## Publisher:

[yuanzhian-patsnap](https://clawhub.ai/user/yuanzhian-patsnap)

### License/Terms of Use:

MIT-0

## Use Case:

IP searchers, patent analysts, and developers use this skill to build applicant-first, topic-constrained PatSnap patent search strategies, formulas, retrieval reports, and optional deduplicated datasets. It is suited for auditable workflows that must preserve applicant expansion, topic boundaries, query provenance, and retrieval gates.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: PatSnap API keys or generated connection URLs could be exposed if copied into reports, logs, or the skill package.

Mitigation: Configure PatSnap access through the client connection flow, keep keys out of reports and versioned files, and rotate or revoke any exposed key.

Risk: Users may expect executed retrieval when PatSnap access is not configured or live retrieval was not explicitly requested.

Mitigation: Use formula_only_mode unless the user requests retrieval and a configured PatSnap account is available; do not fabricate counts, records, or datasets.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/yuanzhian-patsnap/skills/search-applicant-technology-patents-ip)
- [Applicant-topic patent retrieval workflow](references/applicant-retrieval-workflow.md)
- [Topic limitation workflow](references/topic-limitation-workflow.md)
- [PatSnap Open Platform](https://open.patsnap.com/)
- [PatSnap authentication guide](https://open.patsnap.com/devportal/guides/authentication)
- [Advanced Patent Search MCP server](https://open.patsnap.com/marketplace/mcp-servers/patent-search)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance, Files]

**Output Format:** [Markdown reports with PatSnap formulas, tables, execution checklists, optional DOCX reports, and optional dataset exports]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Supports formula-only output by default; live retrieval and dataset preparation require explicit user request, PatSnap access, and successful pre-retrieval gates.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
