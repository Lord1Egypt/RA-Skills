## Description:

Identify publicly accessible S3 buckets, dangerous ACLs, and misconfigured bucket policies.

This skill is ready for commercial/non-commercial use.

## Publisher:

[anmolnagpal](https://clawhub.ai/user/anmolnagpal)

### License/Terms of Use:


## Use Case:

Security engineers, cloud administrators, and developers use this skill to review exported AWS S3 configuration data for public exposure, risky ACLs, misconfigured bucket policies, missing encryption, and missing preventive controls.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Pasted AWS outputs may accidentally include credentials, keys, or sensitive object data.

Mitigation: Share only exported S3 configuration and policy data, and review pasted outputs for accidental secrets or sensitive object data before analysis.

Risk: Incomplete user-provided S3 data can limit the audit and cause exposure issues to be missed.

Mitigation: Provide account-level S3 Block Public Access settings, bucket ACLs, bucket policies, bucket public access block settings, and Security Hub S3 findings when available.

## Reference(s):


## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown with findings tables, policy JSON, AWS CLI command examples, and remediation guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Instruction-only analysis based on user-provided exported AWS S3 configuration and policy data.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
