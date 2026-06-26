## Description: <br>
Download YouTube video audio and upload to Feishu cloud storage. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[yanghuicode](https://clawhub.ai/user/yanghuicode) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
OpenClaw users use this skill to turn a YouTube video into an MP3, prepare it for Feishu Drive upload, and send Feishu message details back to the user. It is suited for personal or workflow automation where the user controls the source URL and Feishu authorization. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill runs local Python and yt-dlp commands to fetch YouTube metadata and download audio. <br>
Mitigation: Install only from a trusted publisher, review the requested YouTube URL before execution, and run it in an environment appropriate for local downloads. <br>
Risk: Feishu upload and message steps require Feishu Drive and message permissions, and the security evidence notes that completion claims may not match every execution path. <br>
Mitigation: Confirm the file actually appears in Feishu, verify message delivery, and treat returned upload or send status as operational output that needs checking. <br>
Risk: Downloaded MP3 files can remain in the temporary directory after a run. <br>
Mitigation: Review and remove leftover temporary audio files after use, especially on shared machines. <br>
Risk: Downloading media can raise copyright or terms-of-use issues. <br>
Mitigation: Use the skill only for content the user is authorized to download and store. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/yanghuicode/youtube-to-feishu) <br>
- [Artifact skill definition](artifact/SKILL.md) <br>
- [Artifact README](artifact/README.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Progress text and JSON status objects with video metadata, downloaded file details, and Feishu next steps.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires Python, yt-dlp, FEISHU_USER_ID, and Feishu Drive/message permissions; the documented Feishu file-size limit is 100 MB.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
