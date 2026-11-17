## Description:

Analyzes uploaded files to detect suspicious characteristics and potential security threats.

This skill is ready for commercial/non-commercial use.

## Publisher:

[krishnakumarmahadevan-cmd](https://clawhub.ai/user/krishnakumarmahadevan-cmd)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, security teams, and organizations use this skill to submit files to a hosted scanning API and receive threat indicators, confidence scores, and handling recommendations for file intake workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Files submitted for scanning are uploaded to the mkkpro.com hosted API.

Mitigation: Submit only files approved for external processing, and avoid confidential, regulated, customer, credential-bearing, or legally restricted files unless retention and privacy terms have been reviewed.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/krishnakumarmahadevan-cmd/skills/suspicious-file-scanner)
- [Suspicious File Scanner API Route](https://api.mkkpro.com/security/suspicious-file-scanner)
- [Suspicious File Scanner API Docs](https://api.mkkpro.com:8013/docs)

## Skill Output:

**Output Type(s):** [JSON, guidance]

**Output Format:** [JSON analysis with threat indicators, confidence scores, and recommendations]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uploads user-selected files to a hosted API for analysis.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
