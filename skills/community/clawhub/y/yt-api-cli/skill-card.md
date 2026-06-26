## Description: <br>
Manage your YouTube account from the command line. Complete CLI for YouTube Data API v3 - list/search videos, upload, manage playlists, and more. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[nerveband](https://clawhub.ai/user/nerveband) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and automation agents use this skill to install, configure, and operate a YouTube Data API v3 CLI for listing, searching, uploading, and managing YouTube account resources. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can guide an agent to use live YouTube account authority for uploads, channel updates, playlist edits, thumbnail changes, and other account-mutating commands. <br>
Mitigation: Require explicit user approval before any account-mutating command is run. <br>
Risk: OAuth client secrets, service account credentials, and stored tokens can grant access if exposed. <br>
Mitigation: Use a dedicated Google OAuth client with minimal scopes, keep credentials out of logs, protect stored tokens, and revoke tokens when no longer needed. <br>
Risk: Installing the referenced CLI from a moving latest release can pull code that has not been reviewed for this deployment. <br>
Mitigation: Pin and verify a specific release or checksum before installation where possible. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/nerveband/yt-api-cli) <br>
- [YouTube API CLI GitHub repository referenced by skill](https://github.com/nerveband/youtube-api-cli) <br>
- [Google Cloud Console](https://console.cloud.google.com) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Shell commands, Configuration, API calls] <br>
**Output Format:** [Markdown guidance with bash commands, YAML configuration examples, and CLI invocation examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [The described CLI defaults to JSON output and also supports table, YAML, and CSV output.] <br>

## Skill Version(s): <br>
1.0.2 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
