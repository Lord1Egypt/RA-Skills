## Description:

Provides read-only access to Symantec Cloud DLP incidents, profiles, detection content, custom groups, data identifiers, and index health.

This skill is ready for commercial/non-commercial use.

## Publisher:

[zw008](https://clawhub.ai/user/zw008)

### License/Terms of Use:

MIT

## Use Case:

Security operations teams and administrators use this skill to inspect Cloud DLP incidents and detection content, search incidents within bounded time ranges, and check index health. It is intended for read-only investigation; missing, partial, or unverified results require follow-up.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Missing, partial, or unverified API responses can be mistaken for a healthy state or zero results.

Mitigation: Check the documented verification status, use bounded searches and pagination, and treat incomplete responses as unknown.

Risk: Connecting to Cloud DLP requires API credentials.

Mitigation: Keep credentials in environment variables and retain TLS verification.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/zw008/skills/symantec-clouddlp-aiops)
- [Project homepage](https://github.com/AIops-tools/Symantec-CloudDLP-AIops)
- [Agent guardrails](references/agent-guardrails.md)

## Skill Output:

**Output Type(s):** [Text, JSON, Guidance]

**Output Format:** [Text summaries and surfaced API response data]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Incident searches use bounded time windows and pagination cursors; response schemas may vary, and missing or partial results remain unknown.]

## Skill Version(s):

0.1.1 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
