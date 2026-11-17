## Description:

This Chinese-language skill helps organizations with Mainland China asset elements assess cross-border RWA or tokenization compliance paths, compare regulatory postures across jurisdictions, and design a Mainland-stop plus Hong Kong or offshore bridge structure.

This skill is ready for commercial/non-commercial use.

## Publisher:

[63619990](https://clawhub.ai/user/63619990)

### License/Terms of Use:

Apache-2.0

## Use Case:

External users and agents use this skill to triage Hong Kong/Mainland cross-border RWA, SPV, QFLP, sandbox, and securities-token issuance questions. It produces educational compliance path analysis, risk boundaries, and action checklists for review by qualified counsel.

### Deployment Geography for Use:

Mainland China and Hong Kong cross-border use cases, with comparisons to the United States, European Union, and Singapore when relevant.

## Known Risks and Mitigations:

Risk: Users may mistake educational compliance analysis for legal or investment advice.

Mitigation: Label outputs as educational risk analysis and require review against current regulator notices and qualified counsel before acting.

Risk: Regulatory treatment for Hong Kong/Mainland cross-border RWA and tokenization can change after the skill's source material was distilled.

Mitigation: Verify each recommended path against current notices from relevant regulators before relying on the guidance.

Risk: The release has low trust-tier server evidence despite passing quality and security checks.

Mitigation: Review the skill content, tests, and publisher profile before deployment in regulated workflows.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/63619990/skills/regulation-hk-sandbox)
- [Source skill](artifact/SKILL.md)
- [Test results](artifact/test-results.md)
- [Test prompts](artifact/test-prompts.json)

## Skill Output:

**Output Type(s):** [Text, Markdown, Guidance]

**Output Format:** [Chinese-language Markdown guidance with checklists and risk analysis]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Educational risk analysis only; outputs should be checked against current regulator notices and qualified counsel.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
