## Description: <br>
Trade Qualifier scores B2B foreign-trade leads across six dimensions and assigns A/B/C/D priority grades. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[wangm-a3](https://clawhub.ai/user/wangm-a3) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Sales and business-development teams use this skill to prioritize potential foreign-trade customers, compare lead quality, and decide follow-up actions from weighted scoring. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill handles business lead and customer-scoring data that may be sensitive. <br>
Mitigation: Use it only with business data you are comfortable sharing with the agent and review outputs before acting on them. <br>
Risk: The release metadata declares a curl binary requirement that is not explained by the documented skill behavior. <br>
Mitigation: Ask the publisher to clarify or remove the requirement if dependency hygiene is important for your environment. <br>
Risk: Automated customer scores and priority grades can be incorrect or misleading when input data is incomplete. <br>
Mitigation: Validate high-impact lead rankings against current source data before outreach or resource-allocation decisions. <br>


## Reference(s): <br>
- [Trade Qualifier on ClawHub](https://clawhub.ai/wangm-a3/trade-qualifier) <br>
- [Publisher profile](https://clawhub.ai/user/wangm-a3) <br>
- [README](README.md) <br>
- [Sample qualifier output](examples/qualifier_output_sample.csv) <br>
- [Related skill: trade-hunter](https://github.com/cloud-travel-skills/trade-hunter) <br>
- [Related skill: trade-closer](https://github.com/cloud-travel-skills/trade-closer) <br>
- [Related skill: trade-dashboard](https://github.com/cloud-travel-skills/trade-dashboard) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, configuration, guidance] <br>
**Output Format:** [Markdown or JSON tables with lead grades, dimension scores, and suggested follow-up actions.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Supports custom scoring weights and visual summaries such as radar or funnel views.] <br>

## Skill Version(s): <br>
1.0.0 (source: SKILL.md frontmatter, package.json, server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
