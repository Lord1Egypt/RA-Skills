## Description: <br>
Get YouTube video info, statistics, descriptions, thumbnails, and optionally transcripts. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[TevfikGulep](https://clawhub.ai/user/TevfikGulep) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External users and developers use this skill to retrieve YouTube video metadata, statistics, thumbnails, descriptions, and optional transcripts from a command-line workflow. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill uses a YouTube API key and may use an Apify token for transcript requests. <br>
Mitigation: Use restricted API keys, protect the credentials file, and install only if this credential access is acceptable. <br>
Risk: Transcript requests can consume Apify usage or billing. <br>
Mitigation: Request transcripts only when needed and monitor Apify account usage. <br>
Risk: The advertised environment variables differ from the script behavior, which expects credentials in the documented OpenClaw credentials file. <br>
Mitigation: Place credentials in the documented OpenClaw credentials file or review the script before relying on environment-variable setup. <br>


## Reference(s): <br>
- [ClawHub Youtube Master skill page](https://clawhub.ai/TevfikGulep/youtube-master) <br>
- [ClawHub TevfikGulep publisher profile](https://clawhub.ai/user/TevfikGulep) <br>
- [Google Cloud Console](https://console.cloud.google.com/) <br>
- [Apify](https://apify.com/) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, configuration, guidance] <br>
**Output Format:** [Plain text command output with Markdown setup and usage instructions] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [The command output can include YouTube metadata, statistics, a shortened description, and optional transcript lines when transcript retrieval is requested.] <br>

## Skill Version(s): <br>
1.0.2 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
