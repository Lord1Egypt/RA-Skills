## Description: <br>
Install, configure, authorize and run wakehook so the user's agent (OpenClaw or Hermes) runs their morning routine when they wake up. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[robbeverhelst](https://clawhub.ai/user/robbeverhelst) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers and automation users use Wakehook to connect Google Health or Fitbit sleep data to agent or webhook-based morning routines. The skill guides installation, OAuth setup, configuration, authorization, and operation for wake-triggered automations. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The built-in /test/replay endpoint can trigger wake actions without authentication in common poll-mode setups if the service is reachable. <br>
Mitigation: Bind or firewall port 8080, avoid exposing /test/replay publicly, and remove or block that endpoint in production where possible. <br>
Risk: Wakehook uses sensitive Google OAuth credentials and stores authorization state. <br>
Mitigation: Protect .env and wake.sqlite with restrictive permissions and encrypted backups, and revoke the Google OAuth grant if the host or database is exposed. <br>
Risk: Configured subscribers receive wake events and may trigger downstream automations. <br>
Mitigation: Only add subscriber URLs you trust and prefer signed or authenticated subscriber delivery. <br>


## Reference(s): <br>
- [Wakehook homepage](https://github.com/robbeverhelst/wakehook) <br>
- [Wakehook ClawHub listing](https://clawhub.ai/robbeverhelst/wakehook) <br>
- [README](artifact/README.md) <br>
- [Design](artifact/DESIGN.md) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, markdown, shell commands, configuration] <br>
**Output Format:** [Markdown guidance with inline JSON, YAML, and shell command blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces setup steps for a Bun-based self-hosted wake-event service and related agent webhook configuration.] <br>

## Skill Version(s): <br>
1.0.1 (source: ClawHub release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
