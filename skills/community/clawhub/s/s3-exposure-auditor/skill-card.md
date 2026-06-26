## Description: <br>
Identify publicly accessible S3 buckets, dangerous ACLs, and misconfigured bucket policies. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[anmolnagpal](https://clawhub.ai/user/anmolnagpal) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Security engineers and cloud administrators use this skill to audit exported AWS S3 bucket data for public exposure, weak access controls, missing encryption, and preventive control gaps. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: User-provided AWS exports could include credentials, secrets, or unrelated sensitive data. <br>
Mitigation: Review exported outputs before sharing them, remove credentials or unrelated secrets, and provide only the bucket data needed for the audit. <br>
Risk: Suggested AWS CLI collection commands may be run with broader access than needed. <br>
Mitigation: Use a least-privileged read-only AWS role when collecting audit data. <br>
Risk: Generated hardened policies and findings may be incorrect or incomplete for a specific AWS environment. <br>
Mitigation: Review recommendations before applying them and validate changes against the intended bucket access model. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/anmolnagpal/s3-exposure-auditor) <br>


## Skill Output: <br>
**Output Type(s):** [Analysis, Markdown, Code, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown report with findings tables, JSON policy snippets, and AWS command or configuration recommendations.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Analyzes user-provided read-only AWS S3 and Security Hub outputs; does not request credentials or directly access AWS accounts.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
