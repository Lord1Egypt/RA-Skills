## Description: <br>
solo-build-free helps agents execute implementation-plan tasks by loading plan and spec context, applying a TDD workflow, running validation, updating progress, and committing completed work. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[thcjp](https://clawhub.ai/user/thcjp) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill when a project already has plan.md and spec.md files and they want an agent to execute implementation tasks, test changes, and track completion. It is not intended for plan creation, deployment, code review, or projects without a plan file. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can automatically modify code and create commits, which may change repository state unexpectedly. <br>
Mitigation: Use it only in trusted repositories, start from a clean working tree or backup branch, and review diffs before accepting commits. <br>
Risk: The skill can run local shell commands during testing and validation. <br>
Mitigation: Run it with least-privilege access, inspect commands before execution when possible, and avoid using it in repositories with untrusted inputs. <br>
Risk: Rollback commands such as git checkout may discard work. <br>
Mitigation: Do not permit rollback commands unless explicitly approved, and preserve important work on a separate branch or backup first. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/thcjp/skills/solo-build-free) <br>


## Skill Output: <br>
**Output Type(s):** [Markdown, Code, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown status summaries with inline code, shell commands, file edits, and commit information] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May edit repository files, run local validation commands, update plan progress, and create git commits when used by an agent.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
