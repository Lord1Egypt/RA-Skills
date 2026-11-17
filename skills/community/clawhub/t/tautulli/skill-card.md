## Description:

Monitor Plex activity and stats via Tautulli API. Check who's watching, view history, get library stats, and see server info.

This skill is ready for commercial/non-commercial use.

## Publisher:

[rjmurillo](https://clawhub.ai/user/rjmurillo)

### License/Terms of Use:

MIT

## Use Case:

External users and operators use this skill to monitor an authorized Plex Media Server through Tautulli, including active streams, watch history, recently added media, library statistics, user statistics, and server status.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Command output can reveal Plex viewing habits, usernames, media titles, watch history, and server details.

Mitigation: Share outputs only with authorized users and redact sensitive viewing or user information before storing logs or pasting results elsewhere.

Risk: TAUTULLI_API_KEY grants access to Tautulli API data and may be exposed through environment configuration, logs, or plaintext HTTP.

Mitigation: Keep the API key restricted, prefer HTTPS in TAUTULLI_URL, avoid echoing secrets in logs, and rotate the key if it may have been exposed.

## Reference(s):

- [Tautulli](https://tautulli.com/)
- [ClawHub Skill Page](https://clawhub.ai/rjmurillo/skills/tautulli)
- [Publisher Profile](https://clawhub.ai/user/rjmurillo)

## Skill Output:

**Output Type(s):** [text, shell commands, configuration, guidance]

**Output Format:** [Plain text command output and Markdown usage guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires curl, jq, TAUTULLI_URL, and TAUTULLI_API_KEY.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
