## Description:

Wan3.0 视频生成与编辑 helps agents generate or edit videos through AI Hive from text prompts and optional image, video, or audio references, then track tasks and download completed results.

This skill is ready for commercial/non-commercial use.

## Publisher:

[wubin1836](https://clawhub.ai/user/wubin1836)

### License/Terms of Use:

MIT-0

## Use Case:

External creators, video editors, post-production teams, advertisers, and e-commerce operators use this skill to create or revise short videos, product videos, ads, TVC material, social content, short drama clips, and comic-style video from prompts and selected media references.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Credential handling requires care because the skill uses an AI Hive API key from CLI arguments, environment variables, or a local config file.

Mitigation: Use a least-privilege API key where possible, avoid pasting keys into shared logs, and keep the generated config file private.

Risk: Media inputs are uploaded to AI Hive or the configured compatible endpoint before video generation.

Mitigation: Install and run the skill only when you trust the endpoint and have permission to upload the selected images, videos, or audio.

Risk: The configured base URL can be overridden, which could redirect credentials and media to an untrusted service.

Mitigation: Keep --base-url, AI_HIVE_BASE_URL, and config base_url pointed at a trusted HTTPS endpoint.

Risk: Generated files are written to a local output directory after task completion.

Mitigation: Use a disposable or task-specific output directory and inspect downloads before moving them into trusted project locations.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/wubin1836/skills/wan-3-0-video-generation-and-editing)
- [AI Hive console](https://ai-hive.iclip.cn/chat)

## Skill Output:

**Output Type(s):** [shell commands, configuration, guidance, files]

**Output Format:** [Markdown guidance with inline shell commands; generated video files are downloaded by the CLI when requested.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Can return task IDs for later polling; generated downloads default to ~/Downloads/AiHive.]

## Skill Version(s):

1.0.0 (source: evidence.json release.version and target metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
