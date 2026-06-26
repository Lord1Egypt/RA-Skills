## Description: <br>
Yang Openclaw Health provides a quick local health check for OpenClaw installations by checking Node.js version, gateway status, config files, port conflicts, environment variables, and common troubleshooting issues. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[yang1002378395-cmyk](https://clawhub.ai/user/yang1002378395-cmyk) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and OpenClaw users use this skill to run a local health check when troubleshooting installation or configuration issues. It checks Node.js version, OpenClaw gateway status, config file presence, port 3000 usage, environment key presence, and common permission problems. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The diagnostic inspects local OpenClaw paths, process and port state, and whether model-provider API-key environment variables are present. <br>
Mitigation: Run it only in a trusted local shell and avoid sharing full diagnostic output when paths, process names, or environment setup details are sensitive. <br>
Risk: Troubleshooting output can suggest configuration issues that still require user judgment before changing an installation. <br>
Mitigation: Review the reported checks before applying fixes, and confirm any configuration or permission changes against the local OpenClaw setup. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/yang1002378395-cmyk/yang-openclaw-health) <br>
- [OpenClaw Install Service Landing Page](https://yang1002378395-cmyk.github.io/openclaw-install-service/) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, guidance] <br>
**Output Format:** [Markdown guidance and terminal diagnostic text] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Local diagnostic output reports pass/fail status for installation checks without exposing API key values.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
