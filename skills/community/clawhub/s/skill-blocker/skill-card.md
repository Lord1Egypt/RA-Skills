## Description: <br>
Skill Blocker - 安全守卫 is an advisory safety gatekeeper that tells an agent to block risky commands, unsafe file operations, suspicious network requests, and dangerous skill behavior before execution. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[squallfire](https://clawhub.ai/user/squallfire) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill as an advisory guardrail for ClawHub and OpenClaw agents to flag destructive shell commands, credential access, unsafe network execution, sensitive configuration edits, and other high-risk actions before execution. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can direct an agent to disable other skills or edit global OpenClaw configuration. <br>
Mitigation: Require explicit user confirmation before changing installed skills or global configuration. <br>
Risk: Blocked-request logging may capture sensitive details from user prompts or operations. <br>
Mitigation: Minimize log contents, avoid secrets, and keep logs local for user review. <br>
Risk: Aggressive blocking guidance may stop legitimate work. <br>
Mitigation: Treat blocks as advisory, explain the matched risk pattern, and ask for confirmation before continuing with ambiguous operations. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/squallfire/skill-blocker) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with command examples and JSON log examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Advisory prompt content; no executable payload is present in the provided artifact evidence.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
