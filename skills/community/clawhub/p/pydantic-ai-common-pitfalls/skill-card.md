## Description: <br>
Avoid common mistakes and debug issues in PydanticAI agents. Use when encountering errors, unexpected behavior, or when reviewing agent implementations. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[anderskev](https://clawhub.ai/user/anderskev) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to review PydanticAI agent implementations, recognize common configuration and tool-definition mistakes, and debug ambiguous runtime failures. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Examples and debugging workflows may involve API keys, tracing, or captured model messages that contain sensitive data. <br>
Mitigation: Keep secrets out of chats and logs, and only trace or capture production data when the logging destination is approved. <br>
Risk: Troubleshooting guidance can be misapplied to unrelated PydanticAI failures. <br>
Mitigation: Review code changes against the current PydanticAI documentation and validate behavior with a minimal reproduction before deployment. <br>


## Reference(s): <br>
- [PydanticAI: registering tools via the tools argument](https://ai.pydantic.dev/agents/#registering-tools-via-the-tools-argument) <br>
- [ClawHub skill page](https://clawhub.ai/anderskev/pydantic-ai-common-pitfalls) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Markdown, Code, Shell commands, Configuration instructions] <br>
**Output Format:** [Markdown with Python code examples and troubleshooting checklists] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Documentation-only guidance; examples may reference API keys, tracing, and captured messages.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
