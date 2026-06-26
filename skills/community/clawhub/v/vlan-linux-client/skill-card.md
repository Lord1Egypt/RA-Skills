## Description: <br>
Helps agents guide VLAN.CN Linux client installation, login, virtual network management, service control, and diagnostics. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[sxf-oss](https://clawhub.ai/user/sxf-oss) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and Linux operators use this skill to manage VLAN.CN client setup, authentication, virtual network connections, service lifecycle commands, and troubleshooting steps. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill includes a curl-to-sh remote installer pattern that may execute unverified code. <br>
Mitigation: Only run the installer after verifying the VLAN.CN source through a trusted channel and explicitly approving execution. <br>
Risk: Login commands can expose credentials if passwords are entered directly on the command line. <br>
Mitigation: Prefer short-lived login codes and avoid placing passwords in shell commands or command history. <br>
Risk: Service control and removal commands can change system state or delete client files. <br>
Mitigation: Manually confirm sudo, service, and deletion commands, including target paths, before allowing an agent to run them. <br>


## Reference(s): <br>
- [VLAN.CN Linux Client Documentation](https://www.vlan.cn/guide/linux-client) <br>
- [VLAN.CN Management Console](https://www.vlan.cn) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Shell commands, Configuration instructions] <br>
**Output Format:** [Markdown with inline bash code blocks and command tables] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Commands may require user-specific VLAN IDs, login codes, credentials, or sudo confirmation.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
