## Description: <br>
Generates a Salesforce report blueprint from real org metadata. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[breynol01](https://clawhub.ai/user/breynol01) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Salesforce administrators, developers, and operations teams use this skill to map reporting questions to live Salesforce objects, fields, relationships, report types, filters, and blockers. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Salesforce CLI access can expose org metadata, schemas, CSVs, query output, or example records that may contain sensitive business data. <br>
Mitigation: Verify the target org alias, prefer a sandbox or least-privileged Salesforce account, keep queries narrow, and protect saved outputs as sensitive data. <br>


## Reference(s): <br>
- [SFDC CLI Reference](references/cli-reference.md) <br>
- [Object Mapping Guide](references/object-mapping.md) <br>
- [Project homepage](https://github.com/breynol01/salesforce-reporting-copilot) <br>
- [ClawHub skill page](https://clawhub.ai/breynol01/salesforce-reporting-copilot) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with Salesforce CLI commands and report blueprint tables] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses live Salesforce metadata and avoids fabricating object or field names.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
