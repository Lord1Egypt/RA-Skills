## Description: <br>
AI Dev Runtime helps developers automate coding, debugging, codebase analysis, terminal execution, and test workflows through a local runtime with optional memory-assisted search. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[molexazwo](https://clawhub.ai/user/molexazwo) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to delegate code reading, search, editing, patching, terminal execution, test running, bug fixing, and codebase analysis to a trusted AiDevRuntime service. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can delegate code edits, terminal commands, and test execution to an external development runtime. <br>
Mitigation: Use it only with a trusted AiDevRuntime service and review requested tasks, generated edits, and command results before relying on them. <br>
Risk: Configured runtime API keys and repository contents may be exposed to the connected service. <br>
Mitigation: Treat AI_DEV_RUNTIME_API_KEY as a credential and avoid sensitive repositories unless the runtime and its memory behavior are trusted. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/molexazwo/skills/super-ai-dev-runtime) <br>
- [Project homepage from metadata](https://github.com/your-org/AiDevRuntime) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown and text responses with code, shell commands, configuration guidance, and task results from the connected runtime.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires AI_DEV_RUNTIME_URL and may use AI_DEV_RUNTIME_API_KEY when the connected runtime requires authentication.] <br>

## Skill Version(s): <br>
1.0.0 (source: release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
