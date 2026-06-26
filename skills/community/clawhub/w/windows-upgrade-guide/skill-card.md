## Description: <br>
Guides Windows users through OpenClaw installation, upgrade, and troubleshooting for crashes, lost configuration, version compatibility, WeChat integration, and WSL versus native Windows setup. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[rfdiosuao](https://clawhub.ai/user/rfdiosuao) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and Windows OpenClaw users use this skill to diagnose upgrade failures, compare WSL2 with native Windows installs, back up and migrate configuration, and recover from compatibility issues. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Troubleshooting commands can install packages and change global OpenClaw state. <br>
Mitigation: Review each command before execution and run it only in the intended Windows or WSL environment. <br>
Risk: Reset steps can remove OpenClaw configuration under ~/.openclaw. <br>
Mitigation: Back up ~/.openclaw before reset and prefer renaming the directory instead of deleting it. <br>
Risk: The Lark/Feishu plugin install step is not clearly scoped to the WeChat recovery workflow. <br>
Mitigation: Run the plugin install only after confirming it is required for the intended recovery path. <br>


## Reference(s): <br>
- [OpenClaw official documentation](https://docs.openclaw.ai) <br>
- [WSL2 installation guide](https://docs.microsoft.com/windows/wsl/install) <br>
- [Node.js downloads](https://nodejs.org/) <br>
- [OpenClaw issue tracker](https://github.com/openclaw/openclaw/issues) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline shell command blocks and configuration guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May propose package installation, backup, reset, migration, and diagnostic commands for user review.] <br>

## Skill Version(s): <br>
1.0.0 (source: skill.json and release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
