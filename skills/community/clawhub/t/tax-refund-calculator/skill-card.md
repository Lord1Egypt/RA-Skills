## Description: <br>
零配置即装即用，计算15+国家购物退税金额含手续费明细，自动识别无退税国家避免踩坑，支持全球退税政策查询含流程指引。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[travel-skills](https://clawhub.ai/user/travel-skills) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Chinese-speaking travelers and travel-planning agents use this skill to estimate shopping tax refunds, check minimum purchase thresholds, and query country-specific refund policies before overseas purchases. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Refund rates, exchange rates, thresholds, and policies may be approximate, outdated, or different from the final amount accepted by customs or refund providers. <br>
Mitigation: Use the output for trip planning only and verify current policy and final refund amounts with the merchant, customs office, or tax-refund provider before relying on it. <br>
Risk: Implemented country coverage is narrower than some description text claims, so unsupported destinations may be missing. <br>
Mitigation: Query the policy overview or a specific country first, and use official country or provider guidance when the destination is not listed. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/travel-skills/tax-refund-calculator) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, guidance] <br>
**Output Format:** [Chinese-language Markdown text, with JSON-formatted error messages for invalid command inputs] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses local built-in refund policy and exchange-rate data; results are planning estimates and not official tax advice.] <br>

## Skill Version(s): <br>
1.0.2 (source: server release metadata and VERSION) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
