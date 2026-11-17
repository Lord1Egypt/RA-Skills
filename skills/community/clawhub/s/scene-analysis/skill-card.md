## Description:

Scene Analysis helps agents evaluate commercial scenarios through Gate0 strategic screening, Gate1 quantitative scoring, and independent blue-force review.

This skill is ready for commercial/non-commercial use.

## Publisher:

[yyf1986](https://clawhub.ai/user/yyf1986)

### License/Terms of Use:

MIT-0

## Use Case:

Business strategy reviewers, product evaluators, and agents use this Chinese-language skill to screen commercial scenarios, produce evidence-based Gate0 and Gate1 ratings, and run a stricter blue-force audit.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may produce advisory business ratings from incomplete scenario evidence because its rules allow marked logic-based deductions when hard evidence is missing.

Mitigation: Review the cited user evidence and any deduction marked as lacking proof before using the rating for business decisions.

Risk: The broad trigger can apply the workflow to requests that are not intended for Chinese-language Gate0/Gate1 commercial scenario scoring.

Mitigation: Install and invoke the skill only when that evaluation workflow is the intended task.

## Reference(s):

- [Gate0 Strategic Screening Standards](references/gate0-standards.md)
- [Gate1 Scoring Rules](references/gate1-scoring-rules.md)
- [Blue-Force Review Rules](references/blue-force-review.md)
- [ClawHub release page](https://clawhub.ai/yyf1986/skills/scene-analysis)

## Skill Output:

**Output Type(s):** [text, markdown, guidance]

**Output Format:** [Markdown evaluation reports in Chinese]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Evidence-dependent Gate0/Gate1 ratings, score calculations, risk deductions, and blue-force review findings.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
