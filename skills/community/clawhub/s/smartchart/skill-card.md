## Description: <br>
smartchart helps agents query data, explore available data tools, and execute data operations through the SmartChart CLI. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[johnyan2017](https://clawhub.ai/user/johnyan2017) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and data users use this skill to discover SmartChart data tools, inspect tool parameters, and run CLI-based data queries with structured output. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Query inputs may be sent through an external SmartChart data platform. <br>
Mitigation: Verify the smartchart Python package and SmartChart service before use, and avoid sending secrets, regulated data, internal identifiers, or confidential business parameters unless the service is trusted. <br>


## Reference(s): <br>
- [SmartChart tool parameter reference](references/api_reference.md) <br>
- [ClawHub smartchart release page](https://clawhub.ai/johnyan2017/smartchart) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, JSON] <br>
**Output Format:** [Markdown guidance with inline shell commands and SmartChart CLI output.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [SmartChart tool results may be returned in raw, json, or array formats.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
