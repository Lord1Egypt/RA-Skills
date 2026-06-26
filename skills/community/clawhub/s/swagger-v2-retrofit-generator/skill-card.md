## Description: <br>
Generates Android Retrofit/Kotlin client code from Swagger v2 (OpenAPI 2.0) API documentation, with optional Swagger fetching over HTTP using no auth, Basic Auth, Bearer Token, or API Key auth. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[opoojkk](https://clawhub.ai/user/opoojkk) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and Android engineers use this skill to fetch Swagger v2 documentation, inspect or filter endpoints, and generate Kotlin Retrofit service interfaces and data classes. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Fetching Swagger documents from untrusted URLs can expose users to unwanted or misleading API definitions. <br>
Mitigation: Use the fetch workflow only with Swagger URLs the user trusts. <br>
Risk: Authentication values passed on the command line can be exposed through shell history, process listings, or CI logs. <br>
Mitigation: Prefer test or limited-scope credentials and avoid putting production secrets directly in shell commands or logs. <br>
Risk: Generated output can overwrite existing files when written to an existing path. <br>
Mitigation: Choose the output path deliberately and review generated files before integrating them. <br>
Risk: Generated Kotlin may need manual adjustment for file upload APIs, complex generic responses, or project-specific type mappings. <br>
Mitigation: Review and test the generated Retrofit interfaces and data classes before using them in an Android application. <br>


## Reference(s): <br>
- [Swagger v2 Structure Reference](references/swagger-v2-structure.md) <br>
- [Retrofit + Kotlin Template Reference](references/retrofit-templates.md) <br>


## Skill Output: <br>
**Output Type(s):** [code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with bash examples and generated Kotlin source files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Can write Swagger JSON and Kotlin output files to user-selected paths.] <br>

## Skill Version(s): <br>
0.1.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
