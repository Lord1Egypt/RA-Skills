## Description:

Polishes response letters by transforming defensive or harsh language into professional, courteous academic prose while preserving the author's scientific position.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ewankeynes](https://clawhub.ai/user/ewankeynes)

### License/Terms of Use:

MIT-0

## Use Case:

Researchers, authors, and academic writing assistants use this skill to revise draft responses to peer reviewers into diplomatic, professional English while preserving the intended scientific stance.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Installing unnecessary requirements may add avoidable dependency risk.

Mitigation: Review or remove the requirements.txt entries for dataclasses and enum, or install the skill in an isolated environment.

Risk: Reviewer comments and author responses may contain confidential manuscript or peer-review material.

Mitigation: Save inputs and outputs only in private, approved locations and avoid sharing generated files outside the review workflow.

Risk: The skill may over-soften or fail to verify the scientific accuracy of a response.

Mitigation: Have the author review the polished response to confirm the scientific position, rationale, and requested manuscript changes remain accurate.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/ewankeynes/skills/response-tone-polisher)
- [Polite Expressions Library](artifact/references/polite_expressions.json)
- [Tone Transformation Patterns](artifact/references/tone_patterns.md)

## Skill Output:

**Output Type(s):** [Text, JSON, Analysis, Guidance]

**Output Format:** [JSON containing polished response text, tone scores, phrase-level improvements, and suggestions]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Human review is recommended before using polished responses in confidential or high-stakes peer-review correspondence.]

## Skill Version(s):

0.1.0 (source: server release metadata; artifact frontmatter says 1.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
