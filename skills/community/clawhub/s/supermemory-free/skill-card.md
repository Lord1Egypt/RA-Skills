## Description:

Cloud knowledge backup and retrieval using Supermemory.ai free tier.

This skill is ready for commercial/non-commercial use.

## Publisher:

[broedkrummen](https://clawhub.ai/user/broedkrummen)

### License/Terms of Use:


## Use Case:

Developers and OpenClaw users use this skill to store selected session knowledge in Supermemory.ai and retrieve it later when local memory is insufficient.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Selected OpenClaw memory-log content may be uploaded to Supermemory.ai, including sensitive material if it is present in session memory.

Mitigation: Review memory contents before upload, prefer dry-run or manual storage, and avoid using this skill with secrets, credentials, private customer data, or regulated information.

Risk: The optional cron job can perform ongoing unattended uploads.

Mitigation: Do not enable cron until you have reviewed the memory directory and accepted recurring uploads; use manual commands when unattended capture is not required.

Risk: The scanner flags .env sourcing and weak redaction as risks.

Mitigation: Keep credentials out of session memory, keep the API key scoped to Supermemory usage, and review extracted content before cloud storage.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/broedkrummen/skills/supermemory-free)
- [Supermemory.ai](https://supermemory.ai)
- [Supermemory Documents Endpoint](https://api.supermemory.ai/v3/documents)
- [Supermemory Search Endpoint](https://api.supermemory.ai/v3/search)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell command examples and optional JSON API responses]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires SUPERMEMORY_OPENCLAW_API_KEY and sends selected content to Supermemory.ai.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
