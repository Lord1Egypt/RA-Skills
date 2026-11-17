## Description:

Discover, prepare, and execute any Risha.ai capability available to the authenticated account.

This skill is ready for commercial/non-commercial use.

## Publisher:

[aimedialab](https://clawhub.ai/user/aimedialab)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and content operators use this skill to discover Risha.ai capabilities available to an authenticated account, prepare valid request payloads, estimate credit use, submit generation jobs, poll for completion, and retrieve generated text, audio, image, video, or multimodal outputs.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Reusable account credentials or derived authorization headers may appear in command output or logs.

Mitigation: Run authentication only in trusted terminals, avoid environments that capture stdout, and redact credentials, cookies, and authorization headers before sharing logs.

Risk: Changing the API base URL can send credentials or generation payloads to an untrusted destination.

Mitigation: Use the default Risha API host unless the user explicitly verifies and trusts a replacement host before setting --base-url or RISHA_API_BASE_URL.

Risk: Generation requests can submit confidential media, prompts, or callback URLs to a third-party service.

Mitigation: Review payloads before submission, avoid confidential inputs unless approved for Risha.ai processing, and use only callback URLs controlled by the user or organization.

## Reference(s):

- [Risha API Reference](references/risha-api.md)
- [Current Risha Capabilities](references/current-capabilities.md)
- [Current Risha Capabilities JSON](references/current-capabilities.json)
- [Risha OpenAPI document](https://adminxcore-api.risha.ai/api/docs/?format=openapi)
- [Risha API base URL](https://adminxcore-api.risha.ai/api)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell commands, JSON payload examples, generated content, and media URLs when returned by Risha.ai.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include credit previews, terminal job status, generated content metadata, and asset or thumbnail URLs.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
