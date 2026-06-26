## Description: <br>
Smart Model Router auto-detects a prompt's intent (fix, plan, or flow) and routes it to an appropriate AI model. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[wizelements](https://clawhub.ai/user/wizelements) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, teams, and OpenClaw users use this skill to route natural-language prompts to fix, plan, or flow model paths, with shell aliases and override flags for manual control. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Prompts may be automatically sent to different cloud model backends. <br>
Mitigation: Confirm which providers receive prompts and avoid routing private code, credentials, customer data, or regulated information unless those providers are approved. <br>
Risk: The artifact does not clearly explain consent, routing history storage, export behavior, or uninstall controls. <br>
Mitigation: Review configuration and shell startup changes before installation, confirm how to disable automatic routing, and document how to remove any added shell sourcing. <br>


## Reference(s): <br>
- [Smart Model Router on ClawHub](https://clawhub.ai/wizelements/smart-router-ai) <br>
- [README.md](artifact/README.md) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, shell commands, configuration] <br>
**Output Format:** [Markdown with inline shell commands and configuration guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Routes prompts by detected intent and supports manual override flags.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and artifact frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
