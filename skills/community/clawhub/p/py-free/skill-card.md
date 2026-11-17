## Description:

编写可靠 Python 代码的基础能力，覆盖可变默认参数陷阱、import 规范与基础异常处理。

This skill is ready for commercial/non-commercial use.

## Publisher:

[thcjp](https://clawhub.ai/user/thcjp)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and teams use this skill to review or draft Python code for common baseline issues, including mutable default arguments, import organization, basic exception handling, resource management, and simple type-hint or None-check concerns.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may be selected for broad development tasks and may lead an agent toward command execution or network/API workflows that are not tightly bounded.

Mitigation: Use it only in trusted review contexts, prefer a revised version with read-only review scope, and require explicit approval for any command execution, file writing, or external network/API call.

Risk: Broad trigger text can make the skill active outside its intended Python baseline-review use case.

Mitigation: Narrow activation to Python code review for mutable defaults, imports, exceptions, resources, and basic typing before deployment in shared or commercial environments.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/thcjp/skills/py-free)
- [Publisher profile](https://clawhub.ai/user/thcjp)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, guidance]

**Output Format:** [Markdown, JSON, or text guidance with optional rewritten Python snippets and command suggestions]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include issue lists, scores, repair suggestions, rewritten code snippets, import ordering, type-hint suggestions, and execution logs.]

## Skill Version(s):

1.0.0 (source: server evidence and artifact metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
