## Description:

Generate USMLE Step 1 and Step 2 CK style clinical cases for medical education and board exam preparation.

This skill is ready for commercial/non-commercial use.

## Publisher:

[aipoch-ai](https://clawhub.ai/user/aipoch-ai)

### License/Terms of Use:

MIT-0

## Use Case:

External learners, educators, and developers use this skill to generate fictional USMLE Step 1 and Step 2 CK practice vignettes, multiple-choice questions, explanations, and learning objectives for medical education review.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The root installation instructions can pull an unnecessary unpinned package named main.

Mitigation: Do not run the documented pip install step unless the dependency file is removed, replaced, or reviewed and pinned.

Risk: Generated clinical cases may contain inaccuracies and are not patient-care advice.

Mitigation: Use outputs only as fictional educational practice material and have qualified medical reviewers verify clinical details before high-stakes use.

## Reference(s):

- [USMLE Case Generator Guidelines](references/guidelines.md)
- [USMLE Question Patterns and Strategies](references/usmle_patterns.md)
- [Medical Specialty Topics](references/topics.json)
- [Case Structure Templates](references/case_templates.json)
- [Sample Input](references/sample_input.json)
- [Sample Output](references/sample_output.json)
- [ClawHub Skill Page](https://clawhub.ai/aipoch-ai/skills/usmle-case-generator)

## Skill Output:

**Output Type(s):** [text, markdown, JSON, guidance]

**Output Format:** [Plain text, JSON, or Markdown clinical vignette with multiple-choice question and optional answer key.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include generated case metadata, patient vignette sections, answer options, explanation, and learning objectives.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
