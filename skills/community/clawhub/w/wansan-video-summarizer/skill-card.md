## Description: <br>
Multi-platform video transcript extraction and AI-powered summarization for YouTube, Bilibili, channel scans, and daily video digests. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[mcdowell8023](https://clawhub.ai/user/mcdowell8023) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users, developers, and agent operators use this skill to extract video transcripts, summarize individual videos or channel batches, and produce daily digest outputs. It is useful when an agent needs structured video metadata, transcript availability, Markdown summaries, and file paths for generated transcript or frame artifacts. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can use Chrome browser cookies while downloading or processing videos. <br>
Mitigation: Install only after deciding whether browser-cookie access is acceptable, and avoid account-restricted videos unless the operator understands and accepts that access pattern. <br>
Risk: Transcript text may be sent to external LLM services for summary generation. <br>
Mitigation: Avoid private or confidential videos unless using a controlled LLM endpoint, and limit environment tokens available to the process. <br>
Risk: Generated media, transcript, and frame files may remain on disk after processing. <br>
Mitigation: Choose safe output locations and clean up generated files after use, especially for sensitive video content. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/mcdowell8023/wansan-video-summarizer) <br>
- [Source repository metadata](https://github.com/mcdowell8023/oc-youtube-summarizer) <br>
- [yt-dlp](https://github.com/yt-dlp/yt-dlp) <br>
- [youtube-transcript-api](https://github.com/jdepoix/youtube-transcript-api) <br>
- [innertube](https://github.com/tombulled/innertube) <br>
- [OpenClaw](https://openclaw.ai) <br>


## Skill Output: <br>
**Output Type(s):** [JSON, Markdown, Text, Files] <br>
**Output Format:** [JSON file containing video metadata, transcript status, statistics, generated Markdown summaries, and paths to transcript or frame files when produced.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Supports text-only, auto-insert, and ai-review modes; Bilibili processing may also produce local transcript and keyframe files.] <br>

## Skill Version(s): <br>
2.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
