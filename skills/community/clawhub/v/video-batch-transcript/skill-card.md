## Description: <br>
Batch-downloads authorized video or audio sources from yt-dlp-compatible sites, transcribes them with Whisper acceleration when available, corrects terminology, and generates structured notes and transcripts. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[shenghoo123-png](https://clawhub.ai/user/shenghoo123-png) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users, developers, and content teams use this skill to turn authorized videos, playlists, channels, and course materials into transcripts, Markdown study notes, and collection summaries. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Browser cookies and cookie files can act like account credentials for logged-in or paid sites. <br>
Mitigation: Review the cookie workflow before installation, use the skill only for content the user is authorized to access, prefer isolated or temporary browser profiles/accounts, keep cookie files out of repositories and shared folders, restrict file permissions, and delete cookies after use. <br>
Risk: Downloaded media, transcripts, notes, and metadata remain on disk after processing. <br>
Mitigation: Review the configured output directory after each run and apply the user's retention, sharing, and deletion requirements to generated files. <br>


## Reference(s): <br>
- [yt-dlp supported sites](https://github.com/yt-dlp/yt-dlp/blob/master/supportedsites.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, JSON, Shell commands, Configuration] <br>
**Output Format:** [Markdown notes, plain-text transcripts, JSON metadata, and command-line/configuration guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Writes downloaded audio, transcripts, per-video notes, collection summaries, and metadata under the configured output directory.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
