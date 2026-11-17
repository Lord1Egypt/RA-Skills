## Description:

Interact with the SoundCloud API to search and analyze tracks, inspect users and playlists, and perform authenticated playlist, like, and follow operations.

This skill is ready for commercial/non-commercial use.

## Publisher:

[leosaucedo](https://clawhub.ai/user/leosaucedo)

### License/Terms of Use:

MIT-0

## Use Case:

External developers and agents use this skill to discover SoundCloud tracks, inspect user and playlist metadata, and manage playlists, likes, and follows through SoundCloud API shell scripts.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Long-lived SoundCloud account tokens may be stored in plaintext cache files or shell profiles.

Mitigation: Prefer a secure credential store or short-lived, revocable tokens, and avoid persisting user tokens in shell profiles when possible.

Risk: Playlist, like, follow, and delete operations can change a user's SoundCloud account.

Mitigation: Require explicit user confirmation for write actions, verify playlist, track, and user IDs before execution, and avoid --force and --no-confirm in agent workflows.

## Reference(s):

- [SoundCloud API Reference](https://developers.soundcloud.com/docs/api/reference)
- [SoundCloud API Security Updates](https://developers.soundcloud.com/blog/security-updates-api/)
- [SoundCloud API Endpoints Reference](references/api_endpoints.md)
- [SoundCloud OAuth 2.0 Authentication Guide](references/oauth_flow.md)
- [SoundCloud API Best Practices](references/best_practices.md)

## Skill Output:

**Output Type(s):** [Text, JSON, CSV, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance with shell commands; script output may be human-readable text, JSON, or CSV.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses SoundCloud API credentials; write operations require a user token.]

## Skill Version(s):

1.0.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
