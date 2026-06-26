## Description: <br>
Enables non-blocking AI agent execution by spawning parallel remora subagents for slow tasks, keeping the main agent responsive and efficient. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[keugenek](https://clawhub.ai/user/keugenek) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent operators use Shark to structure coding-agent work so slow operations run in parallel while the main agent continues reasoning, then aggregates results with timeouts and partial-failure reporting. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can encourage broad parallel or background execution authority for slow work. <br>
Mitigation: Use it only when parallel background execution is intended, and approve shell, SSH, Docker, CI, or filesystem-changing commands before launch. <br>
Risk: The loop command includes behavior that may bypass normal Claude permission checks. <br>
Mitigation: Avoid /shark-loop in sensitive repositories unless the permission-bypass flag is removed or the task runs in a disposable sandbox. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/keugenek/shark) <br>
- [Project Homepage](https://github.com/keugenek/shark-pattern) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, markdown, shell commands, configuration] <br>
**Output Format:** [Markdown guidance with inline shell commands and configuration values] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May produce status summaries, timing recommendations, cleanup reports, and task-completion notes.] <br>

## Skill Version(s): <br>
0.1.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
