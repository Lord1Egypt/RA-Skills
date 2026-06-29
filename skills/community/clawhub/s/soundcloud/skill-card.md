## Description: <br>
Interact with the SoundCloud API for searching tracks, analyzing audio metadata, managing playlists, user operations, likes, follows, and audio discovery. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[leosaucedo](https://clawhub.ai/user/leosaucedo) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and external users use this skill to run SoundCloud discovery, metadata analysis, playlist management, and account interaction workflows from an agent-assisted command-line environment. Write operations require a SoundCloud user OAuth token and can change the user's account state. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill requires SoundCloud API credentials and can cache OAuth tokens locally. <br>
Mitigation: Use a low-privilege or temporary SoundCloud app, avoid non-expiring or wildcard tokens, and review token files under ~/.cache/soundcloud before deployment. <br>
Risk: Write operations can delete playlists, replace or remove playlist tracks, like or unlike tracks, follow or unfollow users, and perform batch account changes. <br>
Mitigation: Require explicit human confirmation before account-changing commands and avoid bypass flags such as --force or --no-confirm unless the operator has reviewed the exact target resources. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/leosaucedo/soundcloud) <br>
- [ClawHub Publisher Profile](https://clawhub.ai/user/leosaucedo) <br>
- [SoundCloud API Reference](https://developers.soundcloud.com/docs/api/reference) <br>
- [SoundCloud API Security Updates](https://developers.soundcloud.com/blog/security-updates-api/) <br>
- [API Endpoints Reference](references/api_endpoints.md) <br>
- [OAuth Flow Reference](references/oauth_flow.md) <br>
- [Best Practices Reference](references/best_practices.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands; scripts may emit human-readable text, JSON, or CSV.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires Bash 4+, curl, jq, SoundCloud client credentials, and a user OAuth token for write operations.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
