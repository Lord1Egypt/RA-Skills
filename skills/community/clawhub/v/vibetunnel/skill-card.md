## Description: <br>
Manage VibeTunnel terminal sessions. Create, list, monitor, and control terminal sessions visible in the VibeTunnel web dashboard. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[basher83](https://clawhub.ai/user/basher83) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and operators use this skill to manage VibeTunnel terminal sessions through REST API commands, including creating sessions, listing status, sending input, resizing terminals, and deleting sessions. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can send input to terminal sessions, so commands may reveal credentials, change files, or perform destructive actions if used carelessly. <br>
Mitigation: Keep VT_URL pointed at a trusted local or controlled VibeTunnel server, review command text before sending it, and avoid credential-revealing or destructive shell input unless explicitly intended. <br>
Risk: Terminal sessions can continue running after the immediate task is complete. <br>
Mitigation: Review active sessions and clean up long-running or exited sessions when they are no longer needed. <br>


## Reference(s): <br>
- [VibeTunnel project homepage](https://github.com/AugmentedMomentum/vibetunnel) <br>
- [ClawHub skill page](https://clawhub.ai/basher83/vibetunnel) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with curl and jq command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses VT_URL to select the VibeTunnel server; examples assume a trusted local or controlled endpoint.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
