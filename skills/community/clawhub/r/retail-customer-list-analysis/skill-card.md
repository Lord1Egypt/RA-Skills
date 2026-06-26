## Description: <br>
客户清单分析基于 Shop API 客户清单数据，统计客户类型、试用转化、导购匹配和客户明细。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[gwyang7](https://clawhub.ai/user/gwyang7) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Retail operators and store managers use this skill to answer customer-list questions from Shop API data, including customer type distribution, trial activity, salesperson matching, and customer detail lookup. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Reports may expose sensitive customer and business data, including customer IDs, visit details, salesperson names, and transaction amounts. <br>
Mitigation: Install only where the Shop API account is authorized for the intended stores and users, and handle generated reports under the organization's customer-data policies. <br>
Risk: Analysis quality depends on the configured Shop API access and local API client. <br>
Mitigation: Verify the API client and Shop API permissions before relying on analyses or sharing outputs. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/gwyang7/retail-customer-list-analysis) <br>


## Skill Output: <br>
**Output Type(s):** [text, JSON, guidance] <br>
**Output Format:** [Structured JSON results and Chinese text report] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include customer identifiers, visit details, salesperson names, and transaction amounts from Shop API responses.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and artifact __version__) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
