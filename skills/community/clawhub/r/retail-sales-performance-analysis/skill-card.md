## Description: <br>
门店销售业绩环比分析工具，支持门店和导购业绩对比、波动归因、异常识别，并输出诊断结论和改进建议。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[gwyang7](https://clawhub.ai/user/gwyang7) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Retail operators, store managers, and business analysts use this skill to compare store or clerk performance across periods, identify drivers of sales changes, flag anomalies, and receive improvement recommendations. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Business sales data could be exposed or analyzed beyond the intended scope. <br>
Mitigation: Use a read-only, least-privileged account and provide only the store IDs, clerk IDs, and date ranges the agent is allowed to analyze. <br>
Risk: The skill depends on a local api_client supplied by the OpenClaw environment. <br>
Mitigation: Install only in a trusted OpenClaw environment and review the local api_client before use. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/gwyang7/retail-sales-performance-analysis) <br>


## Skill Output: <br>
**Output Type(s):** [json, text, guidance] <br>
**Output Format:** [JSON object containing status, analysis period, core metrics, attribution, findings, risks, and recommendations.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires authorized access to the retail API data for the requested store IDs, clerk IDs, and date ranges.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
