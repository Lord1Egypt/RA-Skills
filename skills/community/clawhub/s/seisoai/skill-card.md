## Description:

Unified media generation gateway for agents. Discover tools dynamically, choose API key or x402 auth, invoke image/video/audio/music/3D/training tools, and handle queue jobs reliably.

This skill is ready for commercial/non-commercial use.

## Publisher:

[legendarylibr](https://clawhub.ai/user/legendarylibr)

### License/Terms of Use:


## Use Case:

Developers and agents use this skill to discover Seisoai media-generation tools, fetch schemas, price requests, invoke image, video, audio, music, 3D, and training workflows, and poll queued jobs. It is intended for external agent workflows that need structured API guidance for Seisoai's gateway.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Face-swap and voice-cloning workflows may enable impersonation or deceptive media if used without consent.

Mitigation: Use only media and voices the user has rights and consent to use, avoid impersonation or deceptive content, and review requests before invoking these tools.

Risk: API-key or x402 queue submissions can incur charges once accepted.

Mitigation: Pre-price inputs where possible, confirm paid submissions before invoking, and monitor API-key credit or x402 payment use.

Risk: Agent-scoped routes can operate privileged agent workflows if the agent, tool, or authorization boundary is ambiguous.

Mitigation: Use general invoke routes for normal media generation; for agent-scoped routes, require explicit task need, exact agent binding, tool allowlist checks, and run-note auditing.

## Reference(s):

- [Seisoai Homepage](https://seisoai.com)
- [ClawHub Skill Page](https://clawhub.ai/legendarylibr/skills/seisoai)
- [ClawHub Publisher Profile](https://clawhub.ai/user/legendarylibr)

## Skill Output:

**Output Type(s):** [text, markdown, API calls, JSON payloads, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with HTTP examples, JSON payload patterns, endpoint lists, and operational safety rules]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include API-key or x402 payment flow guidance, queue polling steps, fallback handling, and agent-scoped authorization checks.]

## Skill Version(s):

1.1.1 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
