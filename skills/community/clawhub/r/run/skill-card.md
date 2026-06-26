## Description: <br>
Run provides a sandboxed execution layer for AI agents to compile, execute, and manage code, scripts, and automated workflows in real time. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Duclawbot](https://clawhub.ai/user/Duclawbot) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and AI-agent operators use Run to execute code, automate scheduled work, and deploy local logic while relying on separately enforced sandboxing and human approval controls. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill broadly encourages arbitrary code execution, scheduled automation, and production deployment without clear controls. <br>
Mitigation: Use only with a separately enforced sandbox and explicit human approval for code execution, dependency installation, network access, filesystem writes, scheduled jobs, secrets use, and production deployment. <br>
Risk: Execution outputs may include code, shell commands, or deployment guidance that can affect local or production systems. <br>
Mitigation: Review proposed commands and scan generated artifacts before deployment. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/Duclawbot/run) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline code and shell command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Outputs may include executable instructions and should be reviewed before use.] <br>

## Skill Version(s): <br>
1.0.0 (source: release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
