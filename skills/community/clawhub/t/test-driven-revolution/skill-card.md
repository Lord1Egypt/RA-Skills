## Description: <br>
Test-Driven Revolution implements an AI-driven iterative code workflow for planning, executing, testing, reviewing, and auditing software tasks. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[cjboy007](https://clawhub.ai/user/cjboy007) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineering agents use this skill when a user explicitly requests TDR for multi-step code generation, bug fixing, documentation updates, or security-sensitive changes that benefit from planning, execution, review, and audit loops. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can run task-provided shell commands automatically, which may modify code or execute unsafe actions if instructions are not reviewed. <br>
Mitigation: Install only in a disposable or tightly isolated workspace, restrict the executor, and inspect next_instructions before applying review output. <br>
Risk: Cron heartbeats can repeatedly execute queued tasks with more authority than the documented safety checks can fully control. <br>
Mitigation: Do not enable cron heartbeats until the execution environment and permissions have been reviewed and limited. <br>
Risk: Task JSON and review output can influence execution and may expose or misuse sensitive project data. <br>
Mitigation: Treat task JSON and review output as code, avoid secrets in task files, and avoid use on repositories or machines with sensitive credentials. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/cjboy007/test-driven-revolution) <br>
- [Publisher profile](https://clawhub.ai/user/cjboy007) <br>
- [SKILL.md](artifact/SKILL.md) <br>
- [README.md](artifact/README.md) <br>
- [Model configuration](artifact/config/models.json) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Markdown, Code, Shell commands, Configuration] <br>
**Output Format:** [Markdown guidance with JSON task files, shell commands, and code or configuration changes] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May produce iterative task state, review output, audit output, and event logs in the workspace.] <br>

## Skill Version(s): <br>
2.0.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
