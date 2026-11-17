## Description:

Record experimental procedures and observations via voice commands during lab work, with real-time transcription for structured experiment documentation.

This skill is ready for commercial/non-commercial use.

## Publisher:

[lyla0921](https://clawhub.ai/user/lyla0921)

### License/Terms of Use:

MIT-0

## Use Case:

Researchers, lab staff, and developers use this skill to capture experiment steps, observations, and notes into structured protocol records during laboratory work.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security evidence says documentation and install steps do not match the implementation.

Mitigation: Review the skill before installing and avoid installing dependencies that are not needed by the implementation.

Risk: The security evidence says file-write scope is weakly controlled.

Mitigation: Use a dedicated save directory and confirm storage and retention controls before recording sensitive lab or clinical notes.

Risk: Experiment names and notes may become local filenames or saved protocol content.

Mitigation: Do not pass untrusted experiment names or sensitive notes unless the save location and retention policy are appropriate.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/lyla0921/skills/voice-to-protocol-transcriber)

## Skill Output:

**Output Type(s):** [text, markdown, files, configuration, shell commands]

**Output Format:** [Markdown, JSON, plain text files, and console text]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Protocol entries include timestamps and classifications such as step, observation, note, start, and end.]

## Skill Version(s):

0.1.0 (source: server release metadata; artifact frontmatter lists 1.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
