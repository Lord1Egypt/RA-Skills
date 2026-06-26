## Description: <br>
Checks upcoming live broadcast schedules and current live status for YouTube channels using the YouTube Data API v3. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[stevenho1394](https://clawhub.ai/user/stevenho1394) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill to monitor selected YouTube channels for scheduled and active live broadcasts, including resolving channel handles, maintaining a watchlist, and returning broadcast details. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill requires a YouTube Data API key and can return errors when the key is missing, invalid, or quota-limited. <br>
Mitigation: Provide a scoped YOUTUBE_API_KEY through the agent environment and monitor Google Cloud quota usage. <br>
Risk: The skill stores the channel watchlist on disk in watchlist.json. <br>
Mitigation: Treat watched channel lists as workspace-local data and review persistence expectations before deploying in shared environments. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/stevenho1394/youtube-live-broadcast-checking) <br>


## Skill Output: <br>
**Output Type(s):** [text] <br>
**Output Format:** [JSON objects and arrays with channel, broadcast, timestamp, URL, and error details] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires YOUTUBE_API_KEY; writes a local watchlist.json to persist watched channels across restarts.] <br>

## Skill Version(s): <br>
1.3.7 (source: server release evidence, package.json, openclaw.plugin.json, clawhub.json, SKILL.md) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
