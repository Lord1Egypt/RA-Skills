## Description: <br>
Manage API keys securely via GNOME Keyring and inject them into OpenClaw config. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[jswortz](https://clawhub.ai/user/jswortz) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and OpenClaw operators use this skill to store supported API keys in GNOME Keyring, update OpenClaw credential configuration, propagate environment variables, and restart the gateway service after changes. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill handles API keys and may expose secrets through shell history or plaintext environment files if used carelessly. <br>
Mitigation: Prefer interactive or stdin entry, avoid passing secrets directly as shell arguments, and review any configured secrets environment file before use. <br>
Risk: The skill can change OpenClaw credential configuration and import environment variables into the user systemd session. <br>
Mitigation: Review the target OpenClaw paths and supported key names before running it, and verify the resulting credential configuration after updates. <br>
Risk: The skill restarts the OpenClaw gateway service and may stop related gateway processes inside the configured Distrobox container. <br>
Mitigation: Run it during an acceptable maintenance window and confirm the configured container and gateway service names match the intended environment. <br>


## Reference(s): <br>
- [Secret Manager on ClawHub](https://clawhub.ai/jswortz/secret-manager) <br>


## Skill Output: <br>
**Output Type(s):** [shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with shell command examples and a bash script] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Supports interactive, direct argument, and stdin-based secret entry for configured key names.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
