## Description: <br>
Helps developers implement dependency injection in PydanticAI agents using RunContext and deps_type for database connections, API clients, user context, and other external resources. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[anderskev](https://clawhub.ai/user/anderskev) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to design PydanticAI agents whose tools and prompts receive scoped runtime dependencies such as database handles, API clients, user context, and test doubles. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Dependencies can expose raw API keys or database credentials if examples are copied without scoping. <br>
Mitigation: Pass initialized clients or scoped handles as dependencies, keep secrets out of source code and logs, and avoid placing credentials directly in prompts or outputs. <br>
Risk: Generic database query tools can allow overly broad or unsafe operations. <br>
Mitigation: Prefer purpose-specific, parameterized data-access methods and limit each tool to the current request or user context. <br>
Risk: Tests can pass partial dependency mocks that diverge from production dependency shapes. <br>
Mitigation: Use agent.override with dependency objects that match the production fields and types used by the tools under test. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/anderskev/pydantic-ai-dependency-injection) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, markdown, code, configuration] <br>
**Output Format:** [Markdown guidance with Python code examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Documentation-only skill; examples may need project-specific dependency types and credential handling.] <br>

## Skill Version(s): <br>
1.0.1 (source: server-resolved release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
