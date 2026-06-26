## Description: <br>
Security agent that inventories installed OpenClaw skills, analyzes them for threats, and syncs results to your Clawned dashboard. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[uttamnest](https://clawhub.ai/user/uttamnest) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and OpenClaw users use this agent to inventory installed skills, check their security posture, and sync scan results to a Clawned dashboard. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The agent connects to a remote Clawned service and syncs installed-skill metadata plus hostname and operating-system registration data. <br>
Mitigation: Install only if you trust the Clawned service, use a dedicated API key, and point CLAWNED_SERVER only at the intended service. <br>
Risk: Explicit scan operations can send selected skill file contents to the Clawned server for analysis. <br>
Mitigation: Run scan only on skill directories you intend to submit for analysis and review local data-handling expectations before scanning. <br>
Risk: Cron or watch-style sync can create continuing dashboard updates from the local environment. <br>
Mitigation: Enable scheduled or watch-based sync only when ongoing updates are desired, and disable it when periodic reporting is no longer needed. <br>


## Reference(s): <br>
- [Clawned homepage](https://clawned.io) <br>
- [ClawHub skill page](https://clawhub.ai/uttamnest/skill-sec) <br>
- [Detection patterns](references/detection-patterns.md) <br>
- [Threat model](references/threat-model.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Command-line text with JSON configuration examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires python3 and CLAWNED_API_KEY; CLAWNED_SERVER is optional.] <br>

## Skill Version(s): <br>
1.0.1 (source: server evidence release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
