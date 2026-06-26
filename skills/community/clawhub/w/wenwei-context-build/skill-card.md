## Description: <br>
This skill helps agents recursively trace code from an entry file and produce structured implementation-focused documentation covering code structure, dependencies, interfaces, and core logic. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[wed840313](https://clawhub.ai/user/wed840313) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to analyze frontend, backend, or full-stack modules from a chosen entry file. It is intended to create code-first Markdown knowledge-base notes for AI-assisted understanding of implementation details. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill may read related source files from the user-provided entry point and include implementation details or code snippets in its output. <br>
Mitigation: Use it only on repositories where the agent is allowed to inspect and summarize the relevant code, especially for proprietary or sensitive projects. <br>
Risk: Generated documentation can expose internal architecture, API details, or code paths when shared outside the workspace. <br>
Mitigation: Review generated notes before distribution and remove sensitive implementation details as needed. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/wed840313/wenwei-context-build) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, guidance] <br>
**Output Format:** [Markdown with tables and code blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Default output is conversational Markdown; a .md document is produced only when requested.] <br>

## Skill Version(s): <br>
1.0.0 (source: release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
