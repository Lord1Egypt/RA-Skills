## Description:

Checks subcontractor qualification and safety-permit registers offline across six deterministic table rules, citing source rows and reporting missing material instead of unsupported conclusions.

This skill is ready for commercial/non-commercial use.

## Publisher:

[chenqg618](https://clawhub.ai/user/chenqg618)

### License/Terms of Use:

MIT-0

## Use Case:

External contracting, project, and safety teams use this skill to review subcontractor registers before onboarding, monthly reviews, safety inspections, or tender prequalification.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Subcontractor registers can contain company identifiers and certificate numbers.

Mitigation: Mask company and certificate identifiers before input, as the skill documentation recommends.

Risk: The checker can flag table inconsistencies but does not verify certificate authenticity or legal eligibility.

Mitigation: Use the report as a review aid and confirm high-impact findings against authoritative records and qualified legal or safety review.

Risk: Incomplete or malformed registers can lead to missing-input results rather than conclusions.

Mitigation: Provide a table with the required headers and review missing-field messages before relying on the output.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/chenqg618/skills/subcontractor-qualification-check-free)
- [Source skill definition](artifact/SKILL.md)

## Skill Output:

**Output Type(s):** [Text, JSON, Shell commands, Guidance]

**Output Format:** [Plain text or JSON report with source-row citations and missing-input messages]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Runs locally on text or JSON input; does not replace legal, regulatory, or document-authenticity review.]

## Skill Version(s):

1.0.3 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
