## Description:

Execute a user-supplied PatSnap advanced patent query containing field operators such as ANCS:, TAC_ALL:, DESC_B:, MAINF:, ALL_AN:, PN:, APD:, PBD:, APNO:, or PRNO:, then generate an evidence-backed competitor patent report with portfolio counts, company-level technical summaries, hierarchical patent details, optional literature context, Markdown output, and an accessible HTML rendering.

This skill is ready for commercial/non-commercial use.

## Publisher:

[yuanzhian-patsnap](https://clawhub.ai/user/yuanzhian-patsnap)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to run advanced PatSnap patent queries and produce evidence-backed competitor patent reports. It is intended for workflows that need portfolio counts, company-level technology summaries, patent-detail grouping, and optional literature context.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: REST fallback endpoint and image-download handling could expose credentials, research queries, or writable files.

Mitigation: Run only in a constrained environment with narrowly scoped PatSnap credentials and approved HTTPS PatSnap endpoints; avoid enabling REST or literature credentials unless endpoints are centrally controlled.

Risk: Patent or literature results may be partial, unverified, noisy, or unavailable when access, schema, pagination, or optional connectors fail.

Mitigation: Require verified PatSnap access, preserve source notes and result caps in reports, label partial data explicitly, and skip literature retrieval when no verified connector is configured.

Risk: Generated competitor summaries could be misleading if synthesized from sparse or ambiguous evidence.

Mitigation: Keep retrieved facts separate from AI interpretation, link material claims to retrieved records, and omit summaries when evidence is too sparse.

## Reference(s):

- [PatSnap Advanced Patent Search MCP server](https://open.patsnap.com/marketplace/mcp-servers/patent-search)
- [PatSnap Patent Briefing MCP server](https://open.patsnap.com/marketplace/mcp-servers/patent-briefing)
- [ClawHub skill page](https://clawhub.ai/yuanzhian-patsnap/skills/run-advanced-patent-query-ip)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown report, accessible HTML report, and concise conversation summary with saved report paths]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Records query metadata, result caps, retrieval dates, counting units, source notes, and partial-data limitations when applicable.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
