## Description: <br>
Use when the user asks to create, inspect, render, or repair an HTML-authored video from a brief, website, Markdown/text file, or GitHub repository; needs captions, voiceover, background music, generated images/video clips, or a HyperFrames-like local video pipeline using SenseAudio media APIs and AudioClaw LLM planning. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[fridaylifan](https://clawhub.ai/user/fridaylifan) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and video-production agents use this skill to build editable HTML video projects from briefs, websites, Markdown, text, or repository README content, then generate narration, captions, supporting media, local renders, inspections, and repair passes. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can send prompts, page captures, inspect frames, or generated media requests to external AI and media providers. <br>
Mitigation: Use offline mode, saved inputs, or deterministic planning for sensitive material, and enable live media, LLM, or vision-audit calls only when the content is approved to leave the machine. <br>
Risk: Website capture can use browser profiles or cookies and may expose private, personalized, gated, or region-specific page content. <br>
Mitigation: Prefer the default clean temporary browser profile, use dedicated capture profiles instead of personal sessions, and provide cookies only for sites approved for capture. <br>
Risk: Generated video projects can store local artifacts such as screenshots, transcripts, captions, manifests, audio, and rendered media. <br>
Mitigation: Review project directories and reports before sharing, and remove private source material, browser captures, credentials, or derived media that should not be distributed. <br>


## Reference(s): <br>
- [SenseAudio API Reference](references/api.md) <br>
- [HTML Authoring Guide](references/authoring.md) <br>
- [SenseAudio Media Pipeline](references/media-pipeline.md) <br>
- [Local Renderer](references/renderer.md) <br>
- [Production Workflows](references/workflows.md) <br>


## Skill Output: <br>
**Output Type(s):** [Markdown, Code, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown with inline shell commands, JSON manifests, HTML/CSS/JavaScript project files, captions, reports, and rendered media file paths] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May create local project directories, generated assets, render reports, captions, subtitles, and MP4 outputs; live media and planning paths require configured API credentials.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
