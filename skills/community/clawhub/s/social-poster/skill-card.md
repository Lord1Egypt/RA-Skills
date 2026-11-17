## Description:

Post to social media via the VibePost API for Twitter/X updates, shared updates, and other social content.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jpaulgrayson](https://clawhub.ai/user/jpaulgrayson)

### License/Terms of Use:


## Use Case:

Agents and developers use this skill to publish short social media updates through VibePost, typically to Twitter/X or another selected platform.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: User-provided post text is sent to the VibePost Replit endpoint and may be published to social media.

Mitigation: Use the skill only for content approved for external sharing, and confirm the exact post text and platform before sending.

Risk: The artifact uses a hardcoded shared API key for the posting service.

Mitigation: Replace the shared key with user-specific secrets before production use and avoid redistributing credentials in skill files.

Risk: Broad trigger phrases can make it easy to invoke posting behavior unintentionally.

Mitigation: Narrow invocation triggers and require explicit confirmation before any network request that can publish content.

## Reference(s):

- [Social Poster on ClawHub](https://clawhub.ai/jpaulgrayson/skills/social-poster)
- [VibePost post endpoint](https://vibepost-jpaulgrayson.replit.app/api/quack/post)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, JSON]

**Output Format:** [Markdown guidance with inline shell commands and JSON service responses]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Posts are submitted to a third-party service using caller-provided text and platform parameters.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
