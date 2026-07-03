## Description: <br>
Super Clawcompany coordinates PM, developer, and review agents to turn a software request into task planning, generated code, and review feedback. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[molexazwo](https://clawhub.ai/user/molexazwo) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers use this skill to delegate a software build request to coordinated planning, coding, and review agents for rapid prototyping, feature implementation, or small app creation. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Broad triggers can launch external coding agents that may change project files without a clear confirmation step. <br>
Mitigation: Use dry-run first, run in a disposable or version-controlled project directory, and review generated changes before relying on them. <br>
Risk: Task context may be sent to external agent runtimes and model services. <br>
Mitigation: Avoid sensitive prompts or repository paths, keep API keys out of logs, and configure only the credentials required for the intended run. <br>


## Reference(s): <br>
- [Super Clawcompany on ClawHub](https://clawhub.ai/molexazwo/skills/super-clawcompany) <br>
- [OpenClaw](https://openclaw.ai) <br>
- [GLM API Key Portal](https://open.bigmodel.cn/) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown and JSON-like text with generated code, file paths, review feedback, and shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May spawn external agent sessions and may create or modify files in the selected project directory; dry-run mode avoids file changes.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and package.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
