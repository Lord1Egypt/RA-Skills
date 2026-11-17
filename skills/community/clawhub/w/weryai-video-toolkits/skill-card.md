## Description:

Process and edit existing videos with WeryAI toolkits for background removal, background replacement, anime replacement, subtitle translation or erasure, face change, lip sync, extension, style transfer, upscaling, watermark removal, and task-status checks.

This skill is ready for commercial/non-commercial use.

## Publisher:

[weryai-developer](https://clawhub.ai/user/weryai-developer)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and external users use this skill to route existing video-editing requests to WeryAI tools, collect the needed media inputs and parameters, and return processed video links or task status.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: A configurable WERYAI_BASE_URL could receive the API key and uploaded media if pointed at an untrusted host.

Mitigation: Leave WERYAI_BASE_URL unset unless the endpoint is controlled and trusted, and use a limited or revocable WERYAI_API_KEY.

Risk: Local video, image, or audio paths are uploaded to WeryAI for processing.

Mitigation: Avoid sensitive local media unless uploading it is intended and acceptable for the use case.

Risk: Real submit or wait calls can consume WeryAI credits and create paid processing tasks.

Mitigation: Use dry-run validation for request shape and confirm ambiguous or expensive runs before submission.

## Reference(s):

- [WeryAI Video Toolkits on ClawHub](https://clawhub.ai/weryai-developer/skills/weryai-video-toolkits)
- [Video tools parameter matrix](references/video-tools-matrix.md)
- [WeryAI documentation index](https://docs.weryai.com/llms.txt)
- [Submit Video Anime Replace Task](https://docs.weryai.com/api-references/video-tools/submit-video-anime-replace-task)
- [WeryAI API keys](https://www.weryai.com/api/keys)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, Configuration, API Calls, Markdown]

**Output Format:** [Markdown guidance with JSON command results and playable video links when available]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include task IDs, task status, processed video URLs, request summaries, and WeryAI error details.]

## Skill Version(s):

0.1.3 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
