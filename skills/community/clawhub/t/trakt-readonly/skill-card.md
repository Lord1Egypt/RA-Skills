## Description: <br>
Provides read-only Trakt.tv lookups for a user's watching status, recent episode history, watched shows, profile, stats, and OAuth-backed playback progress. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[dennisooki](https://clawhub.ai/user/dennisooki) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External users and developers use this skill to let an agent retrieve Trakt.tv viewing status, history, profile, stats, and playback progress without performing write operations. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can let an agent query Trakt viewing and profile data. <br>
Mitigation: Install it only for agents that are allowed to access that Trakt data. <br>
Risk: OAuth tokens and client secrets can expose playback access if they are shared or logged. <br>
Mitigation: Configure TRAKT_ACCESS_TOKEN and TRAKT_CLIENT_SECRET only when needed, keep them out of logs and repositories, and rotate them if exposed. <br>
Risk: Playback progress and device activation require additional OAuth credentials. <br>
Mitigation: Use the default client ID and username flow for read-only public-profile queries, and enable OAuth only for playback progress or device activation. <br>


## Reference(s): <br>
- [Trakt API Quick Reference](references/trakt-api.md) <br>
- [ClawHub skill page](https://clawhub.ai/dennisooki/trakt-readonly) <br>
- [Trakt OAuth applications](https://trakt.tv/oauth/applications) <br>
- [Trakt device activation](https://trakt.tv/activate) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Plain text or Markdown responses, with JSON passthrough for OAuth and playback commands.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires curl, jq, TRAKT_CLIENT_ID, and TRAKT_USERNAME; TRAKT_ACCESS_TOKEN and TRAKT_CLIENT_SECRET are optional for playback and device OAuth.] <br>

## Skill Version(s): <br>
1.0.3 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
