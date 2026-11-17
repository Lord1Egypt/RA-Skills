## Description:

Run a lightweight YouTube transcript workflow for repeatable transcript handoff tasks, including transcription, attribution cleanup, translation, and packaging with minimal tooling.

This skill is ready for commercial/non-commercial use.

## Publisher:

[bluebirdback](https://clawhub.ai/user/bluebirdback)

### License/Terms of Use:


## Use Case:

Agents use this skill to guide YouTube transcript generation, conservative speaker-attribution cleanup, optional timestamp-preserving translation, and handoff packaging. It is intended for repeatable transcript workflows where concise process guidance and auditable outputs matter more than custom automation.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Generated transcripts, raw outputs, and translations may contain private or copyrighted content.

Mitigation: Choose output locations and sharing practices deliberately, and review handoff packages before distribution.

Risk: Speaker attribution cleanup can introduce incorrect speaker labels when ambiguous turns are over-edited.

Mitigation: Only change clearly short interjections or questions, leave uncertain turns unchanged, and note ambiguity in handoff notes.

Risk: Translation or cleanup can accidentally alter timestamps, speaker labels, or line counts.

Mitigation: Preserve the original transcript structure and validate final line counts against the source.

## Reference(s):

- [Lite limits and defaults](references/limits.md)
- [ClawHub skill page](https://clawhub.ai/bluebirdback/skills/youtube-transcript-pipeline-lite)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with file and folder names, command suggestions when needed, and transcript handoff notes.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Keeps transcript line counts, timestamps, and speaker structure stable unless the user explicitly asks for changes.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
