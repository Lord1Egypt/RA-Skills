## Description:

Determines whether user-provided automotive quality documents contain IATF 16949 Customer-Specific Requirements (CSR) and produces a structured clause-by-clause judgment report with confidence scoring.

This skill is ready for commercial/non-commercial use.

## Publisher:

[duding-engicool](https://clawhub.ai/user/duding-engicool)

### License/Terms of Use:

MIT-0

## Use Case:

Quality, compliance, and supplier-management teams use this skill to classify uploaded automotive quality documents for IATF 16949 CSR content. It supports clause-level analysis, confidence scoring, and a local Markdown report for review.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Uploaded quality documents may contain supplier or customer-sensitive information.

Mitigation: Use the skill only for intended automotive CSR analysis and avoid retaining sensitive generated reports longer than needed.

Risk: The generated CSR report is saved as a local Markdown file.

Mitigation: Delete generated reports after review when they should not remain on disk.

Risk: CSR classification can affect quality or supplier-management decisions.

Mitigation: Review the report before relying on it for audits, customer communication, or compliance decisions.

## Reference(s):

- [Server-resolved source repository](https://github.com/duding-engicool/skill-csr-analyzer)
- [Server-resolved source commit](https://github.com/duding-engicool/skill-csr-analyzer/tree/2341ead4047113681584b14fc3430f014494140b)
- [ClawHub skill page](https://clawhub.ai/duding-engicool/skills/skill-csr-analyzer)

## Skill Output:

**Output Type(s):** [Analysis, Markdown, Guidance]

**Output Format:** [Markdown report and concise text summary]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Analyzes one uploaded document at a time and writes a local CSR judgment report.]

## Skill Version(s):

0.1.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
