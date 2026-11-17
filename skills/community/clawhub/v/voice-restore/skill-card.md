## Description:

Examines English writing for patterns associated with AI polishing and helps restore an author's style by comparing the text with that author's own writing baseline.

This skill is ready for commercial/non-commercial use.

## Publisher:

[catsmansion](https://clawhub.ai/user/catsmansion)

### License/Terms of Use:

MIT

## Use Case:

Writers and editors use this skill to examine English text for possible signs of AI polishing and, when they have at least 1,000 words of the author's undetected writing in the same genre, revise toward that author's measured style. It reports the metrics, before-and-after comparisons, and changes left untouched.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The install example uses an unpinned package reference, so later installs may retrieve changed code.

Mitigation: Review the package and use a reviewed, pinned version where available.

## Reference(s):

- [ClawHub release page](https://clawhub.ai/catsmansion/skills/voice-restore)
- [Case notes](references/case-notes.md)
- [Voice metrics script](scripts/voice_metrics.py)

## Skill Output:

**Output Type(s):** [Analysis, Text, Markdown, Guidance]

**Output Format:** [Markdown with edited text, before-and-after comparisons, and metric tables]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes measured style metrics and an explicit list of changes not made.]

## Skill Version(s):

1.0.0 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
