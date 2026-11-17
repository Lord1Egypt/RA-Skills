## Description:

Interact with the Trakt API to manage your watchlist, collection, ratings, and discover content.

This skill is ready for commercial/non-commercial use.

## Publisher:

[d-meagher](https://clawhub.ai/user/d-meagher)

### License/Terms of Use:


## Use Case:

OpenClaw users and developers use this skill to let agents issue Trakt API requests for watchlists, viewing history, collections, ratings, search, trending content, popular content, and recommendations.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill gives the agent read and write access to Trakt account data through OAuth-authenticated API requests.

Mitigation: Review account-changing commands before execution and revoke or rotate tokens if access is no longer needed.

Risk: The OAuth helper stores and prints client secrets, access tokens, and refresh tokens.

Mitigation: Run the helper only in a private terminal, avoid shared or recorded sessions, restrict OpenClaw config permissions, and never commit token-bearing config.

Risk: Leaked Trakt client secrets, access tokens, or refresh tokens could allow unauthorized account access.

Mitigation: Treat all Trakt credentials as sensitive and revoke or rotate them immediately if exposure is suspected.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/d-meagher/skills/trakt-tv)
- [Trakt homepage](https://trakt.tv)
- [Trakt API Documentation](https://trakt.docs.apiary.io/)
- [Trakt OAuth Applications](https://trakt.tv/oauth/applications)
- [AgentSkills Specification](https://agentskills.io/)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline bash and JSON examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces Trakt API curl commands and setup guidance that use user-provided OAuth credentials.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
