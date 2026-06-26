## Description: <br>
Generate WHO child growth charts (height, weight, BMI) with percentile curves. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[odrobnik](https://clawhub.ai/user/odrobnik) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External users and caregivers use this skill to generate WHO child growth standard charts and overlay a child's height, weight, or BMI measurements against percentile curves. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill downloads WHO reference data and an emblem from cdn.who.int. <br>
Mitigation: Run it only in environments where those one-way downloads are acceptable and review network access expectations before deployment. <br>
Risk: Generated charts and measurement JSON files can contain private child health information. <br>
Mitigation: Store outputs in an approved private workspace and delete the who-growth-charts cache/output directory when it is no longer needed. <br>


## Reference(s): <br>
- [WHO Growth Charts ClawHub release](https://clawhub.ai/odrobnik/who-growth-charts) <br>
- [Publisher profile: odrobnik](https://clawhub.ai/user/odrobnik) <br>
- [WHO child growth standards data](https://cdn.who.int/media/docs/default-source/child-growth/child-growth-standards/indicators) <br>
- [WHO growth reference data for 5-19 years](https://cdn.who.int/media/docs/default-source/child-growth/growth-reference-5-19-years) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, shell commands, configuration, code, files] <br>
**Output Format:** [Markdown guidance with shell commands and generated PNG chart files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Downloads WHO reference spreadsheets on demand, caches them locally, and writes chart outputs under who-growth-charts by default.] <br>

## Skill Version(s): <br>
1.2.3 (source: frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
