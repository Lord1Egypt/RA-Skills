## Description:

Turns selected uNotes documents into study guides, summaries, cheat sheets, or practice questions and can quiz the user in chat.

This skill is ready for commercial/non-commercial use.

## Publisher:

[devino](https://clawhub.ai/user/devino)

### License/Terms of Use:

MIT-0

## Use Case:

Students and other uNotes users can turn selected documents into study material and practice answering questions without saving anything back to uNotes.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Selected document text is shared with the chat session.

Mitigation: Use only notes the user is comfortable sharing in chat.

Risk: Long documents may be cut off at 12,000 characters, leaving study material incomplete.

Mitigation: Flag truncated source text and avoid claiming coverage of omitted sections.

Risk: Study material or answer checks may introduce claims not supported by the selected notes.

Mitigation: Ground responses in document text and identify topics the source does not cover.

## Reference(s):

- [Building Study Guides on ClawHub](https://clawhub.ai/devino/skills/unotes-building-study-guides)

## Skill Output:

**Output Type(s):** [Text, Markdown]

**Output Format:** [Markdown in chat]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Summaries, study sheets, or practice questions with answers; source text is limited to 12,000 characters per document and results are not saved to uNotes.]

## Skill Version(s):

1.0.1 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
