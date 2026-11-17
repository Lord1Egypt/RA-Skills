## Description:

Seedance 首尾帧生视频 helps creators, marketing teams, commerce teams, and short-form production teams generate first-to-last-frame AI videos through AI Hive by using start and end images, tracking the generation task, and downloading the finished video.

This skill is ready for commercial/non-commercial use.

## Publisher:

[wubin1836](https://clawhub.ai/user/wubin1836)

### License/Terms of Use:

MIT-0

## Use Case:

External creators, advertisers, e-commerce teams, and video production teams use this skill to generate product, advertising, social media, and short-drama video assets from first and last frame inputs. Agents use it to provide setup guidance, construct CLI commands, submit AI Hive video tasks, check task status, and save generated media.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security review says the skill has broad activation text and needs review around API keys, uploads, and downloaded files.

Mitigation: Install only for this video workflow, keep API keys in environment or config-based storage, and review media inputs before generation.

Risk: The skill allows a custom AI Hive base URL.

Mitigation: Use the default AI Hive API endpoint unless the alternate endpoint is fully trusted.

Risk: Generated files are downloaded to a user-selected output directory and may overwrite or clutter important locations.

Mitigation: Choose an output directory where generated media downloads and similarly named task files are acceptable.

Risk: Batch or repeated video generation can incur cost through the connected AI Hive account.

Mitigation: Check runtime pricing and confirm volume before submitting high-count or repeated generation tasks.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/wubin1836/skills/seedance-first-last-frame-to-video)
- [AI Hive API key setup](https://ai-hive.iclip.cn/chat)
- [AI Hive API base URL](https://ai-hive.iclip.cn/api)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, Configuration, JSON, Files]

**Output Format:** [Markdown guidance with bash commands, JSON task responses, and downloaded media files from the CLI.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires an AI Hive API key, uploads user-provided media, and may download generated MP4, MOV, PNG, or other model-supported outputs.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
