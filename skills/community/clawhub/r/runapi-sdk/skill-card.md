## Description: <br>
Helps application developers choose and wire up RunAPI SDK packages for JavaScript, Ruby, or Go. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[runapi-ai](https://clawhub.ai/user/runapi-ai) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill when integrating RunAPI into applications, backends, workers, or libraries. It helps them select core or model-specific SDK packages, understand language package names, and handle API-key configuration. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: RunAPI credentials can be exposed if copied into source code or committed to version control. <br>
Mitigation: Keep the API key in RUNAPI_API_KEY or pass it through a secure client configuration path, and never commit secrets. <br>
Risk: Adding SDK packages without review can introduce unsuitable dependencies into production applications. <br>
Mitigation: Review model-specific SDK packages before production use and install only the packages the application actually needs. <br>
Risk: Using an SDK workflow for one-off media generation can add unnecessary application integration overhead. <br>
Mitigation: Use the RunAPI CLI or a model-specific skill for one-off media tasks. <br>


## Reference(s): <br>
- [RunAPI models and SDK package catalog](https://runapi.ai/models) <br>
- [RunAPI models markdown catalog](https://runapi.ai/models.md) <br>
- [ClawHub skill listing](https://clawhub.ai/runapi-ai/runapi-sdk) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, markdown, code, shell commands, configuration] <br>
**Output Format:** [Markdown with package names, environment-variable guidance, and code or command snippets when useful] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [No files are produced by the skill itself.] <br>

## Skill Version(s): <br>
0.2.4 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
