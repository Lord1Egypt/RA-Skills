## Description: <br>
Creates standardized setup flows for installed OpenClaw skills, including directory structure, configuration templates, core file updates, and setup logs. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[tengcareergmail](https://clawhub.ai/user/tengcareergmail) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and OpenClaw users use this skill to initialize or enable installed skills through repeatable setup steps, configuration and state templates, setup logs, quick references, and proposed updates to core agent files. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can make lasting changes to core agent behavior and memory files such as SOUL.md, AGENTS.md, MEMORY.md, and TOOLS.md. <br>
Mitigation: Require the agent to show each proposed file creation and edit before applying changes, and review the setup log after execution. <br>
Risk: Using the skill on untrusted skill packages could propagate misleading setup instructions into persistent configuration or memory files. <br>
Mitigation: Review and scan the target skill before setup, and limit use to skills from trusted sources. <br>
Risk: Configuration templates and setup logs may encourage storing secrets in markdown files. <br>
Mitigation: Keep API keys and other secrets out of markdown configuration and logs; reference approved secret storage instead. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/tengcareergmail/skill-setup-flow) <br>
- [README](artifact/README.md) <br>
- [Quickstart](artifact/QUICKSTART.md) <br>
- [Setup template](artifact/setup-template.md) <br>
- [Self-improving setup example](artifact/examples/self-improving-setup.md) <br>


## Skill Output: <br>
**Output Type(s):** [Markdown, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown with inline shell commands and file templates] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May propose persistent edits to core agent files and create setup logs or configuration files.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and skill.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
