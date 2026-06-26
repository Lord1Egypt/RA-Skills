## Description: <br>
A staged spec-driven development workflow for cloned Git repositories that guides init, requirements, architecture, process design, planning, coding, testing, bug fixing, code review, release, checkpoint, and rollback phases with required artifacts and gated review. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[listenbehind](https://clawhub.ai/user/listenbehind) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and coding-agent operators use this skill to run a structured development lifecycle inside a Git repository. It produces requirements, architecture, process design, project plans, source code, tests, review reports, release notes, and checkpoint recovery artifacts. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The workflow stores a Git token on disk for repository operations. <br>
Mitigation: Use a short-lived, repository-scoped token in a controlled workspace and remove the matching ~/.git-credentials entry after use. <br>
Risk: The workflow can commit, tag, push, reset, and roll back repository state. <br>
Mitigation: Manually approve clone, push, tag, and reset actions and inspect the working tree before release or rollback steps. <br>
Risk: The workflow may load auxiliary skills from the repository during execution. <br>
Mitigation: Review and scan auxiliary skills before allowing them to participate in the development or review workflow. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/listenbehind/spec-driven-dev) <br>
- [Publisher profile](https://clawhub.ai/user/listenbehind) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown documents, JSON task lists, source and test files, shell commands, and structured review/checkpoint reports] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Can write Git-backed project artifacts and emit structured progress checkpoints.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
