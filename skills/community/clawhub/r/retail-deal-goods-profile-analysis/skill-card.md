## Description: <br>
成交商品画像分析 analyzes retail transaction data by category, price band, color, bag shape, launch date, and period-over-period changes. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[gwyang7](https://clawhub.ai/user/gwyang7) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Retail analysts and store operations teams use this skill to profile sold goods for a store and date range. It produces ranked feature distributions, period-over-period changes, and concise business findings for merchandise review. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill loads an undeclared local api_client from a hardcoded path outside the package. <br>
Mitigation: Inspect and approve the external api_client before use, or replace it with a reviewed packaged dependency. <br>
Risk: The skill accesses store BI transaction data for a supplied store and date range. <br>
Mitigation: Run it only with the expected store BI permissions and review outputs before sharing business-sensitive analysis. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/gwyang7/retail-deal-goods-profile-analysis) <br>
- [ClawHub publisher profile](https://clawhub.ai/user/gwyang7) <br>


## Skill Output: <br>
**Output Type(s):** [text, analysis] <br>
**Output Format:** [Console text report] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Reports category, price band, bag shape, color, launch-date distribution, period-over-period changes, and summary findings.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
