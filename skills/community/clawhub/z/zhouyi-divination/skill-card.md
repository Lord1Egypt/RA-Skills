## Description:

Zhouyi Divination guides an agent to perform I Ching and related Chinese metaphysics readings using multiple divination methods, birth-chart context, and an eight-expert consultation format.

This skill is ready for commercial/non-commercial use.

## Publisher:

[hahacatlsq](https://clawhub.ai/user/hahacatlsq)

### License/Terms of Use:


## Use Case:

External users invoke this agent skill for structured Zhouyi-style divination, timing, decision, fortune, and interpersonal readings. The skill asks the agent to combine traditional methods with practical reasoning and return a clear Markdown analysis with recommendations and cautions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill reads a hard-coded personal birth-chart file before performing readings.

Mitigation: Review the file path and profile data before use; prefer a version that asks before reading profile data and lets the user choose the source file.

Risk: The skill automatically saves every divination result, including personal questions and analysis, into an iCloud-synced folder.

Mitigation: Use only when automatic cloud-synced retention is acceptable; prefer a version with opt-in saving and clear retention and deletion controls.

## Reference(s):

- [Zhouyi Divination on ClawHub](https://clawhub.ai/hahacatlsq/skills/zhouyi-divination)

## Skill Output:

**Output Type(s):** [text, markdown, files, guidance]

**Output Format:** [Markdown divination report with sections for the question, timing, hexagram interpretation, eight-expert consultation, final judgment, advice, and cautions.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The artifact directs the agent to save each completed reading as a Markdown file in an iCloud-synced archive.]

## Skill Version(s):

0.1.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
