## Description: <br>
AI-driven event forecasting skill. Collects multi-source data, cross-validates facts, maps future scenarios with probabilities, and delivers actionable recommendations for investors, managers, and policymakers. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[onecore-me](https://clawhub.ai/user/onecore-me) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External analysts, investors, managers, and policymakers use this skill to turn uncertain events into probability-weighted scenarios, trigger milestones, and role-specific action guidance. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Forecast reports may include buy, sell, options, or policy suggestions that readers could mistake for professional advice. <br>
Mitigation: Treat outputs as scenario-analysis support only and require qualified human review before financial, policy, legal, or operational decisions. <br>
Risk: Connecting private CRM, sales, or internal datasets could expose sensitive information if credentials and access are not controlled. <br>
Mitigation: Use least-privilege credentials, managed secret storage, data minimization, and compliance review before integrating private data sources. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/onecore-me/scenario-forecaster) <br>
- [API reference](docs/api_reference.md) <br>
- [Customization guide](docs/customization_guide.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, guidance] <br>
**Output Format:** [Markdown forecast report with tables, scenario paths, probabilities, trigger milestones, risk and opportunity analysis, and role-specific action lists.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Outputs are scenario-analysis guidance and should not be treated as professional financial, policy, or legal advice.] <br>

## Skill Version(s): <br>
1.3.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
