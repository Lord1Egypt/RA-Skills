## Description:

Use when researchers need to plan, draft, revise, or audit an empirical research paper from their own materials, including Introduction, Methods, Results, Discussion, Conclusion, Abstract, and Title, with evidence-preserving and target-journal-aware guidance.

This skill is ready for commercial/non-commercial use.

## Publisher:

[yila-ai](https://clawhub.ai/user/yila-ai)

### License/Terms of Use:

MIT-0

## Use Case:

Researchers and research-writing assistants use this skill to turn author-supplied empirical study materials into evidence-faithful manuscript plans, drafts, revisions, and audits. It supports common paper sections while preserving supplied facts, citations, limitations, null findings, and claim strength.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Unpublished manuscripts, study data, target-paper notes, and journal models can contain sensitive research material.

Mitigation: Treat those materials as sensitive inputs and use the skill only in approved environments for the manuscript and data involved.

Risk: Generated manuscript prose may still contain incorrect scientific judgment, unsupported claim strength, or missed evidence conflicts.

Mitigation: Review outputs against the author's source materials, preserve null findings and limitations, and require author confirmation before using substantive changes.

Risk: Target-paper adaptation can drift into wording imitation or transfer claims, citations, methods, or findings from papers that are not the author's evidence.

Mitigation: Use target papers only to model section functions and information order; do not copy wording or import scientific content from them.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/yila-ai/skills/science-research-writing)
- [Input and output contract](artifact/references/input-output-contract.md)
- [Certainty and claim-strength contract](artifact/references/certainty-and-claim-strength.md)
- [Target-journal model builder](artifact/references/reverse-engineering-protocol.md)
- [Section function map](artifact/assets/section-function-map.md)
- [Abstract guidance](artifact/references/abstract.md)
- [Introduction guidance](artifact/references/introduction.md)
- [Methods guidance](artifact/references/methods.md)
- [Results guidance](artifact/references/results.md)
- [Discussion guidance](artifact/references/discussion.md)
- [Conclusion guidance](artifact/references/conclusion.md)
- [Title guidance](artifact/references/title.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with manuscript-ready text, diagnoses, section plans, audit notes, and concise next-step guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May reference local validation scripts for draft invariant checks and target-journal model validation when the necessary local files are available.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
