## Description: <br>
Executes implementation plan tasks with a TDD workflow, phase gates, verification, progress updates, and commits. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[fortunto2](https://clawhub.ai/user/fortunto2) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers and engineers use this skill after a planning step has produced plan and specification files. It executes implementation tasks one at a time, verifies changes, updates plan progress, and creates traceable commits. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can edit code, run project commands, install or verify git hooks, and create commits. <br>
Mitigation: Install and run it only in repositories where the plan files, workflow docs, package scripts, Makefile targets, and git hooks are trusted. <br>
Risk: Automated build execution can introduce incorrect changes or commit work before it has been reviewed. <br>
Mitigation: Review diffs, command output, verification results, and generated commits before relying on the completed task or deploying the repository. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/fortunto2/solo-build) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown status updates with inline shell commands, code edits, configuration changes, verification results, and git commit references] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Can modify repository files, update plan documents, run project checks, install or verify git hooks, and create commits when used in a trusted repository.] <br>

## Skill Version(s): <br>
2.2.1 (source: server release metadata and skill frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
