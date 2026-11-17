## Description:

Helps agents check import/export compliance requirements for products, countries, certifications, tariffs, sanctions, embargoes, and regulatory review workflows.

This skill is ready for commercial/non-commercial use.

## Publisher:

[wangm-a3](https://clawhub.ai/user/wangm-a3)

### License/Terms of Use:

MIT-0

## Use Case:

External users, trade teams, and compliance reviewers use this skill to obtain preliminary product-market compliance guidance, sanctions screening prompts, risk scores, and report checklists before cross-border transactions. Its outputs should be treated as starting points for professional and authoritative verification, not as legal or regulatory clearance.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Compliance outputs may understate sanctions, embargo, tariff, export-control, or counterparty risk because the security review found that the skill can produce unsafe low-risk advice from incomplete static data.

Mitigation: Treat every result as a preliminary heuristic and independently verify against current authoritative sanctions, customs, export-control, and legal sources before acting.

Risk: The skill declares use of the Yunlv TradeGPT API with TRADEGPT_API_KEY, so product, country, transaction, or counterparty details may be sent to an external service.

Mitigation: Confirm data-sharing approval, avoid unnecessary sensitive data, and manage the API key through approved secret-handling procedures.

Risk: The artifact describes local storage for screening records, reports, alerts, and logs under ./data/yunlv-skills/complianceCheck/.

Mitigation: Review local retention, access controls, and cleanup requirements before processing customer, counterparty, or transaction data.

Risk: Sanctions, tariffs, certification requirements, and restricted-party lists can change frequently.

Mitigation: Re-screen important transactions at contracting, shipment, and payment milestones and require human review for high-risk or regulated trades.

## Reference(s):

- [ClawHub Skill Listing](https://clawhub.ai/wangm-a3/skills/yunlv-compliance-check)
- [Yunlv Homepage](https://yunlvai.com)
- [Yunlv TradeGPT API](https://api.yunlvai.com)
- [Product Certification Requirements](artifact/references/certification_requirements.md)
- [Sanctions Screening Guide](artifact/references/sanctions_screening.md)
- [Compliance Report Template](artifact/references/compliance_report_template.md)
- [OFAC Sanctions Search](https://sanctionssearch.ofac.treas.gov/)
- [EU Sanctions Map](https://www.sanctionsmap.eu/)
- [UN Security Council Sanctions](https://www.un.org/securitycouncil/sanctions/)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with JSON examples and optional CLI JSON output.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May require TRADEGPT_API_KEY for API-backed compliance checks; bundled CLI commands print JSON to stdout.]

## Skill Version(s):

1.1.0 (source: server release metadata and clawhub.yaml)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
