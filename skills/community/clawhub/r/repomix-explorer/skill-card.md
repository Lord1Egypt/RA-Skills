## Description: <br>
Use this skill when the user wants to analyze or explore a codebase, remote repository, or local repository using Repomix. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[kongyo2](https://clawhub.ai/user/kongyo2) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and engineers use this skill to package a target repository with the Repomix CLI, inspect the generated repository summary, and produce concise structure, metrics, and pattern-finding analysis. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can ask an agent to run Repomix shell commands against repositories and generate packed code files. <br>
Mitigation: Review the proposed command before execution and use scoped include or ignore patterns for private projects. <br>
Risk: Generated Repomix output can contain sensitive source content if broad local folders are scanned. <br>
Mitigation: Avoid scanning folders that may contain secrets and delete generated output files when they include sensitive code. <br>


## Reference(s): <br>
- [Repomix documentation](https://github.com/yamadashy/repomix) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, guidance] <br>
**Output Format:** [Markdown with inline shell commands and file references] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May create Repomix output files that contain packed repository content.] <br>

## Skill Version(s): <br>
0.1.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
