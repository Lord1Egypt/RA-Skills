## Description: <br>
Manage YouTube video thumbnails by guiding users through yutu CLI setup and commands to set custom thumbnails for videos. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[OpenWaygate](https://clawhub.ai/user/OpenWaygate) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to configure yutu and set a custom thumbnail image on a YouTube video by video ID. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill requires YouTube OAuth credentials and a cached token that can grant account access through the yutu CLI. <br>
Mitigation: Install only if the yutu CLI is trusted, keep client_secret.json and youtube.token.json out of source control and shared folders, and use restrictive file permissions. <br>
Risk: A wrong thumbnail file or video ID could update the wrong YouTube video. <br>
Mitigation: Verify the thumbnail file and video ID before running the command, and revoke or delete the token when access is no longer needed. <br>


## Reference(s): <br>
- [Yutu setup guide](references/setup.md) <br>
- [Thumbnail set reference](references/thumbnail-set.md) <br>
- [yutu homepage](https://github.com/eat-pray-ai/yutu) <br>
- [ClawHub skill page](https://clawhub.ai/OpenWaygate/youtube-thumbnail) <br>
- [OpenWaygate publisher profile](https://clawhub.ai/user/OpenWaygate) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown with inline bash code blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Commands require a yutu installation, OAuth client credentials, a cached token, a thumbnail file path, and a YouTube video ID.] <br>

## Skill Version(s): <br>
0.10.7-dev (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
