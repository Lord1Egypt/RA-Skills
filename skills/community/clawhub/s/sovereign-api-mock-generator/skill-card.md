## Description: <br>
Generates mock API servers from OpenAPI specs or examples. Realistic fake data, configurable delays, error simulation. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ryudi84](https://clawhub.ai/user/ryudi84) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and engineers use this skill to generate mock API server implementations or guidance from OpenAPI specifications or example payloads, including fake data, response delays, and error simulation. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Generated mock-server code could behave incorrectly or expose unintended behavior if run without review. <br>
Mitigation: Review generated code and configuration before execution, especially routes, generated responses, and error simulation behavior. <br>
Risk: Using real API examples may expose sensitive request or response data in generated mock data. <br>
Mitigation: Sanitize real API examples before using them as inputs and replace secrets, personal data, and proprietary payloads with safe samples. <br>
Risk: Binding a generated mock server to a public network interface can expose test endpoints outside the intended environment. <br>
Mitigation: Run mock servers on local or restricted interfaces by default and require explicit review before public network exposure. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/ryudi84/sovereign-api-mock-generator) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration] <br>
**Output Format:** [Markdown with code blocks and implementation guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include generated mock-server code, setup commands, configuration examples, and trade-off guidance.] <br>

## Skill Version(s): <br>
1.0.0 (source: server-resolved release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
