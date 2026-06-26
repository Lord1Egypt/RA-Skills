## Description: <br>
Analyze videos to extract reverse prompts, shot-by-shot breakdowns, and AI-ready visual descriptions via the NanoPhoto.AI Video Reverse Prompt API. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[sctc888-hub](https://clawhub.ai/user/sctc888-hub) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and content teams use this skill to turn authorized YouTube videos, direct MP4 URLs, or local MP4 files into shot-by-shot reverse prompts and visual descriptions for AI video workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Selected videos or video URLs are sent to NanoPhoto.AI for processing. <br>
Mitigation: Only submit media the user is authorized to upload and avoid confidential or sensitive media unless NanoPhoto.AI processing, retention, and credit usage terms are acceptable. <br>
Risk: The skill requires a NanoPhoto.AI API key. <br>
Mitigation: Configure NANOPHOTO_API_KEY through secure skill settings or environment injection, and do not paste the key into chat or source files. <br>
Risk: Local file analysis accepts only MP4 inputs up to 30 MB. <br>
Mitigation: Validate file extension and size before upload; use the bundled local upload script for local MP4 files. <br>


## Reference(s): <br>
- [Video Reverse Prompt API Reference](references/api.md) <br>
- [NanoPhoto.AI](https://nanophoto.ai) <br>
- [ClawHub skill page](https://clawhub.ai/sctc888-hub/reverseprompt) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Streaming Markdown text with shot tables, summaries, command examples, and configuration guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Returns analysis for one selected video source per API call; local MP4 uploads are limited to 30 MB and supported locales are documented in the API reference.] <br>

## Skill Version(s): <br>
1.0.0 (source: server-resolved release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
