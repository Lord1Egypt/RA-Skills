## Description: <br>
Process and edit existing videos using WeryAI video toolkits for background removal, background replacement, anime style transfer, and status polling with bounded waits. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[weryai-developer](https://clawhub.ai/user/weryai-developer) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users, creators, and developers use this skill to route existing media through WeryAI video editing tools for subtitle translation, watermark removal, background removal, face changes, lip sync, video extension, style transfer, and upscaling. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Local media paths can be uploaded to WeryAI for processing, which may expose sensitive content. <br>
Mitigation: Use dry-run first, avoid sensitive local files, and only process media you are authorized to upload. <br>
Risk: Real submit and wait calls are paid external operations and may consume WeryAI credits. <br>
Mitigation: Confirm the tool choice and key parameters before paid runs; use status checks for existing tasks. <br>
Risk: The configurable WERYAI_BASE_URL can direct requests to a non-default API host. <br>
Mitigation: Keep WERYAI_BASE_URL on the official WeryAI host unless you intentionally trust another endpoint. <br>


## Reference(s): <br>
- [Video tools parameter matrix](artifact/references/video-tools-matrix.md) <br>
- [WeryAI documentation index](https://docs.weryai.com/llms.txt) <br>
- [Submit Video Anime Replace Task](https://docs.weryai.com/api-references/video-tools/submit-video-anime-replace-task) <br>
- [ClawHub skill page](https://clawhub.ai/weryai-developer/weryai-video-toolkits) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance] <br>
**Output Format:** [JSON from the CLI plus Markdown links and concise parameter summaries for users] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include task IDs, task status, processed video URLs, request summaries, and timeout follow-up guidance.] <br>

## Skill Version(s): <br>
0.1.3 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
