## Description: <br>
Analyze videos with Google Gemini multimodal AI, including downloading from supported video URLs and returning transcripts, descriptions, summaries, and answers to questions about video content. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[bill492](https://clawhub.ai/user/bill492) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and agents use this skill to inspect video URLs, generate structured transcripts and visual descriptions, summarize video content, and answer targeted questions about what appears in a video. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Video URLs or downloaded video content are sent to Google Gemini for processing. <br>
Mitigation: Use the skill only when third-party processing by Google Gemini is acceptable; avoid confidential, private, regulated, or access-restricted videos unless that processing is approved. <br>
Risk: The skill can download media from user-provided URLs for non-YouTube sources. <br>
Mitigation: Review the target URL before execution and keep size limits appropriate for the environment. <br>


## Reference(s): <br>
- [yt-dlp Supported Sites](https://github.com/yt-dlp/yt-dlp/blob/master/supportedsites.md) <br>
- [ClawHub Skill Page](https://clawhub.ai/bill492/video-understanding) <br>


## Skill Output: <br>
**Output Type(s):** [text, JSON, files] <br>
**Output Format:** [Structured JSON by default, raw text when requested, or an MP4 file for download-only mode] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Default JSON includes transcript, description, summary, duration_seconds, speakers, and optionally answer.] <br>

## Skill Version(s): <br>
1.1.0 (source: ClawHub release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
