## Description: <br>
Deploy and manage a SONiC sonic-mgmt KVM virtual testbed with cEOS neighbors for running pytest-based network tests. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[yxieca](https://clawhub.ai/user/yxieca) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and network test engineers use this skill to set up, repair, tear down, and operate a local SONiC KVM testbed with cEOS neighbors for pytest-based sonic-mgmt validation. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill includes documented passwords and credential examples for a real local SONiC virtual testbed. <br>
Mitigation: Use unique lab-only secrets, prefer SSH keys where possible, and do not reuse the documented passwords. <br>
Risk: The skill includes privileged changes such as temporary admin accounts, sudoers entries, and broad Docker socket permissions. <br>
Mitigation: Run only in an isolated disposable lab and remove temporary accounts, sudoers entries, and socket permission changes after testing. <br>
Risk: The DUT and management bridge can expose the lab if connected to untrusted networks. <br>
Mitigation: Keep the DUT and management bridge isolated from untrusted networks. <br>


## Reference(s): <br>
- [Credentials Configuration](references/credentials.md) <br>
- [Troubleshooting](references/troubleshooting.md) <br>
- [SONiC sonic-mgmt repository](https://github.com/sonic-net/sonic-mgmt.git) <br>
- [ClawHub release page](https://clawhub.ai/yxieca/sonic-kvm-testbed) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline shell commands and configuration snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Guidance targets a disposable local SONiC KVM lab and may include privileged host or DUT commands.] <br>

## Skill Version(s): <br>
1.2.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
