## Description:

Imports Logseq pages into a slipbox by parsing page properties and bulleted notes, enriching nested bullets with parent context, and running slipbot for each note.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jrswab](https://clawhub.ai/user/jrswab)

### License/Terms of Use:


## Use Case:

Developers and knowledge-management users use this skill to turn pasted Logseq pages into individual slipbox notes while preserving useful source metadata and parent context.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Large Logseq pages can create many separate slipbox notes after import.

Mitigation: Review the preview summary, note count, and source details before confirming the import.

Risk: Logseq tags and block metadata are intentionally ignored, which may omit categorization users expected to retain.

Mitigation: Confirm that slipbot-generated tags are acceptable before proceeding with the import.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/jrswab/skills/slipbot-logseq-importer)
- [Publisher profile](https://clawhub.ai/user/jrswab)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Markdown guidance with note-preview summaries and slipbot command-style note entries]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Asks for user confirmation before creating notes and reports the number of notes created plus any issues.]

## Skill Version(s):

1.0.0 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
