## Description:

Build and validate expert patent-search branches for Stage 1/4 of a patent-landscape program.

This skill is ready for commercial/non-commercial use.

## Publisher:

[yuanzhian-patsnap](https://clawhub.ai/user/yuanzhian-patsnap)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, patent analysts, and IP teams use this skill to turn a confirmed landscape objective into auditable search branches, validation evidence, and traceable handoff artifacts for downstream patent-landscape analysis.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Patent search scopes, seed records, terminology, and business strategy may be confidential when sent to referenced PatSnap connectors.

Mitigation: Confirm authorization and confidentiality boundaries before using connectors, and only process user-approved scope and patent evidence.

Risk: Live patent-search schemas, field names, proximity operators, result caps, or ranking signals may differ from examples in the artifact.

Mitigation: Inspect the active connector schema before use, record schema and data-cutoff provenance, and disclose fallbacks, capped retrieval, or provisional branches.

Risk: Search branches, recall sets, and preliminary taxonomy paths can be over-interpreted as final patent landscape findings.

Mitigation: Limit Stage 1 outputs to validated search handoff artifacts and label the taxonomy as preliminary pending downstream and human review.

## Reference(s):

- [Query and Preliminary Taxonomy Methodology](references/query-and-taxonomy-methodology.md)
- [PatSnap Advanced Patent Search MCP](https://open.patsnap.com/marketplace/mcp-servers/patent-search)
- [PatSnap Patent Briefing MCP](https://open.patsnap.com/marketplace/mcp-servers/patent-briefing)
- [PatSnap Deep Patent Mining MCP](https://open.patsnap.com/marketplace/mcp-servers/patent-mining)
- [PatSnap Global Core Patent Database MCP](https://open.patsnap.com/marketplace/mcp-servers/core-patents)
- [PatSnap Skill Hub](https://open.patsnap.com/marketplace/skill-hub)
- [PatSnap MCP Marketplace](https://open.patsnap.com/marketplace/mcp-servers)

## Skill Output:

**Output Type(s):** [Files, JSON, CSV, Text, Guidance]

**Output Format:** [Markdown response plus generated JSON, CSV, and plain-text handoff files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces search_config.json, candidate_pool.csv, core_recall.csv, run_config.json, and preliminary tech_taxonomy.txt when scope and connector data are available.]

## Skill Version(s):

1.0.0 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
