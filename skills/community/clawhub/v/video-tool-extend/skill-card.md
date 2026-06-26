## Description: <br>
Extend or continue an existing HTTPS video with a prompt via WeryAI (video-extend). Use when the user wants to lengthen a clip with style and duration controls, not text-to-video from scratch. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[zoucdr](https://clawhub.ai/user/zoucdr) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and video-production agents use this skill to extend an existing public HTTPS video with a WeryAI prompt, style, resolution, and duration. It is scoped to video extension, not text-to-video or local file upload workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Paid WeryAI API calls can consume credits and are not idempotent. <br>
Mitigation: Use dry-run first and require explicit user confirmation of the video URL, prompt, style, resolution, and duration before submit or wait. <br>
Risk: The skill sends the public video URL and prompt to WeryAI. <br>
Mitigation: Avoid private media and sensitive prompts unless the user is comfortable sharing them with WeryAI. <br>
Risk: API keys may be exposed if written into files or prompts. <br>
Mitigation: Keep WERYAI_API_KEY only in the runtime environment and never write it into files. <br>


## Reference(s): <br>
- [WeryAI llms.txt](https://docs.weryai.com/llms.txt) <br>
- [ClawHub skill page](https://clawhub.ai/zoucdr/video-tool-extend) <br>
- [Publisher profile](https://clawhub.ai/user/zoucdr) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, JSON] <br>
**Output Format:** [Markdown guidance with shell commands and JSON CLI responses] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires Node.js 18+, WERYAI_API_KEY, a public HTTPS video URL, and explicit user confirmation before paid submit or wait calls.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
