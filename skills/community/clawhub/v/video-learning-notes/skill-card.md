## Description: <br>
Use this skill when the user provides a video URL and wants a complete Markdown learning note. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[darknoah](https://clawhub.ai/user/darknoah) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, learners, and knowledge workers use this skill to convert a video URL or local video file into structured Chinese learning notes with transcripts, selected timestamped screenshots, summaries, learning objectives, key concepts, and review checklists. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The workflow may use browser cookies for YouTube downloads, which can access a logged-in browser session. <br>
Mitigation: Require explicit approval before allowing --cookies-from-browser, prefer direct public downloads first, and use an isolated browser profile when sensitive accounts are present. <br>
Risk: Downloaded videos and extracted frames may contain copyrighted, private, or sensitive content. <br>
Mitigation: Process only videos the user is authorized to access and keep generated videos, transcripts, and screenshots inside a dedicated task directory. <br>


## Reference(s): <br>
- [Video Learning Notes Reference](references/api_reference.md) <br>
- [ClawHub skill page](https://clawhub.ai/darknoah/video-learning-notes) <br>


## Skill Output: <br>
**Output Type(s):** [markdown, text, shell commands, code, configuration, guidance] <br>
**Output Format:** [Self-contained output directory with a Markdown learning note, transcript, extracted frames, selected screenshots, and manifest files.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses relative paths for the source video and selected screenshots; final notes are written in Chinese unless the user asks otherwise.] <br>

## Skill Version(s): <br>
1.0.2 (source: ClawHub release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
