## Description: <br>
Checks import/export compliance requirements for products and countries, including certifications, tariffs, sanctions, and regulatory screening. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[wangm-a3](https://clawhub.ai/user/wangm-a3) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External trade, operations, and compliance teams use this skill to prepare preliminary import/export compliance checks, screen counterparties, and draft risk reports before legal or specialist review. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: High-stakes trade-compliance outputs may overstate sanctions, tariff, HS-code, export-control, or certification certainty. <br>
Mitigation: Treat results as preliminary assistance and verify all critical findings against official sources or qualified counsel before acting. <br>
Risk: The broad compliance trigger and API-backed workflow may receive sensitive business or counterparty data. <br>
Mitigation: Provide only data needed for the compliance check, avoid unrelated sensitive information, and review API credential handling before deployment. <br>
Risk: Static heuristic artifacts may be stale for sanctions lists, tariff rates, and certification requirements. <br>
Mitigation: Re-check time-sensitive findings through current official sanctions, customs, and certification sources at signing, shipment, and payment milestones. <br>


## Reference(s): <br>
- [Yunlv Homepage](https://yunlvai.com) <br>
- [Yunlv TradeGPT API](https://api.yunlvai.com) <br>
- [Certification Requirements](references/certification_requirements.md) <br>
- [Sanctions Screening Guide](references/sanctions_screening.md) <br>
- [Compliance Report Template](references/compliance_report_template.md) <br>
- [OFAC Sanctions Search](https://sanctionssearch.ofac.treas.gov/) <br>
- [EU Sanctions Map](https://www.sanctionsmap.eu/) <br>
- [UN Security Council Sanctions](https://www.un.org/securitycouncil/sanctions/) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown and JSON-style compliance reports with optional Python CLI commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May require TRADEGPT_API_KEY for API-backed compliance queries; generated findings should be treated as preliminary.] <br>

## Skill Version(s): <br>
1.1.0 (source: server release metadata and clawhub.yaml) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
