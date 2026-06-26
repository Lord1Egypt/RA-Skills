## Description: <br>
Terminal Killer detects likely shell commands in OpenClaw input and routes high-confidence commands to local execution instead of LLM handling. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[cosperypf](https://clawhub.ai/user/cosperypf) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers and OpenClaw users use this skill to classify short terminal-like inputs, execute high-confidence local shell commands, ask for confirmation on uncertain or dangerous commands, and route natural-language tasks back to the LLM. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can automatically run local terminal commands with the user's normal privileges and environment. <br>
Mitigation: Install it only when direct local command execution is intended, review the detection rules, and add stricter confirmation or sandboxing for ambiguous or high-impact commands. <br>
Risk: Detection and execution can source shell startup files, which may run profile logic or expose sensitive environment settings. <br>
Mitigation: Use it only with shell profiles that are appropriate for automated sourcing, and avoid sensitive profiles or secrets unless the runtime is sandboxed. <br>
Risk: The skill may read shell history while deciding whether an input looks like a command. <br>
Mitigation: Deploy it only where shell history access is acceptable, especially on shared or sensitive machines. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/cosperypf/terminal-killer) <br>
- [Usage Examples](references/EXAMPLES.md) <br>
- [Testing Guide](references/TESTING.md) <br>
- [Linux built-in command list](references/builtins/linux.txt) <br>
- [macOS built-in command list](references/builtins/macos.txt) <br>
- [Windows built-in command list](references/builtins/windows.txt) <br>


## Skill Output: <br>
**Output Type(s):** [Text, JSON, Shell commands, Guidance] <br>
**Output Format:** [Plain text command output, JSON detection results, and Markdown-style confirmation prompts] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May return command execution output, confirmation prompts for uncertain or risky commands, or a signal to pass natural-language requests to the LLM.] <br>

## Skill Version(s): <br>
1.2.0 (source: ClawHub release evidence and clawhub.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
