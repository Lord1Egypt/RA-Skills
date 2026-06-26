## Description: <br>
Smart Compact helps OpenClaw agents scan conversation and tool output before compaction, extract important details into local memory files, and produce a pre-compact checklist for user review. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[wavmson](https://clawhub.ai/user/wavmson) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent users use this skill before context compaction to preserve important facts, decisions, errors, preferences, and task progress from long OpenClaw sessions. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill may persist broad conversation and tool-output details into local memory files, including sensitive or access-related information. <br>
Mitigation: Require explicit review before any memory item is saved, redact sensitive values, and disallow passwords, tokens, cookies, login details, or private access material. <br>
Risk: Saved compaction notes may outlive the session and expose stale or private project context. <br>
Mitigation: Periodically inspect and delete generated memory files, and keep the append-only record limited to information needed after compaction. <br>
Risk: Compaction could proceed before unresolved warnings are handled. <br>
Mitigation: Use the generated checklist to resolve warning items first and require explicit user confirmation before running compaction. <br>


## Reference(s): <br>
- [Smart Compact on ClawHub](https://clawhub.ai/wavmson/smart-compact) <br>
- [wavmson publisher profile](https://clawhub.ai/user/wavmson) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, guidance] <br>
**Output Format:** [Markdown checklist with concise guidance and optional shell command suggestions] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May propose append-only local memory file updates before user-confirmed compaction.] <br>

## Skill Version(s): <br>
1.0.4 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
