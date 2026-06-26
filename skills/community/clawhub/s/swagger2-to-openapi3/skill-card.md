## Description: <br>
Use when migrating Java Spring Boot projects from Swagger 2 (Springfox) to OpenAPI 3.0 (SpringDoc), including annotation replacements, import updates, and javax-to-jakarta migration. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[wangteng85859](https://clawhub.ai/user/wangteng85859) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to migrate Java Spring Boot projects from Swagger 2/Springfox to OpenAPI 3.0/SpringDoc, including annotation replacements, import updates, and javax-to-jakarta package changes. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Regex-based source rewrites can break Java edge cases or leave complex Swagger response annotations requiring manual changes. <br>
Mitigation: Run with --dry-run first, review the generated diff, then run project build and tests before merging. <br>
Risk: The migration scripts can modify Java source files under the selected project path. <br>
Mitigation: Use the skill only on projects intended for migration and work from a committed branch or backup. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/wangteng85859/swagger2-to-openapi3) <br>
- [ClawHub publisher profile](https://clawhub.ai/user/wangteng85859) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with code examples, shell commands, and source-file rewrite scripts] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Supports dry-run previews and reports processed files, modified files, annotation replacements, and import replacements.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
