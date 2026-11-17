## Description:

Vocab Deep Dive helps learners generate structured English vocabulary analyses in Chinese, covering definitions, usage, collocations, examples, related words, roots, common mistakes, and IELTS study notes.

This skill is ready for commercial/non-commercial use.

## Publisher:

[shaojie66](https://clawhub.ai/user/shaojie66)

### License/Terms of Use:

MIT-0

## Use Case:

External learners and exam-preparation users use this skill to get concise, structured English word explanations with IELTS-oriented usage guidance. It is intended for vocabulary study, review, and writing or speaking improvement.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Optional third-party dictionary lookup can disclose the queried word or term.

Mitigation: Avoid confidential code names or proprietary terms, or ask the agent to work offline.

Risk: Vocabulary explanations for rare, specialized, or ambiguous terms may be incomplete or inaccurate.

Mitigation: State usage limits for obscure terms and verify uncertain pronunciation or definitions before relying on them.

## Reference(s):

- [Free Dictionary API](https://api.dictionaryapi.dev/api/v2/entries/en/{word})

## Skill Output:

**Output Type(s):** [Text, Markdown, Guidance]

**Output Format:** [Structured Markdown vocabulary analysis in Chinese]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May optionally verify pronunciation or definitions through the Free Dictionary API when the user asks or the model is uncertain.]

## Skill Version(s):

1.0.2 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
