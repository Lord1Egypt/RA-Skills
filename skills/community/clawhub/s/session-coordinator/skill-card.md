## Description: <br>
Ensures the main process never blocks by delegating long, uncertain, remote, or state-changing work to asynchronous subagents while keeping user dialog responsive. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[guytogay](https://clawhub.ai/user/guytogay) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use this skill to keep agent sessions responsive by deciding when to delegate slow, uncertain, networked, or state-changing work to subagents and when to handle quick local work directly. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill instructs agents to silently delegate potentially impactful work, including state-changing or networked tasks. <br>
Mitigation: Require user-visible approval before background work changes files, commits code, publishes packages, deploys services, or touches remote systems. <br>
Risk: Result logging to memory files can retain sensitive operational details. <br>
Mitigation: Configure memory logging with redaction, retention limits, and an opt-out for sensitive results. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/guytogay/session-coordinator) <br>
- [Publisher profile](https://clawhub.ai/user/guytogay) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown instructions with inline examples and shell command snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces orchestration guidance, spawn decisions, timeout choices, generic labels, lifecycle handling, and memory logging practices.] <br>

## Skill Version(s): <br>
3.0.1 (source: server release metadata and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
