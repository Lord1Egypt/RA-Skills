## Description: <br>
Wolverine is a supervised self-healing process manager for OpenClaw that watches crashes, diagnoses errors with AI, proposes reviewed fixes, verifies them, and restarts with backup and rollback support. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[bobbyswhip](https://clawhub.ai/user/bobbyswhip) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and OpenClaw operators use Wolverine to supervise a gateway, recover from crashes, inspect AI-proposed fixes, and manage backup and rollback workflows. It is best suited to supervised staging or non-critical workspaces until operational safeguards are verified for the project. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can change code and control process restarts while supervising a project. <br>
Mitigation: Test in a staging workspace first, confirm approval gates for code changes and operational commands, and verify backup and rollback behavior before supervising important projects. <br>
Risk: Healing activity can affect stability or cost if it repeats without appropriate limits. <br>
Mitigation: Keep documented heal limits and timeouts enabled, know how to disable healing, and monitor repeated failures that should be handed to a human. <br>
Risk: Error text, logs, memory, and backups may contain sensitive project information. <br>
Mitigation: Confirm where memory and backups are stored, keep secret redaction enabled, and review generated logs before sharing them. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/bobbyswhip/wolverine-ai) <br>
- [Project homepage](https://github.com/bobbyswhip/Wolverine) <br>
- [npm package](https://www.npmjs.com/package/wolverine-ai) <br>
- [Website](https://wolverine.dev) <br>


## Skill Output: <br>
**Output Type(s):** [text, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands, JSON configuration examples, and proposed code changes] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May produce backup, rollback, quarantine, and forensic log artifacts during supervised healing workflows.] <br>

## Skill Version(s): <br>
1.0.2 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
