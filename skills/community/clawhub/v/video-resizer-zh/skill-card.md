## Description: <br>
This skill helps users resize and reframe videos for platform aspect ratios such as 9:16, 1:1, and 16:9 using Sparki. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[fischerlam](https://clawhub.ai/user/fischerlam) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and agents use this skill to adapt videos for Reels, Shorts, TikTok, Instagram, YouTube, and other platform formats. It supports prompt-driven resizing workflows that upload selected video files to Sparki and download the resulting edited video. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Selected video files are uploaded to Sparki's cloud service for processing. <br>
Mitigation: Use this skill only for videos the user is comfortable sending to Sparki, and ask for a local or offline workflow when cloud processing is not acceptable. <br>
Risk: A Sparki API key may be stored in the local OpenClaw config directory. <br>
Mitigation: Prefer the SPARKI_API_KEY environment variable when avoiding local key storage, and protect the OpenClaw config directory if setup writes the key there. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/fischerlam/video-resizer-zh) <br>
- [Sparki homepage](https://sparki.io) <br>
- [Sparki Telegram upload](https://t.me/Sparki_AI_bot/upload) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Configuration instructions, Guidance, JSON, Files] <br>
**Output Format:** [Markdown guidance with inline shell commands, JSON CLI responses, and downloaded video files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires a Sparki API key and uploads selected videos to Sparki's cloud service before downloading edited results.] <br>

## Skill Version(s): <br>
1.0.12 (source: SKILL.md frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
