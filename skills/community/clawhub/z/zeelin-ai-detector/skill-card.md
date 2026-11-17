## Description:

ZeeLin AI Detector estimates how likely Chinese text is AI-generated from writing style and expression features, then gives a brief rationale.

This skill is ready for commercial/non-commercial use.

## Publisher:

[dongjiangliu9-tech](https://clawhub.ai/user/dongjiangliu9-tech)

### License/Terms of Use:

MIT-0

## Use Case:

External users and reviewers use this skill to request a cautious, text-only estimate of whether a Chinese passage sounds AI-written, with a short explanation of the observed language features.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Users may treat the percentage estimate as definitive academic integrity evidence or as output from a professional detection service.

Mitigation: Present results as rough, style-based opinions only and retain the limitation statement that no external database or professional detection platform is used.

Risk: Very short text can produce unstable judgments.

Mitigation: Return the documented short-text warning instead of a numeric probability when the sample is too small.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/dongjiangliu9-tech/skills/zeelin-ai-detector)

## Skill Output:

**Output Type(s):** [Text, Markdown, Guidance]

**Output Format:** [Markdown with a percentage estimate, concise bullet analysis, and a limitation statement]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The skill does not claim database comparison, academic plagiarism checking, or professional AI-detection results.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
