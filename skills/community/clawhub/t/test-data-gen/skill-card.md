## Description: <br>
Generates fake test data in JSON, CSV, or SQL formats using built-in or custom templates for users, orders, products, reviews, and addresses. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[shenghoo123-png](https://clawhub.ai/user/shenghoo123-png) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, QA engineers, and test engineers use this skill to generate realistic fake records for API testing, CSV review, database import, and test-environment population. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Generated SQL can write data into a database if executed. <br>
Mitigation: Review generated SQL before running it and import only into disposable test databases. <br>
Risk: Untrusted custom templates can produce unexpected fields or large generated outputs. <br>
Mitigation: Review custom templates before use and start with small row counts before bulk generation. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/shenghoo123-png/test-data-gen) <br>
- [README](artifact/README.md) <br>
- [Skill description](artifact/SKILL.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Code, Files, Shell commands, Guidance] <br>
**Output Format:** [JSON, CSV, or SQL text; optionally written to output files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Supports built-in and custom templates, MySQL/PostgreSQL SQL output, and bounded row counts.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
