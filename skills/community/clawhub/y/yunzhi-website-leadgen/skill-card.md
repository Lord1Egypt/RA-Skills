## Description:

Audits a website's lead-generation funnel, scores pages and forms with a Python script, proposes five prioritized CRO improvements, and can apply approved low-risk CMS changes through MCP tools.

This skill is ready for commercial/non-commercial use.

## Publisher:

[hsqduron](https://clawhub.ai/user/hsqduron)

### License/Terms of Use:

MIT-0

## Use Case:

External site owners, marketers, and developers use this skill to audit website CRO and lead-capture funnels, produce a scored report, and identify five prioritized optimization actions. With authorized MCP credentials and explicit approval, it can help apply low-risk CMS updates such as CTA, trust-signal, product, and form improvements.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The crawler can fetch arbitrary user-provided URLs.

Mitigation: Audit only sites the user is authorized to test, and run crawling from a network sandbox that cannot reach internal services or cloud metadata.

Risk: MCP credentials can allow the agent to read site data and make live CMS changes.

Mitigation: Request MCP Bearer Tokens only for authorized write-back work, keep tokens out of files and chat output, test connectivity first, and require explicit confirmation before each write.

Risk: Lead-generation forms may collect personal data.

Mitigation: Add privacy and consent text before collecting contact details, and avoid inventing customer, case-study, or trust-signal data.

Risk: Live page or form edits can break template bindings or form submission behavior.

Mitigation: Preserve existing template tags, dynamic data bindings, validation, captcha, upload, regional selector, and AJAX submission logic; apply only low-risk changes automatically after approval.

## Reference(s):

- [Skill source](artifact/SKILL.md)
- [Funnel Framework](artifact/references/funnel-framework.md)
- [Optimization Playbook](artifact/references/optimization-playbook.md)
- [MCP Write-back Mapping](artifact/references/mcp-writeback.md)
- [MCP Tools Reference](artifact/references/mcp-tools.md)
- [Custom Form Demo Code Base](artifact/references/customform-democode-base.md)
- [Lead-gen Audit Script](artifact/scripts/leadgen_audit.py)
- [ClawHub skill page](https://clawhub.ai/hsqduron/skills/yunzhi-website-leadgen)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with JSON audit reports, shell commands, code snippets, and CMS change plans]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The audit script emits UTF-8 JSON reports with leadgen_score, stage_scores, signals, and risk-graded suggestions.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
