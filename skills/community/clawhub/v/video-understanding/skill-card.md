## Description: <br>
Analyzes video URLs and local video files with Google Gemini to produce transcripts, visual descriptions, summaries, speaker lists, and answers to targeted questions. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[bill492](https://clawhub.ai/user/bill492) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, support teams, and agents use this skill when they need to understand, summarize, transcribe, inspect, or ask follow-up questions about a video URL or local video file. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Video content and sometimes the video URL are sent to Google Gemini for analysis. <br>
Mitigation: Avoid confidential recordings, private links, and regulated data unless the Gemini account, retention settings, and organizational policy are acceptable. <br>
Risk: Follow-up sessions can reuse Gemini File API uploads or CachedContent, which may keep remote handles active for later questions. <br>
Mitigation: Use cache reuse only when appropriate for the content, and run the skill's cache purge option after sensitive sessions. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/bill492/skills/video-understanding) <br>
- [yt-dlp Supported Sites](https://github.com/yt-dlp/yt-dlp/blob/master/supportedsites.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Guidance] <br>
**Output Format:** [JSON by default, with optional raw text output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Default JSON includes transcript, description, summary, duration_seconds, speakers, and an optional answer field for targeted questions.] <br>

## Skill Version(s): <br>
1.3.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
