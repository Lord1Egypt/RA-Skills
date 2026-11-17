## Description:

Evaluate whether an article, document, video transcript, or webpage is worth reading; recommend full reading or specific sections; maintain a private local reading profile; and learn from explicit feedback.

This skill is ready for commercial/non-commercial use.

## Publisher:

[langingsing](https://clawhub.ai/user/langingsing)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use Readworthy to decide whether articles, documents, video transcripts, or webpages merit a full read, selected section reading, a summary-only treatment, or skipping. The skill also helps maintain a private local profile so future recommendations can account for explicit feedback and prior knowledge.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Persistent local state can retain sensitive reading interests, article records, raw feedback, insights, and timestamped backups.

Mitigation: Set READWORTHY_STATE_DIR to an intended storage location, inspect or delete that directory when long-term history is not desired, and avoid distributing any user's state files with the skill.

## Reference(s):

- [Readworthy state schema v2](references/state-schema-v2.md)
- [Readworthy ClawHub skill page](https://clawhub.ai/langingsing/skills/readworthy)

## Skill Output:

**Output Type(s):** [text, markdown, guidance, shell commands, configuration]

**Output Format:** [Markdown guidance with optional inline shell commands and local JSON state updates]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses A/B/C/D reading recommendations, reading scope, evidence summaries, tradeoffs, feedback records, and local profile or insight updates.]

## Skill Version(s):

1.0.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
