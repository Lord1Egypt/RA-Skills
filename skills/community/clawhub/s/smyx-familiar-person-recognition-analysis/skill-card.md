## Description:

Identifies acquaintances in images or videos by comparing faces with enrolled photos and reports each result's location.

This skill is ready for commercial/non-commercial use.

## Publisher:

[18072937735](https://clawhub.ai/user/18072937735)

### License/Terms of Use:

MIT-0

## Use Case:

Home and office operators can compare faces in supplied images or videos with an enrolled acquaintance database and review recognition locations or prior reports. Results are advisory and are not suitable for legal identity verification.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Facial imagery or video may be sent to an external service for analysis.

Mitigation: Submit footage only when appropriate consent is in place and the service's data handling is acceptable.

Risk: The security evidence reports automatic account creation and credential storage.

Mitigation: Review account and credential handling before use, and run the skill only in an environment where that behavior is acceptable.

Risk: The security evidence reports analysis or uploads in export-only mode.

Mitigation: Treat export-only mode as potentially performing remote processing unless its behavior has been verified; avoid using it with sensitive footage or credentials in the meantime.

## Reference(s):

- [API interface documentation](artifact/references/api_doc.md)
- [Skill demonstration](https://lifeemergence.com/sample.html)

## Skill Output:

**Output Type(s):** [Analysis, JSON, Markdown]

**Output Format:** [Structured recognition report; JSON detail output; Markdown table for history lists.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Reports matched identities and locations; results are advisory, not legal identity verification.]

## Skill Version(s):

1.0.22 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
