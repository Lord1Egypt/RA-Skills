## Description: <br>
Clips and downloads specific time ranges or full YouTube videos in selected qualities, including audio-only MP3 extraction, using precise timestamps. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[sandeepyadav1478](https://clawhub.ai/user/sandeepyadav1478) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Content creators, educators, musicians, researchers, and other ClawHub users can use this skill to extract timestamped YouTube clips, audio segments, or full downloads for workflows where they have rights to access and reuse the media. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill downloads or clips YouTube media and writes media files to disk. <br>
Mitigation: Use only media you have rights to access and reuse, and choose an explicit output directory when you need tighter control over saved files. <br>
Risk: The skill may install yt-dlp with pip and run a temporary Python script to process media. <br>
Mitigation: For stricter environments, preinstall yt-dlp in an isolated environment and review generated commands or scripts before execution. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/sandeepyadav1478/youtube-downloader-clipper) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Code, Shell commands, Files] <br>
**Output Format:** [Markdown guidance with Python and shell command snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May create local media files in the working directory and may use yt-dlp and ffmpeg for media processing.] <br>

## Skill Version(s): <br>
1.1.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
