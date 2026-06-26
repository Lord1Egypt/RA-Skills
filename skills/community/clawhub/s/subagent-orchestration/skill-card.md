## Description: <br>
Subagent Orchestration helps OpenClaw users delegate, spawn, configure, and debug Worker, Researcher, and Council subagents while accounting for sandbox, timeout, and context constraints. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[wahajahmed010](https://clawhub.ai/user/wahajahmed010) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent operators use this skill to coordinate OpenClaw subagents for file work, web research, and multi-model review while avoiding common delegation failures. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Delegated subagents may return incomplete or incorrect results when task instructions are vague or missing context. <br>
Mitigation: Keep subtasks bounded, include required context in the task, and review sub-agent results before acting on them. <br>
Risk: Subagents may fail or time out when assigned web access, inline Python, or context patterns outside their sandbox. <br>
Mitigation: Use explicit tool access for researcher subagents, write scripts to files before delegation, set appropriate timeouts, and use light context to reduce overflow risk. <br>


## Reference(s): <br>
- [Subagent Tool Access Reference](references/tool-access.md) <br>
- [ClawHub Skill Page](https://clawhub.ai/wahajahmed010/subagent-orchestration) <br>
- [Council of LLMs Companion Skill](https://github.com/wahajahmed010/council-of-llms) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with code blocks and configuration snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Subagent tasks should use explicit instructions, bounded scope, appropriate timeouts, and reviewed outputs.] <br>

## Skill Version(s): <br>
1.3.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
