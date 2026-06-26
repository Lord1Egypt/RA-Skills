## Description: <br>
Analyze videos to extract reverse prompts, shot-by-shot breakdowns, and AI-ready visual descriptions via the NanoPhoto.AI Video Reverse Prompt API. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[nanophotohq](https://clawhub.ai/user/nanophotohq) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to turn authorized YouTube links, direct MP4 URLs, or local MP4 files into shot-by-shot video breakdowns and AI-ready visual prompts through NanoPhoto.AI. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Selected video URLs, local MP4 contents, filenames, and related request data are sent to NanoPhoto.AI for processing. <br>
Mitigation: Only process media the user is authorized to upload, avoid sensitive content, and configure NANOPHOTO_API_KEY through secure environment-variable settings. <br>
Risk: API calls may consume NanoPhoto.AI service credits. <br>
Mitigation: Tell users that each analysis may spend credits before making requests. <br>
Risk: Local file uploads are limited to MP4 files up to 30 MB. <br>
Mitigation: Validate file type and size before upload; use the bundled script for local MP4 files. <br>


## Reference(s): <br>
- [Video Reverse Prompt API Reference](references/api.md) <br>
- [NanoPhoto.AI homepage](https://nanophoto.ai) <br>
- [ClawHub skill page](https://clawhub.ai/nanophotohq/video-reverse-prompt) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with streaming text output and optional shell command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Outputs may include shot numbers, framing and camera movement, visual descriptions, audio analysis, duration estimates, and an overall summary.] <br>

## Skill Version(s): <br>
1.0.3 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
