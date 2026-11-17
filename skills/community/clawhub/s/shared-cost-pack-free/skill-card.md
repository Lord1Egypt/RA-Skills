## Description:

Checks shared-cost and allocation worksheets for multiple store directories across six fee categories, printing one conclusion line per store with source file and line citations.

This skill is ready for commercial/non-commercial use.

## Publisher:

[chenqg618](https://clawhub.ai/user/chenqg618)

### License/Terms of Use:

MIT-0

## Use Case:

Finance and cost-accounting teams use this skill before monthly or quarterly cost allocation to run six arithmetic and cross-table checks for each store or project and identify line-cited discrepancies or missing materials.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Users may treat arithmetic and reconciliation findings as accounting, tax, audit, banking, insurance, invoice-authenticity, or policy conclusions.

Mitigation: Use the output as reconciliation support only; have qualified reviewers handle professional judgments, external-system verification, invoices, and tax or audit decisions.

Risk: Store and accounting materials can contain sensitive business data.

Mitigation: Run the checker only in a trusted local environment; the authoritative ClawHub security evidence reports no hidden network use, file writing, persistence, or privilege escalation.

Risk: Missing, incomplete, or unrecognized tabular materials can produce a not-run or insufficient-input result instead of a pass.

Mitigation: Provide complete per-store text or JSON inputs in the documented format and treat not-run or insufficient-input statuses as unresolved review items.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/chenqg618/skills/shared-cost-pack-free)
- [Artifact skill documentation](artifact/SKILL.md)
- [Sample input template](artifact/templates/sample.json)

## Skill Output:

**Output Type(s):** [Text, JSON, Shell commands, Guidance]

**Output Format:** [Human-readable console report, with optional JSON output when run with --json]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Findings cite the store, check, source file, and line when available; results are printed to stdout.]

## Skill Version(s):

1.0.21 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
