## Description: <br>
SSH OP helps an agent use the ssh-op helper workflow to load a 1Password-managed SSH private key into an in-memory ssh-agent before running ssh. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[moodykong](https://clawhub.ai/user/moodykong) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and operators use this skill to configure and run SSH sessions that rely on a 1Password-managed private key, troubleshoot ssh-op setup, and optionally manage SSH host aliases. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The release is incomplete for the documented workflow because the expected scripts/ssh-op executable and config.env.example are not present in the artifact. <br>
Mitigation: Do not install or rely on this release until those files are supplied and reviewed. <br>
Risk: The workflow handles 1Password-managed SSH keys and may update SSH configuration. <br>
Mitigation: Limit the 1Password vault, item, or service account to the minimum needed, verify the key fingerprint, and inspect or back up hosts.conf and ~/.ssh/config before applying changes. <br>


## Reference(s): <br>
- [ssh-op onboarding runbook](references/onboarding.md) <br>
- [ClawHub skill page](https://clawhub.ai/moodykong/ssh-op) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, shell commands, configuration] <br>
**Output Format:** [Markdown guidance with inline shell commands and configuration values] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May reference local config.env, hosts.conf, and SSH command arguments supplied by the user.] <br>

## Skill Version(s): <br>
0.1.0 (source: server-resolved release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
