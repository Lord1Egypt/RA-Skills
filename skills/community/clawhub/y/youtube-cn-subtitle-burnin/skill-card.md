## Description: <br>
Create Simplified Chinese or Chinese-English bilingual hard-subtitled videos from YouTube links or existing video/subtitle files. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[woodenxyz](https://clawhub.ai/user/woodenxyz) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, localization teams, and content operators use this skill to produce Chinese-only or bilingual hard-subtitled YouTube videos while retaining reusable SRT/ASS files, descriptions, thumbnails, previews, and review artifacts. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill downloads and processes YouTube media and can create transformed video outputs. <br>
Mitigation: Use it only for videos you have rights to transform, and review the generated outputs before publication. <br>
Risk: Subtitle mode or layout choices can produce incorrect, unreadable, or occluding subtitles. <br>
Mitigation: Specify Chinese-only versus bilingual output up front, create a preview clip, inspect design confirmation frames, and run the subtitle quality gates before full delivery. <br>
Risk: Reusable feedback updates can change future workflow behavior. <br>
Mitigation: Review proposed feedback-ledger, workflow, and quality-gate changes before repackaging or redistributing the skill. <br>
Risk: External media tools such as ffmpeg, ffprobe, and yt-dlp are required in the local environment. <br>
Mitigation: Confirm the required binaries are installed and use the skill's ffmpeg capability check before burning subtitles. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/woodenxyz/youtube-cn-subtitle-burnin) <br>
- [Project homepage](https://github.com/woodenxyz/youtube-cn-subtitle-burnin) <br>
- [Workflow](references/workflow.md) <br>
- [Quality gates](references/quality-gates.md) <br>
- [Review template](references/review-template.md) <br>
- [Feedback ledger](references/feedback-ledger.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with shell commands, subtitle files, review records, and video or thumbnail outputs] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces local media-processing artifacts such as SRT, ASS, MP4, thumbnails, screenshots, and review notes when used in a project workspace.] <br>

## Skill Version(s): <br>
0.1.0 (source: frontmatter and release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
