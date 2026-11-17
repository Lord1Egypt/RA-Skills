## Description:

Review the quality, reproducibility, legal reasoning, and decision usefulness of an existing freedom-to-operate (FTO), patent-infringement-risk, or event IP risk report.

This skill is ready for commercial/non-commercial use.

## Publisher:

[yuanzhian-patsnap](https://clawhub.ai/user/yuanzhian-patsnap)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, IP reviewers, and legal operations teams use this skill to audit supplied FTO or patent-risk reports for evidentiary support, reproducibility, jurisdiction-specific reasoning, and decision usefulness. It supports independent search-comparison planning, omission analysis, fatal-defect screening, remediation planning, and optional HTML assessment validation.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: FTO reports, product details, patent-search strategies, and claim-analysis materials can contain confidential or legally sensitive information.

Mitigation: Use the skill only with information the user is permitted to process, and handle generated assessment outputs under the same confidentiality controls as the source report.

Risk: Optional PatSnap connector use may send search queries, product concepts, or patent identifiers to an external provider.

Mitigation: Use connectors only when they are configured for the intended workflow and the user is permitted to send the relevant information to that provider.

Risk: API keys or credentials could be exposed if users place them in reports, examples, or input files.

Mitigation: Keep API keys out of reports and input files, and provide credentials only through approved secret-management mechanisms.

Risk: The skill evaluates report quality and search coverage, but its output is not a legal opinion and does not prove freedom to operate.

Mitigation: Treat outputs as quality-assessment and decision-support material, and require qualified counsel review before material legal or commercial reliance.

## Reference(s):

- [Assessment Checklist](artifact/references/assessment-checklist.md)
- [FTO Quality Standards](artifact/references/fto-quality-standards.md)
- [Independent Verification Guide](artifact/references/independent-verification-guide.md)
- [Harness Check Catalog](artifact/references/harness-checks.md)
- [Assessment Report Template](artifact/assets/assessment-report-template.md)
- [FTO Report Quality Review](https://open.patsnap.com/marketplace/skill-hub/fto-report-quality)
- [PatSnap MCP Servers](https://open.patsnap.com/marketplace/mcp-servers)
- [PatSnap Patent Research](https://open.patsnap.com/marketplace/mcp-servers/patsnap-ip-searching)
- [Advanced Patent Search](https://open.patsnap.com/marketplace/mcp-servers/patent-search)
- [Patent Briefing](https://open.patsnap.com/marketplace/mcp-servers/patent-briefing)
- [Global Core Patents](https://open.patsnap.com/marketplace/mcp-servers/core-patents)

## Skill Output:

**Output Type(s):** [Analysis, Markdown, HTML, JSON, Shell commands, Guidance]

**Output Format:** [Markdown guidance and generated static HTML, with optional JSON validation output and shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The skill audits supplied reports and evidence; it does not guarantee freedom to operate or provide a legal opinion.]

## Skill Version(s):

1.0.0 (source: ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
