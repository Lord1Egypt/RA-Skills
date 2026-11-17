## Description:

Seedance 文生视频 helps creators, marketing teams, ecommerce teams, and short-form production teams generate videos from Chinese or English prompts through AI Hive, with task submission, status checks, and finished media downloads.

This skill is ready for commercial/non-commercial use.

## Publisher:

[wubin1836](https://clawhub.ai/user/wubin1836)

### License/Terms of Use:

MIT-0

## Use Case:

External creators, ecommerce operators, marketing teams, and developers use this skill to submit Seedance text-to-video jobs, optionally upload reference media, monitor generation tasks, and retrieve finished video assets for ads, product displays, social content, short dramas, and related AIGC workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security scan marks the release as suspicious because activation scope is broad.

Mitigation: Install only for intended AI Hive Seedance video-generation workflows and review prompts, costs, and generated outputs before use.

Risk: The downloader can write files outside the chosen output folder if the API response is malicious.

Mitigation: Avoid custom or untrusted --base-url values and choose an output directory that does not contain important files.

Risk: The skill stores or reads an AI Hive API key locally.

Mitigation: Use a dedicated AI Hive API key, protect ~/.ai-hive/config.json, and rotate or revoke the key if it may have been exposed.

Risk: Batch or broad generation requests may incur unexpected cost.

Mitigation: Review real-time model pricing and confirm task volume before running large generation jobs.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/wubin1836/skills/seedance-text-to-video)
- [AI Hive chat and API key setup](https://ai-hive.iclip.cn/chat)
- [AI Hive API base URL](https://ai-hive.iclip.cn/api)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell commands, JSON task responses, and downloaded video files from the AI Hive service]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Generated media is saved to a user-selected output directory, defaulting to ~/Downloads/AiHive.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
