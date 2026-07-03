## Description: <br>
Kannaka Constellation monitors status across Kannaka apps, services, swarm health, and connectivity. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[nickflach](https://clawhub.ai/user/nickflach) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use this skill to check the health of Kannaka constellation components, inspect swarm connectivity, monitor NATS transport status, and diagnose cross-service issues. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Some commands can join or communicate with an external swarm and publish agent state. <br>
Mitigation: Use read-only status commands for monitoring, and run join, sync, listen --auto-sync, or brief --peers only when external swarm communication is intended. <br>
Risk: The health --apply command can modify memory-related state. <br>
Mitigation: Run health without --apply first, review the report, and apply changes only when the memory-health actions are expected. <br>
Risk: The skill mixes status checks with commands that can contact external services. <br>
Mitigation: Review the configured NATS and service URLs before use, especially in environments that require read-only or internal-only operations. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/nickflach/skill-kannaka-constellation) <br>
- [Kannaka Radio](https://radio.ninja-portal.com) <br>
- [Kannaka Observatory](https://observatory.ninja-portal.com) <br>
- [GhostSignals markets API](https://radio.ninja-portal.com/api/markets) <br>
- [Kannaka installer download](https://radio.ninja-portal.com/download) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline shell commands and configuration snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Some commands can emit JSON when invoked with --json.] <br>

## Skill Version(s): <br>
1.1.0 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
