## Description: <br>
Tmp Soul Evolver analyzes agent memory and learning files with the MiniMax API, then appends updates to workspace identity files such as SOUL.md, USER.md, and IDENTITY.md. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[relunctance](https://clawhub.ai/user/relunctance) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent operators use this skill to periodically review accumulated memory, learning, and error records and maintain long-lived agent identity/profile files. It is intended for scheduled or manual memory evolution, not one-shot task execution or real-time responses. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Local memory, learning, and profile excerpts can be sent to MiniMax during analysis. <br>
Mitigation: Use a dedicated MiniMax API key, avoid processing sensitive workspaces, review memory sources before execution, and disable hawk-bridge unless vector memory is required. <br>
Risk: Scheduled operation can persistently change long-lived agent identity and profile files. <br>
Mitigation: Run with --dry-run first, review proposed changes before writes, keep backups enabled, and use restore only after confirming the selected backup. <br>
Risk: Target-file and path guardrails are limited in the provided evidence. <br>
Mitigation: Restrict target files through configuration, run in an isolated workspace, and avoid unattended scheduled use until allowlisting and path validation are confirmed. <br>


## Reference(s): <br>
- [Architecture reference](references/ARCHITECTURE.md) <br>
- [ClawHub skill page](https://clawhub.ai/relunctance/soul-evolver) <br>


## Skill Output: <br>
**Output Type(s):** [markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with shell commands and configuration snippets; runtime updates are appended as Markdown blocks.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires python3 and MINIMAX_API_KEY; includes dry-run, status, cron, and restore workflows.] <br>

## Skill Version(s): <br>
1.0.1 (source: ClawHub release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
