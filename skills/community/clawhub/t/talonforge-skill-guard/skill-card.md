## Description: <br>
Scans ClawHub skills before installation for prompt injections, malware patterns, hardcoded secrets, data exfiltration risks, and other threats. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[casperzinou](https://clawhub.ai/user/casperzinou) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent users use this skill to stage a ClawHub skill, scan it before installation, and block installation when security issues are reported. It is intended as a pre-install review step for OpenClaw skill directories. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The installer can bypass scanning when run with --skip-scan. <br>
Mitigation: Use the default scan path and avoid --skip-scan unless the staged skill has already been inspected. <br>
Risk: The installer can overwrite or move skill directories, especially when --force is used. <br>
Mitigation: Run it only where modifying the OpenClaw skills directory is acceptable, and inspect target paths before using --force. <br>
Risk: The workflow depends on live third-party code through uvx mcp-scan@latest and curl-to-shell dependency guidance. <br>
Mitigation: Prefer pinned or verified scanner and dependency installation steps, and run scans in an environment appropriate for third-party code execution. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/casperzinou/talonforge-skill-guard) <br>
- [mcp-scan repository](https://github.com/invariantlabs-ai/mcp-scan) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Guidance, Text] <br>
**Output Format:** [Markdown guidance with bash commands and terminal output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Includes exit-code outcomes for clean install, dependency or network errors, and threats found.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
