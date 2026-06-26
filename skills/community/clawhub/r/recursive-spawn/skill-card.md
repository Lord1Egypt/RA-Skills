## Description: <br>
Enables an Openclaw agent to spawn child Openclaw instances for separable, complex, or parallel work. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[sparky0520](https://clawhub.ai/user/sparky0520) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent operators use this skill to delegate clearly scoped sub-tasks to child Openclaw agents, including sequential, parallel-gather, and fire-and-forget workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Child agents can receive sensitive progress snapshots or broad delegated tools. <br>
Mitigation: Sanitize snapshots for secrets and personal data, require user approval for sensitive delegation, and pass only narrowly scoped tools needed for the sub-task. <br>
Risk: Fire-and-forget delegation can affect important files, accounts, or model costs without immediate parent review. <br>
Mitigation: Avoid fire-and-forget for sensitive or costly work, define an explicit result path and merge point, and review child output before relying on it. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/sparky0520/recursive-spawn) <br>
- [LiteLLM providers](https://docs.litellm.ai/docs/providers) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with Python code examples and JSON payload shapes] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Child agents can return summary text or write result files when narrowly scoped tools are provided.] <br>

## Skill Version(s): <br>
1.0.4 (source: ClawHub release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
