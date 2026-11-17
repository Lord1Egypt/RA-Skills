## Description:

Generate secure, time-limited access links for file sharing with automatic expiration.

This skill is ready for commercial/non-commercial use.

## Publisher:

[krishnakumarmahadevan-cmd](https://clawhub.ai/user/krishnakumarmahadevan-cmd)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, security teams, and operations teams use this skill to create expiring, token-based links for existing file URLs or uploaded files when sharing time-bound materials.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill handles sensitive files and internal file URLs through an external API provider with unclear authentication, storage, logging, deletion, retention, and compliance controls.

Mitigation: Use it only after reviewing the provider controls and avoid uploading confidential or regulated documents unless those controls meet the organization's requirements.

Risk: Token-bearing access URLs may be exposed through logs, sharing history, or replay if not protected by the provider and client workflows.

Mitigation: Keep expirations short, share links only with authorized recipients, and confirm how the provider protects tokens from logging and replay.

Risk: The file-serving endpoint behavior needs review because evidence asks the provider to clarify whether /files/{filename} can be accessed without a valid token.

Mitigation: Validate that file downloads require a valid, unexpired token before using the service for sensitive workflows.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/krishnakumarmahadevan-cmd/skills/temp-access-link)
- [Kong Route](https://api.mkkpro.com/tools/temp-access-link)
- [API Docs](https://api.mkkpro.com:8030/docs)
- [OpenAPI specification](artifact/openapi.json)

## Skill Output:

**Output Type(s):** [API Calls, JSON, Files, Guidance]

**Output Format:** [JSON responses, file content responses, and concise usage guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May produce token-bearing access URLs and file metadata; uploaded files and internal URLs should be treated as sensitive.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
