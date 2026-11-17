## Description:

Detects potential AI-generated text and images, reports confidence and text-segment details, and offers optional rewriting guidance.

This skill is ready for commercial/non-commercial use.

## Publisher:

[autoagc](https://clawhub.ai/user/autoagc)

### License/Terms of Use:

MIT-0

## Use Case:

Content creators, marketers, and reviewers use the skill to check text and images for signs of AI generation before publishing or accepting supplied materials.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Selected text or images are sent to Qinghu for processing and may include sensitive or unpublished material.

Mitigation: Submit only materials approved for third-party processing; avoid confidential, legal, academic, or unpublished commercial content unless that processing is acceptable.

Risk: API calls use a Qinghu key and may consume paid credits.

Mitigation: Obtain consent before calls, explain that charges may apply, and use a key the user has authorized.

Risk: Larger results may be exported or cached in local files without a separate request.

Mitigation: Confirm before exporting results and disclose where exported files or caches are stored.

Risk: AI-generation scores can be wrong and may be mistaken for definitive evidence.

Mitigation: Present scores as uncertain indicators and avoid using them alone for legal, academic, or copyright decisions.

## Reference(s):

- [ClawHub skill release](https://clawhub.ai/autoagc/skills/qinghu-ai-detector)
- [Qinghu API key management](https://www.iqinghu.com/workbench/dashboard/api-keys?urlCode=1788417429126)

## Skill Output:

**Output Type(s):** [Text, Markdown, Guidance, Files]

**Output Format:** [Markdown summary with per-item confidence, text-segment details, and optional exported spreadsheet]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Probabilistic findings, not proof of authorship; optional rewriting advice and exported results.]

## Skill Version(s):

0.1.0 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
