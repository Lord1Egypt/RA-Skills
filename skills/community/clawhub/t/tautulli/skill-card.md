## Description: <br>
Monitor Plex activity and stats via Tautulli API. Check who's watching, view history, get library stats, and see server info. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[rjmurillo](https://clawhub.ai/user/rjmurillo) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
External users and developers use this skill to let an agent query a configured Tautulli instance for Plex activity, watch history, recently added media, library statistics, user statistics, and server status. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can expose Plex server, user, and viewing-history data from the configured Tautulli instance. <br>
Mitigation: Install only for trusted agents and avoid sharing command output in public logs, screenshots, or reports. <br>
Risk: TAUTULLI_API_KEY may grant access to Tautulli data if it is leaked. <br>
Mitigation: Keep the API key in environment configuration, exclude it from repositories and shared logs, and rotate it if exposure is suspected. <br>


## Reference(s): <br>
- [Tautulli](https://tautulli.com/) <br>
- [ClawHub Skill Page](https://clawhub.ai/rjmurillo/tautulli) <br>
- [Publisher Profile](https://clawhub.ai/user/rjmurillo) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, API Calls, Text, Configuration] <br>
**Output Format:** [Plain text summaries from shell command output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires curl, jq, TAUTULLI_URL, and TAUTULLI_API_KEY.] <br>

## Skill Version(s): <br>
1.0.0 (source: server-resolved release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
