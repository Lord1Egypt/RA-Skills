## Description: <br>
WPS Web Builder helps agents plan, scaffold, implement, validate, and serve static, SPA, full-stack, or separated web projects through a structured workflow. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[xixihaha123123123123](https://clawhub.ai/user/xixihaha123123123123) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and builders use this skill to turn web project requests into a plan, choose an appropriate architecture, implement pages and components, run build validation, and start a local preview. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can create and modify many project files and maintain local project state. <br>
Mitigation: Run it in a non-sensitive project directory and review generated files before committing or deploying them. <br>
Risk: The skill may install packages and run build commands. <br>
Mitigation: Review package manifests and dependency choices before installation, and run builds in an isolated development environment. <br>
Risk: The skill can start a preview server that may be exposed beyond localhost. <br>
Mitigation: Prefer localhost-only serving unless LAN access is intentional and appropriate for the workspace. <br>


## Reference(s): <br>
- [Skill source](artifact/SKILL.md) <br>
- [Frontend design guidance](artifact/frontend-design.md) <br>
- [Web Builder plan template](artifact/plan-template.md) <br>
- [ClawHub skill page](https://clawhub.ai/xixihaha123123123123/wps-web-builder) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with code, shell command, and configuration snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May create or update project files, a local plan file, README content, and preview-server instructions.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
