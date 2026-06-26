## Description: <br>
WayinVideo AI video editing and analysis suite for highlight extraction, natural language video search, content summarization, transcription, and export customization for online URLs or local files. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[wayinvideo](https://clawhub.ai/user/wayinvideo) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users, developers, and agent operators use this skill to automate WayinVideo video analysis and editing workflows, including clipping, scene search, summaries, transcripts, and rendered exports. It is suited to content repurposing, review, subtitle generation, and structured learning from videos when sending selected media to WayinVideo is acceptable. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Selected videos, URLs, or uploaded media are sent to the WayinVideo service for AI processing. <br>
Mitigation: Use the skill only for content whose transfer to WayinVideo is acceptable; avoid sensitive meetings, faces, screens, or documents unless that handling is approved. <br>
Risk: Configuration and task results can be stored locally under ~/.wayinvideo. <br>
Mitigation: Review or clear saved config and result files when persistence is not desired, and use no-save options for tasks that should not write result JSON. <br>
Risk: Optional progress notifications can route task status through the local openclaw command. <br>
Mitigation: Leave event notifications disabled unless local progress routing through openclaw is intended. <br>


## Reference(s): <br>
- [ClawHub Release Page](https://clawhub.ai/wayinvideo/video-understanding-and-ai-clipping) <br>
- [AI Clipping Task Basics](basics/ai-clipping.md) <br>
- [Find Moments Task Basics](basics/find-moments.md) <br>
- [Video Summarization Task Basics](basics/video-summarization.md) <br>
- [Video Transcription Task Basics](basics/video-transcription.md) <br>
- [Video Export Task Basics](basics/export.md) <br>
- [Learning from Videos Workflow](advanced/learning_from_videos.md) <br>
- [Finding Specific Content Workflow](advanced/searching_best.md) <br>
- [Supported Languages](references/supported_languages.md) <br>
- [Platform Duration Guidance](references/platform_duration.md) <br>
- [Platform Ratio Guidance](references/platform_ratio.md) <br>
- [Caption Style Reference](references/caption_style.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown responses with WayinVideo CLI commands, local JSON result paths, and export links when available.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires WAYIN_API_KEY; task results may be saved under ~/.wayinvideo/cache unless no-save options are used.] <br>

## Skill Version(s): <br>
1.0.2 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
