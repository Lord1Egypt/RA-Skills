## Description: <br>
Lint Terraform modules and configurations (.tf files) for structure, naming, security, and best practices. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[charlie-morrison](https://clawhub.ai/user/charlie-morrison) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and infrastructure engineers use this skill to inspect Terraform modules and .tf files for structure, naming, security, and best-practice findings before publication or deployment. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Terraform files may include infrastructure structure or embedded secrets in local lint output. <br>
Mitigation: Run the linter only on Terraform modules you intend to inspect and review output before sharing it. <br>
Risk: The skill requires trust in a third-party publisher before local execution. <br>
Mitigation: Install only if you trust the publisher and review the skill files before use. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/charlie-morrison/terraform-module-linter) <br>
- [Publisher profile](https://clawhub.ai/user/charlie-morrison) <br>


## Skill Output: <br>
**Output Type(s):** [Analysis, JSON, Shell commands, Guidance] <br>
**Output Format:** [Text, JSON, or summary output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Reports Terraform lint findings with file, line, rule, severity, message, and category when JSON output is selected.] <br>

## Skill Version(s): <br>
1.0.1 (source: release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
