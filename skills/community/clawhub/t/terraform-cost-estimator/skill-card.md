## Description: <br>
Estimate infrastructure costs from Terraform plans by analyzing resource changes, predicting monthly spend, comparing alternatives, and identifying cost optimization opportunities. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[charlie-morrison](https://clawhub.ai/user/charlie-morrison) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, infrastructure engineers, and FinOps teams use this skill to estimate monthly and annual cost impact from Terraform plans before applying changes. It helps compare cloud resource alternatives and identify optimization opportunities across AWS, GCP, and Azure. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Terraform plan files and plan JSON can reveal sensitive infrastructure details. <br>
Mitigation: Confirm the intended Terraform directory, workspace, and cloud profile before running commands, and treat generated plan files and cost reports as sensitive infrastructure data. <br>
Risk: Estimated cloud costs can be inaccurate when pricing, region, resource utilization, or usage assumptions differ from the plan. <br>
Mitigation: Validate material cost decisions against current provider pricing, billing data, or an approved cost-management tool before relying on the estimate. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/charlie-morrison/terraform-cost-estimator) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, guidance] <br>
**Output Format:** [Markdown with cost tables, recommendations, annual projections, and inline shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Cost estimates are advisory and depend on Terraform plan accuracy, selected cloud region, usage assumptions, and current provider pricing.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
