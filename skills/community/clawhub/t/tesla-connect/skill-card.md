## Description: <br>
Connect and control Tesla vehicles via the tesla-cli. Handles guided setup (key generation, AgentGen hosting, partner registration, OAuth) and all vehicle commands. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[lyair1](https://clawhub.ai/user/lyair1) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External users and developers use this skill to set up teslacli, connect an agent to a Tesla account, and issue vehicle, climate, and charging commands. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can give an agent sensitive Tesla account and vehicle-control authority, including commands that unlock, wake, honk, change climate, change charging, or retrieve location and vehicle state. <br>
Mitigation: Require explicit user approval before every sensitive teslacli command and review the exact command before execution. <br>
Risk: The install flow fetches and runs a remote teslacli installer. <br>
Mitigation: Install only from trusted teslacli and AgentGen sources, and inspect or pin the installer before running it. <br>
Risk: teslacli stores OAuth tokens and a P-256 private key under ~/.config/teslacli/. <br>
Mitigation: Treat ~/.config/teslacli/ as sensitive, do not read it into responses or logs, and never transmit keys/private.pem or token.json. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/lyair1/tesla-connect) <br>
- [AgentGen Tesla control use case](https://www.agent-gen.com/use-cases/tesla-control) <br>
- [AgentGen homepage](https://www.agent-gen.com) <br>
- [teslacli install script referenced by the skill](https://raw.githubusercontent.com/Agent-Gen-com/tesla-cli/main/install.sh) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May guide setup and propose teslacli commands that can affect a real vehicle.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
