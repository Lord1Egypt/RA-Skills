## Description:

Analyzes pet videos from veterinary waiting areas for visible anxiety-related behaviors and returns a 1–5 anxiety level to support triage; it does not diagnose illness or recommend treatment.

This skill is ready for commercial/non-commercial use.

## Publisher:

[18072937735](https://clawhub.ai/user/18072937735)

### License/Terms of Use:

MIT-0

## Use Case:

Veterinary clinic staff can use video-based behavior observations and an anxiety level to identify pets that may need earlier attention or comfort while waiting. The result supports workflow decisions and is not a veterinary diagnosis or treatment plan.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: ClawScan rates this release suspicious and reports possible account-profile, token-storage, report-history, and broad network access, as well as uncertainty about whether export-only prevents video analysis.

Mitigation: Before installing, verify why these accesses are needed and confirm where video uploads go, how they are retained, and which services receive them; do not rely on export-only to prevent analysis.

Risk: The security guidance leaves video handling and retention to be confirmed, which may matter when videos contain sensitive information.

Mitigation: Use only videos you are authorized to share, minimize identifying material where practical, and confirm handling and retention before upload.

## Reference(s):

- [API documentation](references/api_doc.md)
- [Skill demonstration](https://lifeemergence.com/sample.html)

## Skill Output:

**Output Type(s):** [Analysis, JSON, Markdown, Guidance]

**Output Format:** [Structured analysis report with an anxiety level, behavior observations, and a report link; available in JSON or Markdown detail formats.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Behavior-based estimates can be affected by individual and breed differences; use alongside direct observation.]

## Skill Version(s):

1.0.19 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
