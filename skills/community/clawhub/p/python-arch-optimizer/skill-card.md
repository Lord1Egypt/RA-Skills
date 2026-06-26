## Description: <br>
Python project architecture optimization skill for analyzing and refactoring Python project structure toward best practices. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[jjflydudu](https://clawhub.ai/user/jjflydudu) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to assess Python project layout, dependency management, code organization, testing structure, and engineering configuration. It can also propose or help run guarded restructuring workflows after user confirmation. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill may guide an agent to change project files or run migration commands. <br>
Mitigation: Review generated changes before execution, use dry-run previews first, and rely on the documented backup and rollback flow for restructuring operations. <br>
Risk: Generated architecture recommendations can be incorrect or incomplete for a specific codebase. <br>
Mitigation: Validate recommendations against project tests, lint checks, and human review before applying them to important branches or production workflows. <br>


## Reference(s): <br>
- [Python Project Architecture Best Practices](references/best-practices.md) <br>
- [ClawHub Skill Page](https://clawhub.ai/jjflydudu/python-arch-optimizer) <br>
- [Publisher Profile](https://clawhub.ai/user/jjflydudu) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with inline code, shell commands, JSON-style analysis reports, and generated project files when scripts are run.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May create or move files when migration scripts are run; dry-run and backup behavior are described in the artifact.] <br>

## Skill Version(s): <br>
1.0.2 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
