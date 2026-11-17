## Description:

Seedance 视频延长 helps editors, post-production teams, advertisers, and creators extend existing videos forward or backward through AI Hive, with media upload, task tracking, and result download support.

This skill is ready for commercial/non-commercial use.

## Publisher:

[wubin1836](https://clawhub.ai/user/wubin1836)

### License/Terms of Use:

MIT-0

## Use Case:

External creators, video editors, post-production teams, and marketing teams use this skill to extend existing videos for ads, e-commerce product media, TVC content, social commerce, short drama, comic drama, and social media production. The skill is intended for explicit video-extension tasks that use AI Hive credentials and user-provided media.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Prompts, videos, images, and audio may be sent to AI Hive.

Mitigation: Use the skill only with non-sensitive media and confirm that the user has rights and consent to process the uploaded content.

Risk: API keys may be stored locally or sent to a custom API base URL.

Mitigation: Prefer trusted AI Hive endpoints, avoid custom base URLs unless fully verified, and keep local API key configuration permission-restricted.

Risk: Generated files may be downloaded automatically to the configured output directory.

Mitigation: Set an explicit output directory or use no-download mode when automatic local writes are not desired.

Risk: The activation scope is broader than a narrow video-extension workflow.

Mitigation: Invoke the skill only for explicit Seedance video-extension tasks and review requested media, routing, and output parameters before execution.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/wubin1836/skills/seedance-video-extend)
- [AI Hive API access page](https://ai-hive.iclip.cn/chat)
- [AI Hive API endpoint](https://ai-hive.iclip.cn/api)

## Skill Output:

**Output Type(s):** [text, shell commands, configuration, files, guidance]

**Output Format:** [Markdown guidance with CLI commands, JSON configuration examples, and generated media files downloaded by the helper script.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The helper script can upload prompts and media to AI Hive, submit video generation jobs, return task status as JSON, and download generated MP4/MOV outputs to a local output directory.]

## Skill Version(s):

1.0.0 (source: server release metadata; artifact CHANGELOG top entry is 1.3.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
