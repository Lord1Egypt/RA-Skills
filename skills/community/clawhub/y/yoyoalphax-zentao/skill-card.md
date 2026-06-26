## Description: <br>
Integrates ZenTao project management APIs so an agent can query and manage products, projects, executions, stories, tasks, bugs, tests, feedback, and tickets. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[yoyoalphax](https://clawhub.ai/user/yoyoalphax) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and project teams use this skill to let an agent retrieve ZenTao project-management records and perform create, update, delete, review, and test-run actions against a configured ZenTao account. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can perform write and delete actions in ZenTao with the configured account. <br>
Mitigation: Use a least-privilege or read-only ZenTao account when possible and require manual review before create, update, delete, review, or test-run actions. <br>
Risk: ZenTao credentials are stored in TOOLS.md. <br>
Mitigation: Protect TOOLS.md and do not commit or share credentials. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/yoyoalphax/yoyoalphax-zentao) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown tables, terminal text, and inline shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires a configured TOOLS.md ZenTao account; write operations should be manually reviewed before execution.] <br>

## Skill Version(s): <br>
1.0.6 (source: ClawHub release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
