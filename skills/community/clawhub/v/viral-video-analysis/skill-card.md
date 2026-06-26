## Description: <br>
Analyze video ad performance and provide actionable feedback to creators across YouTube, TikTok, Instagram Reels, and Twitter using transcripts, visual analysis, and performance metrics. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[shawnshenopeninterx](https://clawhub.ai/user/shawnshenopeninterx) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Marketing teams, creator managers, and agents use this skill to evaluate short-form video ad performance, identify pacing and word-count issues, and draft creator coaching feedback. It can also compare high- and low-ROI videos or summarize local spreadsheet performance data into a report. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Video URLs are sent to Memories.ai for transcription. <br>
Mitigation: Use a dedicated API key, submit only videos you have permission to analyze, and review the Memories.ai privacy policy before use. <br>
Risk: Batch analysis reads local spreadsheets that may contain creator and ROI data. <br>
Mitigation: Use the minimum necessary spreadsheet data, keep files local, and remove sensitive fields that are not needed for the analysis. <br>
Risk: Creator coaching sections are template-guided recommendations rather than independent proof from spreadsheet data. <br>
Mitigation: Review the generated feedback against the source video, transcript, and business context before sharing it with creators. <br>


## Reference(s): <br>
- [Creator Video Feedback Framework](references/creator-feedback-framework.md) <br>
- [Viral Video Analysis on ClawHub](https://clawhub.ai/shawnshenopeninterx/viral-video-analysis) <br>
- [Memories.ai API Tools](https://api-tools.memories.ai) <br>
- [Memories.ai Privacy Policy](https://memories.ai/privacy) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, guidance, files] <br>
**Output Format:** [Markdown feedback, terminal analysis output, and optional PDF reports] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires MEMORIES_API_KEY; may send video URLs to Memories.ai for transcription and may read local Excel files with creator ROI data.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
