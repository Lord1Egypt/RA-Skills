## Description:

React Orchestrator provides a dual-system ReAct and Reflexion framework for routing agent tasks between fast execution and deeper multi-step reasoning.

This skill is ready for commercial/non-commercial use.

## Publisher:

[yuyonghao-123](https://clawhub.ai/user/yuyonghao-123)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent builders use this skill to orchestrate tool-using AI workflows, automatically choose fast or reflective reasoning modes, and inspect execution history for debugging or audit.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can orchestrate privileged tools and Code Mode can execute generated JavaScript or PowerShell that reads, writes, runs commands, or sends data externally.

Mitigation: Register only reviewed tools, run the skill in a restricted environment, do not pass untrusted or model-generated code to Code Mode, and keep filesystem, command, and network access narrowly scoped.

Risk: Human approval behavior is documented as a safeguard but may not enforce all high-impact actions by itself.

Mitigation: Enforce approvals outside the skill for file writes, command execution, and external data transfer, and require explicit human review before those tools run.

Risk: Current reasoning, parameter extraction, and tool matching rely on heuristics and keywords, which can select the wrong mode or produce incorrect tool parameters.

Mitigation: Validate tool parameters with schemas, test representative workflows before release, and keep high-impact operations behind review gates.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/yuyonghao-123/skills/yuyonghao-react-orchestrator)
- [ReAct Paper](https://arxiv.org/abs/2210.03629)
- [Reflexion Paper](https://arxiv.org/abs/2303.11366)
- [README](artifact/README.md)
- [Usage Guide](artifact/USAGE-GUIDE.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Text answers, Markdown guidance, JavaScript or PowerShell code snippets, configuration examples, and JSON execution history.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs depend on registered tools and may include execution traces, selected reasoning mode, iteration count, duration, and reflections.]

## Skill Version(s):

0.1.0 (source: server release metadata and package.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
