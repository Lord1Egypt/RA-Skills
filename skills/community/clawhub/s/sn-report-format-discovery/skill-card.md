## Description:

Determines a concise request-level output format string for research tasks when the user asks for a recommended deliverable form or when the final format is otherwise unclear.

This skill is ready for commercial/non-commercial use.

## Publisher:

[sensenova-skills](https://clawhub.ai/user/sensenova-skills)

### License/Terms of Use:

MIT-0

## Use Case:

Researchers and agent builders use this skill to normalize a research request into a short output-format label, such as report, paper, table, memo, timeline, or faq. It is useful before downstream research or writing steps need a simple deliverable-type signal.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Non-Chinese reviewers or operators may miss the skill's constraints because the artifact instructions are written in Chinese.

Mitigation: Review a trusted translation before deployment and confirm that only a short format label is expected.

Risk: The selected format label can be wrong when the user's desired deliverable is ambiguous.

Mitigation: Confirm the emitted format before using it to drive downstream research or writing workflows.

## Reference(s):


## Skill Output:

**Output Type(s):** [text, guidance]

**Output Format:** [Single-line text in the form `format: <short non-empty string>`]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Does not create files, schemas, or candidate format objects.]

## Skill Version(s):

2026.9.11 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
