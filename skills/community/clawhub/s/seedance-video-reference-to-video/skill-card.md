## Description:

This skill helps video editors, post-production teams, advertisers, and creators generate reference-to-video outputs with Seedance through AI Hive by uploading required media, submitting generation tasks, tracking progress, and downloading completed videos.

This skill is ready for commercial/non-commercial use.

## Publisher:

[wubin1836](https://clawhub.ai/user/wubin1836)

### License/Terms of Use:

MIT-0

## Use Case:

External creators, video editors, post-production teams, and marketing teams use this skill to create Seedance reference-to-video outputs for advertising, e-commerce product videos, TVC assets, social commerce, short dramas, and social media content. It is useful when users want an agent to prepare AI Hive CLI commands, configure API access, upload reference media, submit tasks, query task status, and retrieve generated video files.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can send the AI Hive API key to an arbitrary configured API host if --base-url, AI_HIVE_BASE_URL, or config base_url is changed.

Mitigation: Use the default AI Hive base URL or another trusted host only, and review local configuration before running commands with an API key.

Risk: Generation uploads reference media to AI Hive and may incur generation costs.

Mitigation: Use --no-download for tests, keep returned task IDs, confirm intended media and route before submitting, and avoid sensitive media unless third-party upload is acceptable.

Risk: The security summary reports local output behavior that writes downloaded results using remote task data.

Mitigation: Use a controlled output directory, inspect generated files before reuse, and avoid writing outputs into sensitive or shared locations.

## Reference(s):

- [ClawHub skill release](https://clawhub.ai/wubin1836/skills/seedance-video-reference-to-video)
- [ClawHub publisher profile](https://clawhub.ai/user/wubin1836)
- [AI Hive API key setup](https://ai-hive.iclip.cn/chat)
- [AI Hive API base URL](https://ai-hive.iclip.cn/api)

## Skill Output:

**Output Type(s):** [Shell commands, Configuration, Guidance, Files]

**Output Format:** [Markdown guidance with bash command examples; runtime commands may return JSON task data and downloaded MP4, MOV, PNG, or model-supported output files.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires an AI Hive API key through CLI arguments, environment variable, or local config; generation may upload reference media to AI Hive and may incur model usage costs.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
