## Description:

Design and calibrate the Stage 3/4 tagging system for a patent-landscape program. Use after search-patents-ip and analyze-patent-search-results-ip to create a versioned four-column technology taxonomy, decision-relevant technical questions, evidence-backed patent groups, a reviewed tagging demonstration, and a complete empty-tag CSV for genuine human tagging at Stage 3.5; validate the returned tagged_pool.csv before routing to create-patent-search-report-ip.

This skill is ready for commercial/non-commercial use.

## Publisher:

[yuanzhian-patsnap](https://clawhub.ai/user/yuanzhian-patsnap)

### License/Terms of Use:

MIT-0

## Use Case:

External patent-landscape analysts, IP strategists, and supporting agent operators use this skill to design an evidence-backed taxonomy, create tagging examples and handoff files, and validate returned human tagging before downstream reporting.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Patent candidate files or MCP connector use may be unauthorized for the project, especially when data is confidential or licensed.

Mitigation: Confirm data rights, connector authorization, and the project privacy boundary before installation or use.

Risk: Full-pool tagging could be mistaken for completed human review if fields are auto-filled.

Mitigation: Keep human tag fields empty in to_be_tagged.csv and require authorized reviewers to complete Stage 3.5 before reporting.

Risk: Taxonomy labels, patent groups, or recommendations may become misleading if unsupported by patent evidence.

Mitigation: Trace every filled tag and package reason to evidence, preserve uncertainty states, and validate returned labels against the controlled taxonomy.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/yuanzhian-patsnap/skills/tag-patent-search-results-ip)
- [PatSnap Skill Hub](https://open.patsnap.com/marketplace/skill-hub)
- [PatSnap MCP marketplace](https://open.patsnap.com/marketplace/mcp-servers)
- [Deep Patent Mining MCP server](https://open.patsnap.com/marketplace/mcp-servers/patent-mining)
- [Patent Briefing MCP server](https://open.patsnap.com/marketplace/mcp-servers/patent-briefing)
- [Advanced Patent Search MCP server](https://open.patsnap.com/marketplace/mcp-servers/patent-search)
- [Global Core Patent Database MCP server](https://open.patsnap.com/marketplace/mcp-servers/core-patents)

## Skill Output:

**Output Type(s):** [Files, JSON, CSV, Guidance, Validation summary]

**Output Format:** [Markdown guidance with JSON and CSV artifact outputs]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces tech_breakdown.json, key_questions.json, patent_packages.csv, tagging_demo_sample.csv, to_be_tagged.csv, and validation feedback for returned tagged_pool.csv.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
