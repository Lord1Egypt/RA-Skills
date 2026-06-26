## Description: <br>
Remove watermark overlays from an existing HTTPS video via WeryAI (video-watermark-remove). Use when the user wants watermark cleanup, not subtitles-only or text-to-video. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[zoucdr](https://clawhub.ai/user/zoucdr) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to remove watermark overlays from an existing public HTTPS video through WeryAI. It supports optional normalized watermark-region boxes and is not intended for local files, subtitle-only erasure, or text-to-video generation. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill sends the video URL and optional watermark-region coordinates to WeryAI under the user's API key. <br>
Mitigation: Install and run it only when that disclosure is acceptable; avoid signed, private, internal, or sensitive media URLs. <br>
Risk: Submit and wait commands can start paid WeryAI jobs. <br>
Mitigation: Confirm the exact URL and custom regions before running paid commands, and use dry-run first to inspect the request. <br>
Risk: Watermark removal can be misapplied to media the user is not authorized to modify. <br>
Mitigation: Use the skill only on videos where the user has the right to process and redistribute the output. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/zoucdr/video-tool-watermark-remove) <br>
- [WeryAI llms.txt](https://docs.weryai.com/llms.txt) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, shell commands, JSON, markdown] <br>
**Output Format:** [Markdown guidance with shell commands and JSON command results] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires WERYAI_API_KEY, Node.js 18+, a public HTTPS video URL, and optional normalized rectangle coordinates.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
