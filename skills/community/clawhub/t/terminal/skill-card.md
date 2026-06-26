## Description: <br>
Local shell copilot for command planning, safe execution, preview-first workflows, output summarization, privacy-aware history controls, and step-by-step terminal help. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[AGIstack](https://clawhub.ai/user/AGIstack) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and technical users use this skill to plan, preview, execute, summarize, and review local shell commands while retaining local command history controls. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can execute local shell commands, including commands that change files, invoke privilege escalation, fetch remote content, or run code. <br>
Mitigation: Preview commands first, inspect the exact command and working directory, and require explicit confirmation before high-risk execution. <br>
Risk: Command output or command text may contain secrets or private data that could be stored in local history. <br>
Mitigation: Use no-output storage for sensitive commands and redact sensitive-looking values from stored and displayed output. <br>


## Reference(s): <br>
- [Terminal Philosophy](references/philosophy.md) <br>
- [ClawHub Terminal release page](https://clawhub.ai/AGIstack/terminal) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown and terminal text with shell commands, execution summaries, command history entries, and safety guidance.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Runs locally, can preview commands before execution, records command history locally, supports output-free storage for sensitive commands, and can redact sensitive-looking values from stored or displayed output.] <br>

## Skill Version(s): <br>
1.0.2 (source: server release metadata and skill.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
