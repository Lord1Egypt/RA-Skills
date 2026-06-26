## Description: <br>
Creates, validates, lists, and resumes structured handoff documents so a fresh agent can continue long-running work with clear context. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[wpank](https://clawhub.ai/user/wpank) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and agent operators use this skill to preserve session state before context loss, pauses, or major milestones, and to resume from prior handoff documents with verification checks. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Handoff files can persist sensitive or personal context if users include secrets, credentials, or private project details. <br>
Mitigation: Review generated handoffs before resuming from or sharing them, keep secrets and personal data out of handoffs, and use the included validation workflow to check for likely secrets. <br>
Risk: Old or externally supplied handoff documents may describe stale project paths, branches, assumptions, or file state. <br>
Mitigation: Treat old or external handoffs as untrusted until their project path and contents are verified, and run the staleness check before relying on them. <br>


## Reference(s): <br>
- [Handoff Template](references/handoff-template.md) <br>
- [Resume Checklist](references/resume-checklist.md) <br>
- [ClawHub Skill Page](https://clawhub.ai/wpank/session-handoff) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, guidance] <br>
**Output Format:** [Markdown handoff documents, validation reports, staleness summaries, and command guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Generated handoffs are stored under .claude/handoffs/ and may include project paths, branch names, recent commits, and modified file lists.] <br>

## Skill Version(s): <br>
0.1.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
