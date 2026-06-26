## Description: <br>
This skill summarizes chat history to extract new budget data models, fields, script patterns, and business rules, then updates related platform-script and budget-data-model skill knowledge. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[lan2898408767](https://clawhub.ai/user/lan2898408767) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and budget-system maintainers use this skill to capture reusable script techniques, data model changes, field definitions, and business rules from a conversation and record them in related skill files. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can persist chat-derived content into other installed skill files without a clear approval step. <br>
Mitigation: Require the agent to show the exact proposed changes and wait for explicit approval before writing, and avoid using it on conversations containing credentials, customer data, private business details, temporary experiments, or unreviewed code. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/lan2898408767/shucheng-summary-budget-model-and-new-script) <br>
- [Skill update log](references/update_log.md) <br>
- [Skill update operation guide](references/使用说明.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, configuration, guidance] <br>
**Output Format:** [Markdown guidance with JSON and Groovy code examples and proposed skill-file updates] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Updates should be shown for review before any files are written.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and package.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
