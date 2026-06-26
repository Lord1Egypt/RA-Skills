## Description: <br>
Download, transcribe, extract frames, and analyze videos or reels from URLs including Instagram, YouTube, TikTok, X, and direct MP4 links for content, strategy, script, visual elements, and marketing breakdowns. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[casperzinou](https://clawhub.ai/user/casperzinou) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users, creators, marketers, and analysts use this skill to turn a video URL into a structured digest that combines transcript content, selected frame observations, visual strategy, engagement tactics, business signals, and viral mechanics. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: A crafted URL or output path could cause unintended shell command execution in the Python helper. <br>
Mitigation: Review or patch the helper before installation, replace shell=True command strings with argument lists, and use the skill only with trusted URLs. <br>
Risk: Downloaded video, audio, frames, transcripts, and metadata can contain sensitive or copyrighted content. <br>
Mitigation: Keep outputs in a dedicated temporary directory and delete generated media, transcripts, and metadata after analysis. <br>
Risk: The downloader can disable certificate checks for yt-dlp and fetch remote media from user-provided URLs. <br>
Mitigation: Validate URL schemes and domains before running the download workflow and avoid disabling certificate checks. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/casperzinou/reel-digest) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, code, configuration, guidance] <br>
**Output Format:** [Markdown digest with transcript excerpts, frame observations, command examples, and generated local media artifacts] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May create video, audio, frame, transcript, and metadata files in a temporary output directory.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
