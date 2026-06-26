## Description: <br>
Interact with the Trakt API to manage your watchlist, collection, ratings, and discover content. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[d-meagher](https://clawhub.ai/user/d-meagher) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External users and developers use this skill to guide an agent through Trakt.tv API operations for watchlists, watch history, collections, ratings, search, and content discovery. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The agent can read and change the user's Trakt account when OAuth credentials are configured. <br>
Mitigation: Ask the agent to confirm before removals, ratings, watch-history changes, or bulk updates. <br>
Risk: Client secrets, access tokens, and refresh tokens can expose the user's Trakt account if shared or committed. <br>
Mitigation: Treat these credentials as passwords, avoid sharing terminal output or committing OpenClaw config, and revoke or rotate tokens if exposed. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/d-meagher/trakt-tv) <br>
- [Trakt.tv](https://trakt.tv) <br>
- [Trakt OAuth Applications](https://trakt.tv/oauth/applications) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline bash, curl, and JSON examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses Trakt API credentials and OAuth tokens supplied through environment variables.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
