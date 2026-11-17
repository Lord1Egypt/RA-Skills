## Description:

Analyzes cat litter box image or video inputs through cloud APIs to report waste characteristics, urine clump observations, health risk alerts, and report links without providing disease diagnosis or treatment advice.

This skill is ready for commercial/non-commercial use.

## Publisher:

[smyx-sunjinhui](https://clawhub.ai/user/smyx-sunjinhui)

### License/Terms of Use:

MIT-0

## Use Case:

External users, pet health monitoring teams, and smart litter box developers use this skill to process cat litter box media and retrieve structured observations about stool morphology, urine clump size, and historical reports. The output is for health monitoring and risk awareness, not veterinary diagnosis.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill sends litter-box media or video URLs, account-linked identifiers, and report metadata to configured backend services.

Mitigation: Review the backend destination and data handling expectations before use, and require user confirmation before first upload or cloud history lookup.

Risk: The skill can silently create or reuse an identity and store local tokens in the workspace.

Mitigation: Document the identity and retention model, limit workspace access to trusted users, and clear local tokens when the skill is no longer needed.

Risk: The skill defaults to development or private HTTP endpoints according to the security evidence.

Mitigation: Switch defaults to approved production HTTPS endpoints before deployment and verify endpoint configuration during review.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/smyx-sunjinhui/skills/smyx-pet-litter-box-waste-analysis)
- [API Documentation](references/api_doc.md)
- [SMYX Analysis API Documentation](skills/smyx_analysis/references/api_doc.md)
- [Skill Demo](https://lifeemergence.com/sample.html)

## Skill Output:

**Output Type(s):** [text, markdown, guidance, shell commands]

**Output Format:** [Markdown and structured JSON-like text]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include cloud report history entries and report export links.]

## Skill Version(s):

1.0.9 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
