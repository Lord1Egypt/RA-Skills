## Description:

使用 AI Hive Seedance 2.5 迁移 Vidu、Vidu AI 或生数科技视频工作流，重点管理多参考主体、角色与道具关系、镜头连续性、编辑保护区和延长接点；不是 Vidu 官方接口。

This skill is ready for commercial/non-commercial use.

## Publisher:

[wubin1836](https://clawhub.ai/user/wubin1836)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and video creators use this skill to migrate Vidu-style video generation and editing workflows to AI Hive Seedance 2.5 while preserving multi-subject identity, prop ownership, shot continuity, edit protection areas, and extension joins.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Prompts and selected media files are sent to AI Hive for video generation.

Mitigation: Use only media and prompts that are approved for upload to AI Hive, and avoid sensitive private media unless the deployment has reviewed the data-sharing terms.

Risk: The helper downloads generated media from server-provided result URLs without destination allowlists, redirect validation, or download size limits.

Mitigation: Run the skill in a controlled workspace and inspect task JSON with no automatic download when handling untrusted or sensitive tasks.

Risk: The skill uses an AI Hive API key that may be stored locally.

Mitigation: Protect local credentials with restrictive file permissions or a managed environment secret, and rotate the key if exposure is suspected.

## Reference(s):

- [AI Hive API endpoint](https://ai-hive.iclip.cn/api)
- [AI Hive API key setup](https://ai-hive.iclip.cn/chat)
- [ClawHub skill page](https://clawhub.ai/wubin1836/skills/vidu-video-generation-alternative)
- [Publisher profile](https://clawhub.ai/user/wubin1836)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, Configuration, API calls, Files]

**Output Format:** [Markdown guidance with bash commands, JSON task output, and generated media files from the helper script]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses a fixed AI Hive Seedance 2.5 video workflow for t2v, i2v, r2v, edit, and extend modes.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
