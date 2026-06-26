## Description: <br>
AI skill to analyze song requests, verify local workspace files, and download missing tracks directly from YouTube bypassing API limits. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[nhathuynguyen19](https://clawhub.ai/user/nhathuynguyen19) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to satisfy music requests by identifying a requested track, checking the OpenClaw workspace for an existing file, and downloading a missing MP3 with yt-dlp for playback through cmus. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can contact YouTube and save requested audio files locally. <br>
Mitigation: Keep downloads user-directed and store files under ~/.openclaw/workspace/music/. <br>
Risk: User text may be incorporated into yt-dlp shell command arguments. <br>
Mitigation: Quote search strings and avoid letting untrusted text control command structure. <br>
Risk: The workflow depends on external yt-dlp and ffmpeg binaries. <br>
Mitigation: Install yt-dlp and ffmpeg only from trusted package sources. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/nhathuynguyen19/yt-dlp-cmus) <br>
- [yt-dlp project homepage](https://github.com/yt-dlp/yt-dlp) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown guidance with shell command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May produce local file paths under ~/.openclaw/workspace/music/ and yt-dlp/ffmpeg command guidance.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and artifact _meta.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
