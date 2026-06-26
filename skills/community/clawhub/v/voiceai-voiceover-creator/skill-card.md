## Description: <br>
Turn scripts into publishable voiceovers with Voice.ai TTS, including segments, chapters, captions, and video muxing. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[gizmoGremlin](https://clawhub.ai/user/gizmoGremlin) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Creators, developers, and content teams use this skill to turn Markdown or text scripts into Voice.ai narration with reusable templates, captions, chapters, review pages, and optional video audio replacement. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Script text is sent to Voice.ai for TTS, and generated outputs may include the original script content. <br>
Mitigation: Use only content approved for Voice.ai processing and handle output directories as content-bearing artifacts. <br>
Risk: Generated ffmpeg helper scripts can turn specially crafted media file paths into shell commands if a user runs those scripts. <br>
Mitigation: Prefer installing ffmpeg and using the direct CLI path; inspect generated helper scripts and quote or rename unusual media paths before running them. <br>


## Reference(s): <br>
- [Skill Documentation](SKILL.md) <br>
- [Voice.ai API Reference](references/VOICEAI_API.md) <br>
- [Troubleshooting](references/TROUBLESHOOTING.md) <br>
- [Voice.ai](https://voice.ai) <br>
- [Agent Skills Specification](https://agentskills.io/specification) <br>


## Skill Output: <br>
**Output Type(s):** [Files, Shell commands, Configuration instructions] <br>
**Output Format:** [CLI-generated audio/video files, SRT captions, chapter text, HTML review pages, JSON metadata, and command guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires VOICE_AI_API_KEY for live Voice.ai TTS; mock mode can generate placeholder audio without API calls; ffmpeg is optional for stitching, MP3 encoding, normalization, and muxing.] <br>

## Skill Version(s): <br>
0.1.3 (source: server release evidence; artifact frontmatter and package.json report 0.2.1) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
