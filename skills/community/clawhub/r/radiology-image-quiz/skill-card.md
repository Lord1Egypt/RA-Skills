## Description:

Formats provided radiology cases into text-based diagnostic quizzes for medical education and board exam practice.

This skill is ready for commercial/non-commercial use.

## Publisher:

[aipoch-ai](https://clawhub.ai/user/aipoch-ai)

### License/Terms of Use:

MIT-0

## Use Case:

Medical educators, residents, and exam-prep authors use this skill to turn radiology case data into structured diagnostic quiz content. It is best suited for text-based study materials that require explicit case history, findings, answer choices, answers, and explanations.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The documentation describes image handling, PDF output, and interactive quiz behavior that are not evidenced by the packaged script.

Mitigation: Use the skill for text-based quiz formatting unless the package is updated and revalidated for image, PDF, or interactive workflows.

Risk: Caller-provided case JSON is printed directly in the generated quiz output.

Mitigation: Review and de-identify case data before use, and avoid including protected health information or sensitive patient details.

Risk: Radiology quiz content may be incomplete or unsuitable for clinical decision-making.

Mitigation: Have a qualified medical reviewer verify diagnoses, findings, answer choices, and explanations before educational or commercial distribution.

## Reference(s):

- [Audit Reference](references/audit-reference.md)
- [ClawHub Skill Page](https://clawhub.ai/aipoch-ai/skills/radiology-image-quiz)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Plain text or Markdown quiz content with optional shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces text quiz output from demo data or caller-provided JSON cases; no actual image handling, PDF output, or interactive quiz behavior is evidenced in the current package.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
