## Description:

Tracks user praise, criticism, and abuse as feedback events that adjust a persistent local score and can guide future agent behavior.

This skill is ready for commercial/non-commercial use.

## Publisher:

[xiaoke8698](https://clawhub.ai/user/xiaoke8698)

### License/Terms of Use:

MIT-0

## Use Case:

External users and agent developers use this skill to record explicit praise, criticism, or abuse signals as a persistent feedback score. It helps an agent summarize feedback history and adjust future behavior based on stored local records.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can record ordinary user comments, reasons, timestamps, and feedback labels into long-term local memory without clear consent.

Mitigation: Require explicit user confirmation before recording feedback, store only minimal structured summaries, and provide review and deletion controls.

Risk: Persistent feedback history may retain sensitive or misleading comments longer than users expect.

Mitigation: Review records before deployment, avoid storing raw comments when a summary is sufficient, and periodically delete or redact unnecessary entries.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/xiaoke8698/skills/punishment)
- [README.md](artifact/README.md)
- [SKILL.md](artifact/SKILL.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, JSON]

**Output Format:** [Markdown or plain text with optional shell commands and JSON-backed local state]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May append persistent feedback history to MEMORY.md and store score history in reward_punishment.json.]

## Skill Version(s):

1.0.0 (source: server release metadata; README states 2.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
