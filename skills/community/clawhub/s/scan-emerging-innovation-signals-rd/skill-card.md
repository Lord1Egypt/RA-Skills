## Description:

Identify potentially protectable technical contributions in R&D updates, meeting notes, design documents, architecture descriptions, experiment records, and technical-improvement narratives. Use when a user asks what may be innovative, patent-review worthy, suitable for trade-secret review, or in need of invention-disclosure follow-up.

This skill is ready for commercial/non-commercial use.

## Publisher:

[yuanzhian-patsnap](https://clawhub.ai/user/yuanzhian-patsnap)

### License/Terms of Use:

MIT-0

## Use Case:

R&D contributors, IP teams, and technical reviewers use this skill to screen engineering materials for potentially protectable technical contributions, evidence gaps, disclosure urgency, and next review steps. It supports early triage for patent, trade-secret, defensive-publication, evidence-collection, monitoring, or archive decisions without making final legal determinations.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Confidential R&D details could be exposed through an external patent-search connector if the environment or audience is not authorized.

Mitigation: Use the skill only with approved PatSnap connector configurations and keep confidential source material within authorized channels.

Risk: Generated screening reports could be mistaken for final patentability, infringement, FTO, ownership, inventorship, or protection decisions.

Mitigation: Review reports before distribution and route outputs to qualified IP, counsel, security, ownership, or business reviewers as appropriate.

## Reference(s):

- [Follow-up Question Library](references/followup_questions.md)
- [Innovation Signal Radar HTML Report Template](references/html_template.md)
- [Innovation-Signal Extraction Standard](references/innovation_extraction_prompt.md)
- [Innovation Taxonomy](references/innovation_taxonomy.md)
- [PatSnap MCP Search Guide](references/mcp_usage_guide.md)
- [Screening and Technical-Evidence Criteria](references/patentability_criteria.md)
- [Protection-Path Decision Framework](references/protection_decision.md)
- [PatSnap Patent Search MCP](https://open.patsnap.com/marketplace/mcp-servers/patent-search)
- [PatSnap Patent Briefing MCP](https://open.patsnap.com/marketplace/mcp-servers/patent-briefing)

## Skill Output:

**Output Type(s):** [text, markdown, guidance]

**Output Format:** [Self-contained HTML report with structured screening analysis and concise follow-up guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs should preserve source locations, evidence gaps, search logs, limitations, and specialist-review requirements.]

## Skill Version(s):

1.0.0 (source: ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
