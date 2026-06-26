## Description: <br>
Remove burnt-in subtitles or on-screen text from an HTTPS video via WeryAI (video-subtitle-erase). Use when the user wants subtitle or text removal, not translation or text-to-video. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[zoucdr](https://clawhub.ai/user/zoucdr) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to call WeryAI's subtitle erasure workflow for an existing public HTTPS video URL. It is scoped to removing burnt-in subtitles or on-screen text and does not perform translation, watermark removal, text-to-video generation, or local file upload. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The workflow can make paid WeryAI API calls when submit or wait is run. <br>
Mitigation: Require explicit user confirmation of the video URL and any selected regions before paid calls, and use dry-run validation first. <br>
Risk: The skill requires a WERYAI_API_KEY and network access to a third-party API. <br>
Mitigation: Keep the API key only in the runtime environment, do not write it to files, and review network use before deployment. <br>
Risk: Incorrect input scope can lead to failed jobs or unintended processing. <br>
Mitigation: Use only public https:// video URLs and normalized rectangle coordinates; do not pass local filesystem paths or unrelated WeryAI workflows. <br>


## Reference(s): <br>
- [WeryAI llms.txt](https://docs.weryai.com/llms.txt) <br>
- [ClawHub skill page](https://clawhub.ai/zoucdr/video-tool-subtitle-erase) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands and JSON CLI results] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [The skill can submit or poll a WeryAI task and returns task status, error details, and final video URLs when available.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
