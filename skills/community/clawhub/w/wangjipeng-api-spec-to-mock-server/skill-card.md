## Description: <br>
Use when a user provides an API spec in OpenAPI or Swagger format and needs a runnable mock server. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[wangjipeng977](https://clawhub.ai/user/wangjipeng977) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to turn OpenAPI or Swagger API specifications into runnable mock server code, endpoint smoke tests, curl examples, and run instructions. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Generated mock server files may reflect sensitive API details or credential requirements contained in the supplied specification. <br>
Mitigation: Provide only API specifications suitable for agent processing, keep credentials in environment variables, and review generated server files before running them. <br>
Risk: Template-like README content may not match the actual activation scope. <br>
Mitigation: Use SKILL.md as the source for activation scope and confirm generated run commands before execution. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/wangjipeng977/wangjipeng-api-spec-to-mock-server) <br>
- [Skill reference index](artifact/references/index.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown with generated server code, shell commands, configuration notes, and curl examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Generated output depends on the supplied API specification and should be reviewed before execution.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
