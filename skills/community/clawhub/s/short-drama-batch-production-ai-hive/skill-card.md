## Description:

Use this skill when the user asks for short-drama batch production, AI short-drama workflows, multi-episode video pipelines, or commercial content production using AI-HIVE planning, generation, polling, and delivery helpers.

This skill is ready for commercial/non-commercial use.

## Publisher:

[wubin1836](https://clawhub.ai/user/wubin1836)

### License/Terms of Use:

MIT-0

## Use Case:

External users and content production teams use this skill to turn Chinese short-drama, comic-drama, ecommerce, advertising, and social media content requirements into production plans, prompts, runnable AI-HIVE commands, generated-media task records, and quality checklists. It is designed for workflows that first lock a sample episode standard and then batch-generate shot-level assets.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill handles AI-HIVE API keys and generated media downloads, which could expose credentials or write files outside the intended output location if endpoints or responses are manipulated.

Mitigation: Use a low-privilege API key, keep the official AI-HIVE endpoint, avoid untrusted AI_HIVE_BASE_URL or config changes, and choose a non-sensitive output folder.

Risk: Batch image or video generation can incur paid API usage.

Mitigation: Review prompts, routing, model choices, and generated commands before submission; run a small sample before batch generation.

Risk: Reference media, brand claims, user testimonials, or platform-specific statements may create copyright, trademark, privacy, authenticity, or compliance issues.

Mitigation: Confirm authorization and factual sources before using reference assets or publishing claims; avoid unauthorized copying, false product claims, fake testimonials, and platform-rule evasion.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/wubin1836/skills/short-drama-batch-production-ai-hive)
- [AI-HIVE chat and API access](https://ai-hive.iclip.cn/chat)
- [AI-HIVE API endpoint](https://ai-hive.iclip.cn/api)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown with JSON files and inline bash commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include generated-media task IDs, pricing snapshots, model routing choices, local file paths, and delivery checklists.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
