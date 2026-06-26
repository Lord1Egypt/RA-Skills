## Description: <br>
Video Analysis Workflow helps agents analyze local or online videos, extract storyboards, visuals, narration, structure, script templates, and transcripts, and organize the results into an Obsidian-ready case library. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[siconvip](https://clawhub.ai/user/siconvip) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External creative teams, video planners, game operations staff, marketers, and AI-assisted creators use this skill to turn reference videos or supported platform links into reusable video case studies, storyboard notes, transcripts, and script templates. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Video analysis can persist extracted frames, transcripts, subtitles, and reports that may contain sensitive content. <br>
Mitigation: Use a dedicated non-sensitive output folder and process confidential videos only when that storage location is appropriate. <br>
Risk: Online video downloads may require browser-cookie access or platform-specific download tools. <br>
Mitigation: Ask for explicit authorization before accessing browser cookies and process only videos the user is authorized to download. <br>
Risk: The reviewed package references a setup script that is not included in the artifact. <br>
Mitigation: Review any setup script before running it and verify dependencies such as FFmpeg, Whisper, and yt-dlp from trusted sources. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/siconvip/video-analysis-workflow) <br>
- [Publisher profile](https://clawhub.ai/user/siconvip) <br>
- [Artifact README](artifact/README.md) <br>
- [Artifact skill definition](artifact/SKILL.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown reports with transcript sidecar files, frame image references, shell command snippets, configuration guidance, and optional HTML report guidance.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces four default case-library reports: case analysis, storyboard frames, transcript, and script template; may also preserve Whisper output files and extracted frame images.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
