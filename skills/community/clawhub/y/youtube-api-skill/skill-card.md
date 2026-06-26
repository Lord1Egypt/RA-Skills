## Description: <br>
YouTube Data API integration with managed OAuth for searching videos, managing playlists, accessing channel data, and interacting with comments. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[byungkyu](https://clawhub.ai/user/byungkyu) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill to search YouTube, inspect channel and video data, and manage authenticated YouTube resources through Maton-backed CLI or API calls. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: YouTube API traffic and OAuth connection handling depend on Maton. <br>
Mitigation: Install only if you trust Maton to handle the intended YouTube account, API traffic, and OAuth connection. <br>
Risk: The skill can modify playlists, subscriptions, comments, and other YouTube resources through a connected account. <br>
Mitigation: Review the target account, resource, and intended effect before approving any create, update, or delete operation. <br>
Risk: The MATON_API_KEY grants access to the Maton-backed integration. <br>
Mitigation: Store the key securely, avoid exposing it in shared output, and rotate or revoke it when access is no longer needed. <br>


## Reference(s): <br>
- [YouTube Data API Overview](https://developers.google.com/youtube/v3) <br>
- [Maton CLI Manual](https://cli.maton.ai/manual) <br>
- [ClawHub YouTube skill](https://clawhub.ai/byungkyu/youtube-api-skill) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with CLI, HTTP, Python, and JavaScript examples.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires network access, MATON_API_KEY, and a connected YouTube OAuth account; write operations require explicit user approval.] <br>

## Skill Version(s): <br>
1.0.5 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
