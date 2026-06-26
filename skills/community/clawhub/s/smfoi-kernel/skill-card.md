## Description: <br>
SMFOI-KERNEL provides a local, auditable 5-step orientation protocol that helps autonomous agents maintain workspace awareness, safety constraints, and turn-level logging. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[rigeneproject](https://clawhub.ai/user/rigeneproject) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent operators use this skill to add an every-turn orientation routine that keeps an agent focused on workspace boundaries, active safety constraints, task intent, and a local audit trail. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill runs on every turn and may create a persistent local audit trail from conversation-derived task context. <br>
Mitigation: Install it only in workspaces where persistent turn-level logs are acceptable, and periodically review or delete ./memory/kernel/state.md. <br>
Risk: Protocol-change suggestions could be mistaken for self-executing changes. <br>
Mitigation: Treat Level 3 recursion output as a human-reviewed text proposal only, consistent with the artifact's non-executable boundary. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/rigeneproject/smfoi-kernel) <br>
- [README](README.md) <br>
- [Skill definition](SKILL.md) <br>
- [Orientation logic](kernel_v0.2.txt) <br>
- [Changelog](CHANGELOG.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, configuration, guidance] <br>
**Output Format:** [Markdown guidance and structured text with local file path references] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May maintain a persistent local audit trail at ./memory/kernel/state.md when installed in an agent workspace.] <br>

## Skill Version(s): <br>
1.0.4 (source: server release evidence; artifact content version 0.2.2) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
