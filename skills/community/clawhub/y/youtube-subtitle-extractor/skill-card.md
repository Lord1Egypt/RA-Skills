## Description: <br>
Downloads YouTube subtitles in SRT, VTT, or TXT using yt-dlp, supporting manual and auto-generated subtitles across languages for videos, channels, and content analysis workflows. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[mcbaivn](https://clawhub.ai/user/mcbaivn) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to extract subtitle and transcript files from YouTube videos or channels for review, analysis, and downstream content-processing workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill installs and runs a persistent local Python script that invokes yt-dlp. <br>
Mitigation: Install only if comfortable with the publisher's local skill and review the script before deployment. <br>
Risk: Channel or playlist URLs can create many subtitle and transcript files. <br>
Mitigation: Use the --limit option for channel or playlist URLs to bound downloads. <br>
Risk: Downloaded subtitles and plain-text transcripts remain on disk. <br>
Mitigation: Choose and manage the Youtube_Subtitles output directory according to local retention and privacy requirements. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/mcbaivn/youtube-subtitle-extractor) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Files, Shell commands, Guidance] <br>
**Output Format:** [SRT, VTT, or ASS subtitle files plus plain-text transcript files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Writes outputs under Youtube_Subtitles/ and supports language, subtitle source, format, and channel or playlist limit options.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
