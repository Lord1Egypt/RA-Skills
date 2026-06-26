## Description: <br>
Use when executing implementation plans with independent tasks in the current session. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[zlc000190](https://clawhub.ai/user/zlc000190) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and engineering agents use this skill to execute an existing implementation plan by coordinating one implementer subagent per independent task, followed by spec-compliance and code-quality review gates. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The workflow can coordinate repository code changes, tests, and commits through subagents. <br>
Mitigation: Use it only on branches and codebases where subagent code changes and commits are acceptable, and keep the review gates enabled. <br>
Risk: An implementation subagent may miss requirements, add unrequested behavior, or report results optimistically. <br>
Mitigation: Require independent spec-compliance review from the actual code before starting code-quality review or marking a task complete. <br>
Risk: Concurrent implementation subagents can create conflicting changes. <br>
Mitigation: Dispatch one implementation subagent at a time and use an isolated worktree as required by the workflow. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/zlc000190/subagent-driven-development) <br>
- [Publisher profile](https://clawhub.ai/user/zlc000190) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, guidance] <br>
**Output Format:** [Markdown guidance and prompt templates for coordinating subagents, reviews, tests, and commits.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [The skill expects an existing implementation plan and produces step-by-step coordination guidance rather than executable code by itself.] <br>

## Skill Version(s): <br>
0.1.0 (source: server-resolved release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
