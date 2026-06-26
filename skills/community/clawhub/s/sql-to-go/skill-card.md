## Description: <br>
Convert MySQL CREATE TABLE statements into Go structs with form, json, and xorm tags, including MySQL type mapping, snake_case to CamelCase field names, and tag generation. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[weirubo](https://clawhub.ai/user/weirubo) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers use this skill to transform MySQL DDL into Go model structs and ORM-ready tags for application code generation. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Generated structs may mishandle nullable columns, DECIMAL precision, time handling, or xorm tags for schema edge cases. <br>
Mitigation: Review generated Go structs against the original MySQL schema before production use and adjust field types or tags where needed. <br>


## Reference(s): <br>
- [MySQL to Go Type Mappings](references/type_mappings.md) <br>


## Skill Output: <br>
**Output Type(s):** [Code, Markdown, Guidance] <br>
**Output Format:** [Markdown with Go code blocks and struct/tag examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Generated structs should be reviewed for nullable fields, DECIMAL precision, time handling, and xorm tags.] <br>

## Skill Version(s): <br>
1.0.0 (source: release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
