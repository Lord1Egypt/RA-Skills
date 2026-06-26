## Description: <br>
Read a line from standard input into a variable. Use for interactive shell prompts and script input handling. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[dinghaibin](https://clawhub.ai/user/dinghaibin) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to capture a single line of interactive standard input for scripts and shell-style prompts. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Password or silent-input usage may expose sensitive entries because the documented no-echo behavior is not supported by the implementation. <br>
Mitigation: Do not use this skill for passwords or other sensitive input unless the implementation is corrected and reviewed for true no-echo option handling. <br>
Risk: Option behavior may not match the documented prompt, timeout, and silent-mode flags. <br>
Mitigation: Review behavior before installing in workflows that depend on shell-like read options. <br>


## Reference(s): <br>
- [Read Tool on ClawHub](https://clawhub.ai/dinghaibin/read-tool) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, guidance] <br>
**Output Format:** [Plain text or Markdown with shell command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces single-line input capture guidance; implementation currently echoes input even where silent input is documented.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
