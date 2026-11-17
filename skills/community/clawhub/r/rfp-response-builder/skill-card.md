## Description:

Builds a U.S. RFP response from a requirement matrix, scores requirement coverage, and flags answers for reviewer verification.

This skill is ready for commercial/non-commercial use.

## Publisher:

[rapidworker1](https://clawhub.ai/user/rapidworker1)

### License/Terms of Use:

MIT-0

## Use Case:

External proposal teams and U.S. government contractors use the skill to organize solicitation requirements, prepare evidence-based responses, track ownership and status, and review coverage before submission by an authorized signer.

### Deployment Geography for Use:

United States

## Known Risks and Mitigations:

Risk: Coverage scores may be mistaken for proof that a response is complete or compliant.

Mitigation: Review each answer and supporting document against the solicitation; treat scores only as field-coverage indicators.

Risk: Procurement guidance or extracted requirements may be incorrect or inapplicable to a particular solicitation.

Mitigation: Independently verify procurement guidance and the solicitation requirements before relying on or submitting the response.

Risk: The optional Windows toolkit is an unsigned executable outside the security verdict for this skill.

Mitigation: Make a separate trust decision, verify the published archive hash, and avoid running the executable as administrator unless necessary.

## Reference(s):

- [RFP response rules](references/rfp-response-rules.md)
- [Publisher profile](https://clawhub.ai/user/rapidworker1)
- [Skill page](https://clawhub.ai/rapidworker1/skills/rfp-response-builder)
- [Optional Windows toolkit repository](https://github.com/rapidworker1/Multiple-AI-models-Toolkit)

## Skill Output:

**Output Type(s):** [Analysis, Guidance, Markdown, CSV]

**Output Format:** [Markdown RFP response with a requirement matrix and coverage table; CSV requirement template and scoring input.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Coverage scores are indicators based on field values, not proof of completeness or compliance.]

## Skill Version(s):

1.0.7 (source: frontmatter, server-resolved release)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
