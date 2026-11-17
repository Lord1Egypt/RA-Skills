## Description:

Add a Telegram private-chat footer (`🧠 Model + 💭 Think + 📊 Context`) to OpenClaw replies, with dry-run preview, backup, syntax validation, rollback, and restart guidance.

This skill is ready for commercial/non-commercial use.

## Publisher:

[c-joey](https://clawhub.ai/user/c-joey)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and OpenClaw operators use this skill to patch installed OpenClaw Telegram reply bundles so private-chat responses include model, thinking level, and context usage footer details. It is intended for controlled OpenClaw environments where the operator can dry-run, back up, apply, restart, and verify the patch through a real Telegram private-chat reply.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill persistently modifies installed OpenClaw JavaScript bundle files.

Mitigation: Run the dry-run flow first, inspect the target files, and apply the patch only on systems you control, preferably in a staging instance before production.

Risk: Rollback may be unreliable after repeated patch or upgrade cycles.

Mitigation: Keep an independent clean backup of the OpenClaw dist directory and verify rollback behavior before relying on the included revert script.

Risk: Static marker checks and smoke tests do not prove the live Telegram reply path was patched.

Mitigation: After applying the patch, perform a true gateway restart with a new process and confirm a real Telegram private-chat reply shows the footer.

## Reference(s):


## Skill Output:

**Output Type(s):** [Shell commands, Code, Configuration, Guidance]

**Output Format:** [Markdown guidance with inline shell commands and Python script usage]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces patch, verification, rollback, and restart guidance; it does not produce model outputs directly.]

## Skill Version(s):

1.0.11 (source: server release metadata and changelog)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
