## Description: <br>
Supernal Coding CLI helps agents use sc for development workflows including task management, requirements tracking, testing, git automation, ralph loops, compliance, and documentation. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ianderrington](https://clawhub.ai/user/ianderrington) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and agent operators use this skill to install and operate Supernal Coding CLI for managing tasks, project health, traceability, specs, code quality checks, documentation, and autonomous ralph execution loops. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Autonomous ralph loops, git automation, initialization, cleanup, and scheduled heartbeat examples can change files or task state in a repository. <br>
Mitigation: Run these commands only in the intended repository after reviewing the current task state, affected files, and planned automation scope. <br>
Risk: The installation flow depends on a global npm package from a third-party publisher. <br>
Mitigation: Install only when the npm package publisher is trusted and the package permissions and source are acceptable for the environment. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/ianderrington/sc) <br>
- [Task workflow guide](docs/TASK_WORKFLOW.md) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Shell commands, Configuration] <br>
**Output Format:** [Markdown with inline bash code blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Commands may modify project task files, git state, compliance outputs, documentation, and knowledge indexes when run.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
