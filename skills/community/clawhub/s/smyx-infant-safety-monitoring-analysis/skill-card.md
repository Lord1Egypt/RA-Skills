## Description:

Analyzes infant videos for potential safety hazards and provides warnings, care suggestions, and report links.

This skill is ready for commercial/non-commercial use.

## Publisher:

[smyx-sunjinhui](https://clawhub.ai/user/smyx-sunjinhui)

### License/Terms of Use:

MIT-0

## Use Case:

Caregivers and families can submit infant videos or video URLs to identify possible hazards, review safety warnings and care suggestions, and access prior reports. The analysis supplements rather than replaces direct supervision.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Sensitive infant and home media or media URLs are sent to a vendor cloud service.

Mitigation: Obtain informed consent before uploading and confirm the publisher's privacy, retention, deletion, and access policies.

Risk: The skill silently creates or logs into an account, retains report-linked identity and tokens locally, and can retrieve cloud history automatically.

Mitigation: Review account authorization and history access, protect local credentials, and limit use to approved users and media.

Risk: Video analysis may miss hazards or provide misleading safety guidance.

Mitigation: Keep a caregiver actively supervising the child; do not rely on alerts as a replacement for direct care.

## Reference(s):

- [Infant Safety Monitoring API Documentation](references/api_doc.md)

## Skill Output:

**Output Type(s):** [Analysis, Guidance]

**Output Format:** [JSON or Markdown with report links]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Supports optional saved results and links to cloud-hosted reports.]

## Skill Version(s):

1.0.17 (source: ClawHub release metadata; bundled SKILL.md lists 1.0.23)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
