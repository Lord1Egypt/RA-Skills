## Description:

Manage social media from chat by scheduling posts, viewing analytics, generating AI content, and listing connected accounts through the SocialRails API.

This skill is ready for commercial/non-commercial use.

## Publisher:

[buildsbymatt](https://clawhub.ai/user/buildsbymatt)

### License/Terms of Use:

MIT

## Use Case:

Social media managers, marketers, and developers use this skill to manage SocialRails-connected accounts from chat, including creating or scheduling posts, reviewing analytics, generating captions, and listing posts or accounts.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: A SocialRails API key can read account data and schedule public posts.

Mitigation: Use the least-privileged API key possible and manually confirm post content and schedules before creating or scheduling posts.

Risk: A misconfigured API base URL can expose the SocialRails API key to an untrusted endpoint.

Mitigation: Keep the default SocialRails API endpoint unless the replacement endpoint is fully trusted.

## Reference(s):

- [SocialRails API Documentation](https://socialrails.com/documentation/api-overview)
- [SocialRails OpenClaw Setup Guide](https://socialrails.com/documentation/openclaw-setup)
- [SocialRails Dashboard](https://socialrails.com/dashboard)
- [ClawHub Skill Page](https://clawhub.ai/buildsbymatt/skills/socialrails)

## Skill Output:

**Output Type(s):** [Text, JSON, Guidance]

**Output Format:** [JSON command results with human-readable message fields]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include post IDs, generated content, analytics summaries, and account or post listings returned by SocialRails.]

## Skill Version(s):

1.0.0 (source: server release metadata, skill.json, package.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
