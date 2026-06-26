## Description: <br>
门店历史基线分析工具，基于 Agent API 数据库视图为门店销售额、订单数、客单价和连带率生成多周期基线、四分位分析和异常判断。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[gwyang7](https://clawhub.ai/user/gwyang7) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Retail operators and analytics agents use this skill to compare a store's current performance against historical weekday, weekly, monthly, quarterly, half-year, and annual baselines. It supports anomaly review and basic variance attribution for sales amount, order count, customer unit price, and attach rate. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Database access may expose sensitive store data if credentials are too broad. <br>
Mitigation: Use only read-only, store-scoped database credentials before installation or execution. <br>
Risk: The release depends on a local api_client module path that is not packaged with the skill. <br>
Mitigation: Replace the local dependency with a reviewed, packaged, and declared dependency in the deployment environment. <br>
Risk: Store IDs and date values are used in database queries and can be unsafe if accepted without controls. <br>
Mitigation: Require parameterized queries or strict validation for store IDs and dates. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/gwyang7/retail-store-poscore-baseline-analysis) <br>


## Skill Output: <br>
**Output Type(s):** [text, code, guidance] <br>
**Output Format:** [Structured Python dictionaries with human-readable baseline and variance-analysis fields] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires access to store POS database views; weekday baselines require at least 6 samples.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and artifact version) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
