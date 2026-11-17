## Description:

This skill helps Chinese video production, advertising, ecommerce, and growth teams analyze the first three seconds of short-form videos, produce hook matrices and original openings, and optionally run AI-HIVE media generation workflows.

This skill is ready for commercial/non-commercial use.

## Publisher:

[wubin1836](https://clawhub.ai/user/wubin1836)

### License/Terms of Use:

MIT-0

## Use Case:

External creators, marketers, editors, and growth teams use this skill to turn a product brief, audience pain point, platform target, and authorized reference media into a reviewable short-video hook analysis, script plan, prompts, commands, and acceptance checklist. When approved, the skill can help submit AI-HIVE image or video generation jobs, track task status, and download generated media.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill stores and uses an AI-HIVE API key for authenticated media generation workflows.

Mitigation: Use a dedicated API key, keep it out of logs and shared projects, and remove or rotate it when the workflow no longer needs access.

Risk: Media generation, upload, polling, and download operations may incur costs.

Mitigation: Review prompts, model choice, routing mode, and price snapshots before submission; use --no-download when only task status is needed.

Risk: Custom AI-HIVE base URLs can redirect API keys and media to endpoints outside the default service.

Mitigation: Use the default base URL unless the alternate endpoint is fully trusted and approved.

Risk: Reference-video workflows can encourage overly similar derivative content or unsupported commercial claims.

Mitigation: Require authorization for source media, preserve only abstract structure, rewrite characters, scenes, dialogue, and visual style, and keep product claims tied to confirmed facts.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/wubin1836/skills/viral-video-hook-analyzer-ai-hive)
- [AI-HIVE Chat](https://ai-hive.iclip.cn/chat)
- [AI-HIVE API Endpoint](https://ai-hive.iclip.cn/api)

## Skill Output:

**Output Type(s):** [Analysis, Markdown, Code, Shell commands, Configuration, Files, API calls, Guidance]

**Output Format:** [Markdown with JSON files and inline shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May create local blueprint JSON files, call AI-HIVE APIs, upload authorized media, poll asynchronous generation tasks, and download generated media after user confirmation.]

## Skill Version(s):

1.0.0 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
