## Description:

Automatically loads recent conversation memory into new sessions and generates AI summaries during compaction to maintain continuity across conversations while preserving recent raw messages for exact resumption.

This skill is ready for commercial/non-commercial use.

## Publisher:

[thomasmarcel](https://clawhub.ai/user/thomasmarcel)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent users use this skill to preserve OpenClaw conversation continuity across sessions by saving summaries and a bounded set of recent raw turns, then loading them at the next session start.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Recent prompts, assistant replies, and summaries may be saved in plaintext under the workspace and reused in later sessions.

Mitigation: Avoid using the skill with secrets, credentials, regulated data, or shared repositories unless redaction and retention controls are added.

Risk: Recalled conversation memory is injected into later sessions with unusually high authority, so stale or prompt-like content could influence future agent behavior.

Mitigation: Review stored memory before reuse in sensitive work and ensure recalled text is treated as untrusted context rather than as instructions.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/thomasmarcel/skills/session-context)
- [ClawHub homepage metadata](https://clawhub.ai/skills/session-context)

## Skill Output:

**Output Type(s):** [Text, Markdown, Configuration]

**Output Format:** [Markdown memory entries and injected text context]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Stores daily memory files; caps injected summaries at 6000 characters and raw messages at 10 turns with 1500 characters per message.]

## Skill Version(s):

0.2.0 (source: server release metadata and skill frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
