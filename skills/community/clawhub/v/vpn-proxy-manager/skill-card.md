## Description: <br>
Manages V2Ray proxy startup, shutdown, system proxy settings, and automatic switching based on network availability. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[BOMBFUOCK](https://clawhub.ai/user/BOMBFUOCK) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers and technical users use this skill to manage a local V2Ray/Xray proxy, configure shell proxy environment variables, test connectivity, and wrap network commands that may need proxy access. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The security summary reports that the skill can run arbitrary shell commands through its command-wrapping mode. <br>
Mitigation: Review command text before using wrap mode and avoid passing untrusted or generated commands. <br>
Risk: The security summary reports that the skill can alter local proxy behavior and write to the user's shell profile. <br>
Mitigation: Review the shell script before installation and confirm the proxy environment changes are appropriate for the target machine. <br>
Risk: The security guidance notes that auto and off modes may start background processes and stop matching V2Ray/Xray processes. <br>
Mitigation: Verify the configured V2Ray path and process matching behavior before running auto or off modes on a shared workstation. <br>
Risk: The security guidance notes that the skill may contact external test sites during network checks. <br>
Mitigation: Confirm external connectivity checks are acceptable for the deployment environment before enabling automatic mode. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/BOMBFUOCK/vpn-proxy-manager) <br>
- [README](README.md) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown with inline bash code blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces local proxy management commands and configuration guidance; no structured API response is defined.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and artifact _meta.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
