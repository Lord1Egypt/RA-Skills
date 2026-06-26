## Description: <br>
Safely remove Google Analytics from a project. Cleans up all tracking code, dependencies, and environment variables. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[jeftekhari](https://clawhub.ai/user/jeftekhari) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and engineering teams use this skill to locate and remove Google Analytics tracking code, dependencies, environment-variable references, and related documentation from projects after explicit confirmation. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can remove tracking code, analytics utility files, package dependencies, and environment-variable references from a project. <br>
Mitigation: Use version control, review each proposed deletion or package uninstall, and confirm only when the removal is intended. <br>
Risk: Project documentation or deployed environments may still contain analytics references after repository cleanup. <br>
Mitigation: Review the final summary and complete any listed manual cleanup steps, including removal of actual environment values outside checked-in examples. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/jeftekhari/remove-analytics) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, code, configuration, guidance] <br>
**Output Format:** [Markdown with inline file, package, and environment-variable changes] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Confirmation-gated removal workflow with a final summary of deleted files, modified files, removed packages, removed environment variables, and manual cleanup steps.] <br>

## Skill Version(s): <br>
0.1.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
