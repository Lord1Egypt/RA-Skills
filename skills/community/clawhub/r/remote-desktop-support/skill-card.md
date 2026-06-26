## Description: <br>
Linux/Fedora-GNOME-first, early but safety-tested skill for short-lived browser-based remote desktop support links using local-only VNC/Guacamole and outbound tunnels. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[tommyclawd](https://clawhub.ai/user/tommyclawd) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Support operators and trusted helpers use this skill to create temporary browser-based access to the publisher's current live Fedora/GNOME desktop for troubleshooting. It is intended for deliberate, short sessions with preflight checks, view-only default behavior, and explicit cleanup. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The live desktop can be exposed through a temporary browser link. <br>
Mitigation: Use only deliberate, short support sessions; default to view-only mode; share the one-click URL only with the intended helper and treat it as password-equivalent. <br>
Risk: Opening access can weaken local lock or VNC protections during the session. <br>
Mitigation: Run preflight and dry-run before opening access; require explicit approval for control or unlocking the current session. <br>
Risk: Automatic expiry may not reliably close the session in every environment. <br>
Mitigation: Verify the expiry method is active, then run close followed by status when support ends or the TTL expires. <br>
Risk: Containers, credentials, listeners, or GNOME VNC state could remain after use. <br>
Mitigation: Use the close workflow and confirm status reports closed; use uninstall --purge when removing runtime state is appropriate. <br>


## Reference(s): <br>
- [Remote Desktop Support Security Model](references/security-model.md) <br>
- [ClawHub Skill Page](https://clawhub.ai/tommyclawd/remote-desktop-support) <br>
- [Publisher Profile](https://clawhub.ai/user/tommyclawd) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Configuration, Guidance, JSON status] <br>
**Output Format:** [Markdown guidance with bash commands; helper script emits JSON for lifecycle commands.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires Linux with python3 and podman; designed for Fedora/GNOME current-session support.] <br>

## Skill Version(s): <br>
0.1.2 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
