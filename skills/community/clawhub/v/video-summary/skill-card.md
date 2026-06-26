## Description: <br>
Video summarization for Bilibili, Xiaohongshu, Douyin, and YouTube. Extract insights from video content through transcription and summarization. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[lifei68801](https://clawhub.ai/user/lifei68801) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent users use this skill to extract transcripts from supported video platforms or local media, then produce structured summary requests or transcript output for downstream summarization. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The security scan warns that transcript or audio remnants may remain in temporary storage. <br>
Mitigation: Use the skill only with videos suitable for local processing, review temporary storage after sensitive runs, and avoid processing confidential media unless cleanup is verified. <br>
Risk: Cookie files can contain session tokens for restricted video content. <br>
Mitigation: Use cookies only when needed, keep cookie files private, and avoid shared or long-lived cookie files. <br>
Risk: Extracted transcript content may be processed by the agent or a configured LLM provider. <br>
Mitigation: Review provider configuration before summarization and avoid sending sensitive transcripts to services that are not approved for the content. <br>


## Reference(s): <br>
- [ClawHub package page](https://clawhub.ai/lifei68801/video-summary) <br>
- [yt-dlp documentation](https://github.com/yt-dlp/yt-dlp) <br>
- [OpenAI Whisper](https://github.com/openai/whisper) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, json, shell commands, configuration, guidance] <br>
**Output Format:** [Plain text, Markdown summary-request blocks, or JSON-style structured output depending on command options.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May save output to a user-specified file and may reference temporary transcript files for agent or external LLM processing.] <br>

## Skill Version(s): <br>
1.6.4 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
