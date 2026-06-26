## Description: <br>
Helps an agent trace a described requirement or defect from a specified code entry point to the key implementation files, call chain, and focused code snippets. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[wed840313](https://clawhub.ai/user/wed840313) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and code-review agents use this skill when they know a requirement, bug, API, UI element, or entry file and need to narrow a workspace to the most relevant implementation location instead of producing broad module documentation. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill is designed to inspect workspace files and surface small code snippets with paths and line numbers, which can expose proprietary or sensitive code in the conversation. <br>
Mitigation: Use it only in workspaces where code sharing is appropriate, and review snippets before forwarding or publishing the conversation. <br>


## Reference(s): <br>


## Skill Output: <br>
**Output Type(s):** [Markdown, Code, Guidance] <br>
**Output Format:** [Markdown with file paths, line numbers, call-chain summaries, and focused code blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include concise snippets and unresolved-path notes when code is outside the workspace.] <br>

## Skill Version(s): <br>
1.0.0 (source: ClawHub release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
