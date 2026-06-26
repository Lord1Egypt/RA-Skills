## Description: <br>
Extract core content and generate structured analysis reports from YouTube, Bilibili, or local video files. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[franklinyung](https://clawhub.ai/user/franklinyung) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill to extract transcripts from YouTube, Bilibili, or local videos and turn them into concise structured Markdown analysis reports. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill imports an unbundled local video-reader project while processing API keys and potentially private transcripts. <br>
Mitigation: Review the separate video-reader project before installing or running the skill, and only provide MiniMax or Whisper credentials in trusted environments. <br>
Risk: Video URLs, recordings, transcripts, and derived analysis may contain private, proprietary, or regulated information. <br>
Mitigation: Avoid private meetings, proprietary recordings, regulated content, and sensitive URLs unless sharing derived content with configured services is acceptable. <br>


## Reference(s): <br>
- [Video Reader Technical Reference](references/api_details.md) <br>
- [ClawHub release page](https://clawhub.ai/franklinyung/video-content-watcher) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Guidance] <br>
**Output Format:** [Markdown report with summary, key takeaways, viewpoints, pros, cons, and target audience] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May also print CLI usage or error text when required inputs, API keys, or dependencies are missing.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
