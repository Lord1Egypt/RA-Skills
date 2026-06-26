## Description: <br>
Helps detect security-relevant changes in AI skills after installation by tracking deltas between audited and current versions that expand permissions, add network endpoints, or alter behavior. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[andyxinweiminicloud](https://clawhub.ai/user/andyxinweiminicloud) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and security reviewers use this skill to compare installed AI skill versions and identify update-related changes that may warrant review before continued use. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill reviews installed skill contents and may fetch comparison data, which can expose more local or network context than a normal writing skill. <br>
Mitigation: Review configuration for allowed skill directories and network sources before use. <br>
Risk: Delta monitoring surfaces signals and cannot determine whether a permission, endpoint, dependency, or instruction change is malicious. <br>
Mitigation: Manually review flagged changes before continuing use or rolling back a skill. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/andyxinweiminicloud/skill-update-delta-monitor) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, guidance] <br>
**Output Format:** [Markdown delta report] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Includes permission, network endpoint, dependency, instruction drift, version velocity, and risk classification fields.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
