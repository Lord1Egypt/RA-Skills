## Description: <br>
Generate secure, time-limited access links for file sharing with automatic expiration. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[krishnakumarmahadevan-cmd](https://clawhub.ai/user/krishnakumarmahadevan-cmd) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Security teams, compliance teams, and developers use this skill to create expiring access links for existing file URLs or uploaded files. It supports time-bound file distribution workflows where access should be revoked after an expiration period. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The service handles files and file URLs through api.mkkpro.com, while retention, deletion, logging, encryption, and access-control details are unclear in the provided evidence. <br>
Mitigation: Use only for files approved for this provider, and avoid regulated, confidential, or incident-response documents unless the provider separately documents the required controls. <br>
Risk: Token-only download enforcement and expiration behavior are not proven by the provided evidence. <br>
Mitigation: Validate expiration, download authorization, and revocation behavior before relying on the service for sensitive distribution workflows. <br>


## Reference(s): <br>
- [ClawHub listing](https://clawhub.ai/krishnakumarmahadevan-cmd/temp-access-link) <br>
- [Kong route](https://api.mkkpro.com/tools/temp-access-link) <br>
- [API docs](https://api.mkkpro.com:8030/docs) <br>
- [ToolWeb](https://toolweb.in) <br>


## Skill Output: <br>
**Output Type(s):** [API calls, JSON, Files, Guidance] <br>
**Output Format:** [JSON responses and file download responses from documented HTTP endpoints] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Creates token-bearing access URLs and accepts existing file URLs or multipart file uploads.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
