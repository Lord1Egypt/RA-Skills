## Description: <br>
Generates Seedance text-to-video and image-to-video clips through WeryAI, with version-aware model selection, prompt expansion, validation, and playable video links. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[zoucdr](https://clawhub.ai/user/zoucdr) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and creative operators use this skill to turn short briefs or public image references into Seedance video generation requests. It helps choose the right Seedance version, validate supported duration, aspect ratio, resolution, audio, and image options, then return playable video links or actionable parameter errors. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Video generation sends prompts and public image URLs to WeryAI and requires a WERYAI_API_KEY. <br>
Mitigation: Keep the API key out of files and logs, avoid sensitive prompts or media, and review the full request table before submitting. <br>
Risk: Each generation run can create a paid remote task. <br>
Mitigation: Confirm the selected model, duration, aspect ratio, resolution, and audio settings before running the wait command. <br>
Risk: Unsupported model or media combinations can fail after submission. <br>
Mitigation: Use the skill's version-aware constraints and WeryAI model reference to validate image counts, first/last-frame support, negative prompts, and resolution before generation. <br>


## Reference(s): <br>
- [WeryAI video CLI and JSON reference](artifact/resources/WERYAI_VIDEO_API.md) <br>
- [Seedance Video Gen 1 2.0 on ClawHub](https://clawhub.ai/zoucdr/seedance-video-gen-1-2-0) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown confirmation tables, shell command examples, JSON CLI results, and Markdown video links] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires Node.js 18+ and WERYAI_API_KEY; image inputs must be public HTTPS URLs and generation may consume WeryAI credits.] <br>

## Skill Version(s): <br>
0.1.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
