## Description: <br>
Converts MySQL CREATE TABLE statements into Java entity classes following MyBatis-Plus or JPA conventions. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[coder-myj](https://clawhub.ai/user/coder-myj) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to turn MySQL DDL into Java entity definitions for ORM-backed applications. It helps generate class names, fields, imports, annotations, and accessors while preserving schema-derived type information. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Generated Java entities may use framework conventions, type choices, or package names that do not match the target project. <br>
Mitigation: Review generated classes against project style, ORM configuration, and schema semantics before committing. <br>
Risk: Database schemas can contain sensitive production structure. <br>
Mitigation: Avoid pasting sensitive production schemas unless approved for use with the coding agent. <br>


## Reference(s): <br>
- [MySQL to Java Type Mappings](artifact/references/type_mappings.md) <br>
- [ClawHub Skill Page](https://clawhub.ai/coder-myj/sql-to-java) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, guidance] <br>
**Output Format:** [Markdown with Java code blocks and concise implementation guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Generated classes should be reviewed for project package names, ORM conventions, schema semantics, and type choices before committing.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
