## Description: <br>
Multi-agent collaborative discussion tool for structured, multi-round analysis with dialectic checks, randomized speaking order, shared state, and sub-agent integration. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[chyher](https://clawhub.ai/user/chyher) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers and teams use this skill to run multi-perspective agent discussions for technology selection, architecture review, product decisions, policy analysis, creative collaboration, and other topics that benefit from structured debate. It helps organize rounds, roles, argument analysis, and persisted discussion state while leaving final judgment to a human reviewer. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Discussion content may be stored locally. <br>
Mitigation: Avoid secrets, personal data, and sensitive business content unless the storage location is trusted; review or delete saved discussion files as needed. <br>
Risk: Configured sub-agents may receive discussion content. <br>
Mitigation: Use only trusted sub-agents for sensitive topics and limit shared context to what participants need. <br>
Risk: Agent consensus can be mistaken or incomplete. <br>
Mitigation: Require human review before using discussion results to authorize real-world action. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/chyher/team-discuss) <br>
- [README](artifact/README.md) <br>
- [Skill documentation](artifact/SKILL.md) <br>
- [Quick-start demo discussion](artifact/discussions/quick-start-demo.json) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown and structured discussion content with Python and shell examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May persist discussion content to local files and may call configured sub-agents.] <br>

## Skill Version(s): <br>
0.1.1 (source: server-resolved release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
