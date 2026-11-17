## Description:

Seedance 参考生视频 helps video editors, post-production teams, advertisers, e-commerce producers, and creators generate Seedance reference-to-video outputs through AI Hive from prompts plus reference images, video, or audio, then track tasks and download finished media.

This skill is ready for commercial/non-commercial use.

## Publisher:

[wubin1836](https://clawhub.ai/user/wubin1836)

### License/Terms of Use:

MIT-0

## Use Case:

External creators, video editors, post-production teams, advertising producers, and e-commerce teams use this skill to create product, social, TVC, short-drama, and marketing videos constrained by provided reference media. It is suited for agents that need to configure AI Hive access, submit Seedance generation jobs, monitor task status, and retrieve generated video files.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill handles an AI Hive API key and may store it in ~/.ai-hive/config.json.

Mitigation: Keep the config file private, avoid sharing command logs or config contents, and rotate the API key if exposure is suspected.

Risk: Reference images, video, and audio are uploaded to AI Hive or its object storage workflow.

Mitigation: Do not upload sensitive, confidential, or copyrighted media unless the user has the rights and accepts sending it to the service.

Risk: A custom base URL can change where credentials and media-related requests are sent.

Mitigation: Use the default AI Hive API endpoint unless the alternative endpoint is trusted and intentionally configured.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/wubin1836/skills/seedance-reference-to-video)
- [AI Hive API key setup](https://ai-hive.iclip.cn/chat)
- [AI Hive API base URL](https://ai-hive.iclip.cn/api)

## Skill Output:

**Output Type(s):** [Shell commands, Configuration, JSON, Files, Guidance]

**Output Format:** [CLI output, JSON task records, and downloaded video files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires an AI Hive API key; generated media is saved to the configured output directory unless no-download mode is used.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
