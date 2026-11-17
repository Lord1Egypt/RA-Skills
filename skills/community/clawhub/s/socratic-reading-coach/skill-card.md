## Description:

A local WeRead companion that maps a book's structure, guides five rounds of highlight-based Socratic questions, and produces a reading summary and Markdown notes.

This skill is ready for commercial/non-commercial use.

## Publisher:

[bonniegeng-max](https://clawhub.ai/user/bonniegeng-max)

### License/Terms of Use:

MIT-0

## Use Case:

Readers use this skill to revisit WeRead highlights, understand a book through guided questions, and turn their reflections into a summary or review notes.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: ClawScan rates the release suspicious, reports serious browser and proxy weaknesses and unsafe process handling, and notes that inspection was incomplete.

Mitigation: Review the reported concerns and components that were not fully inspected before installing; keep the local service on the user's own machine.

Risk: Selected highlights and dialogue are sent to the model provider configured by the user.

Mitigation: Select only reading content you are comfortable sharing and choose a model provider whose data practices you accept.

## Reference(s):

- [WeRead API reference](artifact/references/weread-api.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Guidance]

**Output Format:** [Streamed dialogue, Mermaid diagrams, reading summaries, and downloadable Markdown notes]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Notes can include selected book highlights and source details.]

## Skill Version(s):

1.3.0 (source: frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
