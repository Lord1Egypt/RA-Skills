## Description:

Seedance 视频编辑 helps creators edit existing video by uploading source media, describing the requested change, submitting the AI Hive generation task, tracking progress, and downloading the finished video.

This skill is ready for commercial/non-commercial use.

## Publisher:

[wubin1836](https://clawhub.ai/user/wubin1836)

### License/Terms of Use:

MIT-0

## Use Case:

External creators, video editors, post-production teams, advertisers, and e-commerce operators use this skill to transform existing video assets into edited product, social, ad, TVC, short-drama, or comic-drama videos through AI Hive.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security evidence says the skill can send API keys and user-selected media to configurable endpoints.

Mitigation: Use only the trusted AI Hive base URL, avoid custom --base-url or AI_HIVE_BASE_URL values unless the endpoint is fully trusted, and submit only media intended for AI Hive processing.

Risk: The security evidence flags overbroad activation wording.

Mitigation: Review user intent before running upload or generation commands, especially when the request involves sensitive media, billing, or comparison with unrelated video tools.

Risk: Generation tasks may incur cost and local timeout does not prove remote failure.

Mitigation: Use --no-download or task lookup for long jobs, keep the taskId, and avoid duplicate submissions until the original task status is checked.

Risk: The skill depends on runtime AI Hive model configuration, pricing, file limits, and endpoint availability.

Mitigation: Check live model configuration and pricing before high-volume or time-sensitive use, and pin Python dependencies in a virtual environment.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/wubin1836/skills/seedance-video-edit)
- [AI Hive chat and API key setup](https://ai-hive.iclip.cn/chat)
- [AI Hive API base URL](https://ai-hive.iclip.cn/api)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, API calls, files]

**Output Format:** [Markdown guidance with shell commands; generated videos are downloaded as MP4, MOV, or another format supported by the live model configuration.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The CLI can print task JSON for no-download workflows and saves completed media to the configured output directory.]

## Skill Version(s):

1.0.0 (source: server release metadata; artifact CHANGELOG top entry is 1.3.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
