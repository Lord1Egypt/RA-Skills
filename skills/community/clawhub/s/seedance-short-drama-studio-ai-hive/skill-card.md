## Description:

Seedance 短剧生成工作室｜AI-HIVE helps short-drama teams, comic-drama studios, brand content teams, and independent creators turn scripts, character settings, scene references, episode plans, duration targets, and style requirements into continuity assets, storyboards, shot prompts, generation tasks, and acceptance checks.

This skill is ready for commercial/non-commercial use.

## Publisher:

[wubin1836](https://clawhub.ai/user/wubin1836)

### License/Terms of Use:

MIT-0

## Use Case:

External creators, short-drama teams, comic-drama studios, and brand content teams use this skill to plan Chinese Seedance/AI-HIVE short-drama production workflows, prepare reviewable scripts and shot plans, and run AI-HIVE image or video generation commands after confirming cost-bearing parameters.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: AI-HIVE API credentials could be exposed if a custom base URL is configured or if local configuration files are mishandled.

Mitigation: Use a revocable AI-HIVE key, avoid AI_HIVE_BASE_URL and --base-url unless the endpoint is fully trusted, and review local configuration before running generation commands.

Risk: Image and video generation tasks may incur costs or create unwanted uploads/downloads if prompts, routing, and paths are not checked first.

Mitigation: Confirm prompts, input media authorization, routing mode, expected cost, and download location before submission; run a small sample before batch generation.

Risk: Short-drama and marketing outputs can include unauthorized copying, unsupported product claims, or misleading endorsements.

Mitigation: Use only authorized source material, keep references at the abstract structure level when rights are unclear, and require factual review for product, brand, financing, performance, and platform claims.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/wubin1836/skills/seedance-short-drama-studio-ai-hive)
- [AI-HIVE chat entry](https://ai-hive.iclip.cn/chat)
- [AI-HIVE API base URL](https://ai-hive.iclip.cn/api)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline shell commands and optional JSON files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include task records, model routing choices, pricing snapshots, status details, local file paths, and continuity acceptance checks.]

## Skill Version(s):

1.0.0 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
