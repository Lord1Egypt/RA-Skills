## Description: <br>
Drafts and reviews foreign trade contracts, Proforma Invoices, Sales Contracts, MOUs, NDAs, and related clauses for payment, delivery, Incoterms, and risk allocation. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[wangm-a3](https://clawhub.ai/user/wangm-a3) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External trade, sales, and compliance users use this skill to draft bilingual trade contract materials and review contract clauses for payment, delivery, dispute-resolution, and allocation-of-risk issues. Agents can also use its bundled analyzer to produce structured JSON risk reports for payment terms, Incoterms, and clause completeness. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Confidential contract details may be sent to the Yunlv TradeGPT external API. <br>
Mitigation: Use a dedicated API key, submit only the contract information needed for the task, and confirm the provider's retention and privacy terms before using the skill for sensitive matters. <br>
Risk: Drafts, signed copies, review reports, and logs may be retained locally under the skill's data directory. <br>
Mitigation: Clean up local drafts, signed copies, reviews, and logs after use, especially when processing confidential contracts. <br>
Risk: Generated contract language and risk analysis may be incomplete or unsuitable as legal advice. <br>
Mitigation: Use the output as drafting and review assistance only, and route high-value, regulated, or complex agreements through qualified legal review. <br>


## Reference(s): <br>
- [Yunlv Contract Draft on ClawHub](https://clawhub.ai/wangm-a3/yunlv-contract-draft) <br>
- [Yunlv Homepage](https://yunlvai.com) <br>
- [Yunlv TradeGPT API](https://api.yunlvai.com) <br>
- [Contract Type Templates](references/contract_type_templates.md) <br>
- [Clause Risk Checklist](references/clause_risk_checklist.md) <br>
- [International Commercial Law Reference](references/international_commercial_law.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance, JSON] <br>
**Output Format:** [Markdown contract drafts and review guidance, plus JSON risk reports from the bundled analyzer.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires python3 and TRADEGPT_API_KEY for API-backed contract generation or analysis workflows.] <br>

## Skill Version(s): <br>
1.1.0 (source: server release metadata and clawhub.yaml) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
