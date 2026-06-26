## Description: <br>
Tell the agent to zoom out and give broader context or a higher-level perspective on a section of code. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[genortg](https://clawhub.ai/user/genortg) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill when they need a higher-level map of an unfamiliar codebase, module, or public API before making changes. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill may cause the agent to inspect multiple files in the active project while mapping architecture and callers. <br>
Mitigation: Use it only in workspaces where codebase-wide reading is appropriate. <br>
Risk: A high-level architecture summary can omit details or misstate how unfamiliar code paths connect. <br>
Mitigation: Review the generated map against the cited files before using it to guide implementation decisions. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/genortg/zoom-out) <br>
- [Publisher profile](https://clawhub.ai/user/genortg) <br>


## Skill Output: <br>
**Output Type(s):** [Analysis, Markdown, Guidance] <br>
**Output Format:** [Markdown] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Summarizes module boundaries, dependencies, callers, architectural role, and project vocabulary.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
