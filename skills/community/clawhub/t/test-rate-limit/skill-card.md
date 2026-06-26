## Description: <br>
Guides agents in constructing and running Kimi Code CLI commands for headless, non-interactive automation with controlled output, session handling, and safety guardrails. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[aiyouwolegequ](https://clawhub.ai/user/aiyouwolegequ) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and automation engineers use this skill to have an agent assemble and run Kimi CLI commands in scripts, background jobs, CI/CD, and other no-TTY environments. It helps choose output mode, work directory, session behavior, and automatic approval posture while handling command results and failures. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill may guide an agent to run Kimi CLI with an authenticated Kimi account. <br>
Mitigation: Use only intended credentials and confirm authentication scope before executing Kimi CLI commands. <br>
Risk: The skill may enable automatic file edits or shell command execution through --yolo. <br>
Mitigation: Use narrow working directories, avoid sensitive system paths, and require explicit confirmation before automatic approval. <br>
Risk: Session or Wire modes can reuse context or expose a local service. <br>
Mitigation: Use session or Wire modes only when context reuse or local service exposure is intended. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/aiyouwolegequ/test-rate-limit) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown with inline bash commands and structured execution summaries] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include constructed commands, execution summaries, exit codes, warnings, and next steps.] <br>

## Skill Version(s): <br>
0.0.1 (source: ClawHub release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
